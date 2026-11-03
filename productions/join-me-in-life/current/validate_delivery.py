"""Decode all six delivery videos and verify original AAC packet preservation."""
from pathlib import Path
import hashlib
import json
import struct
import subprocess

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'Revision_4'

def run(args):
    return subprocess.run(args,check=True,capture_output=True,text=True).stdout

def audio_hash(path):
    return run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy',
                '-f','hash','-hash','sha256','-']).strip()

def fast_start(path):
    atoms=[]
    with path.open('rb') as f:
        position=0;total=path.stat().st_size
        while position<total:
            f.seek(position);head=f.read(16)
            size,kind=struct.unpack('>I4s',head[:8])
            if size==1:size=struct.unpack('>Q',head[8:16])[0]
            if size==0:size=total-position
            assert size>=8,(position,size)
            atoms.append(kind.decode('ascii'));position+=size
    return 'moov' in atoms and atoms.index('moov')<atoms.index('mdat')

def main():
    original=audio_hash(ROOT/'audio.mp4')
    expected=[
        'Join_Me_in_Life_Short_Camera.mp4',
        'Join_Me_in_Life_Short_Clean_Camera.mp4',
        'Join_Me_in_Life_Widescreen_Camera.mp4',
        'Join_Me_in_Life_Short_Hybrid_Camera.mp4',
        'Join_Me_in_Life_Short_Clean_Hybrid_Camera.mp4',
        'Join_Me_in_Life_Widescreen_Hybrid_Camera.mp4']
    results=[]
    previous={}
    if (ROOT/'delivery_validation.json').is_file():
        previous={entry['file']:entry for entry in json.loads((ROOT/'delivery_validation.json').read_text()).get('outputs',[])}
    for name in expected:
        path=OUT/name
        file_hash=hashlib.sha256(path.read_bytes()).hexdigest()
        if 'Hybrid' not in name and name in previous and previous[name].get('sha256')==file_hash:
            result=dict(previous[name]);result['unchanged_reference_hash_verified']=True
            results.append(result);print('UNCHANGED_REFERENCE_VALID',name,flush=True);continue
        probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
        video=next(s for s in probe['streams'] if s['codec_type']=='video')
        audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
        progress=run(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(path),
                      '-map','0:v:0','-an','-sn','-progress','pipe:1','-nostats','-f','null','-'])
        decoded=int([line.split('=')[1] for line in progress.splitlines() if line.startswith('frame=')][-1])
        expected_size=(1920,1080) if 'Widescreen' in name else (1080,1920)
        digest=audio_hash(path)
        assert (video['width'],video['height'])==expected_size,name
        assert video['r_frame_rate']=='24/1' and decoded==1439,name
        assert video['codec_name']=='h264' and video['pix_fmt']=='yuv420p',name
        assert video.get('color_space')=='bt709' and video.get('color_range')=='tv',name
        assert audio['codec_name']=='aac' and digest==original,name
        assert fast_start(path),name
        results.append({'file':name,'bytes':path.stat().st_size,
                        'sha256':file_hash,
                        'width':video['width'],'height':video['height'],
                        'fps':video['r_frame_rate'],'decoded_frames':decoded,
                        'video_duration':video['duration'],'audio_duration':audio['duration'],
                        'video_codec':video['codec_name'],'pixel_format':video['pix_fmt'],
                        'color_space':video['color_space'],'color_range':video['color_range'],
                        'audio_packet_hash':digest,'original_audio_preserved':True,
                        'full_decode':'pass','fast_start':True})
        print('DELIVERY_VALID',name,decoded,flush=True)
    (ROOT/'delivery_validation.json').write_text(json.dumps({'original_audio_packet_hash':original,'outputs':results},indent=2)+'\n')

if __name__=='__main__':main()
