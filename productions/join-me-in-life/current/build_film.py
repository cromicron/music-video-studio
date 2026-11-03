"""Native Blender illustrated edits: restrained simple cut and hybrid experiment.

Simple: rigid drawings and approved eye blinks. Hybrid: constant mouth drawing
substitutions, tiny torso-interior controls and two short movie textures.
No facial mesh stretching, optical flow, or interpolated mouth drawings.
"""
import argparse
import json
import sys
from pathlib import Path
import bpy

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from native_animation import draw_mouth,garment_breath
ASSETS=ROOT/'assets'
FPS=24
END=1439

def frame(t):return round(t*FPS)+1

def shot(name,a,b,art,wide,vert,vert_art=None):
    return dict(name=name,t0=a,t1=b,art=art,wide=wide,vert=vert,vert_art=vert_art)

# Camera tuples: normalized x/y and orthographic width (wide) or height (vert).
def get_shots(cut):
    return json.loads((ROOT/f'camera_shots_{cut}.json').read_text())

def linked_camera_samples(shots,fmt):
    """One continuous, monotone camera path over each movie/still join.

    Anchors sit at frame boundaries, rather than being repeated on both sides
    of a join. Adjacent segments share harmonic-mean tangents, so a live clip
    can become a held drawing without a pause or abrupt camera speed change.
    """
    groups={};samples={}
    for sh in shots:
        link=sh.get('camera_link')
        if isinstance(link,dict):link=link.get(fmt)
        if link:groups.setdefault(link,[]).append(sh)
    for members in groups.values():
        assert len(members)>1
        for left,right in zip(members,members[1:]):
            assert frame(left['t1'])==frame(right['t0'])
            assert left[fmt][1]==right[fmt][0]
        times=[frame(sh['t0']) for sh in members]+[frame(members[-1]['t1'])]
        points=[sh[fmt][0] for sh in members]+[members[-1][fmt][1]]
        durations=[b-a for a,b in zip(times,times[1:])]
        tangents=[]
        for axis in range(3):
            slopes=[(b[axis]-a[axis])/h for a,b,h in zip(points,points[1:],durations)]
            m=[slopes[0]]
            for i in range(1,len(points)-1):
                d0,d1=slopes[i-1:i+1];h0,h1=durations[i-1:i+1]
                w1,w2=2*h1+h0,h1+2*h0
                m.append(0.0 if d0*d1<=0 else (w1+w2)/(w1/d0+w2/d1))
            m.append(slopes[-1]);tangents.append(m)
        for i,sh in enumerate(members):
            h=durations[i]
            for f in range(times[i],min(END+1,times[i+1])):
                u=(f-times[i])/h;u2=u*u;u3=u2*u
                samples[(sh['name'],f)]=[
                    (2*u3-3*u2+1)*points[i][j]+(u3-2*u2+u)*h*tangents[j][i]
                    +(-2*u3+3*u2)*points[i+1][j]+(u3-u2)*h*tangents[j][i+1]
                    for j in range(3)]
    return samples

def set_interpolation(owner,mode):
    if not owner.animation_data or not owner.animation_data.action:return
    for layer in owner.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    for key in curve.keyframe_points:key.interpolation=mode

def eye_mask(nodes,links,uv,bounds):
    x,y,rx,ry=bounds
    separate=nodes.new('ShaderNodeSeparateXYZ');links.new(uv,separate.inputs[0]);outputs=[]
    for axis,centre,radius in [('X',x,rx),('Y',1-y,ry)]:
        sub=nodes.new('ShaderNodeMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=centre
        links.new(separate.outputs[axis],sub.inputs[0])
        absolute=nodes.new('ShaderNodeMath');absolute.operation='ABSOLUTE';links.new(sub.outputs[0],absolute.inputs[0])
        ramp=nodes.new('ShaderNodeMapRange');ramp.interpolation_type='SMOOTHERSTEP';ramp.clamp=True
        ramp.inputs['From Min'].default_value=radius*.72;ramp.inputs['From Max'].default_value=radius
        ramp.inputs['To Min'].default_value=1;ramp.inputs['To Max'].default_value=0;links.new(absolute.outputs[0],ramp.inputs[0])
        outputs.append(ramp.outputs[0])
    mult=nodes.new('ShaderNodeMath');mult.operation='MULTIPLY'
    links.new(outputs[0],mult.inputs[0]);links.new(outputs[1],mult.inputs[1]);return mult.outputs[0]

def make_plate(name,filename,offset,start,end,video_t0=None,native=False):
    im=bpy.data.images.load(str(ASSETS/filename),check_existing=True)
    w,h=im.size[0]/100,im.size[1]/100
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata([(-w/2,-h/2,0),(w/2,-h/2,0),(w/2,h/2,0),(-w/2,h/2,0)],[],[(0,1,2,3)])
    mesh.update();uv=mesh.uv_layers.new(name='Unmodified artwork')
    for poly in mesh.polygons:
        for li in poly.loop_indices:
            v=mesh.vertices[mesh.loops[li].vertex_index].co
            uv.data[li].uv=(v.x/w+.5,v.y/h+.5)
    mat=bpy.data.materials.new(name);mat.use_nodes=True
    n=mat.node_tree.nodes;lk=mat.node_tree.links;n.clear()
    tex=n.new('ShaderNodeTexImage');tex.image=im;tex.interpolation='Linear'
    if im.source=='MOVIE':
        tex.image_user.frame_start=frame(video_t0 if video_t0 is not None else (start-1)/FPS)
        tex.image_user.frame_duration=im.frame_duration
        tex.image_user.use_auto_refresh=True;tex.image_user.use_cyclic=False
    em=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial');colour=tex.outputs['Color']
    if filename=='S02_Waiting_Closeup.png':
        # Retain the eye-only blink treatment the user explicitly liked.
        # No vertices, mouths, tears, head positions or body parts are deformed.
        alt=n.new('ShaderNodeTexImage');alt.image=bpy.data.images.load(str(ASSETS/'S02_Blink.png'),check_existing=True)
        uvnode=n.new('ShaderNodeTexCoord')
        for label,bounds,delay in [('Her brief blink',(.267,.365,.075,.065),1.9),('His brief blink',(.606,.286,.065,.055),2.8)]:
            control=n.new('ShaderNodeValue');control.label=label
            keys=[(start,0),(end,0)];at=start+round(delay*FPS)
            if at+5<end:keys += [(at-2,0),(at,1),(at+2,1),(at+4,0)]
            for f,v in sorted(keys):control.outputs[0].default_value=v;control.outputs[0].keyframe_insert('default_value',frame=f)
            mask=eye_mask(n,lk,uvnode.outputs['UV'],bounds)
            factor=n.new('ShaderNodeMath');factor.operation='MULTIPLY'
            lk.new(control.outputs[0],factor.inputs[0]);lk.new(mask,factor.inputs[1])
            mix=n.new('ShaderNodeMixRGB');lk.new(factor.outputs[0],mix.inputs[0]);lk.new(colour,mix.inputs[1]);lk.new(alt.outputs['Color'],mix.inputs[2]);colour=mix.outputs[0]
        set_interpolation(mat.node_tree,'LINEAR')
    if native:
        uvnode=n.new('ShaderNodeTexCoord')
        colour=draw_mouth(n,lk,colour,uvnode.outputs['UV'],start,end,filename,eye_mask,set_interpolation)
    lk.new(colour,em.inputs['Color']);lk.new(em.outputs[0],out.inputs['Surface'])
    obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat);obj.location=(offset,0,0)
    obj['source_artwork']=filename;obj['rigid_artwork']=True
    if native:garment_breath(obj,filename,start,end,set_interpolation)
    return obj,w,h

def scene_setup(fmt,cut='simple'):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.preferences.edit.keyframe_new_interpolation_type='LINEAR'
    s=bpy.context.scene;s.name='Join Me in Life | '+cut+' | '+fmt
    s.render.engine='CYCLES';s.cycles.samples=1;s.cycles.use_denoising=False
    s.cycles.use_adaptive_sampling=False;s.cycles.max_bounces=0
    s.render.threads_mode='FIXED';s.render.threads=4;s.render.use_persistent_data=True
    s.render.resolution_x,s.render.resolution_y=(1920,1080) if fmt=='wide' else (1080,1920)
    s.render.resolution_percentage=100;s.render.fps=FPS;s.frame_start=1;s.frame_end=END
    s.view_settings.view_transform='Standard';s.view_settings.look='None'
    s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=97
    s.render.film_transparent=False
    cam_data=bpy.data.cameras.new('Edited camera');cam=bpy.data.objects.new('Edited camera',cam_data)
    s.collection.objects.link(cam);s.camera=cam;cam_data.type='ORTHO'
    shots=get_shots(cut);issues=[];linked=linked_camera_samples(shots,fmt)
    for i,sh in enumerate(shots):
        a=frame(sh['t0']);b=min(END,frame(sh['t1'])-1)
        fname=(sh.get('vert_art') or sh['art']) if fmt=='vert' else sh['art']
        obj,w,h=make_plate(sh['name'],fname,i*40,a,b,sh.get('video_t0'),native=cut=='experimental')
        obj.hide_render=True;obj.keyframe_insert('hide_render',frame=1)
        obj.hide_render=False;obj.keyframe_insert('hide_render',frame=a)
        if b<END:obj.hide_render=True;obj.keyframe_insert('hide_render',frame=b+1)
        for f in range(a,b+1):
            u=(f-a)/max(1,b-a);ease=sh.get('camera_ease',.25)
            u=(1-ease)*u+ease*(u*u*(3-2*u))
            x,y,scale=linked.get((sh['name'],f),[v0+(v1-v0)*u for v0,v1 in zip(sh[fmt][0],sh[fmt][1])])
            cam.location=(i*40+(x-.5)*w,(.5-y)*h,20);cam.keyframe_insert('location',frame=f)
            cam_data.ortho_scale=scale;cam_data.keyframe_insert('ortho_scale',frame=f)
            vw,vh=(scale,scale*9/16) if fmt=='wide' else (scale*9/16,scale)
            if x*w-vw/2<-.001 or x*w+vw/2>w+.001 or y*h-vh/2<-.001 or y*h+vh/2>h+.001:
                issues.append({'shot':sh['name'],'frame':f,'camera':[x,y,scale],'image':[w,h]})
        s.timeline_markers.new(sh['name'],frame=a)
    set_interpolation(cam,'LINEAR');set_interpolation(cam_data,'LINEAR')
    if issues:raise ValueError('Camera leaves source artwork: '+json.dumps(issues))
    s.sequence_editor_create().strips.new_sound('Original supplied audio',str(ROOT/'audio.mp4'),channel=1,frame_start=1)
    s.render.use_sequencer=False
    s['revision']='4 - uninterrupted waiting-room lead-in and embrace; sustained you vowel held'
    s['cut']=cut
    s['animation_scope']=('Drawn mouth substitutions, subpixel garment breathing, two short generated action clips, approved eye blinks and choreographed camera.' if cut=='experimental' else 'Rigid drawings, choreographed camera, approved eye-only blinks and editorial cuts. No breathing deformation or lip sync.')
    s['latest_user_direction']='One continuous waiting-room shot, matching the first video frame; no extra close-up cutaways or camera resets. Hold the rounded you vowel until the performance shot ends. Her gaze stays away.'
    s['experimental_status']='Separate research cut; not user-approved.' if cut=='experimental' else 'Restrained revision; awaiting user review.'
    s.frame_set(1)
    for im in bpy.data.images:
        if im.source=='FILE':im.pack()
    for snd in bpy.data.sounds:snd.pack()
    return s

def validate(s,fmt,cut):
    shots=get_shots(cut);issues=[]
    for f in range(1,END+1):
        s.frame_set(f)
        visible=[o for o in s.objects if o.type=='MESH' and not o.hide_render]
        if len(visible)!=1:issues.append({'frame':f,'visible':[o.name for o in visible]});continue
        o=visible[0]
        assert len(o.modifiers)==0
        if cut=='simple':assert len(o.data.vertices)==4 and o.data.shape_keys is None
        elif o.data.shape_keys:assert o['maximum_breath_source_pixels']<1.1
        w=max(v.co.x for v in o.data.vertices)-min(v.co.x for v in o.data.vertices)
        h=max(v.co.y for v in o.data.vertices)-min(v.co.y for v in o.data.vertices)
        scale=s.camera.data.ortho_scale
        vw,vh=(scale,scale*9/16) if fmt=='wide' else (scale*9/16,scale)
        cx=s.camera.location.x-o.location.x;cy=s.camera.location.y-o.location.y
        if abs(cx)+vw/2>w/2+.001 or abs(cy)+vh/2>h/2+.001:issues.append({'frame':f,'edge_gap':True})
    s.frame_set(1)
    result={'cut':cut,'format':fmt,'frames_checked':END,'issues':issues,'shape_keys':sum(len(o.data.shape_keys.key_blocks)-1 for o in s.objects if o.type=='MESH' and o.data.shape_keys),'deform_modifiers':0,
            'image_blending':'Local eye blinks; constant drawn mouth exposures in hybrid','mouth_animation':cut=='experimental','packed_images':[im.name for im in bpy.data.images if im.packed_file],
            'external_movies':[im.filepath for im in bpy.data.images if im.source=='MOVIE'],
            'packed_audio':bool(next(iter(bpy.data.sounds)).packed_file),'shots':len(shots)}
    (ROOT/f'validation_{cut}_{fmt}.json').write_text(json.dumps(result,indent=2))
    assert not issues,result
    print('ALL_FRAMES_VALID',cut,fmt,flush=True)

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
    p=argparse.ArgumentParser();p.add_argument('--format',choices=['wide','vert'],default='wide')
    p.add_argument('--cut',choices=['simple','experimental'],default='simple')
    mode=p.add_mutually_exclusive_group()
    mode.add_argument('--render',action='store_true');mode.add_argument('--preview',action='store_true')
    p.add_argument('--start',type=int,default=1);p.add_argument('--end',type=int,default=END)
    a=p.parse_args(argv);s=scene_setup(a.format,a.cut);validate(s,a.format,a.cut)
    d=ROOT/'frames'/a.cut/a.format;d.mkdir(parents=True,exist_ok=True)
    # Keep rebuilt scenes portable, including the external movie textures.
    for image in bpy.data.images:
        if image.source in {'FILE', 'MOVIE'}:
            image.filepath = '//assets/' + Path(image.filepath).name
    for sound in bpy.data.sounds:
        sound.filepath = '//audio.mp4'
    s.render.filepath=f'//frames/{a.cut}/{a.format}/frame_'
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/f'Join_Me_in_Life_{a.cut}_{a.format}.blend'), relative_remap=False)
    (ROOT/f'shot_list_{a.cut}.json').write_text(json.dumps(get_shots(a.cut),indent=2))
    if a.preview:
        d=ROOT/'previews'/a.cut/a.format;d.mkdir(parents=True,exist_ok=True)
        s.render.resolution_percentage=50
        for sh in get_shots(a.cut):
            f=(frame(sh['t0'])+min(END,frame(sh['t1'])-1))//2
            s.frame_set(f);s.render.filepath=str(d/f'{f:04d}.jpg');bpy.ops.render.render(write_still=True)
    if a.render:
        s.render.resolution_percentage=100
        for f in range(a.start,min(END,a.end)+1):
            out=d/f'frame_{f:04d}.jpg'
            if out.exists():continue
            s.frame_set(f);s.render.filepath=str(out);bpy.ops.render.render(write_still=True)
            if f%96==0:print('PROGRESS',a.cut,a.format,f,END,flush=True)

if __name__=='__main__':main()
