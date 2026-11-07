"""Independent encoded-frame evidence; original edit and artwork are read-only."""
from pathlib import Path
import ast, hashlib, json, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
FILM = HERE.parent.parent
PRODUCTION = FILM.parent
VIDEO = FILM / 'exports/Join_Me_in_Life_Short_Performance_Reuse_Proof.mp4'
EXPECTED = '25519287823f517943ffc1efd7f2f94aea5408a13c22775c451ce5f1f5619ad3'
assert hashlib.sha256(VIDEO.read_bytes()).hexdigest() == EXPECTED
manifest = json.loads(VIDEO.with_suffix('.manifest.json').read_text())
selected = {0, 137, 138, 233, 234, 304, 305, 319, 337, 338, 339, 340, 428}
for start in [0, 339]:
    selected.update(start + f for f in list(range(43, 52)) + list(range(64, 73)))
frames, mouths, differences = {}, [], []
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(VIDEO), '-an', '-f',
                      'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
previous = None
n = 0
while True:
    raw = p.stdout.read(960 * 540 * 3)
    if not raw:
        break
    assert len(raw) == 960 * 540 * 3
    rgb = np.frombuffer(raw, np.uint8).reshape(540, 960, 3)
    if previous is not None:
        differences.append([n, float(np.abs(rgb.astype(np.int16)-previous).mean())])
    if n in selected:
        frames[n] = Image.fromarray(rgb.copy())
    if 234 <= n < 339:
        mouths.append(Image.fromarray(rgb[100:220, 355:475].copy()))
    previous = rgb.astype(np.int16)
    n += 1
assert p.wait() == 0 and n == 429

def sheet(items, columns, width, height, path):
    result = Image.new('RGB', (width*columns, (height+21)*((len(items)+columns-1)//columns)), '#181818')
    draw = ImageDraw.Draw(result)
    for i, (label, im) in enumerate(items):
        x, y = i % columns * width, i // columns * (height+21)
        draw.text((x+4, y+4), label, fill='white')
        result.paste(im.resize((width,height), Image.Resampling.LANCZOS), (x,y+21))
    result.save(path, quality=91, subsampling=0)

sheet([(f'proof f{234+i} / S023 f{i}', im) for i,im in enumerate(mouths)],
      7,120,120,HERE/'all-105-performance-faces.jpg')
sheet([(f'proof f{n} / {n/24:.6f}s',frames[n]) for n in [0,137,138,233,234,338,339,428]],
      2,480,270,HERE/'exact-cut-context.jpg')
for start,name in [(0,'s021'),(339,'s024')]:
    items=[]
    for local in list(range(43,52))+list(range(64,73)):
        frame=frames[start+local]
        im=Image.new('RGB',(250,125))
        im.paste(frame.crop((180,115,305,240)),(0,0))
        im.paste(frame.crop((520,80,645,205)),(125,0))
        items.append((f'proof f{start+local} / shot f{local}',im))
    sheet(items,3,250,125,HERE/f'{name}-blink-frames.jpg')
for n in [234,305,338,339]:
    frames[n].save(HERE/f'normal-size-f{n}.jpg',quality=93,subsampling=0)
Image.open(PRODUCTION/'art/04_Performance/P01_Verse_Performance.png').resize(
    (960,540),Image.Resampling.LANCZOS).save(HERE/'original-p01-at-960.jpg',quality=90,subsampling=0)

# Execute the original pure exposure function, not the editor's reconstruction.
source = PRODUCTION/'current/native_animation.py'
provenance=manifest['shots'][2]['drawn_art_segments'][0]['provenance']
for filename in ['native_animation.py','word_timing.json']:
    assert hashlib.sha256((PRODUCTION/'current'/filename).read_bytes()).hexdigest()==provenance[filename]['sha256']
tree=ast.parse(source.read_text())
nodes=[node for node in tree.body if
       isinstance(node,ast.FunctionDef) and node.name=='exposures' or
       isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PATTERNS' for t in node.targets)]
ns={'json':json,'ROOT':PRODUCTION/'current','FPS':24}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ns)
track=[]
for at,pose in ns['exposures']():
    while len(track)<at:
        track.append(last)
    last=pose
track.extend([last]*(1440-len(track)))
original=track[234:339]
actual=[1]*105
for patch in manifest['shots'][2]['drawn_art_segments'][0]['patches']:
    for a,b in patch['runs']:
        actual[a:b]=[patch['pose']]*(b-a)
assert original==actual
assert original[71:]==[3]*34
assert [s['start_frame']-2409 for s in manifest['shots']]==[0,138,234,339]
assert manifest['shots'][-1]['end_frame_exclusive']-2409==429
report={'video_sha256':EXPECTED,'decoded_frames':429,
        'dimensions':[960,540],'original_exposure_comparison':'105/105 exact pose agreement',
        'zero_based_proof_cut_frames':[138,234,339],
        'rounded_vowel_proof_frame_interval_inclusive':[305,338],
        'last_19_frames_required_by_R4_hold_inclusive':[320,338],
        'reaction_first_frame':339,
        'largest_adjacent_full_frame_changes':sorted(differences,key=lambda x:-x[1])[:10],
        'audio_alignment_from_render_manifest':manifest['audio']['waveform_check'],
        'audio_alignment_independently_rerun':False,
        'method':'All 429 frames decoded; every P01 face exposure and both complete blink transitions extracted. Technical data is not listening.'}
(HERE/'encoded-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
