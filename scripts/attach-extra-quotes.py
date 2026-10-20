"""Attach verbatim evidence quotes for sources 11-13 added during review."""
from pathlib import Path
import subprocess

E = Path('D:/4.Code/my-wiki/src/nghien-cuu/ngan-hang-so/agent-reference-architecture/evidence')
S = 'C:/Users/ADMIN/AppData/Local/hermes/skills/research/grounded-citations/scripts/sources.py'
QUOTES = [
    (11, 'source-11.txt',
     'Agent executions produce distributed traces that capture reasoning steps, '
     'tool invocations, memory operations, and inter-agent handoffs, with trace '
     'context propagated across every service boundary.'),
    (12, 'source-12.txt',
     'Agents operate under service identities that are distinct from human identities, '
     'and audit trails attribute every action unambiguously to either an agent or a human actor.'),
    (13, 'source-13.txt',
     'Excessive Agency is the vulnerability that enables damaging actions to be performed '
     'in response to unexpected, ambiguous or manipulated outputs from an LLM, regardless '
     'of what is causing the LLM to malfunction.'),
]
for idx, src, quote in QUOTES:
    subprocess.run(['python', S, '--ledger', str(E / 'citation-ledger.json'),
                    'quote', str(idx), '--text', quote, '--from', str(E / src)], check=True)
