#!/usr/bin/env python3
"""Verify downloaded story23 output bytes and source bindings; never approve motion."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageOps


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text())


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def fitted_pixels(source):
    with Image.open(source) as opened:
        original = opened.convert("RGB")
    fitted = ImageOps.contain(original, (896, 512), Image.Resampling.LANCZOS)
    offset = ((896 - fitted.width) // 2, (512 - fitted.height) // 2)
    canvas = Image.new("RGB", (896, 512), (0, 0, 0))
    canvas.paste(fitted, offset)
    return canvas, {
        "source_dimensions": list(original.size), "contained": list(fitted.size),
        "canvas": [896, 512], "offset": list(offset), "source_sha256": sha(source),
        "rgb_sha256": hashlib.sha256(canvas.tobytes()).hexdigest(),
    }


def verify_take(bundle, results, manifest_name):
    manifest_path = bundle / manifest_name
    manifest = read(manifest_path)
    take_id = manifest["take_id"]
    take_dir = results / take_id
    render_path = take_dir / "render.json"
    render = read(render_path)
    require(render["status"] == "complete" and render["technical_valid"] is True,
            f"{take_id}: child did not report technical completion")
    require(render["manifest"] == manifest, f"{take_id}: returned manifest differs")
    require(render["manifest_sha256"] == sha(manifest_path), f"{take_id}: manifest bytes differ")
    require(read(take_dir / "model-lock.json") == read(bundle / "model-lock.json"),
            f"{take_id}: model lock differs")
    environment = read(take_dir / "environment.json")
    require(len(environment["devices"]) == 2 and
            all("T4" in d["name"] for d in environment["devices"]),
            f"{take_id}: unexpected runtime hardware")
    expected_events = []
    fittings = {}
    for kind in ("start", "end"):
        source = bundle / manifest[kind + "_image"]
        require(sha(source) == manifest[kind + "_image_sha256"], f"{take_id}: {kind} source changed")
        expected_pixels, fitting = fitted_pixels(source)
        fittings[kind] = fitting
        require(render["input_fitting"][kind] == fitting, f"{take_id}: {kind} fitting differs")
        with Image.open(take_dir / (kind + "-fitted.png")) as opened:
            actual = opened.convert("RGB")
        require(actual.size == expected_pixels.size and actual.tobytes() == expected_pixels.tobytes(),
                f"{take_id}: actual fitted {kind} PNG differs")
    for stage, dimensions in ((1, [448, 256]), (2, [896, 512])):
        for kind, index in (("start", 0), ("end", manifest["frames"] - 1)):
            expected_events.append({"guide": kind, "stage": stage, "frame_index": index,
                "rgb_sha256": fittings[kind]["rgb_sha256"], "canvas": [896, 512],
                "stage_dimensions": dimensions, "strength": 1.0})
    require(render["image_guides"] == expected_events, f"{take_id}: actual guide audit differs")
    video = take_dir / "video-silent.mp4"
    video_sha = sha(video)
    require(video_sha == render["video"]["sha256"], f"{take_id}: video hash differs")
    probe = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,width,height,nb_frames,avg_frame_rate,duration", "-of", "json", str(video)
    ], text=True))
    streams = probe["streams"]
    require(len(streams) == 1, f"{take_id}: expected exactly one silent video stream")
    stream = streams[0]
    require((stream["codec_type"], stream["width"], stream["height"], stream["avg_frame_rate"])
            == ("video", 896, 512, "24/1"), f"{take_id}: stream format mismatch")
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-xerror", "-i", str(video), "-map", "0:v:0",
        "-pix_fmt", "rgb24", "-f", "framehash", "-hash", "sha256", "-"
    ], text=True)
    hashes = [line.rsplit(",", 1)[1].strip() for line in raw.splitlines()
              if line.strip() and not line.startswith("#")]
    require(len(hashes) == manifest["frames"], f"{take_id}: decoded frame count mismatch")
    longest = current = 1
    for previous, present in zip(hashes, hashes[1:]):
        current = current + 1 if previous == present else 1
        longest = max(longest, current)
    return {"take_id": take_id, "technical_verification": "pass", "video": str(video),
        "video_sha256": video_sha, "render_sha256": sha(render_path),
        "manifest_sha256": sha(manifest_path), "frames": len(hashes), "fps": 24,
        "duration_seconds": len(hashes) / 24, "full_decode_passed": True,
        "unique_decoded_rgb_frames": len(set(hashes)), "longest_identical_frame_run": longest,
        "source_and_fitted_bytes_exact": True, "both_exact_guides_observed_both_stages": True,
        "generation_seconds": render["generation_seconds"], "child_seconds": render["elapsed_seconds"],
        "action_contract": manifest.get("action_contract"), "planned_intervals": manifest.get("editorial"),
        "motion_acceptance": "requires_independent_review", "cut_acceptance": "not_reviewed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument("--results", required=True, type=Path, help="Directory containing job.json and take directories")
    parser.add_argument("--expected-lock", required=True)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    require(not args.report.exists(), "Existing verification record is preserved; select a fresh report path")
    lock_path = args.bundle / "package-lock.json"
    require(sha(lock_path) == args.expected_lock, "Package lock does not match the verified deployment")
    lock = read(lock_path)
    for relative, expected in lock["files"].items():
        require(sha(args.bundle / relative) == expected, "Changed staged file: " + relative)
    queue = read(args.bundle / "queue.json")
    job_path = args.results / "job.json"
    job = read(job_path)
    require(job["queue_id"] == queue["queue_id"], "Downloaded job belongs to another queue")
    report = {"schema": "jml-v2-downloaded-batch-verification/v1",
        "observed_utc": datetime.now(timezone.utc).isoformat(), "queue_id": queue["queue_id"],
        "package_lock_sha256": args.expected_lock, "job_record_sha256": sha(job_path),
        "provider_job_status": job["status"], "whole_job_seconds": job.get("elapsed_seconds"),
        "scope": "Local actual downloaded source/guide/video byte checks and full decode. Unique frames do not prove meaningful action; no motion or cut approval.",
        "takes": []}
    for manifest_name in queue["manifests"]:
        try:
            report["takes"].append(verify_take(args.bundle, args.results, manifest_name))
        except Exception as error:
            report["takes"].append({"manifest": manifest_name, "technical_verification": "failed",
                                    "error_type": type(error).__name__, "error": str(error)})
    report["all_takes_technically_verified"] = all(t["technical_verification"] == "pass" for t in report["takes"])
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"report": str(args.report), "all_takes_technically_verified": report["all_takes_technically_verified"]}))
    raise SystemExit(0 if report["all_takes_technically_verified"] else 1)


if __name__ == "__main__":
    main()
