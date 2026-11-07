#!/usr/bin/env python3
"""Decode a local benchmark and build review evidence, not a quality verdict."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
from fractions import Fraction

import numpy as np


def run(command):
    return subprocess.run(command,capture_output=True,check=True).stdout


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video',type=Path)
    args=parser.parse_args()
    video=args.video.resolve();out=video.parent
    probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format',
                          '-of','json',str(video)]))
    (out/'ffprobe.json').write_text(json.dumps(probe,indent=2))
    stream=next(s for s in probe['streams'] if s['codec_type']=='video')
    width,height=stream['width'],stream['height']
    # FFmpeg decodes every frame; a failed decode aborts the review.
    raw=run(['ffmpeg','-v','error','-i',str(video),'-pix_fmt','rgb24','-f','rawvideo','-'])
    frames=np.frombuffer(raw,np.uint8).reshape(-1,height,width,3)
    if len(frames)<2:raise ValueError('Need at least two decoded frames')
    expected_path=out/'video-metrics.json'
    expected=json.loads(expected_path.read_text()) if expected_path.exists() else None
    if expected and (len(frames)!=expected['frames'] or width!=expected['width'] or height!=expected['height']):
        raise ValueError('Decoded video differs from requested frame count or dimensions')
    fps=float(Fraction(stream['avg_frame_rate']))
    duration=float(stream.get('duration',probe['format']['duration']))
    if abs(duration-len(frames)/fps)>0.05:
        raise ValueError('Frame count, frame rate, and duration disagree')
    values=frames.astype(np.float32)
    differences=np.abs(np.diff(values,axis=0)).mean(axis=(1,2,3))
    metrics={
        'frames':len(frames),'width':width,'height':height,
        'fps':fps,'duration_seconds':duration,
        'requested_dimensions_and_frames_match':True if expected else None,
        'unique_decoded_frames':len({hashlib.sha256(a.tobytes()).digest() for a in frames}),
        'mean_consecutive_mae_255':float(differences.mean()),
        'max_consecutive_mae_255':float(differences.max()),
        'first_last_mae_255':float(np.abs(values[-1]-values[0]).mean()),
        'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),
        'note':'Pixel change is not a motion-quality or acting score; visual review is required.'}
    (out/'motion-measurements.json').write_text(json.dumps(metrics,indent=2))
    columns=min(9,math.ceil(math.sqrt(len(frames))))
    rows=math.ceil(len(frames)/columns)
    label='drawtext=text=%{n}:x=5:y=5:fontcolor=white:box=1:boxcolor=black@0.7:fontsize=15'
    run(['ffmpeg','-v','error','-i',str(video),'-vf',
         f'scale=256:-1,{label},tile={columns}x{rows}',
         '-frames:v','1','-y',str(out/'all-frames.jpg')])
    indices=np.unique(np.linspace(0,len(frames)-1,10).round().astype(int))
    select='+'.join(f'eq(n\\,{index})' for index in indices)
    run(['ffmpeg','-v','error','-i',str(video),'-vf',
         f'{label},select={select},tile=5x2',
         '-frames:v','1','-y',str(out/'ten-frames-fullsize.jpg')])
    print(json.dumps(metrics,indent=2))


if __name__=='__main__':main()
