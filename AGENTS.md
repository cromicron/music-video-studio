# Mercy in Minor studio

The active edit is `productions/join-me-in-life/current/`. Read its `HANDOFF.txt` before changing picture, sound or timing. The v2 art selection and eight-second pilot are development references. `experimental` in the scene and script names means the current Revision 4 hybrid. `simple` means the restrained Revision 3 comparison.

## Working on an edit

- Start with the tracked portrait export. Identify the precise shot, frame range and the creative request before touching its source. Frames start at 1, at 24 fps. Use the supplied short AAC for this edit. The full-song folder gives the matching point in take 49.
- Edit the hybrid schedule in `camera_shots_experimental.json`. Change drawing exposures in `native_animation.py`. Caption text/timing is generated from `finish.py`. `current/README.txt` explains the logo composite. Store shared band material in `band/` and give each new song its own directory under `productions/`.
- For new art, use A01/A02 for identity and the drawn treatment. Keep backgrounds as graphic as the characters. Check shoulders and head-to-torso alignment, Jaro’s light facial hair, the present-day wardrobe and the summer wardrobe. A03 is a reference for her expression. Compare against the specific shot in the current cut.
- Keep the hospital scene emotionally unresolved. He is frightened and stays beside her. She looks away during the one embrace. Let the warmth of the summer memory carry the contrast. Preserve the logo fade, the rounded vowel through frame 339, and continuous waiting-room camera work unless the requested edit changes them.
- Use existing art, performances and local rendering by default. For a new paid generation, give the specific shot, why it needs generation and the expected cost before committing credits.
- Use a branch for a focused change. Render the affected range before a full export. In the PR record the frames, what changed, how to reproduce it, and a viewable before/after at normal speed for timing or camera changes. Inspect source joins, caption placement, face acting and audio sync. Keep the original baseline and its validation records available for comparison. A new accepted cut gets its own identifying tag and review reference.
- Run `python3 tools/review.py --source-only` after editing project data. The default review command verifies the original Revision 4 baseline. Read `productions/join-me-in-life/BLENDER.md` for native scene and candidate-render checks. Report which tests ran, including actual playback or Blender versions when relevant.

## Sync a saved Codex checkout

At the start of a task, compare `git rev-parse HEAD` with the GitHub `main` SHA. Prefer an ordinary Git fetch. If this shell cannot authenticate, use the connected GitHub account to find the successful **Production source check** run at the exact target SHA. Download its **studio-main-update** artifact with `github_download_workflow_artifact`, verify the ZIP against the artifact's published SHA-256, and extract `studio-main-update.bundle` to a temporary directory. Rerun the source check on `main` if its artifact has expired. The bundle requires the original `join-me-in-life-r4` baseline in the checkout.

Set `bundle` to the extracted file path and `expected_sha` to the full SHA independently reported by GitHub for `main`. Run this from the task's clean checkout:

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
