"""Read-only CPU timing evidence. Outputs are diagnostic, not lyric truth."""
import subprocess, json
import numpy as np
from scipy.signal import stft, find_peaks, fftconvolve
from pathlib import Path
root=Path(__file__).resolve().parent
source=root.parent.parent/'full-song/track-49.mp3'
b=subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-ac','1','-ar','11025','-f','f32le','-'])
y=np.frombuffer(b,dtype=np.float32); sr=11025; hop=256
f,t,z=stft(y,fs=sr,nperseg=1024,noverlap=1024-hop,boundary=None)
m=np.abs(z); flux=np.sum(np.maximum(np.diff(m,axis=1),0),axis=0); flux-=np.mean(flux)
ac=fftconvolve(flux,flux[::-1],mode='full')[len(flux)-1:]; lags=np.arange(len(ac))*hop/sr
idx=np.flatnonzero((lags>60/180)&(lags<60/70)); peaks,_=find_peaks(ac[idx]); best=sorted(idx[peaks],key=lambda k:ac[k],reverse=True)[:5]
candidates=[]
for k in best:
 a,b,c=[float(ac[v]) for v in [k-1,k,k+1]]; correction=0.5*(a-c)/(a-2*b+c)
 candidates.append({'bpm_coarse':float(60/lags[k]),'bpm_parabolic':float(60/((k+correction)*hop/sr)),'normalized_autocorrelation':float(ac[k]/ac[0])})
secs=[]
for k in range(int(np.ceil(len(y)/sr))):
 s=y[k*sr:(k+1)*sr]
 secs.append({'t':k,'rms_dbfs':round(float(20*np.log10(np.sqrt(np.mean(s*s))+1e-9)),2),'peak_dbfs':round(float(20*np.log10(np.max(np.abs(s))+1e-9)),2)})
(root/'audio-energy.json').write_text(json.dumps({'sr':sr,'duration_decoded':len(y)/sr,'tempo_candidates':candidates,'tempo_note':'Coarse spectral-flux autocorrelation; not an independently verified beat grid.','per_second':secs},indent=2)+'\n')
print(json.dumps(candidates))
