"""Render start/end crops for inspecting camera travel before final output."""
import argparse,json,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--cut',choices=['simple','experimental'],required=True)
p.add_argument('--format',choices=['wide','vert'],required=True)
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
a=p.parse_args(argv)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/f'Join_Me_in_Life_{a.cut}_{a.format}.blend'))
s=bpy.context.scene;s.render.resolution_percentage=40
out=ROOT/'camera_review'/a.cut/a.format;out.mkdir(parents=True,exist_ok=True)
for sh in json.loads((ROOT/f'camera_shots_{a.cut}.json').read_text()):
    first=round(sh['t0']*24)+1;last=min(1439,round(sh['t1']*24))
    for label,f in [('start',first),('end',last)]:
        s.frame_set(f);s.render.filepath=str(out/f"{sh['name']}_{label}.jpg")
        bpy.ops.render.render(write_still=True)
print('CAMERA_ENDPOINTS_READY',a.cut,a.format,flush=True)
