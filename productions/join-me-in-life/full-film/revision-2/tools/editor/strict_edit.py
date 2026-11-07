#!/usr/bin/env python3
"""Frame-exact v2 assembly. Never substitute stills, loop, retime or pad a shot."""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import re
import subprocess

FULL_FILM = Path(__file__).resolve().parents[3]
REPOSITORY = FULL_FILM.parents[2]
SCHEMA = "jml-story-edit/v2"
FPS, TOTAL_FRAMES = 24, 6667
SONG_SHA256 = "0fe0f566e985a0b028e12543679d3b142ee7b1b62425fcb595799b35ba116cbb"
spec = importlib.util.spec_from_file_location("jml_original_editor", FULL_FILM / "edit.py")
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def local_file(root, value):
    require(text(value) and not Path(value).is_absolute(), "Use relative source/review paths")
    path = (root / value).resolve()
    require(path.is_file(), f"Missing source/review: {value}")
    require(path.is_relative_to(REPOSITORY), "Source/review must be within the repository workspace")
    return path


def validate_story(plan, total_frames=TOTAL_FRAMES):
    """Story fields are a review ledger, not a machine judgment of dramatic quality."""
    require(plan.get("schema") == SCHEMA and plan.get("fps") == FPS, "Unsupported plan schema/fps")
    require(plan.get("total_frames") == total_frames, "Wrong full-song picture extent")
    require(isinstance(plan.get("sources"), dict), "sources must be an object")
    require(isinstance(plan.get("shots"), list) and plan["shots"], "A shot plan is required")
    end, ids = 0, set()
    for shot in plan["shots"]:
        name = shot.get("id", "")
        require(isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9_-]+", name), "Unsafe/missing shot ID")
        require(name not in ids, f"Duplicate shot ID: {name}"); ids.add(name)
        a, b = shot.get("start_frame"), shot.get("end_frame_exclusive")
        require(integer(a) and integer(b) and a == end and b > a, f"Timeline gap/overlap/empty shot: {name}")
        end = b
        require(text(shot.get("section")), f"Missing song section: {name}")
        story = shot.get("story", {})
        require(all(text(story.get(k)) for k in ("before", "action", "after")), f"Missing action/consequence ledger: {name}")
        continuity = shot.get("continuity", {})
        for side in ("entry", "exit"):
            state = continuity.get(side, {})
            require(text(state.get("location")) and text(state.get("blocking")) and isinstance(state.get("props"), dict),
                    f"Missing {side} location/blocking/props: {name}")
        require(text(continuity.get("cut_to_next")), f"Missing cut intent: {name}")
        require(not any(k in shot for k in ("speed", "loop", "hold_frames", "lead_in_frames", "endpoint_hold_frames", "still")),
                f"Padding/loop/retiming fields are prohibited: {name}")
        fade = shot.get("fade_out_frames", 0)
        require(integer(fade) and 0 <= fade <= b-a, f"Invalid fade length: {name}")
        require(not fade or b == total_frames, "Only the final moving shot may fade out")
    require(end == total_frames, "The plan must cover every full-song frame")


def source_timing(path):
    """Decode every source frame, rejecting damaged streams and changed cadence."""
    cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_frames",
           "-show_entries", "stream=width,height,avg_frame_rate,time_base:frame=best_effort_timestamp_time",
           "-of", "json", str(path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    require(result.returncode == 0 and not result.stderr.strip(), f"Source decode failure: {path.name}: {result.stderr[-500:]}")
    data = json.loads(result.stdout)
    require(len(data.get("streams", [])) == 1 and data.get("frames"), f"Missing video frames: {path.name}")
    stream = data["streams"][0]
    require(Fraction(stream["avg_frame_rate"]) == FPS, f"Source is not natural 24fps: {path.name}")
    points = [Fraction(f["best_effort_timestamp_time"]) for f in data["frames"]]
    tolerance = max(Fraction(1, 100000), min(Fraction(1, FPS*4), Fraction(stream["time_base"]) * Fraction(101, 100)))
    require(all(a < b for a, b in zip(points, points[1:])), f"Source has duplicate/nonincreasing timestamps: {path.name}")
    require(all(abs(t-points[0]-Fraction(i, FPS)) <= tolerance for i, t in enumerate(points)),
            f"Source has missing/irregular frame cadence: {path.name}")
    return {"frames": len(points), "width": stream["width"], "height": stream["height"],
            "frame_rate": "24/1", "decoded_source_timing": "passed"}


def bind_sources(plan, shots, root=FULL_FILM):
    """Only explicitly accepted frame ranges can enter a render."""
    sources, used, take_files, bound = {}, defaultdict(list), {}, []
    for shot in shots:
        name, selection = shot["id"], shot.get("source", {})
        key = selection.get("id")
        require(key in plan["sources"], f"Missing selected motion source: {name}")
        if key not in sources:
            src = plan["sources"][key]
            require(src.get("kind") == "video", f"Still/image fallback prohibited: {key}")
            path = local_file(root, src["path"])
            digest = legacy.sha256(path)
            require(digest == src.get("sha256"), f"Source SHA changed: {key}")
            require(text(src.get("take_id")), f"Missing original take identity: {key}")
            require(src["take_id"] not in take_files or take_files[src["take_id"]] == digest,
                    f"One take ID points to different binaries: {key}")
            take_files[src["take_id"]] = digest
            approval = src.get("review", {})
            require(approval.get("status") == "accepted", f"Source has no accepted interval review: {key}")
            review_path = local_file(root, approval["path"])
            require(legacy.sha256(review_path) == approval.get("sha256"), f"Review SHA changed: {key}")
            require(digest in review_path.read_text(), f"Review does not name this exact source SHA: {key}")
            ranges = approval.get("accepted_ranges", [])
            require(ranges and all(isinstance(r, list) and len(r) == 2 and all(integer(x) for x in r)
                                  and 0 <= r[0] < r[1] for r in ranges), f"Missing accepted source ranges: {key}")
            timing = source_timing(path)
            require(all(r[1] <= timing["frames"] for r in ranges), f"Review range exceeds decoded source: {key}")
            sources[key] = dict(src, absolute_path=str(path), **timing)
        src = sources[key]
        a, b = selection.get("in_frame"), selection.get("out_frame_exclusive")
        count = shot["end_frame_exclusive"] - shot["start_frame"]
        require(integer(a) and integer(b) and 0 <= a < b <= src["frames"], f"Source interval exceeds footage: {name}")
        require(b-a == count, f"Source does not exactly fill shot; no hold/retiming allowed: {name}")
        require(any(x <= a and b <= y for x, y in src["review"]["accepted_ranges"]), f"Selected interval is unreviewed: {name}")
        for earlier_a, earlier_b, earlier_name in used[src["sha256"]]:
            require(b <= earlier_a or a >= earlier_b, f"Repeated source frames: {earlier_name} and {name}")
        used[src["sha256"]].append((a, b, name))
        require(shot.get("framing", "contain") == "contain", f"Unreviewed source crop prohibited: {name}")
        bound.append(dict(shot, source=dict(selection, **src), frames=count))
    return bound


def render_shot(shot, output, width=1920, height=1080, crf=18, threads=3):
    """Frame trim, full-image contain, optional final fade. No fps filter or tpad."""
    src = shot["source"]
    # Source cadence was checked above. Normalize container tick rounding to an
    # exact 24fps timebase without adding, dropping or reordering a frame.
    vf = (f"trim=start_frame={src['in_frame']}:end_frame={src['out_frame_exclusive']},settb=1/24000,setpts=N*1000,"
          f"scale={width}:{height}:force_original_aspect_ratio=decrease:force_divisible_by=2:flags=lanczos,"
          f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1")
    if shot.get("fade_out_frames"):
        vf += f",fade=t=out:start_frame={shot['frames']-shot['fade_out_frames']}:nb_frames={shot['fade_out_frames']}"
    vf += ",format=yuv420p"
    legacy.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-n", "-i", src["absolute_path"],
                "-map", "0:v:0", "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", str(crf), "-threads", str(threads), "-filter_threads", "1",
                "-r", "24", "-enc_time_base", "1/24", "-fps_mode", "cfr",
                "-video_track_timescale", "24000", "-movflags", "+faststart", output])
    stream = next(s for s in legacy.probe(output)["streams"] if s["codec_type"] == "video")
    require(int(stream["nb_frames"]) == shot["frames"] and Fraction(stream["avg_frame_rate"]) == FPS,
            f"Rendered source interval/cadence mismatch: {shot['id']}")
    return output


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("plan", type=Path)
    ap.add_argument("--draft", action="store_true", help="Validate story timeline/ledger only; not a motion pass")
    ap.add_argument("--shots", help="Contiguous inclusive ID range, e.g. V201:V204; excerpt only")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--output", type=Path)
    ap.add_argument("--work-dir", type=Path)
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--threads", type=int, default=3)
    args = ap.parse_args()
    require(not args.draft or not args.render, "A draft can never be rendered as accepted motion")
    plan = json.loads(args.plan.read_text())
    validate_story(plan)
    if args.draft:
        print(f"Story ledger only: {len(plan['shots'])} shots / 6667 frames. No creative/motion approval implied.")
        return
    shots = plan["shots"]
    if args.shots:
        first, last = args.shots.split(":")
        ids = [s["id"] for s in shots]
        a, b = ids.index(first), ids.index(last)
        require(a <= b, "Reversed excerpt selection")
        shots = shots[a:b+1]
    bound = bind_sources(plan, shots)
    audio = local_file(FULL_FILM, plan["audio"]["path"])
    require(plan["audio"].get("sha256") == SONG_SHA256 == legacy.sha256(audio), "Original take49 song changed")
    print(f"Validated {len(bound)} source intervals; zero padding, zero interval reuse; cuts still need visual review.", flush=True)
    if not args.render:
        return
    require(args.output is not None and args.work_dir is not None, "Explicit new output/work paths required")
    output, work = args.output.resolve(), args.work_dir.resolve()
    require(not output.exists(), "Preserve existing output; select a new candidate path")
    require(not output.with_suffix(".manifest.json").exists(), "Existing delivery manifest would be overwritten")
    require(args.width > 0 and args.height > 0 and args.width % 2 == args.height % 2 == 0
            and args.width * 9 == args.height * 16, "Use even 16:9 output dimensions")
    work.mkdir(parents=True, exist_ok=True); output.parent.mkdir(parents=True, exist_ok=True)
    require(not any(work.iterdir()), "Use an empty work directory; no stale cached source render is accepted")
    parts = []
    for shot in bound:
        print(f"Render {shot['id']}: {shot['frames']} source frames", flush=True)
        parts.append(render_shot(shot, work / f"{shot['id']}.mp4", args.width, args.height, args.crf, args.threads))
    require(all("'" not in str(p) for p in parts), "Work path cannot contain a single quote")
    concat = work / "concat.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in parts))
    start = bound[0]["start_frame"] / FPS
    frames = sum(s["frames"] for s in bound)
    full = frames == TOTAL_FRAMES and start == 0
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-n", "-f", "concat", "-safe", "0", "-i", concat]
    if not full:
        cmd += ["-ss", str(start), "-t", str(frames/FPS)]
    cmd += ["-i", audio, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
            "-movflags", "+faststart", "-metadata", "title=Join Me in Life — revision 2 review candidate", output]
    legacy.run(cmd)
    info = legacy.probe(output)
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    require(int(video["nb_frames"]) == frames and Fraction(video["avg_frame_rate"]) == FPS, "Final frame/fps mismatch")
    legacy.run(["ffmpeg", "-v", "error", "-xerror", "-i", output, "-f", "null", "-"])
    audio_check = legacy.waveform_check(audio, output, start, None if full else frames/FPS)
    require(audio_check["correlation"] >= .995 and abs(audio_check["offset_seconds"]) <= .03, "Original-song alignment failed")
    manifest = {"schema": "jml-v2-edit-manifest/v1", "plan_sha256": legacy.sha256(args.plan), "frames": frames,
                "fps": FPS, "full_song": full, "start_frame": bound[0]["start_frame"], "shots": bound,
                "source_padding_frames": 0, "reused_source_interval_frames": 0, "full_decode": "passed",
                "audio": {"original_sha256": SONG_SHA256,
                          "mode": ("Original full song" if full else "Original-song excerpt at declared start_frame") + ", AAC256k once; no generated audio or mix edits",
                          "alignment": audio_check}, "output_sha256": legacy.sha256(output),
                "review_state": "Candidate only; source checks do not approve story, shot joins, subjective musical pace or final viewing"}
    output.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Rendered and decoded candidate: {output}")


if __name__ == "__main__":
    main()
