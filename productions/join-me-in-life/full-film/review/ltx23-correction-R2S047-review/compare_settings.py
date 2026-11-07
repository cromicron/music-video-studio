"""Verify the R2S047/P1L09 comparison without attributing causality."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'studio.json').is_file())
BASE=ROOT/'productions/join-me-in-life/full-film/assets/motion'
OLD=BASE/'ltx23-positive-continuation/P1/P1L09'
NEW=BASE/'ltx23-positive-corrections/R2S/R2S047'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((OLD/'render.json').read_text());b=json.loads((NEW/'render.json').read_text())
keys=['seed','width','height','fps','start_image_sha256','end_image_sha256','start_image_dimensions','end_image_dimensions','conditioning','supplied_audio','model_audio_output']
unchanged={k:a['manifest'][k] for k in keys if a['manifest'][k]==b['manifest'][k]}
assert len(unchanged)==len(keys)
assert a['manifest']['frames']==225 and b['manifest']['frames']==113
assert a['manifest']['prompt']!=b['manifest']['prompt']
assert (OLD/'model-lock.json').read_bytes()==(NEW/'model-lock.json').read_bytes()
assert (OLD/'patches-applied.json').read_bytes()==(NEW/'patches-applied.json').read_bytes()
steps=lambda r:[(s['pass_no'],s['step']) for s in r['steps']]
assert steps(a)==steps(b)
ea=json.loads((OLD/'environment.json').read_text());eb=json.loads((NEW/'environment.json').read_text())
differences={k:{'P1L09':ea.get(k),'R2S047':eb.get(k)} for k in sorted(set(ea)|set(eb)) if ea.get(k)!=eb.get(k)}
assert set(differences)=={'host_available_bytes'}
for name in ['start-fitted.png','end-fitted.png']:assert (OLD/name).read_bytes()==(NEW/name).read_bytes()
record={'unchanged_manifest_fields':unchanged,'changed':{'frames':[225,113],'prompt':[a['manifest']['prompt'],b['manifest']['prompt']]},'identical_model_lock':True,'identical_patches':True,'identical_fitted_guide_files':True,'step_schedule':steps(b),'environment_differences':differences,'hashes':{str(p.relative_to(ROOT)):sha(p) for path in [OLD,NEW] for p in [path/'render.json',path/'model-lock.json',path/'patches-applied.json',path/'environment.json']},'scope':'Both duration and positive prompt changed. This is not a single-variable causal comparison; source behavior requires visual review.'}
(HERE/'comparison-checks.json').write_text(json.dumps(record,indent=2)+'\n')
print('Both duration and prompt changed; retained model/seed/guides/step schedule verified.')
