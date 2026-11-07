"""Orient studio sessions and verify layout or remotely saved checkpoints."""

import argparse
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_RECORDS = ("README.md", "STATUS.md", "DECISIONS.md", "SESSIONS.md")
REQUIRED_FILES = (
    "README.md", "AGENTS.md", "PROJECT_MEMORY.md", "MEDIA.md", "studio.json",
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


def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], text=True,
                            capture_output=True, timeout=60)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"git {' '.join(args)} failed: {detail or result.returncode}")
    return result.stdout.strip()


def refresh(root):
    """Update remote-tracking refs only; preserve local branches and working files."""
    git(root, "fetch", "--prune", "--no-tags", "origin",
        "+refs/heads/*:refs/remotes/origin/*")


def branch_awareness(root, production):
    """Describe fetched alternatives without selecting or merging one."""
    refs = git(root, "for-each-ref", "--format=%(refname:short) %(objectname) %(symref)",
               "refs/remotes/origin/")
    heads = {}
    for line in refs.splitlines():
        fields = line.split()
        if len(fields) == 2 and fields[0] != "origin/codex-sync":
            heads[fields[0]] = fields[1]
    print("\nFetched origin branches (cached; use --refresh to update):")
    if not heads:
        print("None available. Remote persistence is unverified.")
        return
    if git(root, "rev-parse", "--is-shallow-repository") == "true":
        print("History is shallow; merge relationships describe only the fetched history.")
    main = heads.get("origin/main")
    if not main:
        print("origin/main is missing; merged/unmerged relationships are unverified.")
    scope = ("AGENTS.md", "PROJECT_MEMORY.md", "studio.json", "docs/", str(production))
    for name, sha in sorted(heads.items()):
        label = ""
        relevant = False
        if main and name != "origin/main":
            merged = subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor",
                                     sha, main], capture_output=True, text=True)
            if merged.returncode not in (0, 1):
                raise ValueError(f"Cannot compare {name} with origin/main: {merged.stderr.strip()}")
            if merged.returncode == 1:
                # Compare trees, not a guessed current branch; also supports unrelated histories.
                relevant = bool(git(root, "diff", "--name-only", main, sha, "--", *scope))
                label = " — unmerged; active-production/continuity differences" if relevant else " — unmerged"
            else:
                label = " — included in origin/main"
        print(f"{name} {sha}{label}")
        if relevant:
            for path in ("PROJECT_MEMORY.md", f"{production}/STATUS.md", f"{production}/SESSIONS.md"):
                if git(root, "ls-tree", "--name-only", sha, "--", path):
                    print(f"  Read exact record: git show {sha}:{path}")


def checkpoint(root):
    """Verify committed recovery records and the live configured upstream, without writes."""
    if git(root, "status", "--porcelain", "--untracked-files=all"):
        raise ValueError("Checkpoint not durable: tracked edits or untracked files remain; "
                         "review and commit the intended work first")
    head = git(root, "rev-parse", "HEAD")
    branch = git(root, "rev-parse", "--abbrev-ref", "HEAD")
    if branch == "HEAD":
        raise ValueError("Checkpoint unverified: detached HEAD has no branch upstream")
    # Cloud checkouts may fetch only main. Git's %(upstream) then stays empty for a
    # successfully pushed task branch, even with correct branch remote/merge config.
    # Read that explicit config and verify its live ref instead of trusting a cache.
    values = []
    for key in ("remote", "merge"):
        result = subprocess.run(["git", "-C", str(root), "config", "--get-all",
                                 f"branch.{branch}.{key}"], text=True,
                                capture_output=True, timeout=10)
        if result.returncode not in (0, 1):
            raise ValueError(f"Cannot read branch upstream: {result.stderr.strip()}")
        entries = result.stdout.splitlines()
        values.append(entries[0] if len(entries) == 1 else "")
    remote, ref = values
    if not remote or remote == "." or not ref.startswith("refs/heads/"):
        raise ValueError("Checkpoint unverified: configure a remote branch upstream; "
                         "a local branch alone is not durable")
    with tempfile.TemporaryDirectory(prefix="studio-checkpoint-") as directory:
        archive = Path(directory) / "committed.tar"
        cold = Path(directory) / "checkout"
        cold.mkdir()
        git(root, "archive", "--format=tar", f"--output={archive}", head)
        with tarfile.open(archive) as source:
            source.extractall(cold, filter="data")
        # Ignore rules and export attributes must not conceal required continuation files.
        counts = check_structure(cold)
    live = git(root, "ls-remote", "--exit-code", remote, ref)
    matches = [line.split()[0] for line in live.splitlines() if line.split()[1] == ref]
    if matches != [head]:
        raise ValueError(f"Checkpoint not durable at the intended upstream: HEAD {head}; "
                         f"live {remote}/{ref} is {', '.join(matches) or 'missing'}")
    print(f"Checkpoint verified: {branch} {head} equals live {remote}/{ref}")
    print(f"Cold committed archive: {counts[0]} production(s), {counts[1]} documents, {counts[2]} links")
    print("This verifies branch recovery, not merge into main, provider credentials, "
          "external media retention or creative approval.")


def orientation(root, refreshed=False):
    data = load_studio(root)
    active = next(entry for entry in data["productions"]
                  if entry["id"] == data["active_production"])
    production = Path("productions") / active["id"]
    print(f"Mercy in Minor studio — {active['title']}")
    print(f"Repository: {root}")
    print("\n" + (root / "PROJECT_MEMORY.md").read_text(encoding="utf-8").strip())
    print(f"Read: {production / 'README.md'}, DECISIONS.md and latest SESSIONS.md")
    print("Session method: docs/SESSION_GUIDE.md; folder ownership: docs/STRUCTURE.md")
    print("\nLocal Git state (origin heads fetched this run):" if refreshed else
          "\nLocal Git state (cached refs; live GitHub has NOT been checked):")
    for args in (("status", "--short", "--branch", "--untracked-files=all"),
                 ("log", "-1", "--format=%h %s")):
        print(git(root, *args))
    branch_awareness(root, production)
    print("\n" + (root / production / "STATUS.md").read_text(encoding="utf-8").strip())
    print("\nChecks: python3 tools/studio.py --check; python3 tools/review.py --source-only")
    print("Before handoff: python3 tools/studio.py --checkpoint (requires committed, pushed work)")
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
    mode.add_argument("--refresh", action="store_true", help="Fetch origin heads without merging, then orient")
    mode.add_argument("--checkpoint", action="store_true", help="Verify clean committed records and live upstream")
    mode.add_argument("--runtime", action="store_true", help="Probe the original Join Me in Life bpy runtime")
    args = parser.parse_args()
    if args.check:
        productions, documents, links = check_structure(ROOT)
        print(f"Studio structure OK: {productions} production(s), {documents} maintained documents, "
              f"{links} local links")
    elif args.runtime:
        verify_runtime(ROOT)
    elif args.checkpoint:
        checkpoint(ROOT)
    else:
        if args.refresh:
            refresh(ROOT)
        orientation(ROOT, refreshed=args.refresh)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        sys.exit(f"Studio check failed: {exc}")
