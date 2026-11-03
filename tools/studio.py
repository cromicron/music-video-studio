"""Orient a studio session and check its durable records without changing files."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_RECORDS = ("README.md", "STATUS.md", "DECISIONS.md", "SESSIONS.md")
REQUIRED_FILES = (
    "README.md", "AGENTS.md", "MEDIA.md", "studio.json",
    "docs/SESSION_GUIDE.md", "docs/STRUCTURE.md", "band/README.md",
    "tools/README.md", "tools/studio.py", "tools/review.py",
    "tools/restore_media.py", "tools/setup-blender-linux.sh",
    "tools/requirements-bpy.txt", ".github/README.md",
    ".github/workflows/source-check.yml", ".github/workflows/render-edit.yml",
    ".github/workflows/native-review.yml", ".github/workflows/review-short.yml",
    *(f"templates/production/{name}" for name in PRODUCTION_RECORDS),
)
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
PLACEHOLDER = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")


def load_studio(root):
    data = json.loads((root / "studio.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != "mercy-in-minor-studio/v1":
        raise ValueError("studio.json: unsupported studio schema")
    entries = data.get("productions")
    if not isinstance(entries, list) or not entries:
        raise ValueError("studio.json: productions must be a non-empty list")
    ids = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("studio.json: production entries must be objects")
        slug, title = entry.get("id"), entry.get("title")
        if not isinstance(slug, str) or not SLUG.fullmatch(slug):
            raise ValueError(f"studio.json: invalid production ID {slug!r}")
        if slug in ids:
            raise ValueError(f"studio.json: duplicate production ID {slug}")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"studio.json: missing title for {slug}")
        ids.add(slug)
    active = data.get("active_production")
    if not isinstance(active, str) or active not in ids:
        raise ValueError("studio.json: active_production must name a registered production")
    return data


def maintained_documents(root, entries):
    """Exclude imported notes and optional/generated media from document ownership."""
    paths = set(root.glob("*.md"))
    for folder in ("docs", "band", "tools", ".github", "templates"):
        paths.update((root / folder).rglob("*.md"))
    for entry in entries:
        production = root / "productions" / entry["id"]
        for path in production.rglob("*.md"):
            parts = path.relative_to(production).parts
            if any(part in {"archive", "frames", "previews", "camera_review", "revision4_review"}
                   or part.startswith("Revision_") for part in parts[:-1]):
                continue
            if parts[0] == "notes" and path.name != "README.md":
                continue
            paths.add(path)
    return sorted(paths)


def check_structure(root):
    root = root.resolve()
    data = load_studio(root)
    required = list(REQUIRED_FILES)
    for entry in data["productions"]:
        required.extend(f"productions/{entry['id']}/{name}" for name in PRODUCTION_RECORDS)
    for relative in required:
        path = root / relative
        if not path.is_file() or not path.stat().st_size:
            raise ValueError(f"Missing or empty required file: {relative}")

    registered = {entry["id"] for entry in data["productions"]}
    for path in (root / "productions").iterdir():
        if path.is_dir() and not path.name.startswith(".") and path.name not in registered:
            raise ValueError(f"Unregistered production directory: {path.name}; update studio.json")

    documents = maintained_documents(root, data["productions"])
    links = 0
    for document in documents:
        relative = document.relative_to(root)
        content = document.read_text(encoding="utf-8")
        if relative.parts[0] != "templates" and PLACEHOLDER.search(content):
            raise ValueError(f"Unfilled production template in {relative}")
        for match in LINK.finditer(content):
            target = match.group(1).strip().removeprefix("<").removesuffix(">")
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            destination = (document.parent / unquote(url.path)).resolve()
            if not destination.is_relative_to(root) or not destination.exists():
                raise ValueError(f"Broken/nonportable local link in {relative}: {target}")
            links += 1
    return len(data["productions"]), len(documents), links


def orientation(root):
    data = load_studio(root)
    active = next(entry for entry in data["productions"]
                  if entry["id"] == data["active_production"])
    production = Path("productions") / active["id"]
    print(f"Mercy in Minor studio — {active['title']}")
    print(f"Repository: {root}")
    print(f"Read: {production / 'README.md'}, DECISIONS.md and latest SESSIONS.md")
    print("Session method: docs/SESSION_GUIDE.md; folder ownership: docs/STRUCTURE.md")
    print("\nLocal Git state (live GitHub main has NOT been checked by this command):")
    for args in (("status", "--short", "--branch"), ("log", "-1", "--format=%h %s")):
        result = subprocess.run(["git", "-C", str(root), *args], check=True,
                                text=True, capture_output=True)
        print(result.stdout.strip())
    print("\n" + (root / production / "STATUS.md").read_text(encoding="utf-8").strip())
    print("\nChecks: python3 tools/studio.py --check; python3 tools/review.py --source-only")
    print("Before scene work: python3 tools/studio.py --runtime (Join Me in Life module route)")


def verify_runtime(root):
    python = root / ".venv-bpy" / "bin" / "python"
    if not python.is_file():
        raise ValueError("No .venv-bpy/bin/python; see productions/join-me-in-life/BLENDER.md "
                         "for setup or the official Blender executable route")
    scene = root / "productions/join-me-in-life/current/Join_Me_in_Life_experimental_vert.blend"
    code = """
import sys
from pathlib import Path
import bpy
if sys.version_info[:2] != (3, 13) or bpy.app.version != (5, 2, 3):
    raise RuntimeError('Expected Python 3.13 and bpy 5.2.3 for the original scene')
bpy.ops.wm.open_mainfile(filepath=sys.argv[1], load_ui=False, use_scripts=False)
s = bpy.context.scene
if not (s.camera and (s.render.resolution_x, s.render.resolution_y) == (1080, 1920)
        and s.render.resolution_percentage == 100
        and s.render.fps == 24 and s.render.fps_base == 1
        and (s.frame_start, s.frame_end) == (1, 1439)):
    raise RuntimeError('Original portrait camera, dimensions or timeline differ')
missing = [im.filepath for im in bpy.data.images if im.source == 'MOVIE'
           and not Path(bpy.path.abspath(im.filepath)).is_file()]
if missing:
    raise RuntimeError(f'Missing external movie sources: {missing}')
print(f'Python {sys.version.split()[0]} / bpy {bpy.app.version_string}')
print(f'{s.name}: {s.camera.name}; 1080x1920; 24 fps; frames 1-1439')
print('Scene opened read-only; external movies present; no save or render performed')
"""
    subprocess.run([str(python), "-c", code, str(scene)], check=True, timeout=60)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Validate structure and maintained local links")
    mode.add_argument("--runtime", action="store_true", help="Probe the original Join Me in Life bpy runtime")
    args = parser.parse_args()
    if args.check:
        productions, documents, links = check_structure(ROOT)
        print(f"Studio structure OK: {productions} production(s), {documents} maintained documents, "
              f"{links} local links")
    elif args.runtime:
        verify_runtime(ROOT)
    else:
        orientation(ROOT)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        sys.exit(f"Studio check failed: {exc}")
