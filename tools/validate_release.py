#!/usr/bin/env python3
"""Pure static integrity/sanitisation checks for the four public workflow JSON files."""
import json, pathlib, re, sys
BASE=pathlib.Path(__file__).resolve().parents[1]
expected={'crm-governance-engine.json':2,'prospect-processor.json':25,'batch-uat.json':8,'single-prospect-live-uat.json':8}
for filename,count in expected.items():
    d=json.loads((BASE/'workflows'/filename).read_text())
    ns={n['name'] for n in d['nodes']}
    assert len(ns)==count==len(d['nodes'])
    assert not d.get('active')
    assert d.get('pinData')=={}
    assert not any(k in d for k in ('id','meta','versionId','tags'))
    for n in d['nodes']:
        assert 'credentials' not in n and 'webhookId' not in n
        if n['type']=='n8n-nodes-base.executeWorkflow':
            r=n['parameters']['workflowId']
            assert r['value']=='' and not r.get('cachedResultUrl')
    for s,v in d['connections'].items():
        assert s in ns
        for port in v['main']:
            for target in port:assert target['node'] in ns
    starts=[n['name'] for n in d['nodes'] if n['type'] in ('n8n-nodes-base.manualTrigger','n8n-nodes-base.executeWorkflowTrigger')]
    assert len(starts)==1
    seen=set(starts); todo=starts[:]
    while todo:
        s=todo.pop()
        for port in d['connections'].get(s,{}).get('main',[]):
            for t in port:
                k=t['node']
                if k not in seen:seen.add(k);todo.append(k)
    assert seen==ns
    print(f'PASS {filename}: {count} connected nodes, no exported instance/credential refs')
print('PASS: four public JSON workflows passed static checks (not a runtime test).')
