# Independent continuity audit

Checked **2026-11-07 UTC** against the working repository, live Git remote and current primary documentation. This audit changed no existing project files, created no external records and spent no money. Findings describe the checkout at inspection time; another agent may subsequently repair them.

## Finding and choice

**Keep the existing repository-backed memory design; make persistence and recovery verifiable.** It already resembles the strongest published agent-harness patterns. The immediate failure is that a comprehensive handoff can remain uncommitted, while both the working tree and an obsolete committed snapshot pass the same check. Adding a memory product would not fix that.

Recommended incremental cost: **€0 in new services**. Use Git, the existing Python checker, small structured continuation fields and existing private artifact storage. A fresh Codex task used for acceptance consumes the existing plan allowance. Do not promise zero usage cost or automatic cross-task recovery from chat history.

## Observed evidence

| Observation | Consequence |
|---|---|
| Local HEAD and independently read live `main` were `dead4f4b545f13aa2776e539cfe439d047e7df83`. `git ls-remote` returned no `feat/join-me-in-life-complete-video` remote branch. | The full-film task had no remotely discoverable branch checkpoint at inspection time. |
| `full-film/` and `.agents/` were untracked; STATUS, DECISIONS and SESSIONS were modified. | A new clone could not recover the current work or installed skill from Git. |
| Working tree: `studio.py --check` passed, 45 documents/236 links. All seven unit tests and original source-only checks passed. | Tests cover structure and the original Short, not whether the current task is durably recoverable. |
| An isolated `git archive HEAD` snapshot also passed: 23 documents/135 links. It contained no `full-film/`, no Be Ambitious and no current full-film request in STATUS. | **Reproduced failure:** “checks passed” can coexist with complete loss of this task in a fresh checkout. |
| README still describes the full song as later development. The newest session entry and ACCESS_SETUP contain old pending-verification statements below later successful updates; DECISIONS includes stale setup state. | Multiple valid-looking present-tense summaries can make an agent redo setup or choose a superseded next action. |
| Review/render Actions artifacts expire after seven days; the main-sync bundle artifact after 30 days. | Workflow success and artifact URLs alone do not provide durable media recovery. |

Good existing design: a short entry path through AGENTS and `studio.json`; separate STATUS, DECISIONS and SESSIONS; explicit candidate-versus-approval distinctions; safe fast-forward rules; hash-verified connector bundle transport; stable original media paths. Preserve those choices.

Code reviewed: [studio.py](../../tools/studio.py), [tests](../../tests/test_studio.py), [source CI](../../.github/workflows/source-check.yml), [session guide](../SESSION_GUIDE.md), [structure](../STRUCTURE.md). `check_structure()` checks nonempty required files, registry consistency, template placeholders and local link existence. It does **not** check tracking, commit inclusion, remote availability, current task coverage, stale statements, artifact recovery, authorization provenance or meaningful acceptance criteria. `orientation()` correctly warns that it has not checked live main. Do not mislabel these current functions as broken; their scope is simply narrower than a continuity guarantee.

## Primary patterns worth copying

All sources below were retrieved on the audit date; living documentation may change.

| Pattern and source | What to adopt here | Boundary |
|---|---|---|
| OpenAI, [Harness engineering](https://openai.com/index/harness-engineering/), **11 February 2026** | Short AGENTS as an index; repository documents as the record; mechanical checks and ongoing correction of stale material. | A large instruction manual is not reliable memory. The article reports engineering experience, not a platform persistence guarantee. |
| OpenAI, [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex), **23 February 2026** | Explicit outcome/constraints, milestone acceptance criteria, operating runbook, continuously updated status/decisions and verification. Existing studio files can serve these roles. | A successful 25-hour experiment does not establish cross-task filesystem recovery. |
| Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents), **26 November 2025** | Startup reads progress and Git history, checks a basic working baseline, advances one bounded milestone and records a clean checkpoint. | Compaction alone is insufficient; a feature must not be marked done only because code or unit tests exist. Transfer the workflow, not the Claude SDK dependency. |
| Cline, [Memory Bank](https://docs.cline.bot/best-practices/memory-bank), living documentation | Separate stable brief, active context, technical context and progress. | It is a Markdown methodology, not a paid database or automatic sync service. We already have equivalent files; six additional duplicate summaries would increase drift. |
| Anthropic, [Claude project memory](https://code.claude.com/docs/en/memory), living documentation | Small index plus topic files; version-controlled project instructions. | Its auto-memory directory is machine-local, shared across local worktrees but **not** across machines/cloud environments. Claude-specific auto-loading, hooks and settings are not Codex Cloud features. |
| [Beads](https://github.com/gastownhall/beads), inspected commit `8c3eb30f30f7fbb509d80cd12cb13e54bdbbb45d` | Dependency-aware tasks, explicit claims, durable facts and provenance become useful with many concurrent workers. | Current Beads uses **Dolt** as source of truth. Ordinary Git commits of `.beads/issues.jsonl` are not its canonical sync. Fresh clones need bootstrap and Dolt history under a separate `refs/dolt/data` ref. `bd setup codex` documents Codex **CLI** integration, not a verified Codex Cloud installation. |

Beads is capable, but brings a binary, database/schema lifecycle, separate sync semantics and another recovery test. Our current `codex-sync` bundle would not include its Dolt ref. For one active production, the cheapest close alternative is also the best immediate choice: improve the existing documents and checker. Revisit a task graph only when parallel task coordination exceeds a small explicit queue. No Beads code was executed or installed during this audit.

## Codex Cloud compatibility

Current [Codex Cloud help](https://help.openai.com/en/articles/20001545-using-codex-cloud) explicitly distinguishes the original task from a new task: new tasks have separate workspaces and do not recover another task's uncommitted changes. It states a default saved-VM recovery window of **up to seven days after the last turn start/task resume**. That is not conversation retention or a backup contract.

The current [environment guide](https://learn.chatgpt.com/docs/environments/cloud-environments) describes reusable published files, install instructions and a start skill. Existing tasks retain their own state; republishing affects new tasks. Repository refresh runs in the background without rerunning installation/startup. Thus prepare dependencies in the environment, but keep task truth in remote source control and verify the checkout at startup. Do not assume a published setup captures later task changes or that every new dependency appears merely because Git refreshed. Legacy Cloud is separately documented; test the actual selected environment rather than importing old setup-script assumptions.

[Codex Goals](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex) are thread-scoped durable state, not global/project memory. [Agents SDK sandbox memory](https://developers.openai.com/api/docs/guides/agents/sandboxes) is an API capability with its own configuration; it is not evidence that this ChatGPT Codex Cloud task automatically has that store. Do not add an API-billed custom harness just to preserve a few repository records.

## Minimum reliable recovery contract

1. **Checkpoint the actual work.** Include source, current task/constraints, evidence and necessary small assets in a reviewed commit. Put large required media in durable private storage with hashes and a tested retrieval command. Record what is reconstructible versus irreplaceable. Verify the remote branch's exact commit after an authorized push; a local commit is not a cloud backup.
2. **Make the continuation discoverable.** Integrate a valid checkpoint into the default branch, or place a durable pointer there to the exact unmerged branch/commit and its task. New sessions starting from main cannot infer an unknown branch. Never relabel unmerged work as main, reset a dirty checkout or force-push over another session.
3. **Have one current view.** STATUS holds objective, active milestone, next action, blocker, latest evidence and unresolved decisions. Keep dated historical facts in SESSIONS. Replace contradictory current claims instead of piling follow-up paragraphs onto them. Mark external quota/login observations with a timestamp and a read-only recheck command; do not ask Dario to repeat successful setup without testing access first.
4. **Separate kinds of evidence.** Record implementation, technical validation, motion review and user acceptance independently. A user approval needs scope, source/date and relevant limits; summaries, tool success and another agent's claim cannot enlarge it. Preserve the withdrawn Runway proposal as withdrawn. Persist spending limits and permissions faithfully, without treating either the existence of a connector or a remembered budget as permission to spend.
5. **Add a distinct checkpoint check.** Keep structural checks usable during ordinary dirty work. A separate handoff/remote check should verify that required continuation paths and artifact manifests are in the intended commit, report local-only changes, confirm the remote SHA and expose unmerged work. Missing credentials/network should produce “remote persistence unverified,” not success or invented authorization.
6. **Control concurrent changes with Git.** Give independent tasks separate branches/worktrees and a named owner/base revision. Serialize integration of STATUS; preserve per-session evidence. A rejected non-fast-forward push requires reconciliation. A local lock file in one isolated cloud VM does not coordinate another VM. Avoid adding a lock service for a single active root task.

These are small additions to the current architecture, not a proposal for another sprawling memory directory. For future test coverage, prioritize missing/untracked continuation evidence, stale remote checkpoints, lost artifact recovery and false acceptance over tests that merely assert field names.

## Acceptance test before claiming success

After the checkpoint is durable, start a **genuinely fresh Codex Cloud task** from the selected published environment, wait for startup to finish, and give an unseeded request such as “Continue the active studio work.” Do not paste the expected filenames, current decision or hidden answer into that prompt.

It passes only if the fresh task independently finds the correct production and checkpoint; explains the actual outstanding milestone; preserves the four bridge pleas and withdrawn spending proposal; identifies the animatic as unfinished; retrieves a required source/review artifact and verifies its hash; checks existing provider access without unnecessary signup; and proposes the correct next bounded action. Also test an unmerged branch and a missing cache. Report what was actually recovered, not only that the docs parsed.

This audit performed a clean **committed-file snapshot** test, not the final fresh-cloud acceptance test. The observed snapshot failed task recovery while passing structural validation. That is the concrete gap to close.
