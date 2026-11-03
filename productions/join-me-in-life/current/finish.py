"""Encode Blender frames, preserve the supplied audio, and add optional lyrics."""
from pathlib import Path
import subprocess
import json
import argparse

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'Revision_4'

# Source lyric wording, aligned to the actual recording with local Whisper
# word timestamps. Corrections to recognition errors use the supplied lyrics.
CUES=[
 (0.00,5.55,"You say you're just a weight we carry"),
 (6.06,9.50,"That we'd be lighter with you gone"),
 (9.80,13.60,"That's the night talking, it isn't you"),
 (14.38,17.75,"And it's had your voice too long"),
 (17.88,22.00,"But who would sing the wrong words with me"),
 (22.10,26.12,"To every stupid summer song"),
 (26.38,30.10,"I know how it pulls you, it pulled at me too"),
 (30.28,33.72,"Some days it still takes the light"),
 (33.98,38.30,"But I'll sit with you there in the waiting room"),
 (38.38,41.90,"Till they call your name tonight"),
 (42.28,44.65,"Baby, join me in life"),
 (44.66,50.12,"Just tonight, just tonight"),
 (50.12,54.80,"Give me one more winter morning"),
 (55.00,58.80,"Stay with me until it's light"),
]

def tc(t,ass=False):
    if ass:
        v=round(t*100);return f'{v//360000}:{v//6000%60:02}:{v//100%60:02}.{v%100:02}'
    v=round(t*1000);return f'{v//3600000:02}:{v//60000%60:02}:{v//1000%60:02},{v%1000:03}'

def caption_files(cut='simple'):
    brand_suffix='_hybrid' if cut=='experimental' else ''
    srt='\n\n'.join(f'{i+1}\n{tc(a)} --> {tc(b)}\n{text}' for i,(a,b,text) in enumerate(CUES))+'\n'
    (ROOT/'Join_Me_in_Life_English.srt').write_text(srt)
    for fmt,w,h in [('wide',1920,1080),('vert',1080,1920)]:
        fs,margin=(44,75) if fmt=='wide' else (47,350)
        title_size=(34 if fmt=='wide' else 36) if brand_suffix else (36 if fmt=='wide' else 38)
        title_top=(135 if fmt=='wide' else 212) if brand_suffix else (85 if fmt=='wide' else 162)
        header=f'''[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,DejaVu Sans,{fs},&H00F7F5EF,&H00FFFFFF,&H00241A13,&H80000000,0,0,0,0,100,100,0,0,1,2.2,1,2,85,115,{margin},1
Style: Artist,DejaVu Sans,{'25' if fmt=='wide' else '26'},&H00E6E0D6,&H00FFFFFF,&H60241A13,&H90000000,0,0,0,0,100,100,4,0,1,1,0,{'7' if fmt=='wide' else '8'},70,70,{'45' if fmt=='wide' else '120'},1
Style: Title,DejaVu Serif,{title_size},&H00F7F5EF,&H00FFFFFF,&H60241A13,&H90000000,0,0,0,0,100,100,1,0,1,1.4,0,{'7' if fmt=='wide' else '8'},70,70,{title_top},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
        branded=header
        if not brand_suffix:branded+='Dialogue: 0,0:00:00.35,0:00:04.80,Artist,,0,0,0,,{\\fad(400,650)}MERCY IN MINOR\n'
        branded+='Dialogue: 0,0:00:00.35,0:00:04.80,Title,,0,0,0,,{\\fad(400,650)}Join Me in Life\n'
        (ROOT/f'titles{brand_suffix}_{fmt}.ass').write_text(branded)
        lines=[]
        for a,b,text in CUES:
            if fmt=='vert':
                splits={
                 "You say you're just a weight we carry":"You say you're just\\Na weight we carry",
                 "That we'd be lighter with you gone":"That we'd be lighter\\Nwith you gone",
                 "That's the night talking, it isn't you":"That's the night talking,\\Nit isn't you",
                 "And it's had your voice too long":"And it's had your voice\\Ntoo long",
                 "But who would sing the wrong words with me":"But who would sing\\Nthe wrong words with me",
                 "I know how it pulls you, it pulled at me too":"I know how it pulls you,\\Nit pulled at me too",
                 "Some days it still takes the light":"Some days it still\\Ntakes the light",
                 "But I'll sit with you there in the waiting room":"But I'll sit with you there\\Nin the waiting room",
                 "Till they call your name tonight":"Till they call your name\\Ntonight",
                 "Give me one more winter morning":"Give me one more\\Nwinter morning",
                 "Just tonight, just tonight":"Just tonight,\\Njust tonight",
                 "Stay with me until it's light":"Stay with me\\Nuntil it's light",
                }
                text=splits.get(text,text)
            lines.append(f'Dialogue: 1,{tc(a,True)},{tc(b,True)},Lyric,,0,0,0,,{{\\fad(90,110)}}{text}')
        (ROOT/f'lyrics{brand_suffix}_{fmt}.ass').write_text(branded+'\n'.join(lines)+'\n')
    (ROOT/'lyric_cues.json').write_text(json.dumps(CUES,indent=2))

def encode(fmt,lyrics=False,cut='simple',first=1,last=1439):
    if not 1 <= first <= last <= 1439:
        raise ValueError('Frame range must lie within 1–1439')
    preview = (first, last) != (1, 1439)
    offset = first - 1
    frame_count = last - first + 1
    OUT.mkdir(parents=True,exist_ok=True)
    brand_suffix='_hybrid' if cut=='experimental' else ''
    subtitle=ROOT/f'{"lyrics" if lyrics else "titles"}{brand_suffix}_{fmt}.ass'
    output=OUT/('Join_Me_in_Life_Short.mp4' if fmt=='vert' else 'Join_Me_in_Life_Widescreen.mp4')
    if fmt=='vert' and not lyrics:output=OUT/'Join_Me_in_Life_Short_Clean.mp4'
    if cut=='experimental':output=output.with_stem(output.stem+'_Hybrid')
    output=output.with_stem(output.stem+'_Camera')
    if preview:
        output = output.with_stem(f'{output.stem}_f{first:04d}-f{last:04d}')
    temporary=output.with_name(output.name+'.tmp')
    frames=ROOT/'frames'/cut/fmt/'frame_%04d.jpg'
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','warning','-framerate','24','-start_number',str(first),'-i',str(frames),'-i',str(ROOT/'audio.mp4')]
    colour='scale=in_color_matrix=bt601:out_color_matrix=bt709:in_range=pc:out_range=tv,format=yuv420p'
    # ASS and the logo fades use the full-song-excerpt clock. The encoded
    # preview starts at zero, with audio cut from the same source frame.
    captions = f'ass={subtitle.name}'
    logo_trim = ''
    if preview:
        captions = f'settb=1/24,setpts=PTS+{offset},{captions},setpts=PTS-STARTPTS'
        logo_trim = f',trim=start_frame={offset},setpts=PTS-STARTPTS'
    if brand_suffix:
        w,h=(1920,1080) if fmt=='wide' else (1080,1920)
        logo_w,x,y=(330,65,25) if fmt=='wide' else (600,240,38)
        cmd+=['-loop','1','-framerate','24','-i',str(ROOT/'assets/Band_Logo_Original.png')]
        graph=(f'[0:v]format=gbrp[base];[2:v]scale={logo_w}:-1:flags=lanczos,format=gbrp,'
               f'pad={w}:{h}:{x}:{y}:color=black,fade=t=in:st=0.35:d=0.4,fade=t=out:st=4.15:d=0.65{logo_trim}[logo];'
               f'[base][logo]blend=all_mode=screen:all_opacity=0.94:shortest=1,format=gbrp,{captions},{colour}[video]')
        cmd+=['-filter_complex_threads','2','-filter_complex',graph,'-map','[video]','-map','1:a:0']
    else:
        cmd+=['-map','0:v:0','-map','1:a:0','-vf',f'{captions},{colour}']
    if preview:
        # The production AAC is 48 kHz; each 24 fps picture frame spans 2000 samples.
        audio_options = ['-af', f'atrim=start_sample={offset*2000}:end_sample={last*2000},asetpts=PTS-STARTPTS',
                         '-c:a', 'aac', '-b:a', '256k']
        cmd += ['-r:v', '24', '-fps_mode:v', 'cfr']
        duration = f'{frame_count / 24:.9f}'
    else:
        audio_options = ['-c:a', 'copy']
        duration = '59.95'
    cmd+=[
         '-c:v','libx264','-preset','slow','-crf','17','-threads','8','-pix_fmt','yuv420p',
         '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
         *audio_options,'-t',duration,'-movflags','+faststart','-metadata','title=Join Me in Life',
         '-metadata','artist=Mercy in Minor','-metadata','comment=Unresolved music-video excerpt. Blender 2D limited animation.',
         '-f','mp4',str(temporary)]
    print('Encoding',output.name,flush=True);subprocess.run(cmd,check=True,cwd=ROOT)
    # Keep partially written containers out of the delivery location. Confirm
    # the MP4 index is readable before making the completed file visible.
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(temporary)]))
    video=next(st for st in probe['streams'] if st['codec_type']=='video')
    assert int(video['nb_frames'])==frame_count,video
    if preview:
        assert video['avg_frame_rate']=='24/1',video
    assert any(st['codec_type']=='audio' and st['codec_name']=='aac' for st in probe['streams'])
    temporary.replace(output)
    print('FINISHED',output,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--format',choices=['wide','vert']);p.add_argument('--lyrics',action='store_true')
    p.add_argument('--cut',choices=['simple','experimental'],default='simple')
    p.add_argument('--first-frame',type=int,default=1);p.add_argument('--last-frame',type=int,default=1439)
    a=p.parse_args()
    caption_files(a.cut)
    if a.format:encode(a.format,a.lyrics,a.cut,a.first_frame,a.last_frame)
