"""Restore optional original media for Join Me in Life using Python 3."""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from zipfile import BadZipFile, ZipFile

PRODUCTION = Path(__file__).resolve().parents[1] / "productions" / "join-me-in-life"
CAMERA = "Join_Me_in_Life_Camera_Blender.zip"
PREVIEW = "Join_Me_in_Life_Waiting_Room_Fix.mp4"
CONSOLIDATED = "Music_Video_Consolidated_Package.zip"
VISUALS = "Join_Me_in_Life_Full_Package.zip"


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def restore_file(relative, data, expected, conflicts):
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f"checksum mismatch for {relative}")
    target = PRODUCTION / relative
    if target.resolve() != target or PRODUCTION not in target.parents:
        raise ValueError(f"unsafe destination: {relative}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if file_hash(target) != expected:
            conflicts.append(str(relative))
        return
    stream = target.open("xb")
    try:
        with stream:
            stream.write(data)
    except (OSError, KeyboardInterrupt):
        target.unlink(missing_ok=True)
        raise
    print(f"Restored {relative}")


def restore_visuals(archive, rows, conflicts):
    for row in rows:
        if row["production_path"].startswith("archive/visual-development-v1/"):
            member = row["original_source"].split("!/")[-1]
            restore_file(row["production_path"], archive.read(member), row["sha256"], conflicts)


def restore(path, name, rows, checksums, conflicts):
    if file_hash(path) != checksums[name]:
        raise ValueError(f"{path.name} differs from the original {name}")
    if name == PREVIEW:
        restore_file(Path("current/exports") / PREVIEW, path.read_bytes(), checksums[name], conflicts)
        return
    with ZipFile(path) as archive:
        if name == CAMERA:
            base = "Join_Me_in_Life_Camera_Project/"
            outputs = json.loads(archive.read(base + "delivery_validation.json"))["outputs"]
            for output in outputs:
                filename = output["file"]
                member = base + "exports/" + filename
                restore_file(Path("current/exports") / filename, archive.read(member), output["sha256"], conflicts)
        elif name == CONSOLIDATED:
            row = next(r for r in rows if r["original_source"] == CONSOLIDATED + "!/CHECKSUMS.sha256")
            restore_file(row["production_path"], archive.read("CHECKSUMS.sha256"), row["sha256"], conflicts)
            with ZipFile(io.BytesIO(archive.read(VISUALS))) as nested:
                restore_visuals(nested, rows, conflicts)
        else:
            restore_visuals(archive, rows, conflicts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", type=Path, nargs="+", help="downloaded package(s), preview, or a folder containing them")
    inputs = parser.parse_args().inputs
    with (PRODUCTION / "notes/source-map.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    checksums = {
        CAMERA: "802140697455fc997fc16701da88b3ecdea83b87cef2b702f6ba04d7650b5192",
        PREVIEW: "f2bed481cd49b27d7c58be86e5427ec9a66805b7c9d7a8f996eebfec0e21d046",
    }
    for row in rows:
        if row["original_source"] in (CONSOLIDATED, CONSOLIDATED + "!/" + VISUALS):
            checksums[row["original_source"].split("!/")[-1]] = row["sha256"]

    conflicts = []
    for arg in inputs:
        paths = [arg]
        if arg.is_dir():
            paths = sorted(p for p in arg.iterdir() if p.is_file() and p.name.endswith(tuple(checksums)))
        if not paths:
            parser.exit(1, f"No supported files in {arg}. See MEDIA.md.\n")
        for path in paths:
            name = next((n for n in checksums if path.name.endswith(n)), None)
            if name is None:
                parser.exit(1, f"Unrecognized input {path.name}. Use an original filename from MEDIA.md.\n")
            try:
                restore(path, name, rows, checksums, conflicts)
            except (OSError, ValueError, BadZipFile, KeyError) as error:
                parser.exit(1, f"Restore stopped: {error}\n")
    if conflicts:
        parser.exit(1, "Preserved differing local files:\n" + "\n".join(conflicts) + "\n")
    print("All requested media matches the original checksums.")


if __name__ == "__main__":
    main()
