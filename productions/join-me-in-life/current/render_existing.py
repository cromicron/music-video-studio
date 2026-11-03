"""Resume a saved native Blender edit without rebuilding its animation."""
import argparse
import sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--format',choices=['wide','vert'],required=True)
p.add_argument('--cut',choices=['simple','experimental'],default='experimental')
p.add_argument('--ranges',default='1:1439',help='Inclusive ranges, e.g. 235:339,1011:1086')
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
a=p.parse_args(argv);bpy.ops.wm.open_mainfile(filepath=str(ROOT/f'Join_Me_in_Life_{a.cut}_{a.format}.blend'))
s=bpy.context.scene;s.render.resolution_percentage=100
dest=ROOT/'frames'/a.cut/a.format;dest.mkdir(parents=True,exist_ok=True)
for span in a.ranges.split(','):
    begin,end=map(int,span.split(':'))
    for f in range(begin,end+1):
        out=dest/f'frame_{f:04d}.jpg'
        if out.exists():continue
        s.frame_set(f);s.render.filepath=str(out);bpy.ops.render.render(write_still=True)
        if f%96==0:print('PROGRESS',a.format,f,flush=True)
print('RENDER_COMPLETE',a.format,a.ranges,flush=True)
