#!/usr/bin/env python3
"""Check bootstrap consistency, not the live Todo authority or skill effectiveness."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
PREFIX='planning/kernelbender-bootstrap/'


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-manifest',action='store_true')
    args=parser.parse_args()
    errors=[];checks=[]
    def require(test,msg):
        if not test: errors.append(msg)
    def safe(p):return isinstance(p,str) and bool(p) and not PurePosixPath(p).is_absolute() and '..' not in PurePosixPath(p).parts
    def within(p,scopes):return any(p==s or p.startswith(s.rstrip('/')+'/') for s in scopes)
    def load(p):return json.loads((ROOT/p).read_text())
    try:
        for f in ROOT.rglob('*.json'):json.loads(f.read_text())
        checks.append('All JSON parses')
        sources=load('sources/local-inputs.json')['sources']+load('sources/external-sources.json')['sources']
        source_ids={x['id'] for x in sources}
        require(len(source_ids)==len(sources),'Duplicate source IDs')
        for s in sources:
            if 'content_sha256' in s:
                require(bool(re.fullmatch('[0-9a-f]{64}',s['content_sha256'])),f'Invalid source hash: {s["id"]}')
                require(safe(s['path']),f'Unsafe source path: {s["id"]}')
            else:require(urlsplit(s['url']).scheme=='https',f'Invalid source URL: {s["id"]}')
        checks.append('Source IDs, hash syntax and locators')
        for f in ROOT.rglob('*.md'):
            text=f.read_text()
            for ref in re.findall(r'\[([A-Z][A-Z0-9-]{2,})\](?!\()',text):
                require(ref in source_ids,f'Unresolved source {ref}: {f.relative_to(ROOT)}')
            for ref in re.findall(r'\[[^\]\n]+\]\(([^)]+)\)',text):
                parts=urlsplit(ref)
                if parts.scheme or ref.startswith('#'):continue
                target=(f.parent/unquote(parts.path)).resolve()
                require(target.is_relative_to(ROOT) and target.exists(),f'Broken local link {ref}: {f.relative_to(ROOT)}')
        checks.append('Markdown links and source citations')
        for name in ['kernelbender.todo-plan.json','kda-integration.todo-plan.json']:
            plan=load('planning/'+name)
            require(plan['schema_version']==3,f'Not native v3: {name}')
            ts=plan['tasks'];ids=[t['id'] for t in ts];by={t['id']:t for t in ts}
            require(len(ids)==len(set(ids)),f'Duplicate tasks: {name}')
            edges={};gids=[]
            for t in ts:
                tid=t['id'];edges[tid]=[]
                require(bool(t.get('notes')),f'Missing persisted task notes: {tid}')
                require(t.get('kind') in {'task','epic','integration'},f'Unsupported kind: {tid}')
                require(t['parallel_policy']=='serial',f'Unexpected initial lane policy: {tid}')
                scope=t['scope'];allowed=scope['exclusive_paths']+scope['read_paths']
                for group in ('exclusive_paths','read_paths','forbidden_paths'):
                    require(all(safe(p) for p in scope[group]),f'Unsafe scope: {tid}')
                if t.get('parent_id'):require(t['parent_id'] in by,f'Unknown parent: {tid}')
                for d in t.get('depends_on',[]):
                    require(d['type']=='task' and d['task_id'] in by,f'Unknown dependency: {tid}')
                    require(d['task_id']!=t.get('parent_id'),f'Aggregate incorrectly blocks child: {tid}')
                    edges[tid].append(d['task_id'])
                for a in t.get('produced_artifacts',[]):
                    require(safe(a['path']) and within(a['path'],scope['exclusive_paths']),f'Artifact outside owned paths: {tid}/{a["path"]}')
                for g in t['gates']:
                    gids.append(g['id'])
                    require(g['type'] in {'command','manual','task_state'},f'Unknown gate: {g["id"]}')
                    if g['type']=='command':
                        require(isinstance(g.get('argv'),list) and g['argv'] and all(isinstance(a,str) for a in g['argv']),f'Invalid argv: {g["id"]}')
                        require(g.get('cwd')=='.' and bool(g.get('input_paths')),f'Unscoped cwd: {g["id"]}')
                    if g['type']=='task_state':require(g.get('task_id') in by and g.get('status')=='done',f'Invalid aggregate gate: {g["id"]}')
                    for p in g.get('input_paths',[]):
                        require(safe(p) and within(p,allowed),f'Gate input outside scope: {g["id"]}/{p}')
                for ref in re.findall(r'planning/kernelbender-bootstrap/([^,\n]+)',t['notes']):
                    # Explicit design refs are checked via their original files below; prose may have sentence punctuation.
                    if ref.endswith('.'):
                        ref=ref[:-1]
                    if ' ' not in ref:
                        require((ROOT/ref).exists(),f'Missing task input: {tid}/{ref}')
            require(len(gids)==len(set(gids)),f'Duplicate gates: {name}')
            seen=set();active=set()
            def visit(tid):
                if tid in active:raise ValueError('Dependency cycle: '+tid)
                if tid in seen:return
                active.add(tid)
                for d in edges[tid]:visit(d)
                active.remove(tid);seen.add(tid)
            for tid in ids:visit(tid)
            for run in plan['runs']:
                require(isinstance(run['charter'],dict) and run['root_task_id'] in by,'Invalid run root/charter')
                require(sum(not l.get('parent_lane_id') for l in run['lanes'])==1,'Run lacks unique root lane')
                assigned=[tid for l in run['lanes'] for tid in l['tasks']]
                require(len(assigned)==len(set(assigned)) and set(assigned)==set(ids),'Task lane assignment mismatch')
        checks.append('Both plan DAGs, IDs, notes, artifacts, scoped gates and lane assignments (structural only)')
        skill=ROOT/'draft/skills/kernelbender'
        text=(skill/'SKILL.md').read_text()
        match=re.match(r'^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n',text)
        require(bool(match),'Draft frontmatter not the expected simple portable form')
        if match:
            require(match[1]==skill.name and len(match[1])<=64,'Skill name mismatch')
            require(0<len(match[2])<=1024,'Skill description length')
        require(len(text.splitlines())<500,'SKILL.md exceeds proposed line budget')
        require(len(list((skill/'references/bridges').glob('*.md')))==10,'Expected ten bridges')
        require(len(list((skill/'examples').glob('*.md')))==4,'Expected four worked examples')
        for f in skill.rglob('*.md'):
            require('evaluation/scenarios.json' not in f.read_text() and 'evaluation/native-pilot.json' not in f.read_text(),'Evaluator answer material leaked into runtime docs')
        require(len(load('evaluation/scenarios.json')['scenarios'])==6,'Expected six probes')
        require(load('evaluation/native-pilot.json')['results'] is None,'Pilot results must not be fabricated')
        checks.append('Draft skill metadata, declared substrate, example counts and evaluator separation')
        if args.verify_manifest:
            listed=set()
            for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
                digest,name=line.split('  ',1)
                require(safe(name),'Unsafe manifest entry')
                listed.add(name);p=ROOT/name
                require(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,'Manifest mismatch: '+name)
            actual={f.relative_to(ROOT).as_posix() for f in ROOT.rglob('*') if f.is_file() and f.name!='MANIFEST.sha256' and '__pycache__' not in f.parts}
            require(listed==actual,'Manifest coverage mismatch')
            checks.append('Manifest hashes and complete file coverage')
    except (OSError,ValueError,KeyError,TypeError) as e:errors.append(type(e).__name__+': '+str(e))
    print(json.dumps({'status':'passed' if not errors else 'failed','checks':checks,'errors':errors,'limits':['Structural package checks are not native Todo validation or application.','No model/skill efficacy trial, GPU execution or KDA installation was performed.']},indent=2))
    return int(bool(errors))

if __name__=='__main__':raise SystemExit(main())
