# Mercy in Minor studio

## Every session

This repository is Dario's Mercy in Minor music-video studio. Its durable working memory is in Git, not in a prior chat. Read [README.md](README.md) and [docs/SESSION_GUIDE.md](docs/SESSION_GUIDE.md), then run `python3 tools/studio.py` from the repository root. [studio.json](studio.json) identifies the active production; read that production's `README.md`, `STATUS.md`, `DECISIONS.md` and latest `SESSIONS.md` entry before substantive work. Recover the existing context yourself rather than asking Dario to repeat it.

Compare the checkout with live GitHub main using the sync section below. Preserve local edits and unmerged task commits. Use one focused branch for changes. At the end, update the production status and session log with actual results, remaining work and where the work is saved. Record new decisions separately from proposals and technical checks. Run `python3 tools/studio.py --check` after structural/documentation changes; CI enforces it. [docs/STRUCTURE.md](docs/STRUCTURE.md) defines folder ownership and how to add a production.

Join Me in Life is the first registered production. Its active edit is `productions/join-me-in-life/current/`. Read its `HANDOFF.txt` before changing picture, sound or timing. The v2 art selection and eight-second pilot are development references. `experimental` in the scene and script names means the current Revision 4 hybrid. `simple` means the restrained Revision 3 comparison. The rules below concern this existing cut; do not copy its story or timings into an unrelated song.

## Working on an edit

- Start with the tracked portrait export. Identify the precise shot, frame range and the creative request before touching its source. Frames start at 1, at 24 fps. Use the supplied short AAC for this edit. The full-song folder gives the matching point in take 49.
- Edit the hybrid schedule in `camera_shots_experimental.json`. Change drawing exposures in `native_animation.py`. Caption text/timing is generated from `finish.py`. `current/README.txt` explains the logo composite. Store shared band material in `band/` and give each new song its own directory under `productions/`.
- For new art, use A01/A02 for identity and the drawn treatment. Keep backgrounds as graphic as the characters. Check shoulders and head-to-torso alignment, Jaro’s light facial hair, the present-day wardrobe and the summer wardrobe. A03 is a reference for her expression. Compare against the specific shot in the current cut.
- Keep the hospital scene emotionally unresolved. He is frightened and stays beside her. She looks away during the one embrace. Let the warmth of the summer memory carry the contrast. Preserve the logo fade, the rounded vowel through frame 339, and continuous waiting-room camera work unless the requested edit changes them.
- Use existing art, performances and local rendering by default. For a new paid generation, give the specific shot, why it needs generation and the expected cost before committing credits.
- Use a branch for a focused change. Render the affected range before a full export. In the PR record the frames, what changed, how to reproduce it, and a viewable before/after at normal speed for timing or camera changes. Inspect source joins, caption placement, face acting and audio sync. Keep the original baseline and its validation records available for comparison. A new accepted cut gets its own identifying tag and review reference.
- Run `python3 tools/review.py --source-only` after editing project data. The default review command verifies the original Revision 4 baseline. Read `productions/join-me-in-life/BLENDER.md` for native scene and candidate-render checks. Report which tests ran, including actual playback or Blender versions when relevant.
- Keep the production's original scripts, `.blend` scenes and adjacent `assets/` paths stable. `current/SOURCES.md` separates editable inputs, generated derivatives and baseline evidence. Preserve historical handoffs and validation records; place current state in `STATUS.md`, direction/evidence in `DECISIONS.md`, and continuation notes in `SESSIONS.md`.
- Check the prepared `.venv-bpy/bin/python` before choosing a system Blender or installing anything. `python3 tools/studio.py --runtime` verifies the local bpy 5.2.3 scene-opening route; `BLENDER.md` documents recovery if that environment is absent. Never replace a working runtime merely to match an old absolute path in a historical handoff.

## Sync a saved Codex checkout

At the start of a task, compare `git rev-parse HEAD` with GitHub’s current `main` SHA. Prefer an ordinary Git fetch. When the shell cannot reach GitHub, the connected GitHub tools can transfer an update without shell HTTP.

1. Get GitHub’s `main` and `codex-sync` branch heads. Read `manifest.json` at that exact **codex-sync commit SHA** with `github_fetch_file` (`repository_full_name="cromicron/music-video-studio"`, `encoding="utf-8"`). Check that `schema` is `studio-codex-sync/v1` and `main_sha` equals GitHub’s independent `main` SHA. If the mirror is behind, wait for that main commit’s **Production source check**.
2. At the same pinned sync commit, use `github_fetch_file` for each path in `parts`. Transfer each returned UTF-8 `content` directly into a temporary file through the tool runner. Decode each part as base64 and concatenate its bytes **in manifest order**. Verify the bundle’s byte count and SHA-256 against `size` and `sha256`. A mismatch aborts the sync. The generated branch is an agent-readable transport for bundles up to 4 MiB.
3. If `parts` is empty, get the larger **studio-main-update** artifact for `run_id` with `github_download_workflow_artifact`, materialize the returned file, and verify the ZIP against GitHub’s published artifact digest before extracting `studio-main-update.bundle`. The bundle needs the original `join-me-in-life-r4` baseline.

Set `bundle` to the verified bundle path and `expected_sha` to the full SHA independently reported by GitHub for `main`. Run this from the task's clean checkout:

```sh
(
  set -eu
  test -z "$(git status --porcelain)"
  git bundle verify "$bundle"
  git fetch "$bundle" refs/heads/studio-sync
  test "$(git rev-parse FETCH_HEAD)" = "$expected_sha"
  git merge-base --is-ancestor HEAD FETCH_HEAD
  git merge --ff-only FETCH_HEAD
  test "$(git rev-parse HEAD)" = "$expected_sha"
)
```

If the checkout contains edits or its history has diverged, preserve it. Start a separate worktree from the verified `FETCH_HEAD` for work on current `main`; fetch and verify the target first if the cleanliness check stopped the block.
