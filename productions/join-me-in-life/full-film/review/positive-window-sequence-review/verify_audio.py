"""Independent decoded waveform timing check, with no listening claim."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np

HERE=Path(__file__).resolve().parent
FILM=HERE.parent.parent
ROOT=FILM.parents[2]
OUT=ROOT/'build/positive-window-sequence-review'
OUT.mkdir(parents=True,exist_ok=True)
SOURCE=FILM.parent/'full-song/track-49.mp3'
VIDEO=FILM/'exports/Join_Me_in_Life_Positive_Window_Context_Proof.mp4'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='0fe0f566e985a0b028e12543679d3b142ee7b1b62425fcb595799b35ba116cbb'
assert hashlib.sha256(VIDEO.read_bytes()).hexdigest()=='dfece1dd258e0da59a2d58fe468670a76447a3ab17bdd3ab1d9afd5f436791d2'

def decode(path,trim):
    command=['ffmpeg','-v','error']
    if trim:command+=['-ss',str(998/24)]
    command+=['-i',str(path)]
    if trim:command+=['-t',str(898/24)]
    return np.frombuffer(subprocess.check_output(command+['-vn','-ac','1','-ar','4000','-f','f32le','-']),dtype='<f4').astype(float)

source,output=decode(SOURCE,True),decode(VIDEO,False)
def correlation(lag):
    a,b=(source[-lag:],output) if lag<0 else (source,output[lag:])
    n=min(len(a),len(b));a,b=a[:n],b[:n]
    a,b=a-a.mean(),b-b.mean()
    return float(np.dot(a,b)/np.sqrt(np.dot(a,a)*np.dot(b,b)))

coarse=max(range(-400,401,10),key=correlation)
lag=max(range(coarse-10,coarse+11),key=correlation)
score=correlation(lag)
assert lag==0 and score>0.999
result={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'source_start_seconds':998/24,'source_duration_seconds':898/24,'source_seek':'FFmpeg input-side -ss','sample_rate':4000,'lag_search_seconds':[-0.1,0.1],'correlation':score,'offset_seconds':lag/4000,'source_samples':len(source),'output_samples':len(output),'scope':'Independent decoded waveform alignment; no listening or phoneme-sync claim.'}
(OUT/'audio-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
