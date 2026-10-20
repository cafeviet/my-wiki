"""Fetch additional primary sources to close source-scope gaps found in review."""
import concurrent.futures
import json
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import requests

E = Path('D:/4.Code/my-wiki/src/nghien-cuu/ngan-hang-so/agent-reference-architecture/evidence')
S = 'C:/Users/ADMIN/AppData/Local/hermes/skills/research/grounded-citations/scripts/sources.py'
EXTRA = [
 ('AWS — Observability (AGENTOPS05)', 'https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops05.html'),
 ('AWS — Identity & permissions (AGENTSEC03)', 'https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec03.html'),
 ('OWASP — LLM06:2025 Excessive Agency', 'https://genai.owasp.org/llmrisk/llm062025-excessive-agency/'),
]
class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip = 0; self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'): self.skip += 1
        if tag in ('p','h1','h2','h3','li','div','section','br'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'): self.skip = max(0, self.skip-1)
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def fetch(item):
    title, url = item
    try:
        r = requests.get(url, timeout=65, headers={'User-Agent': 'Mozilla/5.0'})
        r.raise_for_status()
        p = Text(); p.feed(r.text)
        text = '\n'.join(x.strip() for x in ''.join(p.parts).splitlines() if x.strip())
        return {'title': title, 'url': url, 'status': r.status_code, 'text': text}
    except Exception as exc:
        return {'title': title, 'url': url, 'error': str(exc)}

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(fetch, EXTRA))
    out = []
    for i, item in enumerate(results, start=11):
        text = item.pop('text', '')
        if not text:
            print('FAILED', item, flush=True); out.append(item); continue
        path = E / f'source-{i}.txt'
        path.write_text(text, encoding='utf-8')
        res = subprocess.run(['python', S, '--ledger', str(E / 'citation-ledger.json'), 'add', item['url'], '--title', item['title']], capture_output=True, text=True, check=True)
        print(res.stdout.strip(), '->', path.name, len(text), flush=True)
        item['evidence_file'] = path.name
        out.append(item)
    (E / 'retrieval-extra.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
