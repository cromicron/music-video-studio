#!/usr/bin/env python3
"""Verify an encoded delivery derivative against its accepted master, without raw dumps."""
import argparse, hashlib, json, re, struct, subprocess
from fractions import Fraction
from pathlib import Path

def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True,check=True)
    return r

def probe(path,args):
    r=run(['ffprobe','-v','error']+args+['-of','json',str(path)])
    assert not r.stderr.strip(),r.stderr
    return json.loads(r.stdout)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--encode-record',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(); assert not a.output.exists()
    rec=json.loads(a.encode_record.read_text()); master=Path(rec['accepted_master']['file']); viewing=Path(rec['viewing_copy']['file'])
    for key in ['accepted_master','viewing_copy']:
        data=rec[key]; path=Path(data['file'])
        assert path.stat().st_size==data['bytes']
        assert hashlib.file_digest(path.open('rb'),'sha256').hexdigest()==data['sha256']
    assert viewing.stat().st_size<100*1024**2
    streams=probe(viewing,['-show_streams'])['streams']
    assert len(streams)==2
    for s in streams: assert Fraction(s['start_time'])==0
    v=next(s for s in streams if s['codec_type']=='video')
    assert (v['width'],v['height'],v['pix_fmt'],v['avg_frame_rate'])==(1920,1080,'yuv420p','24/1')
    points=probe(viewing,['-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time'])['frames']
    pts=[Fraction(f['best_effort_timestamp_time']) for f in points]
    assert len(pts)==6667 and pts[0]==0
    assert all(abs(t-Fraction(i,24))<=Fraction(1,100000) for i,t in enumerate(pts))
    packetargs=['-select_streams','a:0','-show_packets','-show_entries','packet=pts,dts,duration,size,data_hash','-show_data_hash','sha256']
    audio_a=probe(master,packetargs)['packets']; audio_b=probe(viewing,packetargs)['packets']
    assert audio_a==audio_b
    print(json.dumps({'frames':len(pts),'audio_packets':len(audio_a),'both_stream_origins':0}),flush=True)
    run(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(viewing),'-f','null','-'])
    cmd=['ffmpeg','-hide_banner','-threads','2','-i',str(master),'-threads','2','-i',str(viewing),'-filter_complex_threads','1','-lavfi','[0:v][1:v]ssim','-an','-f','null','-']
    ssim=run(cmd); score=[l for l in ssim.stderr.splitlines() if 'SSIM Y:' in l][-1]
    atoms=[]
    with viewing.open('rb') as f:
        while f.tell()<viewing.stat().st_size:
            off=f.tell(); size,typ=struct.unpack('>I4s',f.read(8))
            if size==1: size=struct.unpack('>Q',f.read(8))[0]
            if size==0: size=viewing.stat().st_size-off
            atoms.append({'type':typ.decode(),'offset':off,'bytes':size}); f.seek(off+size)
    assert next(t['offset'] for t in atoms if t['type']=='moov')<next(t['offset'] for t in atoms if t['type']=='mdat')
    out={'schema':'jml-c-final-viewing-technical/v1','master':rec['accepted_master'],'viewing_copy':rec['viewing_copy'],'frames':len(pts),'cadence':'All decoded PTS checked against frame index /24, tolerance10us, zero origin.','streams':[{k:s.get(k) for k in ['codec_type','codec_name','width','height','pix_fmt','start_time','duration','avg_frame_rate','sample_rate','channels']} for s in streams],'audio_packets_and_timestamps_identical':True,'audio_packet_count':len(audio_a),'audio_packet_list_sha256':hashlib.sha256(json.dumps(audio_a,sort_keys=True).encode()).hexdigest(),'full_decode_pass':True,'ssim':score,'ssim_all':float(re.search(r'All:([0-9.]+)',score).group(1)),'ssim_command':cmd,'mp4_atoms':atoms,'faststart_verified':True,'below_100MiB':True,'encode_record':str(a.encode_record),'scope':'Technical derivative check. Native sampled visual quality and actual brief browser playback recorded separately.'}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'result':'PASS_TECHNICAL','ssim':score,'output':str(a.output)}))
if __name__=='__main__': main()
