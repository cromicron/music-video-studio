# Studio tools

Run commands from the repository root. Source checks use only Python 3.11+ and the standard library; rendering is optional.

| Command | Purpose / side effects |
| --- | --- |
| `python3 tools/studio.py` | Read-only session orientation: registered production, current state, branch, commit and local changes. No network, install or render. |
| `python3 tools/studio.py --check` | Check the registry, production records, local maintained-document links and required workflow/tool paths. No rendering. Enforced by CI. |
| `python3 tools/studio.py --runtime` | Verify the optional `.venv-bpy` runtime and open the original Join Me in Life portrait scene read-only. Requires bpy 5.2.3; does not install, save or render. This is an explicit check for that production, regardless of the active production ID. |
| `python3 tools/review.py --source-only` | Check Join Me in Life's source assets, two contiguous 1,439-frame timelines, saved scenes and cue ordering. Does not render or change source. |
| `python3 tools/review.py` | Check present original hybrid export hashes and AAC, then write a timestamped baseline contact sheet under `build/join-me-in-life/`. Needs FFmpeg/ffprobe/fonts. |
| `python3 tools/review.py --full-decode` | Same baseline check plus decoding all present original hybrid exports end to end. This is not a candidate-export validator. |
| `python3 tools/restore_media.py <downloaded-package-or-directory>` | Restore optional original media with SHA-256 verification. Skips matching files and preserves differing files. See [MEDIA.md](../MEDIA.md). |
| `bash tools/setup-blender-linux.sh` | Reuse production Blender 5.2.3 on PATH or download/checksum/cache the official Linux binary under `build/tools/`; prints its path. Requires allowed access to the download host when absent. |

The prepared `.venv-bpy` module route and its recovery commands are documented in [BLENDER.md](../productions/join-me-in-life/BLENDER.md). [requirements-bpy.txt](requirements-bpy.txt) pins the production module version. Existing `.venv-bpy` and ignored `build/tools/` files are local conveniences, not the only record of setup.

Scripts in [current/](../productions/join-me-in-life/current/) belong to that production and use adjacent data paths. See [their read/write map](../productions/join-me-in-life/current/SOURCES.md) before invoking a builder, caption generator, delivery validator or packager. Some overwrite tracked scenes and baseline reports; only use those intentionally on an appropriate working branch/copy.

The new layout checker has behavior checks under `tests/`: `python3 -m unittest discover -s tests`. These use temporary fixtures and do not need Blender, FFmpeg or network access.
