"""Check the Join Me in Life source and reproduce a visual review of Revision 4."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "productions" / "join-me-in-life" / "current"
SHEET = ROOT / "build" / "join-me-in-life" / "revision4-contact-sheet.jpg"
# One-based Blender frame numbers. Includes the held vowel, both waiting-room
# joins, the uninterrupted reach, the summer memory and the final picture.
FRAMES = (25, 321, 339, 340, 541, 725, 817, 853, 877, 937, 1010, 1439)
FPS, END = 24, 1439
PRIMARY = "Join_Me_in_Life_Short_Hybrid_Camera.mp4"


def read_json(name):
    return json.loads((PROJECT / name).read_text(encoding="utf-8"))


def require_file(path):
    if not path.is_file():
        raise ValueError(f"Missing {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")


def check_sources():
    require_file(PROJECT / "audio.mp4")
    require_file(PROJECT / read_json("brand_source.json")["asset"])
    for cut in ("experimental", "simple"):
        shots = read_json(f"camera_shots_{cut}.json")
        end = 0
        for shot in shots:
            start = round(shot["t0"] * FPS)
            stop = round(shot["t1"] * FPS)
            if start != end or stop <= start:
                raise ValueError(f"{cut}/{shot['name']}: gap, overlap or empty shot at frame {start + 1}")
            for art in (shot["art"], shot.get("vert_art")):
                if art:
                    require_file(PROJECT / "assets" / art)
            end = stop
        if end != END:
            raise ValueError(f"{cut}: timeline ends at frame {end}, expected {END}")
        for fmt in ("vert", "wide"):
            require_file(PROJECT / f"Join_Me_in_Life_{cut}_{fmt}.blend")
            for art in read_json(f"validation_{cut}_{fmt}.json")["packed_images"]:
                require_file(PROJECT / "assets" / art)
        print(f"{cut}: {len(shots)} timeline segments, {end} contiguous frames")

    cues = read_json("lyric_cues.json")
    if not cues:
        raise ValueError("Lyric cue list is empty")
    previous_end = 0.0
    for start, stop, lyric in cues:
        if not previous_end <= start < stop <= END / FPS or not lyric.strip():
            raise ValueError(f"Invalid lyric cue at {start}: {lyric}")
        previous_end = stop
    print(f"{len(cues)} lyric cues in time order")


def run(command):
    return subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()


def audio_hash(path):
    return run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0",
                "-c", "copy", "-f", "hash", "-hash", "sha256", "-"])


def check_exports(directory, full_decode):
    baseline = read_json("delivery_validation.json")
    original = audio_hash(PROJECT / "audio.mp4")
    if original != baseline["original_audio_packet_hash"]:
        raise ValueError("The source AAC payload differs from the Revision 4 record")
    files = [entry for entry in baseline["outputs"] if "_Hybrid_" in entry["file"]]
    if len(files) != 3:
        raise ValueError("Expected three hybrid deliveries in the Revision 4 record")
    require_file(directory / PRIMARY)
    reviewed = 0
    for entry in files:
        path = directory / entry["file"]
        if not path.exists():
            print(f"{path.name}: optional export absent; skipped")
            continue
        with path.open("rb") as handle:
            if hashlib.file_digest(handle, "sha256").hexdigest() != entry["sha256"]:
                raise ValueError(f"{path.name}: encoded file differs from the Revision 4 baseline")
        if audio_hash(path) != original:
            raise ValueError(f"{path.name}: original AAC payload differs")
        if full_decode:
            log = run(["ffmpeg", "-v", "error", "-xerror", "-threads", "2", "-i", str(path),
                       "-map", "0:v:0", "-map", "0:a:0", "-progress", "pipe:1",
                       "-nostats", "-f", "null", "-"])
            frames = [int(line.split("=")[1]) for line in log.splitlines() if line.startswith("frame=")]
            if not frames or frames[-1] != END:
                raise ValueError(f"{path.name}: decoder returned {frames[-1:]}, expected {END} frames")
        reviewed += 1
        print(f"{path.name}: exact baseline and original AAC" +
              (f", decoded {END} frames" if full_decode else ""), flush=True)
    print(f"Verified {reviewed} of 3 Revision 4 hybrid exports present")


def contact_sheet(video):
    # Select decoded frames before timestamp labels or tiling. The clock in
    # the footer is the source PTS, measured from the start of the full cut.
    selection = "+".join(f"eq(n,{frame - 1})" for frame in FRAMES)
    filters = (
        f"select='{selection}',scale=216:384,setsar=1,"
        "pad=216:416:0:0:color=0x172437,"
        r"drawtext=text='%{pts\:hms}':font=monospace:fontsize=17:fontcolor=white:"
        "x=(w-tw)/2:y=390,tile=4x3:padding=4:margin=4:color=0x0c1018"
    )
    SHEET.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=SHEET.parent) as work:
        image = Path(work) / "sheet.jpg"
        run(["ffmpeg", "-v", "error", "-xerror", "-threads", "2", "-i", str(video),
             "-an", "-vf", filters, "-frames:v", "1", "-q:v", "2", str(image)])
        image.replace(SHEET)
    print(f"Wrote {SHEET.relative_to(ROOT)} ({len(FRAMES)} timestamped frames)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--source-only", action="store_true", help="Check the Git source tree without FFmpeg or exports")
    modes.add_argument("--full-decode", action="store_true", help="Also decode each available hybrid delivery end to end")
    parser.add_argument("--exports", type=Path, default=PROJECT / "exports",
                        help="Directory containing original Revision 4 hybrid MP4s")
    args = parser.parse_args()
    check_sources()
    if args.source_only:
        return
    if not shutil.which("ffmpeg"):
        raise ValueError("Install FFmpeg with drawtext support to review the baseline exports")
    if not args.exports.is_dir():
        raise ValueError("Restore current/exports from the full project ZIP or pass --exports DIR")
    check_exports(args.exports, args.full_decode)
    contact_sheet(args.exports / PRIMARY)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Review failed: {exc}")
