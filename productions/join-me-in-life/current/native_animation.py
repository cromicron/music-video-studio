"""Small, editable 2D animation controls. No generated video is needed here.

Mouth drawings are exposed with CONSTANT keys; no face geometry is stretched.
Breathing is confined to torso interiors with compact support, under 1.1 px
in the source image. Faces, silhouettes and background stay fixed. Hair and
jewellery lying on those torso areas can share the very small displacement.
"""
import json
import math
from pathlib import Path
import bpy

ROOT=Path(__file__).resolve().parent
FPS=24

# 0 closed, 1 narrow/parted, 2 open vowel, 3 rounded vowel.
# Sparse vowel/consonant groups, edited against the supplied word timestamps.
PATTERNS={
 'that\'s':[(0,1),(.16,2),(.7,1)],'the':[(0,1),(.25,2)],
 'night':[(0,1),(.14,2),(.62,1)],'talking':[(0,1),(.12,2),(.55,1),(.73,2),(.87,1)],
 'it':[(0,1)],"isn't":[(0,1),(.45,2),(.72,1)],'you':[(0,1),(.13,3)],
 'i':[(0,2),(.65,1)],'know':[(0,1),(.2,3)],'how':[(0,2),(.62,3)],
 'pulls':[(0,0),(.16,3),(.8,1)],'pulled':[(0,0),(.16,3),(.8,1)],
 'at':[(0,2),(.75,1)],'me':[(0,0),(.14,1)],'too':[(0,1),(.14,3)],
 'baby':[(0,0),(.12,2),(.45,0),(.56,1)],'join':[(0,1),(.15,3),(.55,2),(.8,1)],
 'in':[(0,1)],'life':[(0,1),(.12,2),(.7,1)],
 'just':[(0,1),(.15,2),(.78,1)],'tonight':[(0,1),(.1,3),(.3,1),(.38,2),(.80,1)],
 'give':[(0,1),(.2,2),(.8,1)],'one':[(0,3),(.25,2),(.78,1)],
 'more':[(0,0),(.16,3)],'winter':[(0,3),(.2,1),(.60,2),(.8,1)],
 'morning':[(0,0),(.13,3),(.56,1),(.72,2),(.85,1)],
 'stay':[(0,1),(.2,2),(.8,1)],'with':[(0,3),(.23,1)],
 'until':[(0,2),(.42,1)],"it's":[(0,1)],'light':[(0,1),(.15,2),(.8,1)],
}

def exposures():
    data=json.loads((ROOT/'word_timing.json').read_text()); poses=[0]*1440
    for seg in data:
        for word in seg['words']:
            a,b=word['start'],word['end'];w=word['word'].strip().lower().strip('.,!?')
            if w not in PATTERNS:continue
            # Each word owns its interval. A following word overrides the one-
            # frame lead overlap; no previous-word closure may interrupt it.
            start=max(0,round(a*FPS)-1);end=min(len(poses),round(b*FPS))
            changes=[(max(0,round((a+(b-a)*fraction)*FPS)-1),pose) for fraction,pose in PATTERNS[w]]
            for f in range(start,end):
                pose=changes[0][1]
                for at,value in changes:
                    if at<=f:pose=value
                poses[f]=pose
    # The automatic word alignment ends "you" before the sung /u:/ finishes.
    # Preserve its rounded drawing through the remaining performance shot;
    # its existing onset is untouched. No closing pose during the held note.
    for f in range(round(13.32*FPS),round(14.125*FPS)):
        poses[f]=3
    return [(f,p) for f,p in enumerate(poses) if f==0 or p!=poses[f-1]]

def draw_mouth(nodes,links,base_colour,uv,start,end,filename,mask_function,interpolation):
    if filename not in ['P01_Verse_Performance.png','P02_Chorus_Performance.png']:return base_colour
    control=nodes.new('ShaderNodeValue');control.label='Drawn mouth exposure (0 closed, 1 narrow, 2 open, 3 round)'
    keys=exposures();initial=0
    for f,p in keys:
        if f+1<=start:initial=p
    local=[(start,initial)]+[(f+1,p) for f,p in keys if start<f+1<=end]
    for f,p in local:
        control.outputs[0].default_value=p;control.outputs[0].keyframe_insert('default_value',frame=f)
    colour=base_colour
    if filename=='P01_Verse_Performance.png':
        bounds=(.428,.320,.023,.026)
        drawings=[(0,'P01_Mouth_Closed.png'),(2,'P01_Open_Vowel.png'),(3,'P01_Mouth_Round.png')]
    else:
        bounds=(.261,.140,.0145,.019)
        drawings=[(0,'P02_Mouth_Closed.png'),(1,'P02_Mouth_Narrow.png'),(3,'P02_Mouth_Round.png')]
    mask=mask_function(nodes,links,uv,bounds)
    for pose,asset in drawings:
        tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(ROOT/'assets'/asset),check_existing=True)
        equal=nodes.new('ShaderNodeMath');equal.operation='COMPARE';equal.inputs[1].default_value=pose;equal.inputs[2].default_value=.1
        links.new(control.outputs[0],equal.inputs[0]);factor=nodes.new('ShaderNodeMath');factor.operation='MULTIPLY'
        links.new(equal.outputs[0],factor.inputs[0]);links.new(mask,factor.inputs[1])
        mix=nodes.new('ShaderNodeMixRGB');links.new(factor.outputs[0],mix.inputs[0]);links.new(colour,mix.inputs[1]);links.new(tex.outputs['Color'],mix.inputs[2]);colour=mix.outputs[0]
    interpolation(control.id_data,'CONSTANT')
    return colour

def compact(u,v,cx,cy,rx,ry):
    x=(u-cx)/rx;y=(v-cy)/ry
    if abs(x)>=1 or abs(y)>=1:return 0.0
    return (1-x*x)**2*(1-y*y)**2

def garment_breath(obj,filename,start,end,interpolation):
    fields={
      'P01_Verse_Performance.png':[(.46,.59,.028,.13,1.0),(.46,.81,.052,.10,.65)],
      'P02_Chorus_Performance.png':[(.286,.29,.025,.065,.45),(.287,.365,.025,.035,.25)],
      'S02_Waiting_Closeup.png':[(.27,.69,.045,.11,.50),(.64,.72,.065,.13,.65)],
    }.get(filename)
    if not fields:return
    old=obj.data;w=max(v.co.x for v in old.vertices)-min(v.co.x for v in old.vertices);h=max(v.co.y for v in old.vertices)-min(v.co.y for v in old.vertices)
    nx,ny=120,68;verts=[];faces=[]
    for j in range(ny+1):
        for i in range(nx+1):verts.append(((i/nx-.5)*w,(.5-j/ny)*h,0))
    for j in range(ny):
        for i in range(nx):
            p=j*(nx+1)+i;faces.append((p,p+1,p+nx+2,p+nx+1))
    mesh=bpy.data.meshes.new(obj.name+' | tiny garment rig');mesh.from_pydata(verts,[],faces);mesh.update();uv=mesh.uv_layers.new()
    for p in mesh.polygons:
        for li in p.loop_indices:
            co=mesh.vertices[mesh.loops[li].vertex_index].co;uv.data[li].uv=(co.x/w+.5,co.y/h+.5)
    for mat in old.materials:mesh.materials.append(mat)
    obj.data=mesh;obj['rigid_artwork']=False;obj['native_breath']='Torso interiors only; maximum 1.1 source pixels; face and silhouette pinned'
    obj.shape_key_add(name='Unmodified drawing')
    max_px=0
    for k,(cx,cy,rx,ry,amplitude) in enumerate(fields):
        key=obj.shape_key_add(name=f'Subtle cloth breath {k+1}')
        for i,vert in enumerate(mesh.vertices):
            u=vert.co.x/w+.5;v=.5-vert.co.y/h
            weight=compact(u,v,cx,cy,rx,ry)
            dy=amplitude*.01*weight;dx=amplitude*.002*weight*((u-cx)/rx)
            key.data[i].co.x+=dx;key.data[i].co.y+=dy;max_px=max(max_px,math.hypot(dx,dy)*100)
        # Unequal inhale/exhale durations and a rest, no mechanical sine pumping.
        period=5.4 if k==0 else 5.9;offset=.14*k
        for f in range(start,end+1,3):
            phase=(((f-start)/FPS)+offset)%period/period
            if phase<.48:value=.5-.5*math.cos(math.pi*phase/.48)
            elif phase<.88:value=.5+.5*math.cos(math.pi*(phase-.48)/.40)
            else:value=0
            key.value=value;key.keyframe_insert('value',frame=f)
    interpolation(obj.data.shape_keys,'BEZIER')
    obj['maximum_breath_source_pixels']=max_px
    assert max_px<1.1

