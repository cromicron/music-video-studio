"""Compare only these later supplied-mouth instructions with original pure exposures()."""
from pathlib import Path
import ast,hashlib,json
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
PROD=ROOT/'productions/join-me-in-life';FILM=PROD/'full-film'
manifest=json.loads((FILM/'exports/Join_Me_in_Life_Later_Short_Performance_Proof_v2.manifest.json').read_text())
segments=[s for shot in manifest['shots'] for s in shot.get('drawn_art_segments',[])]
source=PROD/'current/native_animation.py'
for filename in ['native_animation.py','word_timing.json']:
 assert hashlib.sha256((PROD/'current'/filename).read_bytes()).hexdigest()==segments[0]['provenance'][filename]['sha256']
tree=ast.parse(source.read_text())
nodes=[n for n in tree.body if (isinstance(n,ast.FunctionDef) and n.name=='exposures') or (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PATTERNS' for t in n.targets))]
ns={'json':json,'ROOT':PROD/'current','FPS':24}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ns)
track=[];last=0
for at,pose in ns['exposures']():
 while len(track)<at:track.append(last)
 last=pose
track.extend([last]*(1440-len(track)))
result=[]
for seg in segments:
 n=seg['frames'];default=1 if seg['source_key']=='verse_performance' else 2
 actual=[default]*n
 for patch in seg['patches']:
  for a,b in patch['runs']:actual[a:b]=[patch['pose']]*(b-a)
 offset=seg['start_frame']-2409;expected=track[offset:offset+n]
 result.append({'sourceKey':seg['source_key'],'masterFrameStart':seg['start_frame'],'frames':n,'matchedOriginalInstructions':sum(a==b for a,b in zip(actual,expected)),'allAgree':actual==expected,'poses':actual})
 assert actual==expected
out=ROOT/'build/short-reuse-placement-review/exposure-checks.json'
out.write_text(json.dumps({'scope':'Instruction comparison with original pure function; encoded face inspection is separate. Not an acoustic sync test.','segments':result},indent=2)+'\n')
print(json.dumps([{k:v for k,v in s.items() if k!='poses'} for s in result],indent=2))
