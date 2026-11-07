#!/usr/bin/env python3
"""Deterministic full-song animatic/editor. FFmpeg is the only rendering dependency.

Read edit.json; never change baseline assets. Video enters only through an explicit
review/approved-motion.json record. Outputs remain candidates pending review.
"""
from __future__ import annotations

import argparse
import ast
from array import array
import hashlib
import json
import math
from pathlib import Path
from fractions import Fraction
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
VERSION = "jml-editor-1.6.2"
LOGO_PATH = "../current/assets/Band_Logo_Original.png"
REVIEWED_ANIMATIC = ROOT / "exports/Join_Me_in_Life_Full_Animatic.mp4"

DRAWN_LAYOUTS = {
    "P01_Verse_Performance.png": {
        "kind": "mouth", "bounds": [.428, .320, .023, .026],
        "poses": {0: "P01_Mouth_Closed.png", 2: "P01_Open_Vowel.png", 3: "P01_Mouth_Round.png"}},
    "P02_Chorus_Performance.png": {
        "kind": "mouth", "bounds": [.261, .140, .0145, .019],
        "poses": {0: "P02_Mouth_Closed.png", 1: "P02_Mouth_Narrow.png", 3: "P02_Mouth_Round.png"}},
    "S02_Waiting_Closeup.png": {
        "kind": "eyes", "eyes": [([.267, .365, .075, .065], 1.9),
                                     ([.606, .286, .065, .055], 2.8)]},
}


def run(cmd, capture=False):
    p = subprocess.run([str(x) for x in cmd], stdout=subprocess.PIPE if capture else None,
                       stderr=subprocess.PIPE, check=False)
    if p.returncode:
        raise RuntimeError(f"Command failed ({p.returncode}): {cmd[0]}\n{p.stderr.decode(errors='replace')[-6000:]}")
    return p.stdout if capture else None


def probe(path):
    return json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                           "-of", "json", path], True))


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def verified_drawing_file(record):
    """Registered still art/code is provenance, never a video-approval shortcut."""
    path = resolve_path(record["path"])
    if sha256(path) != record.get("sha256"):
        raise ValueError(f"Historical drawing provenance checksum changed: {path.name}")
    return path


def historical_pose_track(registry):
    """Carry over the original pure exposure rules without importing/rendering bpy."""
    if registry.get("schema") != "jml-r4-drawn-reuse/v1" or registry.get("fps") != 24:
        raise ValueError("Unsupported historical drawing registry")
    if registry.get("full_song_origin_frame") != 2409:
        raise ValueError("Historical drawings require the measured Short origin at frame 2409")
    files = {name: verified_drawing_file(rec) for name, rec in registry["source_files"].items()}
    # Read only the literal pattern table, not imports or executable Blender code.
    tree = ast.parse(files["native_animation.py"].read_text())
    assignment = next((n for n in tree.body if isinstance(n, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == "PATTERNS" for t in n.targets)), None)
    if assignment is None:
        raise ValueError("Original mouth pattern table missing")
    patterns = ast.literal_eval(assignment.value)
    poses = [0] * 1440
    for segment in json.loads(files["word_timing.json"].read_text()):
        for word in segment["words"]:
            a, b = word["start"], word["end"]
            text = word["word"].strip().lower().strip(".,!?")
            if text not in patterns:
                continue
            changes = [(max(0, round((a + (b-a)*fraction)*24)-1), pose)
                       for fraction, pose in patterns[text]]
            for frame in range(max(0, round(a*24)-1), min(len(poses), round(b*24))):
                pose = changes[0][1]
                for at, value in changes:
                    if at <= frame:
                        pose = value
                poses[frame] = pose
    # Original R4 correction: keep the rounded vowel through one-based frame339.
    poses[round(13.32*24):round(14.125*24)] = [3] * (round(14.125*24)-round(13.32*24))
    return poses


def frame_runs(values, target):
    runs, first = [], None
    for n, value in enumerate(values + [None]):
        if value == target and first is None:
            first = n
        elif value != target and first is not None:
            runs.append([first, n])
            first = None
    return runs


def drawn_segments(edit, shot, poses):
    requested = shot.get("drawn_art_segments", [])
    if not requested:
        return []
    registry = edit["historical_drawn_art"]
    if not isinstance(requested, list):
        raise ValueError("Historical drawing segments must be a list")
    result, cursor = [], shot["start_frame"]
    for part in requested:
        a, b = part["start_frame"], part["end_frame_exclusive"]
        if (isinstance(a, bool) or isinstance(b, bool) or not isinstance(a, int)
                or not isinstance(b, int) or a != cursor or b <= a or b > shot["end_frame_exclusive"]):
            raise ValueError("Historical drawing segments must cover their shot exactly once")
        source = edit["sources"][part["source_key"]]
        path = resolve_path(source["path"])
        layout = DRAWN_LAYOUTS.get(path.name)
        if layout is None or part["kind"] != layout["kind"]:
            raise ValueError("Historical drawings require a registered, matching source plate")
        registered = verified_drawing_file(registry["drawings"][path.name])
        if sha256(path) != sha256(registered):
            raise ValueError("Historical drawing base does not match its supplied original")
        stream = next(x for x in probe(path)["streams"] if x["codec_type"] == "video")
        dimensions = [stream["width"], stream["height"]]
        patches = []
        if layout["kind"] == "mouth":
            offset = a - registry["full_song_origin_frame"]
            if offset < 0 or offset + b-a > len(poses):
                raise ValueError("Historical mouth exposures may only occupy their matched Short span")
            selected = poses[offset:offset+b-a]
            candidates = [(filename, layout["bounds"], {"runs": frame_runs(selected, pose), "pose": pose})
                          for pose, filename in layout["poses"].items()]
        else:
            candidates = []
            for bounds, delay in layout["eyes"]:
                at = round(delay*24)
                # Same original four blink keys; no random or repeating blink loop.
                keys = [[at-2, 0], [at, 1], [at+2, 1], [at+4, 0]] if at+5 < b-a-1 else []
                candidates.append(("S02_Blink.png", bounds, {"opacity_keys": keys}))
        for filename, bounds, timing in candidates:
            if not timing.get("runs") and not timing.get("opacity_keys"):
                continue
            patch = verified_drawing_file(registry["drawings"][filename])
            size = next(x for x in probe(patch)["streams"] if x["codec_type"] == "video")
            if [size["width"], size["height"]] != dimensions:
                raise ValueError("Historical drawing registration requires identical image dimensions")
            patches.append(dict(path=str(patch), sha256=sha256(patch), bounds=bounds, **timing))
        result.append(dict(part, frames=b-a, source=dict(source, absolute_path=str(path),
                             sha256=sha256(path), native_dimensions=dimensions), patches=patches,
                           provenance=registry["source_files"], full_song_origin_frame=2409,
                           scope="Supplied R4 drawn exposure reuse; not new LTX or phoneme-complete lip sync"))
        cursor = b
    if cursor != shot["end_frame_exclusive"]:
        raise ValueError("Historical drawing segments must cover their shot exactly once")
    return result


def verify_existing_review(approval, source_digest):
    """Bind a scoped legacy-source exception to an actual superseding review."""
    if (approval.get("status") != "approved"
            or approval.get("usage") != "reused_existing_video"
            or not isinstance(approval.get("review_note"), str)
            or not approval["review_note"].strip()):
        raise ValueError("Existing video reuse requires explicit approval and a nonblank review note")
    if approval.get("reviewed_source_sha256") != source_digest:
        raise ValueError("Motion approval must match the reviewed source checksum")
    review = approval.get("superseding_review")
    if not isinstance(review, dict) or not isinstance(review.get("path"), str) or not review["path"].strip():
        raise ValueError("Existing video reuse needs a superseding review file and checksum")
    path = (ROOT / review["path"]).resolve()
    if not path.is_file() or sha256(path) != review.get("sha256"):
        raise ValueError("Superseding review file is missing or its checksum changed")
    if source_digest not in path.read_text(encoding="utf-8"):
        raise ValueError("Superseding review must identify the exact existing source checksum")


def resolve_path(path, *, existing_approval=None):
    p = (ROOT / path).resolve()
    if not p.is_file():
        raise ValueError(f"Source missing: {p}")
    if p.name in {"M01_Embrace.mp4", "M02_Summer.mp4"}:
        if existing_approval is None:
            raise ValueError(f"Rejected baseline motion is prohibited without scoped superseding review: {p.name}")
        verify_existing_review(existing_approval, sha256(p))
    return p


def validate_edit(edit):
    if edit["fps"] != 24 or edit["total_frames"] != 6667:
        raise ValueError("This take requires 24 fps and 6667 picture frames")
    end = 0
    for s in edit["shots"]:
        if s["start_frame"] != end or s["end_frame_exclusive"] <= end:
            raise ValueError(f"Noncontiguous or empty shot: {s['id']}")
        end = s["end_frame_exclusive"]
        if s.get("title") and s["start_frame"] != 0:
            raise ValueError("Opening branding may appear only at full-song frame zero")
        resolve_path(edit["sources"][s["source_key"]]["path"])
        c = s["camera"]
        closeup = s.get("framing_intent") == "deliberate_stationary_closeup"
        if closeup and (c["zoom_start"] != c["zoom_end"] or c["center_start"] != c["center_end"]):
            raise ValueError(f"Deliberate close-up must be stationary: {s['id']}")
        max_zoom = 2 if closeup else 1.5
        if not 1 <= c["zoom_start"] <= max_zoom or not 1 <= c["zoom_end"] <= max_zoom:
            raise ValueError(f"Unsafe crop in {s['id']}")
    if end != edit["total_frames"]:
        raise ValueError("Edit does not cover the entire picture timeline")
    resolve_path(edit["audio"])


def video_duration(path):
    """Use the picture extent, not a potentially longer audio/container duration."""
    video = next((s for s in probe(path)["streams"] if s["codec_type"] == "video"), None)
    if video is None:
        raise ValueError(f"Motion source has no video stream: {path}")
    try:
        duration = float(video["duration"])
    except (KeyError, ValueError, TypeError):
        try:
            duration = int(video["nb_frames"]) / float(Fraction(video["avg_frame_rate"]))
        except (KeyError, ValueError, ZeroDivisionError, TypeError) as exc:
            raise ValueError(f"Cannot establish video duration: {path}") from exc
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError(f"Invalid video duration: {path}")
    return duration


def approved_clips(edit):
    f = ROOT / edit["approved_motion"]
    if not f.exists():
        return [], "No approved-motion manifest exists; every shot uses still artwork."
    data = json.loads(f.read_text())
    if data.get("schema") != "jml-approved-motion/v1":
        raise ValueError("Unsupported approval schema; refusing unreviewed motion")
    good = []
    for c in data.get("clips", []):
        if c.get("status") != "approved":
            continue
        if not isinstance(c.get("review_note"), str) or not c["review_note"].strip():
            raise ValueError(f"Motion approval needs a review note: {c.get('id')}")
        usage = c.get("usage", "newly_generated_video")
        if usage not in {"newly_generated_video", "reused_existing_video"}:
            raise ValueError(f"Unsupported motion usage: {c.get('id')}")
        framing = c.get("framing_policy", "fill")
        if framing not in {"fill", "contain"}:
            raise ValueError(f"Unsupported motion framing policy: {c.get('id')}")
        p = resolve_path(c["path"], existing_approval=c if usage == "reused_existing_video" else None)
        start, dur = float(c.get("in_seconds", 0)), float(c["duration_seconds"])
        actual = video_duration(p)
        if (not math.isfinite(start) or not math.isfinite(dur) or start < 0 or dur <= 0
                or start + dur > actual + 1e-6):
            raise ValueError(f"Invalid natural-speed clip selection: {c.get('id')}")
        digest = sha256(p)
        if c.get("reviewed_source_sha256") != digest:
            raise ValueError(f"Motion approval must match the reviewed source checksum: {c.get('id')}")
        if usage == "reused_existing_video":
            verify_existing_review(c, digest)
        lead = c.get("lead_in_frames", 0)
        if isinstance(lead, bool) or not isinstance(lead, int) or lead < 0:
            raise ValueError(f"lead_in_frames must be a nonnegative integer: {c.get('id')}")
        if c.get("source_key") not in edit["sources"]:
            raise ValueError(f"Unknown motion source key: {c.get('id')}")
        targets = c.get("shot_ids", [])
        if not isinstance(targets, list) or any(not isinstance(t, str) for t in targets):
            raise ValueError(f"Invalid motion target list: {c.get('id')}")
        compatible = {s["id"] for s in edit["shots"] if s["source_key"] == c["source_key"]}
        if not set(targets).issubset(compatible):
            raise ValueError(f"Motion targets do not match the reviewed source key: {c.get('id')}")
        c = dict(c, in_seconds=start, duration_seconds=dur, absolute_path=str(p),
                 source_sha256=digest, source_video_duration_seconds=actual,
                 usage=usage, lead_in_frames=lead, framing_policy=framing)
        good.append(c)
    if len({c["id"] for c in good}) != len(good):
        raise ValueError("Duplicate approved clip IDs")
    return good, "Each approved source interval plays once at natural speed; any first/final-frame holds are separately counted. Source approval does not approve new holds, joins or the full sequence."


def assemble_plan(edit):
    clips, note = approved_clips(edit)
    poses = historical_pose_track(edit["historical_drawn_art"]) if any(
        s.get("drawn_art_segments") for s in edit["shots"]) else None
    used = set()
    plan = []
    provenance = {}
    for shot in edit["shots"]:
        s = dict(shot)
        source = edit["sources"][s["source_key"]]
        path = resolve_path(source["path"])
        if str(path) not in provenance:
            stream = next(x for x in probe(path)["streams"] if x["codec_type"] == "video")
            provenance[str(path)] = {"sha256": sha256(path),
                                     "native_dimensions": [stream["width"], stream["height"]]}
        s["source"] = dict(source, absolute_path=str(path), **provenance[str(path)])
        if s.get("title"):
            if s["start_frame"] != 0:
                raise ValueError("Opening branding may appear only at full-song frame zero")
            logo = resolve_path(LOGO_PATH)
            s["branding"] = {"path": LOGO_PATH, "absolute_path": str(logo), "sha256": sha256(logo),
                             "method": "original silver artwork; planar RGB screen blend, opacity 0.94",
                             "lockup": "song title directly below original logo on dark upper facade; shared fade",
                             "fade_in_seconds": [0.35, 0.75], "fade_out_seconds": [4.15, 4.80]}
        s["frames"] = s["end_frame_exclusive"] - s["start_frame"]
        candidates = [c for c in clips if c["id"] not in used and
                      c.get("source_key") == s["source_key"] and
                      (not c.get("shot_ids") or s["id"] in c["shot_ids"])]
        if candidates:
            c = dict(candidates[0])
            used.add(c["id"])
            available = s["frames"] - c["lead_in_frames"]
            if available <= 0:
                raise ValueError(f"Lead-in leaves no source playback in {s['id']}")
            c["used_frames"] = min(available, math.floor(c["duration_seconds"] * 24 + 1e-6))
            if c["used_frames"] < 1:
                raise ValueError("Approved clip is shorter than one output frame")
            c["endpoint_hold_frames"] = available - c["used_frames"]
            c["source_start_timeline_frame"] = s["start_frame"] + c["lead_in_frames"]
            c["source_end_timeline_frame_exclusive"] = c["source_start_timeline_frame"] + c["used_frames"]
            s["motion"] = c
            kind = "reviewed_reused_existing_video" if c["usage"] == "reused_existing_video" else "reviewed_generated_video"
            s["classification"] = kind + ("_with_holds" if c["used_frames"] != s["frames"] else "")
        else:
            s["motion"] = None
            s["classification"] = "still_artwork_with_camera_move"
        s["drawn_art_segments"] = drawn_segments(edit, s, poses)
        if s["drawn_art_segments"]:
            if s["motion"]:
                raise ValueError("A shot cannot combine approved video with historical drawn exposures")
            s["classification"] = "reused_supplied_drawn_exposures_with_camera_move"
        plan.append(s)
    return plan, note


def ease_expr(frames, var="on"):
    u = f"({var}/{max(1, frames - 1)})"
    return f"({u}*{u}*(3-2*{u}))"


def still_filter(shot, width, height, streamed=False):
    c, n = shot["camera"], shot["frames"]
    e = ease_expr(shot.get("camera_total_frames", n),
                  f"(on+{shot.get('camera_frame_offset', 0)})")
    z = f"({c['zoom_start']}+({c['zoom_end']-c['zoom_start']})*{e})"
    cx = f"({c['center_start'][0]}+({c['center_end'][0]-c['center_start'][0]})*{e})"
    cy = f"({c['center_start'][1]}+({c['center_end'][1]-c['center_start'][1]})*{e})"
    # Pre-scale once to twice the output resolution. Zoompan works from one
    # source frame, with bounded subpixel camera coordinates and smooth spacing.
    return (f"scale={width*2}:{height*2}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={width*2}:{height*2},setsar=1,"
            f"zoompan=z='{z}':x='max(0,min(iw-iw/zoom,iw*{cx}-iw/zoom/2))':"
            f"y='max(0,min(ih-ih/zoom,ih*{cy}-ih/zoom/2))':"
            f"d={1 if streamed else n}:s={width}x{height}:fps=24")


def prepare_drawing_patch(patch, dimensions, work):
    """Local feathered source-drawing patch. All pixel operations use FFmpeg."""
    width, height = dimensions
    cx, cy, rx, ry = [v * dim for v, dim in zip(patch["bounds"], [width, height, width, height])]
    x, y = max(0, math.floor(cx-rx)), max(0, math.floor(cy-ry))
    w, h = min(width, math.ceil(cx+rx))-x, min(height, math.ceil(cy+ry))-y
    key = hashlib.sha256(json.dumps([VERSION, patch["sha256"], patch["bounds"], dimensions]).encode()).hexdigest()
    folder = work / "drawing-patches"; folder.mkdir(exist_ok=True)
    output = folder / f"{key}.png"
    if not output.exists():
        def feather(axis, offset, center, radius):
            u = f"clip((abs(({axis}+{offset}-{center})/{radius})-.72)/.28,0,1)"
            return f"(1-(6*pow({u},5)-15*pow({u},4)+10*pow({u},3)))"
        alpha = f"255*{feather('X', x, cx, rx)}*{feather('Y', y, cy, ry)}"
        vf = (f"format=rgba,crop={w}:{h}:{x}:{y}:exact=1,"
              f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='{alpha}'")
        run(["ffmpeg", "-v", "error", "-y", "-i", patch["path"], "-vf", vf,
             "-frames:v", "1", "-threads", "1", "-filter_threads", "1", output])
    return output, x, y


def drawing_composite(s, args, work, cmd):
    art = s["drawn_art"]
    cmd += ["-loop", "1", "-framerate", "24", "-i", s["source"]["absolute_path"]]
    filters = ["[0:v]format=rgba[base0]"]
    for index, patch in enumerate(art["patches"], 1):
        path, x, y = prepare_drawing_patch(patch, art["source"]["native_dimensions"], work)
        cmd += ["-loop", "1", "-framerate", "24", "-i", path]
        patch_filter = f"[{index}:v]format=rgba"
        if patch.get("opacity_keys"):
            keys = patch["opacity_keys"]
            # Original linear interpolation across the four blink exposure keys.
            expression = "0"
            for (a, va), (b, vb) in reversed(list(zip(keys, keys[1:]))):
                value = f"({va}+({vb-va})*(N-{a})/{b-a})"
                expression = f"if(between(N,{a},{b}),{value},{expression})"
            patch_filter += f",geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='alpha(X,Y)*({expression})'"
            enable = "1"
        else:
            enable = "+".join(f"between(n,{a},{b-1})" for a, b in patch["runs"])
        filters.append(patch_filter + f"[patch{index}]")
        filters.append(f"[base{index-1}][patch{index}]overlay=x={x}:y={y}:"
                       f"enable='{enable}':format=rgb:alpha=straight:shortest=1[base{index}]")
    filters.append(f"[base{len(art['patches'])}]" + still_filter(s, args.width, args.height, streamed=True))
    return ";".join(filters)


def render_drawing_segments(s, args, work, output):
    parts = []
    for i, part in enumerate(s["drawn_art_segments"], 1):
        child = dict(s, id=f"{s['id']}-drawn-{i:02}", source=part["source"],
                     start_frame=part["start_frame"], end_frame_exclusive=part["end_frame_exclusive"],
                     frames=part["frames"], drawn_art_segments=[], drawn_art=part,
                     camera_frame_offset=part["start_frame"]-s["start_frame"], camera_total_frames=s["frames"])
        parts.append(render_shot(child, args, work))
    listing = work / f"{s['id']}-drawn-concat.txt"
    if any("'" in str(p) for p in parts):
        raise ValueError("Output path may not contain a single quote")
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", listing,
         "-an", "-c:v", "copy", "-movflags", "+faststart", output])


def title_filter(width, height):
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    if not Path(font).exists():
        raise ValueError("Required title font missing")
    # Draw on the same RGB layer as the original logo, before their shared fade.
    logo_width, x, y = round(width * .34), round(width * .49), round(height * .04)
    title_y = y + round(logo_width / 3) + round(height * .012)
    return (f",drawtext=fontfile='{font}':text='Join Me in Life':fontsize={round(height*.046)}:"
            f"fontcolor=white:x={x}+({logo_width}-tw)/2:y={title_y}")


def opening_composite(vf, width, height):
    """R4's paired logo/title fade, on the opening exterior's quiet upper facade."""
    logo_width, x, y = round(width * .34), round(width * .49), round(height * .04)
    return (f"[0:v]{vf},format=gbrp[base];"
            f"[1:v]scale={logo_width}:-1:flags=lanczos,format=gbrp,"
            f"pad={width}:{height}:{x}:{y}:color=black{title_filter(width, height)},"
            "fade=t=in:st=0.35:d=0.4,fade=t=out:st=4.15:d=0.65[logo];"
            "[base][logo]blend=all_mode=screen:all_opacity=0.94:shortest=1,format=gbrp")


def render_shot(s, args, work):
    out = work / f"{s['id']}.mp4"
    stamp = work / f"{s['id']}.json"
    key = hashlib.sha256(json.dumps({"editor": VERSION, "shot": s, "width": args.width,
                                    "height": args.height, "crf": args.crf},
                                   sort_keys=True).encode()).hexdigest()
    if not args.force and out.exists() and stamp.exists() and json.loads(stamp.read_text()).get("fingerprint") == key:
        return out
    if s.get("drawn_art_segments"):
        if s.get("title") or s.get("final_fade_seconds"):
            raise ValueError("Drawing sequences cannot carry opening branding or final fades")
        render_drawing_segments(s, args, work, out)
        video = next(x for x in probe(out)["streams"] if x["codec_type"] == "video")
        if int(video["nb_frames"]) != s["frames"]:
            raise ValueError(f"Wrong drawn-sequence frame count: {s['id']}")
        stamp.write_text(json.dumps({"fingerprint": key, "frames": s["frames"],
                                     "method": "supplied drawing patches composited by FFmpeg"}, indent=2) + "\n")
        return out
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-threads", "2"]
    if s["motion"]:
        m = s["motion"]
        cmd += ["-i", m["absolute_path"]]
        keep = m["used_frames"]
        if m.get("framing_policy", "fill") == "contain":
            framing = (f"scale={args.width}:{args.height}:force_original_aspect_ratio=decrease:"
                       f"force_divisible_by=4:flags=lanczos,"
                       f"pad={args.width}:{args.height}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,")
        else:
            # Preserve all existing default fill behavior.
            framing = (f"scale={args.width}:{args.height}:force_original_aspect_ratio=increase:flags=lanczos,"
                       f"crop={args.width}:{args.height},setsar=1,")
        # Bound the decoded source interval before cadence conversion. Keep the
        # fps metadata through tpad: a second setpts would discard it in FFmpeg 7.
        vf = (f"trim=start={m['in_seconds']}:duration={m['duration_seconds']},setpts=PTS-STARTPTS,"
              f"fps=24,trim=end_frame={keep},"
              f"{framing}"
              f"tpad=start_mode=clone:start={m['lead_in_frames']}:"
              f"stop_mode=clone:stop={m['endpoint_hold_frames']},trim=end_frame={s['frames']}")
    elif s.get("drawn_art"):
        vf = drawing_composite(s, args, work, cmd)
    else:
        cmd += ["-i", s["source"]["absolute_path"]]
        vf = still_filter(s, args.width, args.height)
    branded = bool(s.get("title"))
    if branded:
        if s["start_frame"] != 0:
            raise ValueError("Opening branding may appear only at full-song frame zero")
        cmd += ["-loop", "1", "-framerate", "24", "-i", s["branding"]["absolute_path"]]
        vf = opening_composite(vf, args.width, args.height)
    fade = s.get("final_fade_seconds", 0)
    if fade:
        vf += f",fade=t=out:st={s['frames']/24-fade}:d={fade}"
    vf += ",format=yuv420p"
    if branded or s.get("drawn_art"):
        cmd += ["-filter_complex_threads", "1", "-filter_complex", vf + "[video]", "-map", "[video]"]
    else:
        cmd += ["-vf", vf]
    cmd += ["-an", "-frames:v", str(s["frames"]), "-c:v", "libx264",
            "-preset", "veryfast", "-crf", str(args.crf), "-threads", str(args.threads),
            "-filter_threads", "1", "-r", "24", "-video_track_timescale", "24000",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-colorspace", "bt709", "-color_range", "tv", "-movflags", "+faststart", out]
    run(cmd)
    info = probe(out)
    v = next(x for x in info["streams"] if x["codec_type"] == "video")
    if int(v["nb_frames"]) != s["frames"]:
        raise ValueError(f"Wrong encoded frame count: {s['id']}")
    stamp.write_text(json.dumps({"fingerprint": key, "frames": s["frames"], "filter": vf,
                                "motion_framing_policy": s["motion"].get("framing_policy", "fill")
                                if s["motion"] else None}, indent=2) + "\n")
    return out


def packet_hashes(path):
    j = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_packets",
                       "-show_data_hash", "sha256", "-show_entries", "packet=data_hash",
                       "-of", "json", path], True))
    return [p["data_hash"] for p in j["packets"]]


def audio_pcm(path, start_seconds=0, duration_seconds=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start_seconds), "-i", path]
    if duration_seconds is not None:
        cmd += ["-t", str(duration_seconds)]
    b = run(cmd + ["-vn", "-ac", "1", "-ar", "4000", "-f", "s16le", "-"], True)
    a = array("h"); a.frombytes(b)
    if sys.byteorder != "little":
        a.byteswap()
    return a


def waveform_check(source, output, source_start_seconds=0, duration_seconds=None):
    a, b = audio_pcm(source, source_start_seconds, duration_seconds), audio_pcm(output)
    if a == b:
        return {"sample_rate": 4000, "decoded_pcm_identical": True, "correlation": 1.0,
                "offset_seconds": 0, "source_samples": len(a), "output_samples": len(b)}
    def corr(lag, stride):
        a0, b0 = max(0, -lag), max(0, lag)
        n = min(len(a)-a0, len(b)-b0)
        xs = a[a0:a0+n:stride]; ys = b[b0:b0+n:stride]
        dot = sum(x*y for x,y in zip(xs,ys))
        den = math.sqrt(sum(x*x for x in xs)*sum(y*y for y in ys))
        return dot/den if den else 0
    lag = max(range(-400, 401, 10), key=lambda v:corr(v, 40))
    lag = max(range(lag-10, lag+11), key=lambda v:corr(v, 10))
    score = corr(lag, 1)
    return {"sample_rate": 4000, "decoded_pcm_identical": False, "correlation": score,
            "offset_seconds": lag/4000, "source_samples": len(a), "output_samples": len(b),
            "note": "Normalized cross-correlation, +/-100 ms lag search; technical alignment, not listening."}


def report(edit, shots, note, output=None):
    n = sum(s["frames"] for s in shots)
    full_song = (n == edit["total_frames"] and shots[0]["start_frame"] == 0
                 and shots[-1]["end_frame_exclusive"] == edit["total_frames"])
    gen = sum(s["motion"]["used_frames"] for s in shots if s["motion"] and s["motion"]["usage"] == "newly_generated_video")
    reused = sum(s["motion"]["used_frames"] for s in shots if s["motion"] and s["motion"]["usage"] == "reused_existing_video")
    leads = sum(s["motion"]["lead_in_frames"] for s in shots if s["motion"])
    holds = sum(s["motion"]["endpoint_hold_frames"] for s in shots if s["motion"])
    drawn = sum(s["frames"] for s in shots if s.get("drawn_art_segments"))
    still = n-gen-reused-leads-holds-drawn
    providers = sorted({s["motion"].get("provider", "unspecified in review manifest")
                        for s in shots if s["motion"]})
    new_providers = sorted({s["motion"].get("provider", "unspecified in review manifest")
                           for s in shots if s["motion"] and s["motion"]["usage"] == "newly_generated_video"})
    historical_providers = sorted({s["motion"].get("provider", "unspecified in review manifest")
                                  for s in shots if s["motion"] and s["motion"]["usage"] == "reused_existing_video"})
    new_art_used = any(s["source"].get("kind") in {"storyboard_panel", "refined_storyboard_redraw"}
                       and (not s["motion"] or s["motion"]["usage"] != "reused_existing_video")
                       for s in shots)
    return {"schema": "jml-delivery-manifest/v1", "editor": VERSION,
            "status": (("FULL-LENGTH ANIMATIC" if full_song else "ANIMATIC EXCERPT") + " — not completed music video"
                       if gen + reused + drawn == 0 else "HYBRID REVIEW CANDIDATE — new sequence and holds require review"),
            "production_tools": edit["production_tools"],
            "production_tools_status": "planned route; not proof all three tools contributed accepted new picture",
            "actual_picture_production_tools": (["ChatGPT image generation"] if new_art_used else []) + new_providers + ["FFmpeg"],
            "historical_reused_source_providers": historical_providers,
            "provider_accounting_note": "Reused video retains its historical source provider; importing it is not a new provider call or new LTX generation.",
            "three_tool_completed_video_requirement_met": False,
            "motion_provider_used_in_final_picture": providers[0] if len(providers) == 1 else providers or None,
            "warning": note, "output": str(output) if output else None,
            "fps": 24, "frames": n, "duration_seconds": n/24,
            "coverage": {"start_frame": shots[0]["start_frame"], "end_frame_exclusive": shots[-1]["end_frame_exclusive"],
                         "full_song": full_song},
            "motion_accounting": {"generated_video_seconds": gen/24,
                                  "new_generated_video_seconds": gen/24,
                                  "reused_existing_video_seconds": reused/24,
                                  "reused_drawn_exposure_sequence_seconds": drawn/24,
                                  "lead_in_hold_seconds": leads/24,
                                  "endpoint_hold_seconds": holds/24,
                                  "still_camera_seconds": still/24,
                                  "generated_video_share": gen/n,
                                  "note": "New generation, reused existing source frames, supplied drawn-exposure sequences, first-frame holds, endpoint holds and still-camera frames are separate. Drawn-exposure duration measures the sequence, not continuous body motion or phoneme-complete sync. Source approval is not sequence approval."},
            "source_image_resolution_warning": "Actual source dimensions are recorded per shot. Enlarging a source for export does not create native detail.",
            "review": {"normal_speed_audiovisual_review_performed": False,
                       "technical_checks_are_not_motion_quality_approval": True},
            "shots": shots}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--edit", type=Path, default=ROOT / "edit.json",
                    help="Named edit configuration; source paths remain relative to the full-film root")
    ap.add_argument("--render", action="store_true", help="Render; otherwise print validated plan summary")
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--height", type=int, default=540)
    ap.add_argument("--crf", type=int, default=20)
    ap.add_argument("--threads", type=int, default=3)
    ap.add_argument("--output", type=Path, default=ROOT / "exports/Join_Me_in_Life_Full_Candidate.mp4")
    ap.add_argument("--work-dir", type=Path, default=ROOT / "work/edit-960x540")
    ap.add_argument("--shots", help="Contiguous inclusive numeric range, e.g. 1:3; diagnostic excerpt only")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--audio-copy", action="store_true", help="Opt-in MP3 packet copy; default AAC 256k for mobile/browser compatibility")
    args = ap.parse_args()
    if args.width % 2 or args.height % 2 or args.width*9 != args.height*16:
        raise ValueError("Use even 16:9 dimensions, e.g. 960x540 or 1920x1080")
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise ValueError(f"Required executable missing: {tool}")
    edit_path = args.edit.resolve()
    edit = json.loads(edit_path.read_text())
    validate_edit(edit)
    shots, note = assemble_plan(edit)
    if args.shots:
        first,last = map(int,args.shots.split(":"))
        if not 1 <= first <= last <= len(shots):
            raise ValueError("Invalid shot selection")
        shots = shots[first-1:last]
    output = args.output.resolve()
    if args.render and output == REVIEWED_ANIMATIC.resolve():
        raise ValueError("The reviewed animatic is preserved; choose a separate candidate output path")
    r = report(edit, shots, note, output)
    r["edit_config"] = {"path": str(edit_path), "sha256": sha256(edit_path)}
    print(json.dumps({k:v for k,v in r.items() if k != "shots"}, indent=2), flush=True)
    if not args.render:
        return
    work = args.work_dir.resolve(); work.mkdir(parents=True,exist_ok=True)
    output.parent.mkdir(parents=True,exist_ok=True)
    parts=[]
    for i,s in enumerate(shots,1):
        print(f"[{i}/{len(shots)}] {s['id']} {s['section']} {s['frames']} frames — {s['classification']}", flush=True)
        parts.append(render_shot(s,args,work))
    concat=work/"concat.txt"
    # Paths are controlled local outputs. Reject a single quote rather than
    # risk generating an ambiguous FFmpeg concat instruction.
    if any("'" in str(p) for p in parts):
        raise ValueError("Output path may not contain a single quote")
    concat.write_text("".join(f"file '{p}'\n" for p in parts))
    audio=resolve_path(edit["audio"])
    audio_start = shots[0]["start_frame"]/24 if args.shots else 0
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",concat]
    if args.shots:
        cmd += ["-ss",str(audio_start),"-t",str(r["duration_seconds"])]
    cmd += ["-i",audio,"-map","0:v:0","-map","1:a:0","-c:v","copy"]
    if args.shots or not args.audio_copy:
        cmd += ["-c:a","aac","-b:a","256k"]
        r["audio"]={"mode":"AAC 256k encoded once from original MP3 for portable MP4 playback",
                     "original_audio_sha256":sha256(audio),"packet_identity_claimed":False}
    else:
        cmd += ["-c:a","copy"]
        r["audio"]={"mode":"Original MP3 compressed packets copied into MP4; no audio re-encoding",
                     "original_audio_sha256":sha256(audio),
                     "compatibility_note":"MP3 in MP4 is supported by FFmpeg and common desktop/browser players; use AAC derivative if a target player rejects this combination."}
    title = "Join Me in Life — " + ("Full candidate" if r["coverage"]["full_song"] else "Review excerpt")
    cmd += ["-movflags","+faststart","-metadata",f"title={title}",
            "-metadata","comment=Review candidate. Reused source, new generation and still/endpoint holds are separately reported; sequence acceptance is pending.",output]
    run(cmd)
    outinfo=probe(output)
    video=next(s for s in outinfo["streams"] if s["codec_type"]=="video")
    if int(video["nb_frames"])!=r["frames"] or video["r_frame_rate"]!="24/1":
        raise ValueError("Final video frame count/fps mismatch")
    run(["ffmpeg","-v","error","-i",output,"-f","null","-"])
    r["technical_validation"]={"full_decode":"passed","video_frames":int(video["nb_frames"]),
                               "width":video["width"],"height":video["height"],"pixel_format":video["pix_fmt"],
                               "container_duration":float(outinfo["format"]["duration"])}
    if not args.shots and args.audio_copy:
        original_hashes, final_hashes = packet_hashes(audio),packet_hashes(output)
        identical=original_hashes==final_hashes
        r["audio"]["packet_payloads_identical"]=identical
        r["audio"]["source_packet_count"]=len(original_hashes)
        r["audio"]["output_packet_count"]=len(final_hashes)
        if not identical:
            raise ValueError("MP3 packet preservation failed")
    r["audio"]["source_start_seconds"] = audio_start
    r["audio"]["waveform_check"]=waveform_check(
        audio, output, source_start_seconds=audio_start,
        duration_seconds=r["duration_seconds"] if args.shots else None)
    if r["audio"]["waveform_check"]["correlation"]<0.995 or abs(r["audio"]["waveform_check"]["offset_seconds"]) > 0.03:
        raise ValueError("Audio preservation/alignment failed")
    r["output_sha256"]=sha256(output)
    manifest=output.with_suffix(".manifest.json")
    manifest.write_text(json.dumps(r,indent=2)+"\n")
    print(f"Rendered and decoded: {output}\nDelivery manifest: {manifest}",flush=True)


if __name__=="__main__":
    main()
