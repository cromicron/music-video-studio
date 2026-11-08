<!-- Standing instructions: originally copied from jenewmetrics scripts/codex-global/codex-global-AGENTS.md; reconciled with Dario's explicit /workspace instructions on 2026-11-07. The external canonical file was not changed here. -->

# "Do this for me" means: the best result for what it costs

A task from Dario is a request for an outcome. Get it the way a capable person would:

1. **Start from the best result that exists.** Find the best examples of what is wanted and how the people who made them did it: recent posts, videos, write-ups. Your knowledge of techniques is months old, and neither your first idea nor the tools at hand set the approach. What you are after is a way of working, not a product.
2. **Then copy it as cheaply as possible.** Weigh the best route against the cheapest one that comes close, by what each delivers and what it costs, then pick one yourself; do not hand the choice back, even while an input is still missing. What we already pay for costs nothing extra (the Claude and ChatGPT subscriptions with Codex and its image model, the monthly API credit, our machines and cloud accounts), so it wins when it comes close. Pay where paying buys clearly better quality that is worth its price, and not where it does not.
3. **If it will be used many times, make it ours:** our own code, kept and improved, rather than a dependency on someone else's service.
4. **Improve on what exists** instead of starting from zero.

Small, clear jobs (a page, a chart, a function, a text): just do them, without research. On anything bigger, tell Dario early, in a few lines, which route you chose, why, and what it costs, then build. Everything you need from him (a login, a purchase, a go) goes into that one message, each item with the default you will use if he does not answer. Spending money or credits, sending, publishing, or writing into his accounts waits for his go.

When operating apps or websites, prefer APIs, commands, and browser controls that leave Dario's mouse and keyboard free. If desktop control is needed to complete important work, use it; Dario authorizes taking control when necessary. Prefer an equally effective method that lets him keep working.

Getting the necessary tools working is part of the task. Before stopping for a missing capability, inspect what is actually available, set up a supported effective alternative within the authorized scope, and test it; report a concrete unresolved blocker only after those routes fail. Keep reusable setup and recovery instructions with the environment.

When Dario asks you to start work in another Codex chat or cloud environment, carry these standing instructions into its initial prompt. Keep verification prompts unseeded and allow cloud startup to complete before judging automatic instruction-file loading.

**Why:** Dario, 2026-11-04: *"Find out what the best way to do it is, the way others do it. Try to copy that approach as cheaply as possible."* Asked for a cartoon music video, an agent first reached for a paid video app, then generated one image per frame; the established way is one ChatGPT storyboard image with every shot, animated from there. More rules hinder more than they help, so this section is deliberately short.

# Mercy in Minor studio

## Every session

This repository is Dario's Mercy in Minor music-video studio. Its durable working memory is in Git, not in a prior chat. Read [PROJECT_MEMORY.md](PROJECT_MEMORY.md), [README.md](README.md) and [docs/SESSION_GUIDE.md](docs/SESSION_GUIDE.md), then run `python3 tools/studio.py --refresh` from the repository root. Fetching all heads is necessary: useful prior sessions may be unmerged. Inspect relevant branch records before deciding they are superseded. [studio.json](studio.json) identifies the active production; read that production's `README.md`, `STATUS.md`, `DECISIONS.md`, `LESSONS.md` when present, and latest `SESSIONS.md` entry before substantive work. Recover the existing context yourself rather than asking Dario to repeat it.

Compare the checkout with live GitHub main using the sync section below. Preserve local edits and unmerged task commits. Use one focused branch for changes. After meaningful results or corrections, update the owning current record and checkpoint coherent work; do not wait until the end of a long task. At the end, update the production status and session log with actual results, remaining work and where the work is saved. Verify remote persistence with `python3 tools/studio.py --checkpoint` after committing/pushing; a local link check is not proof another task can recover it. [History coverage](docs/HISTORY_INDEX.md) names recovered and missing sources; [Cloud continuity](docs/CLOUD_CONTINUITY.md) distinguishes supported features from local-only memory. Record new decisions separately from proposals and technical checks. Run `python3 tools/studio.py --check` after structural/documentation changes; CI enforces it. [docs/STRUCTURE.md](docs/STRUCTURE.md) defines folder ownership and how to add a production.

Join Me in Life is the first registered production. Its current completed selected C film, source selection, delivery and reviews are in `productions/join-me-in-life/full-film/unfinished-morning/`; read its `DELIVERY.md` and production STATUS before revising it. The parent `full-film/DELIVERY.md` belongs to the historical first hybrid film, not the current C version. `productions/join-me-in-life/current/` remains the preserved Revision 4 Short, not the newer full-film edit. Read that Short's `HANDOFF.txt` before changing its picture, sound or timing. The v2 art selection and eight-second pilot are development references. `experimental` in the Short's scene/script names means Revision 4; `simple` means the restrained Revision 3 comparison. The rules below concern that Short; full-film timing and acceptance are owned by its separate records. Do not copy one song's story or timings into another.

## Working on the preserved Short

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
