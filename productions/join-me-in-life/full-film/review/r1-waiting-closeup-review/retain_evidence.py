"""Retain compact, hash-bound V4 closeup review evidence."""
from pathlib import Path
import gzip, hashlib, json, shutil
DEST=Path(__file__).resolve().parent
ROOT=next(p for p in DEST.parents if (p/'studio.json').is_file())
SRC=ROOT/'build/r1-waiting-closeup-review'
for name in ['checks.json','playback-summary.json','v4-joins-native.jpg',
             '1080-native-000.jpg','1080-native-crown.jpg','1080-eye-phases-native.jpg',
             'waiting-v4-playback-11.80.jpg','waiting-v4-playback-17.50.jpg']:
    shutil.copyfile(SRC/name,DEST/name)
(DEST/'playback-full.json.gz').write_bytes(gzip.compress((SRC/'playback.json').read_bytes(),mtime=0))
shutil.copyfile(ROOT/'productions/join-me-in-life/full-film/exports/Join_Me_in_Life_Waiting_Correction_Context_Proof_v4.manifest.json',DEST/'v4-export-manifest.json')
shutil.copyfile(ROOT/'build/r1-waiting-closeup-1080.manifest.json',DEST/'1080-export-manifest.json')
files=sorted(p for p in DEST.iterdir() if p.is_file() and p.name!='evidence-sha256.json')
(DEST/'evidence-sha256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
