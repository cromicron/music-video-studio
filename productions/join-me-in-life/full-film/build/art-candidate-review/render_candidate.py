"""Review-only frames/proof; import the existing editor without altering it."""
from pathlib import Path
from types import SimpleNamespace
from concurrent.futures import ThreadPoolExecutor
import copy
import hashlib
import importlib.util
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
config_path = ROOT / "edit-art-candidate.json"
original_path = ROOT / "edit.json"
original_bytes = original_path.read_bytes()
config_bytes = config_path.read_bytes()
candidate = json.loads(config_bytes)
spec = importlib.util.spec_from_file_location("jml_candidate_editor", ROOT / "edit.py")
editor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)
editor.validate_edit(candidate)
shots, note = editor.assemble_plan(candidate)
assert not any(s["motion"] for s in shots), "This is a still-art proof only"
keys = set(candidate["candidate_scope"]["source_replacements"])

groups = {}
for s in shots:
    if s["source_key"] not in keys:
        continue
    key = json.dumps([s["source_key"], s["camera"]], sort_keys=True)
    if key not in groups:
        groups[key] = {"representative": s, "shot_ids": []}
    groups[key]["shot_ids"].append(s["id"])


def camera_frames(item):
    number, group = item
    s = group["representative"]
    folder = HERE / f"camera-{number:02d}-{s['source_key']}"
    folder.mkdir(exist_ok=True)
    selected = [0, (s["frames"] - 1) // 2, s["frames"] - 1]
    select = "+".join(f"eq(n\\,{i})" for i in selected)
    vf = editor.still_filter(s, 960, 540) + f",select='{select}'"
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", s["source"]["absolute_path"], "-vf", vf,
        "-fps_mode", "vfr", "-frames:v", "3", "-threads", "2",
        "-filter_threads", "1", str(folder / "frame-%02d.png")
    ], check=True)
    assert len(list(folder.glob("frame-*.png"))) == 3
    return {
        "source_key": s["source_key"], "source_sha256": s["source"]["sha256"],
        "shot_ids": group["shot_ids"], "representative_shot": s["id"],
        "camera": s["camera"], "sample_frame_indices": selected,
        "files": [str((folder / f"frame-{i:02d}.png").relative_to(ROOT)) for i in [1, 2, 3]],
        "note": "Actual editor still_filter, source and camera only; no title/fade applied to geometry diagnostics."
    }


with ThreadPoolExecutor(max_workers=2) as pool:
    diagnostics = list(pool.map(camera_frames, enumerate(groups.values(), 1)))
(HERE / "camera-manifest.json").write_text(json.dumps(diagnostics, indent=2) + "\n")
print(f"Rendered {len(diagnostics)} source/camera groups x first/middle/last", flush=True)

work = HERE / "opening-render"
work.mkdir(exist_ok=True)
args = SimpleNamespace(width=1920, height=1080, crf=19, force=True, threads=3)
opening = shots[0]
assert opening["frames"] == 156 and opening["title"]
part = editor.render_shot(opening, args, work)
out = ROOT / "exports/Join_Me_in_Life_Opening_Refined_Animatic_Proof.mp4"
out.parent.mkdir(exist_ok=True)
audio = editor.resolve_path(candidate["audio"])
editor.run([
    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
    "-i", part, "-ss", "0", "-t", "6.5", "-i", audio,
    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
    "-c:a", "aac", "-b:a", "256k", "-t", "6.5", "-movflags", "+faststart",
    "-metadata", "title=Join Me in Life — Refined opening animatic proof",
    "-metadata", "comment=6.5-second still-art camera and original-logo composite proof. No generated character animation.", out
])
info = editor.probe(out)
video = next(s for s in info["streams"] if s["codec_type"] == "video")
assert int(video["nb_frames"]) == 156 and video["r_frame_rate"] == "24/1"
editor.run(["ffmpeg", "-v", "error", "-i", out, "-f", "null", "-"])
waveform = editor.waveform_check(audio, out)
assert waveform["correlation"] > 0.995 and abs(waveform["offset_seconds"]) < 0.03
report = editor.report(candidate, [opening], note, out)
report["source_image_resolution_warning"] = "This opening uses a 1672x941 redraw enlarged to 1920x1080. It is not native 1080p source art."
report["candidate_config"] = {"path": str(config_path.relative_to(ROOT)), "sha256": hashlib.sha256(config_bytes).hexdigest()}
report["audio"] = {"mode": "Original take-49 MP3 excerpt 0–6.5s, encoded once as AAC 256k", "original_audio_sha256": editor.sha256(audio), "waveform_check": waveform}
report["technical_validation"] = {"full_decode": "passed", "video_frames": 156, "fps": "24/1", "width": 1920, "height": 1080, "container_duration": float(info["format"]["duration"])}
report["output_sha256"] = editor.sha256(out)
report["baseline_untouched"] = {"edit_json_sha256": hashlib.sha256(original_bytes).hexdigest(), "asserted_after_render": original_path.read_bytes() == original_bytes}
assert original_path.read_bytes() == original_bytes
out.with_suffix(".manifest.json").write_text(json.dumps(report, indent=2) + "\n")
selected = [0, 8, 18, 48, 78, 100, 115, 155]
select = "+".join(f"eq(n\\,{i})" for i in selected)
editor.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-vf", f"select='{select}'", "-fps_mode", "vfr", "-frames:v", str(len(selected)), str(HERE / "opening-frame-%02d.png")])
(HERE / "opening-samples.json").write_text(json.dumps({"indices_zero_based": selected, "fps": 24, "file_pattern": "opening-frame-%02d.png"}, indent=2) + "\n")
print(json.dumps({"output": str(out), "sha256": report["output_sha256"], "waveform": waveform, "original_edit_unchanged": True}), flush=True)
