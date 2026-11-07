"""Compact framing diagnostics only; no image/production-editor mutations."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib
import importlib.util
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
HERE.mkdir(exist_ok=True)
config = json.loads((ROOT / "edit-production-candidate.json").read_text())
spec = importlib.util.spec_from_file_location("jml_aftermath_editor", ROOT / "edit.py")
editor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)
editor.validate_edit(config)
shots, note = editor.assemble_plan(config)
assert not any(s["motion"] for s in shots), "Do not silently introduce generated motion"

groups = [
    {"name": "wide", "representative": "S032", "shot_ids": ["S032", "S047"]},
    {"name": "closer", "representative": "S030", "shot_ids": ["S030", "S042"]},
]
results = []
for group in groups:
    shot = next(s for s in shots if s["id"] == group["representative"])
    indices = [0, (shot["frames"] - 1) // 2, shot["frames"] - 1]
    select = "+".join(f"eq(n\\,{i})" for i in indices)
    vf = editor.still_filter(shot, 960, 540) + f",select='{select}',format=rgb24"
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", shot["source"]["absolute_path"],
        "-vf", vf, "-fps_mode", "vfr", "-frames:v", "3", "-filter_threads", "1", "-threads", "2",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
    ]
    raw = subprocess.run(command, check=True, stdout=subprocess.PIPE).stdout
    size = 960 * 540 * 3
    assert len(raw) == size * 3
    parts = [raw[i * size:(i + 1) * size] for i in range(3)]
    frames = [Image.frombytes("RGB", (960, 540), part) for part in parts]
    frames[0].save(HERE / f"{group['name']}-representative.jpg", quality=94, subsampling=0)
    contact = Image.new("RGB", (1440, 300), (20, 20, 20))
    draw = ImageDraw.Draw(contact)
    for i, (frame, index) in enumerate(zip(frames, indices)):
        contact.paste(frame.resize((480, 270), Image.Resampling.LANCZOS), (i * 480, 30))
        draw.text((i * 480 + 8, 8), f"{group['name']} {shot['id']} frame {index}", fill="white")
    contact.save(HERE / f"{group['name']}-first-middle-last.jpg", quality=91, subsampling=0)
    results.append({
        **group, "camera": shot["camera"], "sample_indices_zero_based": indices,
        "source_sha256": shot["source"]["sha256"],
        "raw_frame_sha256": [hashlib.sha256(part).hexdigest() for part in parts],
        "locked_frames_identical": len(set(parts)) == 1,
        "contact": f"{group['name']}-first-middle-last.jpg",
        "representative_jpeg": f"{group['name']}-representative.jpg",
        "no_motion_approval": True,
    })
(HERE / "framing-manifest.json").write_text(json.dumps({
    "config": "edit-production-candidate.json", "config_sha256": editor.sha256(ROOT / "edit-production-candidate.json"),
    "source": "../current/assets/M01_Embrace_End.png", "output": "JPEG framing diagnostics only; no rendered film",
    "groups": results, "motion_note": note,
}, indent=2) + "\n")
print(json.dumps(results, indent=2))
