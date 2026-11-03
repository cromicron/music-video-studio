"""Create an editable 2D animation scene using Blender's native rig and renderer."""
import bpy
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
if not ASSETS.exists():
    ASSETS = ROOT.parent / 'anime_pilot' / 'assets'
ROOT.mkdir(exist_ok=True)
(ROOT / 'frames').mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 16
scene.cycles.use_denoising = False
scene.cycles.max_bounces = 1
scene.cycles.transparent_max_bounces = 12
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 192
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.world = bpy.data.worlds.new('Night')
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.015, 0.025, 0.055, 1)

def keyed(socket, points, interpolation='BEZIER'):
    for frame, value in points:
        socket.default_value = value
        socket.keyframe_insert('default_value', frame=frame)

def make_image(name, files, transitions=None):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    n, links = mat.node_tree.nodes, mat.node_tree.links
    n.clear()
    out = n.new('ShaderNodeOutputMaterial')
    emit = n.new('ShaderNodeEmission')
    trans = n.new('ShaderNodeBsdfTransparent')
    mix = n.new('ShaderNodeMixShader')
    links.new(trans.outputs[0], mix.inputs[1])
    links.new(emit.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], out.inputs['Surface'])
    textures = []
    for f in files:
        t = n.new('ShaderNodeTexImage')
        t.image = bpy.data.images.load(str(ASSETS / f), check_existing=True)
        t.image.alpha_mode = 'STRAIGHT'
        t.interpolation = 'Linear'
        t.extension = 'CLIP'
        textures.append(t)
    color, alpha = textures[0].outputs['Color'], textures[0].outputs['Alpha']
    eye_mask = None
    if transitions:
        uv = n.new('ShaderNodeTexCoord')
        sep = n.new('ShaderNodeSeparateXYZ'); links.new(uv.outputs['UV'],sep.inputs[0])
        masks=[]
        for axis,center,inner,outer in [('X',.49,.155,.19),('Y',.77,.043,.066)]:
            sub=n.new('ShaderNodeMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=center;links.new(sep.outputs[axis],sub.inputs[0])
            ab=n.new('ShaderNodeMath');ab.operation='ABSOLUTE';links.new(sub.outputs[0],ab.inputs[0])
            ramp=n.new('ShaderNodeMapRange');ramp.interpolation_type='SMOOTHERSTEP';ramp.clamp=True
            ramp.inputs['From Min'].default_value=inner;ramp.inputs['From Max'].default_value=outer
            ramp.inputs['To Min'].default_value=1;ramp.inputs['To Max'].default_value=0
            links.new(ab.outputs[0],ramp.inputs['Value']);masks.append(ramp.outputs[0])
        mask=n.new('ShaderNodeMath');mask.operation='MULTIPLY';links.new(masks[0],mask.inputs[0]);links.new(masks[1],mask.inputs[1]);eye_mask=mask.outputs[0]
    for i, t in enumerate(textures[1:]):
        cm = n.new('ShaderNodeMixRGB')
        cm.label = transitions[i][0]
        links.new(color, cm.inputs[1])
        links.new(t.outputs['Color'], cm.inputs[2])
        if i<2:
            control=n.new('ShaderNodeMath');control.operation='MULTIPLY';links.new(eye_mask,control.inputs[1]);keyed(control.inputs[0],transitions[i][1]);links.new(control.outputs[0],cm.inputs[0])
            color=cm.outputs[0]
        else:
            keyed(cm.inputs[0], transitions[i][1])
            am = n.new('ShaderNodeMixRGB')
            links.new(alpha, am.inputs[1])
            links.new(t.outputs['Alpha'], am.inputs[2])
            keyed(am.inputs[0], transitions[i][1])
            color, alpha = cm.outputs[0], am.outputs[0]
    links.new(color, emit.inputs['Color'])
    links.new(alpha, mix.inputs[0])
    return mat

def plane(name, width, height, position, material, nx=1, ny=1):
    verts = [((i/nx-.5)*width, (j/ny-.5)*height, 0) for j in range(ny+1) for i in range(nx+1)]
    faces=[]
    for j in range(ny):
        for i in range(nx):
            a=j*(nx+1)+i
            faces.append((a,a+1,a+nx+2,a+nx+1))
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    uv=mesh.uv_layers.new(name='Image coordinates')
    for polygon in mesh.polygons:
        for li in polygon.loop_indices:
            v=mesh.vertices[mesh.loops[li].vertex_index].co
            uv.data[li].uv=(v.x/width+.5,v.y/height+.5)
    obj=bpy.data.objects.new(name,mesh)
    scene.collection.objects.link(obj)
    obj.location=position
    obj.data.materials.append(material)
    return obj

bg=plane('Lake at dusk',18.4,18.4*941/1672,(0,0,-1),make_image('Painted background',['background.png']))
character=plane('Character drawing',7.2,10.8,(-2.6,-1.05,1),make_image('Expression drawings',
    ['character_neutral.png','character_gaze_down.png','character_blink.png','character_turned.png'],[
    ('Lower gaze',[(1,0),(73,0),(74,1),(192,1)]),
    ('Blinks',[(1,0),(35,0),(36,1),(38,1),(39,0),(71,0),(72,1),(75,1),(76,0),(192,0)]),
    ('Second shot',[(1,0),(96,0),(97,1),(192,1)])]),24,36)

arm=bpy.data.armatures.new('Reusable portrait rig')
rig=bpy.data.objects.new('Portrait animation controls',arm)
scene.collection.objects.link(rig)
rig.location=character.location
bpy.context.view_layer.objects.active=rig
rig.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
specs=[('Breath',(0,-5,0),(0,.2,0),None),('Head',(0,.2,0),(0,3.9,0),'Breath'),
       ('Left hair',(-1.3,2.7,0),(-2.6,-2,0),'Breath'),('Right hair',(1.5,2.7,0),(3,-2,0),'Breath')]
for name,head,tail,parent in specs:
    b=arm.edit_bones.new(name); b.head=head; b.tail=tail
    if parent: b.parent=arm.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT')
groups={name:character.vertex_groups.new(name=name) for name,*_ in specs}
def clamp(x): return max(0,min(1,x))
def smooth(x):
    x=clamp(x)
    return x*x*(3-2*x)
for v in character.data.vertices:
    x,y,_=v.co
    head=smooth((y-.1)/1.7)
    hair_height=smooth((3.5-y)/2)*smooth((y+4.7)/1.5)
    left=smooth((-x-1.15)/1.7)*hair_height*.85
    right=smooth((x-1.45)/1.5)*hair_height*.85
    remaining=1-left-right
    weights={'Head':head*remaining,'Breath':(1-head)*remaining,'Left hair':left,'Right hair':right}
    for name,w in weights.items():
        if w>0: groups[name].add([v.index],w,'REPLACE')
mod=character.modifiers.new('Native Blender armature','ARMATURE')
mod.object=rig
for b in rig.pose.bones:
    b.rotation_mode='XYZ'
for frame in [1,25,49,73,96,97,121,145,169,192]:
    t=(frame-1)/24
    breath=rig.pose.bones['Breath']
    breath.scale=(1+.0015*math.sin(t*1.55),1+.003*math.sin(t*1.55),1)
    breath.keyframe_insert('scale',frame=frame)
    head=rig.pose.bones['Head']
    head.rotation_euler.z=.008*math.sin(t*.85)-(.005 if frame>=73 else 0)
    head.keyframe_insert('rotation_euler',frame=frame)
    for name,phase in [('Left hair',0),('Right hair',1.4)]:
        b=rig.pose.bones[name]
        b.rotation_euler.z=.014*math.sin(t*1.4+phase)
        b.keyframe_insert('rotation_euler',frame=frame)

# A separate atmospheric layer uses Blender's procedural texture and keyframes.
fog=bpy.data.materials.new('Drifting lake mist'); fog.use_nodes=True
n,lk=fog.node_tree.nodes,fog.node_tree.links; n.clear()
out=n.new('ShaderNodeOutputMaterial'); tr=n.new('ShaderNodeBsdfTransparent')
em=n.new('ShaderNodeEmission'); em.inputs['Color'].default_value=(.24,.32,.48,1)
mix=n.new('ShaderNodeMixShader'); lk.new(tr.outputs[0],mix.inputs[1]); lk.new(em.outputs[0],mix.inputs[2]);lk.new(mix.outputs[0],out.inputs[0])
uv=n.new('ShaderNodeTexCoord'); mapping=n.new('ShaderNodeMapping'); lk.new(uv.outputs['UV'],mapping.inputs['Vector'])
mapping.inputs['Scale'].default_value=(3,9,1)
for frame,val in [(1,(0,0,0)),(192,(.5,0,0))]:
    mapping.inputs['Location'].default_value=val; mapping.inputs['Location'].keyframe_insert('default_value',frame=frame)
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2;lk.new(mapping.outputs[0],noise.inputs['Vector'])
mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=.11;lk.new(noise.outputs['Fac'],mul.inputs[0])
sep=n.new('ShaderNodeSeparateXYZ');lk.new(uv.outputs['UV'],sep.inputs[0])
angle=n.new('ShaderNodeMath');angle.operation='MULTIPLY';angle.inputs[1].default_value=math.pi;lk.new(sep.outputs['Y'],angle.inputs[0])
feather=n.new('ShaderNodeMath');feather.operation='SINE';lk.new(angle.outputs[0],feather.inputs[0])
alpha=n.new('ShaderNodeMath');alpha.operation='MULTIPLY';lk.new(mul.outputs[0],alpha.inputs[0]);lk.new(feather.outputs[0],alpha.inputs[1]);lk.new(alpha.outputs[0],mix.inputs[0])
plane('Mist over water',18,2.1,(0,-.4,0),fog)

camdata=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',camdata);scene.collection.objects.link(cam)
cam.location=(0,0,10);camdata.type='ORTHO';scene.camera=cam
for frame,x,y,scale in [(1,0,0,16),(96,-.25,.10,15.4),(97,-1.65,.88,13.0),(192,-1.9,1.02,12.6)]:
    cam.location=(x,y,10);cam.keyframe_insert('location',frame=frame)
    camdata.ortho_scale=scale;camdata.keyframe_insert('ortho_scale',frame=frame)

scene.timeline_markers.new('Eye contact',frame=1)
scene.timeline_markers.new('Blink',frame=36)
scene.timeline_markers.new('Lower gaze',frame=74)
scene.timeline_markers.new('Cut to three-quarter portrait',frame=97)
scene['workflow']='GPT image assets; native Blender armature, keyframes, procedural mist and Cycles rendering. No video generation.'
scene['scope']='Eight-second silent limited-animation study. Pose change is an editorial cut, not a continuous head turn.'
bpy.ops.file.pack_all()
scene.frame_set(1)
scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(ROOT/'frames'/'frame_')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Melancholy_Blender_Pilot.blend'))
scene.render.resolution_percentage=50
scene.render.filepath=str(ROOT/'preview.png')
bpy.ops.render.render(write_still=True)
print('READY',flush=True)
