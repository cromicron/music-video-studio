# Studio tools

Run commands from the repository root. Source checks use only Python 3.11+ and the standard library; rendering is optional.

| Command | Purpose / side effects |
| --- | --- |
| `python3 tools/studio.py` | Read-only session orientation: PROJECT_MEMORY, registered production, current state, branch, commit, local changes and fetched origin branches. Unmerged production work includes exact commit/path read commands. No network, install or render. |
| `python3 tools/studio.py --check` | Check the registry, production records, local maintained-document links and required workflow/tool paths. No rendering. Enforced by CI. |
| `python3 tools/studio.py --refresh` | Fetch all origin branch heads into remote-tracking refs, remove stale remote-tracking refs, then orient. Requires remote read access. Does not merge, reset, switch branches or select another task; preserves local changes. Excludes generated `codex-sync` from the branch overview. |
| `python3 tools/studio.py --checkpoint` | Require a clean committed checkout and configured remote upstream; check structure/links in a temporary archive of HEAD; compare HEAD with the live upstream branch SHA. Requires remote read access. Changes only temporary files, not source or Git refs. Does not commit, push or claim the branch is merged. |
| `python3 tools/studio.py --runtime` | Verify the optional `.venv-bpy` runtime and open the original Join Me in Life portrait scene read-only. Requires bpy 5.2.3; does not install, save or render. This is an explicit check for that production, regardless of the active production ID. |
| `python3 tools/review.py --source-only` | Check Join Me in Life's source assets, two contiguous 1,439-frame timelines, saved scenes and cue ordering. Does not render or change source. |
| `python3 tools/review.py` | Check present original hybrid export hashes and AAC, then write a timestamped baseline contact sheet under `build/join-me-in-life/`. Needs FFmpeg/ffprobe/fonts. |
| `python3 tools/review.py --full-decode` | Same baseline check plus decoding all present original hybrid exports end to end. This is not a candidate-export validator. |
| `python3 tools/restore_media.py <downloaded-package-or-directory>` | Restore optional original media with SHA-256 verification. Skips matching files and preserves differing files. See [MEDIA.md](../MEDIA.md). |
| `bash tools/setup-blender-linux.sh` | Reuse production Blender 5.2.3 on PATH or download/checksum/cache the official Linux binary under `build/tools/`; prints its path. Requires allowed access to the download host when absent. |

The prepared `.venv-bpy` module route and its recovery commands are documented in [BLENDER.md](../productions/join-me-in-life/BLENDER.md). [requirements-bpy.txt](requirements-bpy.txt) pins the production module version. Existing `.venv-bpy` and ignored `build/tools/` files are local conveniences, not the only record of setup.

Scripts in [current/](../productions/join-me-in-life/current/) belong to that production and use adjacent data paths. See [their read/write map](../productions/join-me-in-life/current/SOURCES.md) before invoking a builder, caption generator, delivery validator or packager. Some overwrite tracked scenes and baseline reports; only use those intentionally on an appropriate working branch/copy.

The new layout checker has behavior checks under `tests/`: `python3 -m unittest discover -s tests`. These use temporary fixtures and do not need Blender, FFmpeg or network access.

Run `--check` freely during work; it intentionally permits dirty files and does not prove persistence. Before a handoff, commit and push the intended source/evidence under the user's authorization, then run `--checkpoint`. Its cold archive catches links that work only because ignored files remain in the current task. Missing upstreams, network failures and remote SHA mismatches fail visibly. A success verifies recovery of that branch's committed records; it does not establish merge into main, recovery of external media or credentials, or creative approval. Keep a discoverable continuation pointer when the current task is on an unmerged branch.

Fetched branches can be stale until `--refresh` succeeds. The overview exposes alternate records without choosing them: read the listed exact-SHA STATUS and session record, reconcile their scope with the current request, and preserve the working branch. Separate cloud tasks do not share local uncommitted files. The continuity tests use real temporary Git remotes to exercise unseen branches, unpublished commits, remote advances, dirty work and ignored evidence missing from the committed archive.
