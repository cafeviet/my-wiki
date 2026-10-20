"""Retrieve primary references; keep reproducible text evidence."""
import concurrent.futures
import json
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import requests

ROOT = Path('D:/4.Code/my-wiki/src/nghien-cuu/ngan-hang-so/agent-reference-architecture')
EVIDENCE = ROOT / 'evidence'
LEDGER = EVIDENCE / 'citation-ledger.json'
SCRIPT = 'C:/Users/ADMIN/AppData/Local/hermes/skills/research/grounded-citations/scripts/sources.py'
SOURCES = [
 ('Nguồn gốc: Quản trị Agent Doanh nghiệp Ngân hàng', 'http://localhost:6677/nghien-cuu/ngan-hang-so/mb-enterprise-agent-governance/'),
 ('Anthropic — Building effective agents', 'https://www.anthropic.com/engineering/building-effective-agents'),
 ('Google Cloud — Agent harness', 'https://cloud.google.com/discover/agent-harness'),
 ('AWS — Agentic AI Lens', 'https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentic-ai-lens.html'),
 ('AWS — Alignment (AGENTSEC04)', 'https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04.html'),
 ('AWS — Evaluation (AGENTOPS06)', 'https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops06.html'),
 ('AWS — Legacy integration (AGENTREL06)', 'https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentrel06.html'),
 ('AWS — Reasoning cost (AGENTCOST01)', 'https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentcost01.html'),
 ('NIST — Zero Trust Architecture', 'https://csrc.nist.gov/pubs/sp/800/207/final'),
 ('RFC 8693 — OAuth 2.0 Token Exchange', 'https://www.rfc-editor.org/rfc/rfc8693'),
 ('OWASP — Excessive Agency', 'https://genai.owasp.org/llmrisk/llm06-excessive-agency/'),
]
class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip = 0; self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'): self.skip += 1
        if tag in ('p', 'h1', 'h2', 'h3', 'li', 'div', 'section', 'br'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'): self.skip = max(0, self.skip-1)
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def fetch(item):
    title, url = item
    try:
        response = requests.get(url, timeout=65, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        parser = Text(); parser.feed(response.text)
        text = '\n'.join(x.strip() for x in ''.join(parser.parts).splitlines() if x.strip())
        return {'title': title, 'url': url, 'resolved_url': response.url, 'status': response.status_code, 'text': text}
    except Exception as exc: return {'title': title, 'url': url, 'error': str(exc)}

if __name__ == '__main__':
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    subprocess.run(['python', SCRIPT, '--ledger', str(LEDGER), 'reset'], check=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: results = list(pool.map(fetch, SOURCES))
    registry = []
    for item in results:
        text = item.pop('text', '')
        if text:
            result = subprocess.run(['python', SCRIPT, '--ledger', str(LEDGER), 'add', item['url'], '--title', item['title']], capture_output=True, text=True, check=True)
            print(result.stdout.strip(), item['title'], len(text), flush=True)
            item['ledger_output'] = result.stdout.strip()
            idx = len(registry)+1
            path = EVIDENCE / f'source-{idx:02d}.txt'
            path.write_text(text, encoding='utf-8')
            item['evidence_file'] = path.name
        else: print('FAILED', item, flush=True)
        registry.append(item)
    (EVIDENCE / 'retrieval.json').write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
