#!/usr/bin/env python3
"""Make a short, explicitly labelled story check from the reviewed animatic."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "exports/Join_Me_in_Life_Full_Animatic.mp4"
OUTPUT = ROOT / "exports/Join_Me_in_Life_Story_Check.mp4"
WORK = ROOT / "work/story-check"
WORK.mkdir(parents=True, exist_ok=True)
FPS = 24
SEGMENTS = [
    (2141, 2273, "HOSPITAL | She stays withdrawn. He is frightened."),
    (2838, 2939, "EARLIER SUMMER | Warmth belongs to their memory."),
    (4891, 5388, "BRIDGE | All four cries are pleas, including the first."),
    (5561, 5657, "DAWN | They remain together. Recovery is unresolved."),
]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
(WORK / "title.txt").write_text("JOIN ME IN LIFE  |  STORY CHECK  |  ANIMATIC", encoding="utf-8")
filters = ["[0:v]split=4[v0][v1][v2][v3]", "[0:a]asplit=4[a0][a1][a2][a3]"]
manifest = []
out_frame = 0
for i, (start, end, label) in enumerate(SEGMENTS):
    caption = WORK / f"caption-{i}.txt"
    caption.write_text(label, encoding="utf-8")
    duration = (end - start) / FPS
    filters.append(
        f"[v{i}]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,"
        "pad=960:636:0:36:color=0x10151e,"
        f"drawtext=fontfile={FONT}:textfile={WORK / 'title.txt'}:fontsize=18:fontcolor=0xc5ceda:x=20:y=9,"
        f"drawtext=fontfile={FONT}:textfile={caption}:fontsize=22:fontcolor=white:x=20:y=596[vo{i}]"
    )
    filters.append(
        f"[a{i}]atrim=start={start/FPS:.9f}:end={end/FPS:.9f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d=0.015,afade=t=out:st={duration-0.015:.9f}:d=0.015[ao{i}]"
    )
    manifest.append({"source_start_frame": start, "source_end_frame_exclusive": end,
                     "output_start_frame": out_frame, "output_end_frame_exclusive": out_frame + end - start,
                     "label": label})
    out_frame += end-start
filters.append("".join(f"[vo{i}][ao{i}]" for i in range(4)) + "concat=n=4:v=1:a=1[v][a]")
script = WORK / "filters.txt"
script.write_text(";\n".join(filters), encoding="utf-8")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(SOURCE),
                "-filter_complex_script", str(script), "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(OUTPUT)], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-i", str(OUTPUT), "-f", "null", "-"], check=True)
record = {"schema": "jml-story-check/v1", "status": "animatic excerpt; no generated acting approved",
          "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          "output_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
          "fps": FPS, "frames": out_frame, "duration_seconds": out_frame/FPS,
          "full_decode": "pass", "segments": manifest,
          "audio": "Original animatic audio at matching source timestamps, 15 ms boundary fades; bridge continuous.",
          "limit": "This tests remembered story direction. It does not prove animation, lip sync, or exact lyric alignment."}
(ROOT / "review/story-check.json").write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
print(json.dumps({"output": str(OUTPUT), "duration": out_frame/FPS, "frames": out_frame, "decode": "pass"}))
