"""Make saved project paths relative, retaining packed drawings and audio."""
from pathlib import Path
import json
import bpy
ROOT=Path(__file__).resolve().parent
report=[]
for cut in ['simple','experimental']:
    for fmt in ['wide','vert']:
        path=ROOT/f'Join_Me_in_Life_{cut}_{fmt}.blend'
        bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene
        for im in bpy.data.images:
            if im.source in ['FILE','MOVIE']:
                im.filepath='//assets/'+Path(im.filepath).name
                if im.source=='FILE' and not im.packed_file:im.pack()
        for snd in bpy.data.sounds:snd.filepath='//audio.mp4'
        for strip in s.sequence_editor.strips:
            if strip.type=='SOUND':strip.sound.filepath='//audio.mp4'
        s.render.filepath=f'//frames/{cut}/{fmt}/frame_'
        s.frame_set(1)
        for screen in bpy.data.screens:
            for area in screen.areas:
                if area.type=='VIEW_3D':
                    area.spaces.active.region_3d.view_perspective='CAMERA'
                    area.spaces.active.shading.type='MATERIAL'
        movies=[im.filepath for im in bpy.data.images if im.source=='MOVIE']
        missing=[p for p in movies if not (ROOT/p.removeprefix('//')).is_file()]
        assert not missing,missing
        bpy.ops.wm.save_as_mainfile(filepath=str(path))
        report.append({'file':path.name,'relative_movies':movies,'missing_movies':missing,
                       'packed_images':sum(bool(im.packed_file) for im in bpy.data.images),
                       'packed_audio':all(snd.packed_file for snd in bpy.data.sounds),
                       'output_path':s.render.filepath})
(ROOT/'portability_validation.json').write_text(json.dumps(report,indent=2))
print('PORTABLE_PROJECTS_VALID',len(report))
