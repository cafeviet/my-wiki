"""Register source provenance, attach exact evidence, verify article."""
import json
from pathlib import Path
import subprocess
import sys
ROOT = Path('D:/4.Code/my-wiki/src/nghien-cuu/ngan-hang-so/agent-reference-architecture')
E = ROOT / 'evidence'
S = 'C:/Users/ADMIN/AppData/Local/hermes/skills/research/grounded-citations/scripts/sources.py'
def call(*args):
    return subprocess.run(['python', S, '--ledger', str(E / 'citation-ledger.json'), *args], check=True)
if '--prepare' in sys.argv:
    original = ROOT.parent / 'mb-enterprise-agent-governance/index.md'
    (E / 'original-article.txt').write_text(original.read_text(encoding='utf-8'), encoding='utf-8')
    call('add', 'http://localhost:6677/nghien-cuu/ngan-hang-so/mb-enterprise-agent-governance/', '--title', 'Bài gốc — Quản trị Agent Doanh nghiệp Ngân hàng (bản Markdown tại repo)')
    quotes = [
      (1, 'source-02.txt', 'When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed.'),
      (2, 'source-03.txt', 'An agent harness—also commonly referred to as an agentic harness— is a software environment that surrounds an artificial intelligence model, giving it the ability to interact with outside tools, remember past interactions, and execute multi-step tasks.'),
      (3, 'source-04.txt', 'Agent behavior is stochastic: LLM-powered decisions are inherently non-deterministic, the same input might produce different outputs across invocations.'),
      (4, 'source-05.txt', 'Operational and policy boundaries for each agent are defined up front and enforced through layered controls rather than prompt instructions alone.'),
      (5, 'source-06.txt', 'Evaluation datasets, prompts, and scoring rubrics are versioned and kept current as agent capabilities and use cases evolve.'),
      (6, 'source-07.txt', 'Retries are applied without idempotency guarantees, so recovery from transient failures creates duplicate transactions, corrupted state, or silent inconsistency.'),
      (7, 'source-08.txt', 'Agent reasoning cycles are bounded by explicit termination conditions and confidence-based exits, so token consumption is predictable and proportional to decision complexity.'),
      (8, 'source-09.txt', 'Zero trust assumes there is no implicit trust granted to assets or user accounts based solely on their physical or network location'),
      (9, 'source-10.txt', 'The actor_token request parameter, however, does provide a means for providing information about the desired actor'),
      (10, 'original-article.txt', 'Tư duy Harness tổ chức các năng lực bao bọc quanh tác nhân AI thành bốn góc phần tư cốt lõi'),
    ]
    for idx, file, quote in quotes: call('quote', str(idx), '--text', quote, '--from', str(E / file))
else:
    call('render', '--replace-in', str(ROOT / 'index.md'))
    call('verify', str(ROOT / 'index.md'), '--strict', '--evidence')
    text = (ROOT / 'index.md').read_text(encoding='utf-8')
    assert text.count('```') % 2 == 0, 'Unbalanced code fences'
    assert all(x in text for x in ['KNOW', 'DO', 'CONTROL', 'VERIFY & LEARN', 'UNKNOWN', 'R1', 'R2', 'R3'])
    for key in [f'AT{i}' for i in range(1,6)] + [f'FM{i}' for i in range(1,6)] + [f'AC{i:02d}' for i in range(1,11)]:
        assert key in text, f'Missing {key}'
    print(json.dumps({'structural_checks': 'PASS', 'chars': len(text), 'lines': len(text.splitlines()), 'mermaid_diagrams': text.count('```mermaid')}, ensure_ascii=False))
