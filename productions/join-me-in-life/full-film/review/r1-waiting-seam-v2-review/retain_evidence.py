"""Keep compact frozen v2/v3 review evidence beside the report."""
from pathlib import Path
import gzip, hashlib, json, shutil
DEST=Path(__file__).resolve().parent
ROOT=next(p for p in DEST.parents if (p/'studio.json').is_file())
SRC=ROOT/'build/r1-waiting-seam-v2-review'
for name in ['checks.json','playback-summary.json','v3-joins-native.jpg',
             'waiting-v3-playback-11.40.jpg','waiting-v3-playback-11.80.jpg']:
    shutil.copyfile(SRC/name,DEST/name)
(DEST/'playback-full.json.gz').write_bytes(gzip.compress((SRC/'playback.json').read_bytes(),mtime=0))
for version in ['v2','v3']:
    name=f'Join_Me_in_Life_Waiting_Correction_Context_Proof_{version}.manifest.json'
    shutil.copyfile(ROOT/'productions/join-me-in-life/full-film/exports'/name,DEST/f'{version}-export-manifest.json')
files=sorted(p for p in DEST.iterdir() if p.is_file() and p.name!='evidence-sha256.json')
(DEST/'evidence-sha256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
