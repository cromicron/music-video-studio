#!/usr/bin/env python3
"""Rank native adjacent-frame changes for human review; never judge motion quality."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np


def spatial_score(pixel_difference):
    height, width = pixel_difference.shape
    tile = 32
    patches = pixel_difference.reshape(height//tile,tile,width//tile,tile).mean(axis=(1,3))
    y,x = np.unravel_index(np.argmax(patches), patches.shape)
    return {'fullframe_mean':float(pixel_difference.mean()),'maximum_32px_patch_mean':float(patches[y,x]),
            'maximum_patch_xywh':[int(x)*tile,int(y)*tile,tile,tile]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video',required=True,type=Path)
    parser.add_argument('--keeper',required=True,nargs=2,type=int)
    parser.add_argument('--report',required=True,type=Path)
    args=parser.parse_args()
    if args.report.exists():parser.error('Preserve evidence; choose a fresh report')
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,nb_frames,avg_frame_rate','-of','json',str(args.video)],text=True))['streams'][0]
    width,height=probe['width'],probe['height'];first,last=args.keeper
    if width%32 or height%32:parser.error('Native dimensions must divide into32pixel patches')
    if not 0<=first<last<=int(probe['nb_frames']):parser.error('Keeper outside raw clip')
    proc=subprocess.Popen(['ffmpeg','-v','error','-xerror','-i',str(args.video),'-map','0:v:0','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    size=width*height*3;previous=None;older=None;adjacent=[];reversals=[];index=0
    while True:
        data=proc.stdout.read(size)
        if not data:break
        if len(data)!=size:raise RuntimeError('Partial decoded frame')
        frame=np.frombuffer(data,dtype=np.uint8).reshape(height,width,3).astype(np.int16)
        if previous is not None:
            diff=np.abs(frame-previous).mean(axis=2)
            adjacent.append({'transition':[index-1,index],**spatial_score(diff)})
        if older is not None:
            # Triangle surplus highlights one-frame reversals; natural action can also score high.
            reversal=(np.abs(older-previous)+np.abs(previous-frame)-np.abs(older-frame)).mean(axis=2)
            reversals.append({'middle_frame':index-1,**spatial_score(reversal)})
        older,previous=previous,frame;index+=1
    error=proc.stderr.read().decode();code=proc.wait()
    if code or index!=int(probe['nb_frames']):raise RuntimeError('Incomplete decode: '+error)
    boundaries=[x for x in adjacent if any(abs(x['transition'][1]-edge)<=4 for edge in [first,last-1,last])]
    top=lambda values:sorted(values,key=lambda x:x['maximum_32px_patch_mean'],reverse=True)[:16]
    report={'schema':'jml-native-temporal-triage/v1','observed_utc':datetime.now(timezone.utc).isoformat(),
        'video':str(args.video),'video_sha256':hashlib.sha256(args.video.read_bytes()).hexdigest(),
        'frames':index,'fps':probe['avg_frame_rate'],'dimensions':[width,height],'keeper':args.keeper,
        'scope':'Read-only review prioritization, not anomaly detection or motion/identity acceptance. Scores are RGB0–255 units. Real acting/camera movement can rank high; subtle defects can rank low.',
        'mandatory_boundary_transitions':boundaries,'ranked_fullframe_changes':sorted(adjacent,key=lambda x:x['fullframe_mean'],reverse=True)[:16],'ranked_adjacent_changes':top(adjacent),'ranked_single_frame_reversals':top(reversals),
        'all_adjacent_changes':adjacent,'all_single_frame_reversals':reversals,
        'review_gate':'Always inspect exact keeper entry/tail and native guide transitions irrespective of ranking, plus full-range1x motion and musical joins.'}
    args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'report':str(args.report),'top_fullframe':[x['transition'] for x in sorted(adjacent,key=lambda x:x['fullframe_mean'],reverse=True)[:16]],'top_adjacent':[x['transition'] for x in top(adjacent)],'top_reversal_frames':[x['middle_frame'] for x in top(reversals)],'acceptance':'none'}))

if __name__=='__main__':main()
