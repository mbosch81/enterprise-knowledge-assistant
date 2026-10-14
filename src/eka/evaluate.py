import json
from pathlib import Path
from eka.core import MemoryStore, ingest, answer


def run():
    store = MemoryStore()
    store.upsert(ingest(Path('data/synthetic/policies.md'), 'demo'))
    cases = json.loads(Path('data/evaluation-v1.json').read_text())
    rows = []
    for case in cases:
        result = answer(store, 'demo', case['question'])
        retrieval = store.search('demo', case['question'])
        rows.append({'question': case['question'], 'retrieval_hit': any(c.source == case['source'] for _,c in retrieval) if case['source'] else None, 'passed': case['expected'] in result['answer'] if case['expected'] else result['abstained']})
    report = {'provider': 'offline-extractive-v1', 'cases': rows, 'passed': sum(r['passed'] for r in rows), 'total': len(rows), 'limitations': 'Tiny synthetic lexical baseline; no semantic quality, fairness or real LLM evidence.'}
    print(json.dumps(report, indent=2))
    if report['passed'] != report['total']:
        raise SystemExit(1)

if __name__ == '__main__':
    run()
