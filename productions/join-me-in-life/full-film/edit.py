#!/usr/bin/env python3
"""Deterministic full-song animatic/editor. FFmpeg is the only rendering dependency.

Read edit.json; never change baseline assets. Video enters only through an explicit
review/approved-motion.json record. Outputs remain candidates pending review.
"""
from __future__ import annotations

import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
VERSION = "jml-editor-1.0"


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


def resolve_path(path):
    p = (ROOT / path).resolve()
    if not p.is_file():
        raise ValueError(f"Source missing: {p}")
    if p.name in {"M01_Embrace.mp4", "M02_Summer.mp4"}:
        raise ValueError(f"Rejected baseline motion is prohibited: {p.name}")
    return p


def validate_edit(edit):
    if edit["fps"] != 24 or edit["total_frames"] != 6667:
        raise ValueError("This take requires 24 fps and 6667 picture frames")
    end = 0
    for s in edit["shots"]:
        if s["start_frame"] != end or s["end_frame_exclusive"] <= end:
            raise ValueError(f"Noncontiguous or empty shot: {s['id']}")
        end = s["end_frame_exclusive"]
        resolve_path(edit["sources"][s["source_key"]]["path"])
        c = s["camera"]
        if not 1 <= c["zoom_start"] <= 1.5 or not 1 <= c["zoom_end"] <= 1.5:
            raise ValueError(f"Unsafe crop in {s['id']}")
    if end != edit["total_frames"]:
        raise ValueError("Edit does not cover the entire picture timeline")
    resolve_path(edit["audio"])


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
        p = resolve_path(c["path"])
        if not c.get("review_note"):
            raise ValueError(f"Motion approval needs a review note: {c.get('id')}")
        start, dur = float(c.get("in_seconds", 0)), float(c["duration_seconds"])
        actual = float(probe(p)["format"]["duration"])
        if start < 0 or not 0 < dur <= 5 or start + dur > actual + 1 / 24:
            raise ValueError(f"Invalid natural-speed clip selection: {c.get('id')}")
        c = dict(c, absolute_path=str(p), source_sha256=sha256(p))
        good.append(c)
    if len({c["id"] for c in good}) != len(good):
        raise ValueError("Duplicate approved clip IDs")
    return good, "Each approved clip is used at most once; no reversal, loop, or action retiming."


def assemble_plan(edit):
    clips, note = approved_clips(edit)
    used = set()
    plan = []
    hashes = {}
    for shot in edit["shots"]:
        s = dict(shot)
        source = edit["sources"][s["source_key"]]
        path = resolve_path(source["path"])
        hashes.setdefault(str(path), sha256(path))
        s["source"] = dict(source, absolute_path=str(path), sha256=hashes[str(path)])
        s["frames"] = s["end_frame_exclusive"] - s["start_frame"]
        candidates = [c for c in clips if c["id"] not in used and
                      c.get("source_key") == s["source_key"] and
                      (not c.get("shot_ids") or s["id"] in c["shot_ids"])]
        if candidates:
            c = dict(candidates[0])
            used.add(c["id"])
            c["used_frames"] = min(s["frames"], math.floor(c["duration_seconds"] * 24 + 1e-6))
            if c["used_frames"] < 1:
                raise ValueError("Approved clip is shorter than one output frame")
            s["motion"] = c
            s["classification"] = "reviewed_generated_video_with_endpoint_hold"
        else:
            s["motion"] = None
            s["classification"] = "still_artwork_with_camera_move"
        plan.append(s)
    return plan, note


def ease_expr(frames, var="on"):
    u = f"({var}/{max(1, frames - 1)})"
    return f"({u}*{u}*(3-2*{u}))"


def still_filter(shot, width, height):
    c, n = shot["camera"], shot["frames"]
    e = ease_expr(n)
    z = f"({c['zoom_start']}+({c['zoom_end']-c['zoom_start']})*{e})"
    cx = f"({c['center_start'][0]}+({c['center_end'][0]-c['center_start'][0]})*{e})"
    cy = f"({c['center_start'][1]}+({c['center_end'][1]-c['center_start'][1]})*{e})"
    # Pre-scale once to twice the output resolution. Zoompan works from one
    # source frame, with bounded subpixel camera coordinates and smooth spacing.
    return (f"scale={width*2}:{height*2}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={width*2}:{height*2},setsar=1,"
            f"zoompan=z='{z}':x='max(0,min(iw-iw/zoom,iw*{cx}-iw/zoom/2))':"
            f"y='max(0,min(ih-ih/zoom,ih*{cy}-ih/zoom/2))':"
            f"d={n}:s={width}x{height}:fps=24")


def title_filter(width, height):
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if not Path(font).exists():
        raise ValueError("Required title font missing")
    # Native title, not a fabricated rendition of the band wordmark. It sits
    # over the live picture; no black title card or long static opening.
    alpha = "if(lt(t,0.7),0,if(lt(t,1.7),(t-0.7),if(lt(t,4.1),1,if(lt(t,5.2),(5.2-t)/1.1,0))))"
    return (f",drawtext=fontfile='{font}':text='JOIN ME IN LIFE':fontsize={round(height*.050)}:"
            f"fontcolor=white:shadowcolor=black@0.5:shadowx=1:shadowy=2:"
            f"x=(w-tw)/2:y=h*0.77:alpha='{alpha}',"
            f"drawtext=fontfile='{font}':text='MERCY IN MINOR':fontsize={round(height*.022)}:"
            f"fontcolor=white@0.85:shadowcolor=black@0.5:shadowx=1:shadowy=1:"
            f"x=(w-tw)/2:y=h*0.84:alpha='{alpha}'")


def render_shot(s, args, work):
    out = work / f"{s['id']}.mp4"
    stamp = work / f"{s['id']}.json"
    key = hashlib.sha256(json.dumps({"editor": VERSION, "shot": s, "width": args.width,
                                    "height": args.height, "crf": args.crf},
                                   sort_keys=True).encode()).hexdigest()
    if not args.force and out.exists() and stamp.exists() and json.loads(stamp.read_text()).get("fingerprint") == key:
        return out
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-threads", "2"]
    if s["motion"]:
        m = s["motion"]
        cmd += ["-ss", str(m["in_seconds"]), "-i", m["absolute_path"]]
        keep = m["used_frames"]
        vf = (f"fps=24,trim=end_frame={keep},setpts=PTS-STARTPTS,"
              f"scale={args.width}:{args.height}:force_original_aspect_ratio=increase:flags=lanczos,"
              f"crop={args.width}:{args.height},setsar=1,"
              f"tpad=stop_mode=clone:stop_duration={s['frames']/24},trim=end_frame={s['frames']}")
    else:
        cmd += ["-i", s["source"]["absolute_path"]]
        vf = still_filter(s, args.width, args.height)
    if s.get("title"):
        vf += title_filter(args.width, args.height)
    fade = s.get("final_fade_seconds", 0)
    if fade:
        vf += f",fade=t=out:st={s['frames']/24-fade}:d={fade}"
    vf += ",format=yuv420p"
    cmd += ["-vf", vf, "-an", "-frames:v", str(s["frames"]), "-c:v", "libx264",
            "-preset", "veryfast", "-crf", str(args.crf), "-threads", str(args.threads),
            "-filter_threads", "1", "-r", "24", "-video_track_timescale", "24000",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-colorspace", "bt709", "-color_range", "tv", "-movflags", "+faststart", out]
    run(cmd)
    info = probe(out)
    v = next(x for x in info["streams"] if x["codec_type"] == "video")
    if int(v["nb_frames"]) != s["frames"]:
        raise ValueError(f"Wrong encoded frame count: {s['id']}")
    stamp.write_text(json.dumps({"fingerprint": key, "frames": s["frames"], "filter": vf}, indent=2) + "\n")
    return out


def packet_hashes(path):
    j = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_packets",
                       "-show_data_hash", "sha256", "-show_entries", "packet=data_hash",
                       "-of", "json", path], True))
    return [p["data_hash"] for p in j["packets"]]


def audio_pcm(path):
    b = run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", "4000",
             "-f", "s16le", "-"], True)
    a = array("h"); a.frombytes(b)
    if sys.byteorder != "little":
        a.byteswap()
    return a


def waveform_check(source, output):
    a, b = audio_pcm(source), audio_pcm(output)
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
    gen = sum(s["motion"]["used_frames"] for s in shots if s["motion"])
    holds = sum(s["frames"]-s["motion"]["used_frames"] for s in shots if s["motion"])
    still = n-gen-holds
    return {"schema": "jml-delivery-manifest/v1", "editor": VERSION,
            "status": "FULL-LENGTH ANIMATIC — not completed music video" if gen == 0 else "HYBRID REVIEW CANDIDATE — not final creative acceptance",
            "production_tools": edit["production_tools"],
            "actual_picture_production_tools": edit["production_tools"] if gen else ["ChatGPT image generation", "FFmpeg"],
            "three_tool_completed_video_requirement_met": False,
            "motion_provider_used_in_final_picture": "LTX-2.5" if gen else None,
            "warning": note, "output": str(output) if output else None,
            "fps": 24, "frames": n, "duration_seconds": n/24,
            "coverage": {"start_frame": shots[0]["start_frame"], "end_frame_exclusive": shots[-1]["end_frame_exclusive"],
                         "full_song": n == edit["total_frames"]},
            "motion_accounting": {"generated_video_seconds": gen/24,
                                  "endpoint_hold_seconds": holds/24,
                                  "still_camera_seconds": still/24,
                                  "generated_video_share": gen/n,
                                  "note": "Generated-video duration is not a claim that every frame contains character motion. Camera-only animation is separately counted."},
            "source_image_resolution_warning": "Seven new storyboard panel crops are approximately 550x306; the corrected room pair is approximately 1176x660. HD export upscales these images and is not native HD artwork.",
            "review": {"normal_speed_audiovisual_review_performed": False,
                       "technical_checks_are_not_motion_quality_approval": True},
            "shots": shots}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--render", action="store_true", help="Render; otherwise print validated plan summary")
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--height", type=int, default=540)
    ap.add_argument("--crf", type=int, default=20)
    ap.add_argument("--threads", type=int, default=3)
    ap.add_argument("--output", type=Path, default=ROOT / "exports/Join_Me_in_Life_Full_Animatic.mp4")
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
    edit = json.loads((ROOT / "edit.json").read_text())
    validate_edit(edit)
    shots, note = assemble_plan(edit)
    if args.shots:
        first,last = map(int,args.shots.split(":"))
        if not 1 <= first <= last <= len(shots):
            raise ValueError("Invalid shot selection")
        shots = shots[first-1:last]
    output = args.output.resolve()
    r = report(edit, shots, note, output)
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
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",concat]
    if args.shots:
        cmd += ["-ss",str(shots[0]["start_frame"]/24),"-t",str(r["duration_seconds"])]
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
    cmd += ["-movflags","+faststart","-metadata","title=Join Me in Life — Full Animatic",
            "-metadata","comment=Review animatic. Still-camera movement is not full character animation.",output]
    run(cmd)
    outinfo=probe(output)
    video=next(s for s in outinfo["streams"] if s["codec_type"]=="video")
    if int(video["nb_frames"])!=r["frames"] or video["r_frame_rate"]!="24/1":
        raise ValueError("Final video frame count/fps mismatch")
    run(["ffmpeg","-v","error","-i",output,"-f","null","-"])
    r["technical_validation"]={"full_decode":"passed","video_frames":int(video["nb_frames"]),
                               "width":video["width"],"height":video["height"],"pixel_format":video["pix_fmt"],
                               "container_duration":float(outinfo["format"]["duration"])}
    if not args.shots:
        if args.audio_copy:
            original_hashes, final_hashes = packet_hashes(audio),packet_hashes(output)
            identical=original_hashes==final_hashes
            r["audio"]["packet_payloads_identical"]=identical
            r["audio"]["source_packet_count"]=len(original_hashes)
            r["audio"]["output_packet_count"]=len(final_hashes)
            if not identical:
                raise ValueError("MP3 packet preservation failed")
        r["audio"]["waveform_check"]=waveform_check(audio,output)
        if r["audio"]["waveform_check"]["correlation"]<0.995 or abs(r["audio"]["waveform_check"]["offset_seconds"]) > 0.03:
            raise ValueError("Audio preservation/alignment failed")
    r["output_sha256"]=sha256(output)
    manifest=output.with_suffix(".manifest.json")
    manifest.write_text(json.dumps(r,indent=2)+"\n")
    print(f"Rendered and decoded: {output}\nDelivery manifest: {manifest}",flush=True)


if __name__=="__main__":
    main()
