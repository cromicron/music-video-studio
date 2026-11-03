"""Render the entire corrected passage's key moments, including source joins."""
from pathlib import Path
import argparse,sys,bpy
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--format',choices=['wide','vert'],required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/f'Join_Me_in_Life_experimental_{a.format}.blend'))
s=bpy.context.scene;s.render.resolution_percentage=40
dest=ROOT/'revision4_review'/a.format;dest.mkdir(parents=True,exist_ok=True)
frames=[307,319,321,329,335,339,725,769,815,816,817,818,841,853,865,876,877,889,913,936,937,938,961,1009,1010]
for f in frames:
    s.frame_set(f);s.render.filepath=str(dest/f'{f:04d}.jpg');bpy.ops.render.render(write_still=True)
print('REVISION4_SAMPLES_READY',a.format,flush=True)
