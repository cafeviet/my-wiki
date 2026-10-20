"""Blocker 1 fix: remove the self-referential internal doc (id 10) from the
citation ledger. It is an internal design document, not a retrievable web
source, and its registered localhost URL never yielded content.

Ids of all remaining sources are preserved (1-9, 11-13 keep their identity);
id 10 is simply retired, leaving a gap. This is NOT renumbering.
"""
import json
from pathlib import Path

LEDGER = Path('D:/4.Code/my-wiki/src/nghien-cuu/ngan-hang-so/agent-reference-architecture/evidence/citation-ledger.json')
RETIRED = Path(LEDGER.parent / 'retired-sources.json')

data = json.loads(LEDGER.read_text(encoding='utf-8'))
keep, retired = [], []
for src in data['sources']:
    (retired if src['id'] == 10 else keep).append(src)

assert len(retired) == 1, f'expected exactly one retired source, got {len(retired)}'
assert retired[0]['url'].startswith('http://localhost'), 'guard: only the localhost internal doc may be retired'
kept_ids = [s['id'] for s in keep]
assert kept_ids == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13], f'unexpected id set: {kept_ids}'

data['sources'] = keep
LEDGER.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
RETIRED.write_text(json.dumps({
    'reason': 'Internal design document, not an independent retrievable source. '
              'Registered localhost URL returned an empty body (SPA); the attached quote '
              'came from the repo Markdown file, not that URL. Cited in-text as [TK] '
              '(de-xuat thiet ke) with a relative internal link instead.',
    'retired': retired,
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'retired id 10; ledger now holds ids {kept_ids}')
