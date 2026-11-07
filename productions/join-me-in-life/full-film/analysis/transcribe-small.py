from faster_whisper import WhisperModel
import json,time,subprocess,numpy as np
from pathlib import Path
root=Path(__file__).resolve().parent
model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=3,download_root=str(root.parents[3]/'build/asr-model-cache'))
pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(root.parent.parent/'full-song/track-49.mp3'),'-f','f32le','-ac','1','-ar','16000','-'])
audio=np.frombuffer(pcm,dtype=np.float32)
segments,info=model.transcribe(audio,language='en',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
out=[]
for s in segments:
 d={'start':s.start,'end':s.end,'text':s.text,'avg_logprob':s.avg_logprob,'no_speech_prob':s.no_speech_prob,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in s.words]}
 out.append(d);print(f'{s.start:.2f}–{s.end:.2f}: {s.text}',flush=True)
 (root/'asr-small-en.json').write_text(json.dumps(out,indent=2))
print('Done',flush=True)
