"""Original-master alignment and ending level; no listening or phoneme claim."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np

HERE=Path(__file__).resolve().parent;FILM=HERE.parent.parent;ROOT=FILM.parents[2]
OUT=ROOT/'build/final-full-film-review';OUT.mkdir(parents=True,exist_ok=True)
SOURCE=FILM.parent/'full-song/track-49.mp3';VIDEO=ROOT/'build/Join_Me_in_Life_Full_Music_Video_QC.mp4'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='0fe0f566e985a0b028e12543679d3b142ee7b1b62425fcb595799b35ba116cbb'
assert hashlib.sha256(VIDEO.read_bytes()).hexdigest()=='ce666666ad5f81effa5ee47db624c2dff7f7f10a044b8e7c60a6baf1474b9f09'
def decode(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(path),'-vn','-ac','1','-ar','4000','-f','f32le','-']),dtype='<f4').astype(float)
source,output=decode(SOURCE),decode(VIDEO)
def correlation(lag):
    a,b=(source[-lag:],output) if lag<0 else (source,output[lag:])
    n=min(len(a),len(b));a,b=a[:n],b[:n];a,b=a-a.mean(),b-b.mean()
    return float(np.dot(a,b)/np.sqrt(np.dot(a,a)*np.dot(b,b)))
coarse=max(range(-400,401,10),key=correlation);lag=max(range(coarse-10,coarse+11),key=correlation);score=correlation(lag)
assert lag==0 and score>0.999
result={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),'sample_rate':4000,'lag_search_seconds':[-0.1,0.1],'correlation':score,'offset_seconds':lag/4000,'source_samples':len(source),'output_samples':len(output),'source_duration_seconds':len(source)/4000,'output_duration_seconds':len(output)/4000,'video_duration_seconds':6667/24,'last_10ms_output_rms':float(np.sqrt(np.mean(output[-40:]**2))),'scope':'Decoded original-master waveform alignment and end-level evidence. No listening or phoneme-sync claim.'}
(OUT/'audio-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
