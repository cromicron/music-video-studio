# Starting and handing over a studio session

The repository is the working memory for Mercy in Minor's music-video studio. A new chat does not inherit previous conversations, local caches, or a prepared Python environment. Keep the information needed to continue in the files below.

## Start

1. Open the repository root and read [AGENTS.md](../AGENTS.md). If the shell starts in `/workspace`, the restored repository is currently `/workspace/music-video-studio`; find the Git root rather than assuming `/workspace` is the repository.
2. Read [PROJECT_MEMORY.md](../PROJECT_MEMORY.md), then run `python3 tools/studio.py --refresh`. It fetches remote branch heads without changing your work and prints the active production's current state, the branch/commit, local changes, and where to continue. Without `--refresh`, it uses cached Git refs. Neither mode installs, renders, merges or resets. Inspect relevant unmerged branch records, using the exact SHA/path commands it prints.
3. Compare HEAD with current GitHub main using the [saved-checkout sync procedure](../AGENTS.md#sync-a-saved-codex-checkout). Preserve local edits and commits. Sync only by a verified fast-forward; if the task branch contains work beyond main, report that relationship and continue there. Never reset it to main to make a status check pass.
4. Read the active production's `README.md`, `STATUS.md`, `DECISIONS.md`, `LESSONS.md` when present, and latest `SESSIONS.md` entry. [HISTORY_INDEX](HISTORY_INDEX.md) maps recovered branches and explicit gaps. `studio.json` identifies the active production. Read `current/HANDOFF.txt` and `BLENDER.md` before changing an existing cut, then inspect the actual requested shot or export.
5. Run `python3 tools/studio.py --check` and `python3 tools/review.py --source-only`. The second command currently checks **Join Me in Life**, regardless of which production is active. For native scene work, also run `python3 tools/studio.py --runtime` and follow the production render guide.
6. Continue the user's current request. A fresh session or a vague “continue” is not a reason to invent a new edit, regenerate assets, or restart a completed pilot. If no creative task is recorded, give the current state and ask only for the missing creative direction.

## While working

- Use one focused task branch. Keep media beside the scripts and scenes that reference it. The [repository map](STRUCTURE.md) explains what is editable, generated, historical, or shared.
- Record a new confirmed direction in the production's `DECISIONS.md`, including its scope and source. Mark proposals and technical findings as such. A successful render or automated review does not establish Dario's creative approval.
- After a meaningful result, user correction, failed hypothesis or access change, reconcile the owning records and checkpoint coherent work. Do not depend on a local SessionEnd hook or wait until the final answer. Add lessons with evidence and changed next hypothesis, rather than another competing summary.
- Maintain `STATUS.md` when the active cut, task, blocker, available result, or next step changes. Replace stale present-tense statements there; preserve past events in `SESSIONS.md`.
- Store scratch under `work/`, reproducible checks under `build/`, and render output at the script's documented destination. Link reviewable results from the session record; temporary artifacts need a durable reference if the next session must use them.
- The archived handoffs, manifests, and baseline validation records retain their provenance. Add current interpretation in the maintained documents rather than rewriting history or replacing baseline hashes with candidate results.

## Before finishing

1. Run the layout/document check and the relevant production checks. Record the actual commands and results, including what was not reviewed. Timing, performance, and camera changes need playback with sound as well as source/frame checks.
2. Update `STATUS.md` with what exists now, unresolved items, and the exact next action. Add to `DECISIONS.md` only if a decision or a material constraint changed.
3. Prepend a dated entry to `SESSIONS.md` using the format below. Use the user's Europe/Berlin date. Link the source, review artifacts, and any PR. Git history identifies the final commit; do not write a commit's own hash into itself.
4. Inspect `git diff --check`, the diff, and `git status`. After the intended work is committed and pushed, run `python3 tools/studio.py --checkpoint`: it compares the live upstream SHA and validates a cold committed archive. This is separate from structure checks and from a real fresh-cloud behavior test. Keep task changes on the task branch. To survive a fresh clone, the documents and source must be committed and pushed, and merged to main if new sessions start from main. A local edit, ignored file, or chat message alone does not update GitHub. State clearly where the work is saved; do not claim that main contains an unmerged change.

```md
## YYYY-MM-DD — task name

- Request: what Dario asked for.
- Branch/base: branch and starting commit or PR.
- Result: implemented change and paths to source/review outputs.
- Decisions: links to new decisions, or none.
- Verification: commands/results; playback and runtime if relevant.
- Remaining: blockers, unreviewed work, and the next concrete action.
- Persistence: local branch, pushed branch/PR, or merged main.
```

Current Cloud behavior and the researched verification plan are in [CLOUD_CONTINUITY](CLOUD_CONTINUITY.md). Never call a child-agent or local-archive test a new cloud VM test.

For a new song, follow [Add a production](STRUCTURE.md#add-a-production). New sessions should be able to recover the current work from these records without Dario repeating the history.
