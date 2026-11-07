"""Hash-bound held-aftermath insertion/cut checks; writes ignored build only.

Independent integer source trims, whole-image containment and matching CRF18
encoding are compared with every decoded motion frame in the pinned export.
"""
from pathlib import Path
import hashlib, json, subprocess
import numpy as np
from PIL import Image, ImageDraw

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'studio.json').is_file())
BASE = ROOT / 'productions/join-me-in-life/full-film'
OUT = ROOT / 'build/positive-held-aftermath-sequence-review'
OUT.mkdir(parents=True, exist_ok=True)
CONTEXT = BASE / 'exports/Join_Me_in_Life_Positive_Held_Aftermath_Context_Proof.mp4'
CONFIG_SHA = '8422bf9fb4849e02e1ead09148b4615538c4a3780d13161f4f598e94932f7bb6'
CONTEXT_SHA = '1dc8e8586dc70ed13ccf6af7a5a853cc3d707d830e9cb8eb0c31a26fe5bee3a5'
SOURCE = BASE / 'assets/motion/ltx23-positive-continuation/P1/P1L06/video-silent.mp4'
SOURCE_SHA = '7f411bf2fde1955369b2856cd7542d3ef8dd488680483537a62ee01ae11aa8ac'
R1_PROOF = BASE / 'exports/Join_Me_in_Life_Held_Correction_S032_Proof.mp4'
R1_SHA = '7a3f1b928cc6a2f44dfa90c21c2712f027bedd990235c7dc2afc885804aa0725'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def frame_md5(path):
    result = subprocess.check_output(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path),
        '-map', '0:v:0', '-fps_mode', 'passthrough', '-pix_fmt', 'yuv420p', '-f', 'framemd5', '-'], text=True)
    (OUT / (path.stem + '.framemd5')).write_text(result)
    return [line.rsplit(',', 1)[1].strip() for line in result.splitlines() if not line.startswith('#')]

assert sha(CONTEXT) == CONTEXT_SHA and sha(SOURCE) == SOURCE_SHA and sha(R1_PROOF) == R1_SHA
manifest = json.loads(CONTEXT.with_suffix('.manifest.json').read_text())
assert manifest['edit_config']['sha256'] == CONFIG_SHA and manifest['output_sha256'] == CONTEXT_SHA
assert manifest['coverage'] == {'start_frame': 3624, 'end_frame_exclusive': 4113, 'full_song': False}
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
    'stream=index,codec_name,codec_type,width,height,pix_fmt,r_frame_rate,avg_frame_rate,time_base,start_time,duration,nb_frames:format=start_time,duration',
    '-of', 'json', str(CONTEXT)], text=True))
video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
assert (video['width'], video['height'], video['avg_frame_rate'], video['nb_frames']) == (960, 540, '24/1', '489')
(OUT / 'ffprobe.json').write_text(json.dumps(probe, indent=2)+'\n')
actual = frame_md5(CONTEXT)
assert len(actual) == 489
checks = {
    'scope': 'Exact decoded picture checks; author audio correlation is technical evidence, not listening.',
    'config_sha256': CONFIG_SHA, 'context_sha256': CONTEXT_SHA,
    'manifest_sha256': sha(CONTEXT.with_suffix('.manifest.json')),
    'context_frames': len(actual), 'context_global_range_zero_based': [3624, 4113],
    'full_video_decode': 'passed', 'author_audio_check': manifest['audio'], 'insertions': {},
}
old = frame_md5(R1_PROOF)
assert old == actual[100:196]
checks['insertions']['S032'] = {'source_frames_zero_based': [101, 197], 'context_frames_zero_based': [100, 196],
    'previously_reviewed_proof_sha256': R1_SHA, 'all_96_decoded_frames_equal_previous_proof': True}
for shot, lo, hi, start, end in [('S033', 3, 102, 196, 295), ('S034', 102, 198, 295, 391)]:
    vf = f'trim=start_frame={lo}:end_frame={hi},setpts=PTS-STARTPTS,fps=24,scale=944:540:flags=lanczos,pad=960:540:8:0:color=black,setsar=1,format=yuv420p'
    reconstructed = OUT / f'{shot}-independent-reconstruction.mp4'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-threads', '2', '-i', str(SOURCE), '-vf', vf,
        '-an', '-frames:v', str(hi-lo), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
        '-threads', '3', '-filter_threads', '1', '-r', '24', '-video_track_timescale', '24000',
        '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
        '-color_range', 'tv', '-movflags', '+faststart', str(reconstructed)]
    subprocess.run(cmd, check=True)
    expected = frame_md5(reconstructed)
    equal = [a == b for a, b in zip(expected, actual[start:end])]
    checks['insertions'][shot] = {'source_sha256': SOURCE_SHA, 'source_frames_zero_based': [lo, hi],
        'context_frames_zero_based': [start, end], 'filter': vf, 'encoding_command': cmd,
        'reconstructed_sha256': sha(reconstructed), 'identical_frames': sum(equal),
        'all_decoded_frames_identical': len(expected) == end-start and all(equal)}
    assert checks['insertions'][shot]['all_decoded_frames_identical']

cuts = [100, 196, 295, 391]
phases = [0, 49, 99, 100, 148, 195, 196, 210, 241, 265, 278, 286, 294, 295, 301, 314, 326, 349, 373, 390, 391, 440, 488]
selected = sorted(set(phases + [i for c in cuts for i in range(c-3, c+3)]))
selection = '+'.join(f'eq(n\\,{i})' for i in selected)
raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-xerror', '-i', str(CONTEXT),
    '-vf', 'select='+selection, '-fps_mode', 'passthrough', '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'])
decoded = np.frombuffer(raw, np.uint8).reshape(-1, 540, 960, 3)
assert len(decoded) == len(selected)
frames = {}; edges = []
for n, rgb in zip(selected, decoded):
    frames[n] = Image.fromarray(rgb)
    frames[n].save(OUT / f'native-{n:03}.jpg', quality=96)
    if 100 <= n < 391:
        active = np.where(rgb[20:520].mean(axis=(0,2)) > 8)[0]
        edges.append([int(active[0]), int(959-active[-1])])
assert set(frames) == set(selected)
checks['inspected_native_frame_candidates_zero_based'] = selected
checks['sampled_motion_mean_column_padding_pixels'] = sorted(set(map(tuple, edges)))
for c in cuts:
    pair = Image.new('RGB', (1920, 566), '#171717'); d = ImageDraw.Draw(pair)
    for j, i in enumerate([c-1, c]):
        d.text((j*960+5, 5), f'Context local f{i}, master f{i+3624}', fill='white')
        pair.paste(frames[i], (j*960, 26))
    pair.save(OUT / f'join-{c:03}-native.jpg', quality=95)
sheet = Image.new('RGB', (4*480, ((len(phases)+3)//4)*294), '#171717'); d = ImageDraw.Draw(sheet)
for j, i in enumerate(phases):
    x, y = j%4*480, j//4*294
    source = f'P1 source f{i-193}' if 196 <= i < 391 else 'R1 source f'+str(i+1) if 100 <= i < 196 else 'still + camera'
    d.text((x+4, y+4), f'local f{i} / master f{i+3624} / {source}', fill='white')
    sheet.paste(frames[i].resize((480,270), Image.Resampling.LANCZOS), (x,y+24))
sheet.save(OUT / 'context-phases.jpg', quality=93)
(OUT / 'encoded-checks.json').write_text(json.dumps(checks, indent=2)+'\n')
(OUT / 'pinned-manifest.json').write_bytes(CONTEXT.with_suffix('.manifest.json').read_bytes())
print(json.dumps(checks, indent=2))
