# Continuous project memory in Codex Cloud

Research and implementation date: **7 November 2026**. The goal is a new session that can recover the work and improve it without Dario retelling the history. The original film remains the production goal; continuity is the immediate prerequisite.

## Chosen approach and cost

Use the private Git repository as the durable project record, with a small automatically discovered `AGENTS.md` entry map, maintained current facts, linked evidence and an explicit checkpoint/recovery test. Reuse the existing STATUS / DECISIONS / SESSIONS structure. Add lessons and branch coverage where this project demonstrably lost information. No new subscription, memory database, paid API or always-on service is needed.

This adapts OpenAI's demonstrated repository-knowledge approach [1], rather than inventing a new memory product. It is selective retrieval plus regular consolidation: read the small map, retrieve the relevant source, reconcile corrections, persist the result, verify another reader can recover it. Automatic personal recall can supplement this, but required project facts must remain inspectable and versioned [2].

## What the current product actually supports

| Capability | Verified documentation / implication here |
| --- | --- |
| Reusable current Cloud environment | A new task gets an **isolated workspace from the published environment**. An existing task retains its own saved files and tools. Background repository refresh preserves caches; it does not rerun installation/start commands. “Saved state doesn't replace source control.” Default task VM recovery is up to seven days after the last turn/resume. [3] |
| Install script and Start skill | Supported fields in the environment's setup flow. Saving configuration and publishing a prepared filesystem are separate operations. Republish changes the setup for new tasks; existing tasks retain their state. A file added here is not evidence that the environment's Start skill was configured or republished. [3] |
| `AGENTS.md` discovery | Codex reads instructions at run start, layering global and project files down to its working directory. An override can replace the file in that directory; the default combined cap is 32 KiB. Keep this a short map, and test actual discovery. Starting in `/workspace` is not the same as starting in the nested Git root. [4] |
| Local Codex memories | Local CLI/desktop/IDE host memory is a separate generated store, normally under `~/.codex/memories`. It is background/idle generated, may skip some chats and quota-limited passes, and is off by default. ChatGPT web/Work uses its own available memory settings. Copying a local feature flag is not a verified cloud memory solution. [2] |
| Local session hooks | Current hooks documentation does **not** make repository shell SessionStart/SessionEnd hooks a reliable personal-cloud solution. Enterprise cloud orchestration has a restricted admin-managed MCP hook path; personal accounts/Work Cloud without local access do not use those enterprise hooks. No untrusted or bypassed hooks were installed. [5] |
| Projects and Sources | Shared project files, instructions and sources help related chats; each chat retains its own transcript. Pinning affects visibility, not context access. A project is not proof that every transcript has been read. [6] |
| Legacy Codex Cloud | Old setup/maintenance scripts and a twelve-hour container cache belong to the explicitly labelled **Legacy** guide. They are not the lifecycle description used for this current environment. [7] |
| Other always-on agents or memory services | Can offer proactive work or recall, but would add a separate product/control surface. Not needed to recover this repository, and not evidence of access to all old chats. No new service was installed. |

The week-of-November-2–6 release note was also checked [8]. Pages without publication dates are cited as **accessed 7 November**, not assigned invented release dates. Search metadata sometimes differs from the visible article date; the visible date is used for dated articles.

## The observed failure and its repair

Before this change, seven structure tests passed. Yet an independent `git archive HEAD` cold checkout lacked `full-film/`, Be Ambitious and the current task in STATUS. The dirty live workspace also passed its document check. Both results were correct for the narrow check; neither proved continuity.

Fetching all remote heads exposed three additional unmerged work streams, including PR #2's six commits and a prior full-length production-method investigation. They were absent from main. Current documents also contradicted completed Kaggle verification and finished CPU benchmarks. See [history coverage](HISTORY_INDEX.md) and the [independent audit](research/continuity-independent-audit.md).

The repair has four parts:

1. **Load:** `AGENTS.md` points to [PROJECT_MEMORY](../PROJECT_MEMORY.md); the orientation command prints the map and current state. The agent reads decision/lesson/source detail before dependent work.
2. **Discover:** `studio.py --refresh` fetches all origin heads and exposes relevant unmerged records, without changing the working branch. A branch's evidence is reconciled, never automatically treated as approval or merged wholesale.
3. **Consolidate:** update the owning current-state record during work; put durable corrections in DECISIONS, failed hypotheses in LESSONS, provenance in HISTORY_INDEX, and the dated result in SESSIONS. Preserve raw imported history. Use scoped facts with sources, not a growing all-purpose transcript dump.
4. **Persist and verify:** commit coherent work, push its authorized branch, compare live remote SHA with HEAD, and check a cold archive. A fresh reader must recover the task, constraints, failed routes, completed setup and next action with no answer cues.

Concurrent sessions should use separate task branches, fetch each other's saved work, and reconcile it through review. Do not overwrite STATUS blindly or use last timestamp wins. Checkpoints should happen after a meaningful result/correction, not only at the very end when interruption can lose the thread.

## Startup and recovery

The normal repository-root command is:

```sh
python3 tools/studio.py --refresh
```

Use ordinary Git fetch first. If Git networking fails, inspect the [connector sync fallback](../AGENTS.md#sync-a-saved-codex-checkout) and verify that its pinned manifest matches live main. On 9 November the optional mirror became stale after cumulative Actions bundles exhausted artifact quota; [transport evidence and limits](CONNECTOR_SYNC_LIMITS.md) distinguish this from the passing source checks and tested primary Git recovery. Do not wait indefinitely for an already failed upload or accept an old manifest as current. The transport mirrors main only; discover additional work through GitHub branches/PRs separately. If an environment is still starting, let it finish before diagnosing instruction loading.

For the environment's **Start skill**, the concrete reusable instruction is:

> Find `/workspace/music-video-studio` (or the checked-out `cromicron/music-video-studio` Git root), read its `AGENTS.md` and `PROJECT_MEMORY.md`, run `python3 tools/studio.py --refresh`, and follow the session guide. Preserve local work. Reconcile relevant unmerged records before continuing. This is orientation, not permission to generate media, spend money or publish.

This text is ready for the supported environment setup flow. No configuration/publish tool is exposed in this task, so this document does **not** claim that field was installed. Repository startup remains usable without it. A scoped [workspace entrypoint](WORKSPACE_ENTRYPOINT.md) was also appended to the active task's `/workspace/AGENTS.md` without changing global instructions; its versioned source is ready for published setup, but this local change alone does not update other tasks. The published setup, correct primary directory and actual first-turn behavior should be checked in a genuinely new cloud task; a child agent in this task does not prove those platform steps.

## Acceptance and limits

- `--check`: structure and links; useful during work, **not** a persistence claim.
- `--checkpoint`: clean committed work, intended live remote branch at exactly HEAD, and valid records/artifacts in a cold archive. Main inclusion is still separate.
- Unseeded fresh-reader test: pass only if it retrieves the actual assignment, budget, tool count, current completion state and any remaining work, actual spending and current authorization, critical creative corrections, prior failures, completed access and next action from files.
- Actual fresh-cloud test: use an ordinary prompt such as “Continue this project,” after startup completes. Observe loaded instructions and first actions; do not seed the prompt with the expected answers. Keep this distinct from the automated and child-agent tests.

An October community issue [9] reports successful setup/bootstrap checks followed by missing first-turn memory. It remains an open report, not a confirmed universal platform bug. It is a reason to test recovery behavior separately from installation.

Final verification and persistence evidence is recorded in [continuity verification](research/continuity-verification.md). Unknown private chat history remains explicitly listed in HISTORY_INDEX; this system prevents new avoidable gaps, but cannot reconstruct inaccessible conversations.

## Sources

1. OpenAI, **Harness engineering**, visible date 11 February 2026: [article](https://openai.com/index/harness-engineering/). “We treat it as the table of contents”; structured repository knowledge, progressive disclosure, linked execution plans, mechanical checks and documentation gardening. A demonstrated internal workflow, not a guarantee that every cloud product loads every file.
2. OpenAI, [Memories](https://learn.chatgpt.com/docs/customization/memories), accessed 7 November 2026: “Keep required team guidance in `AGENTS.md` or checked-in documentation.” Local/background memory limitations and separate web/Work controls.
3. OpenAI, [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments), accessed 7 November 2026. Current published-environment, isolated-task, refresh, Start skill and saved-state semantics.
4. OpenAI, [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), accessed 7 November 2026. Discovery, hierarchy, size cap and verification.
5. OpenAI, [Hooks](https://learn.chatgpt.com/docs/hooks), accessed 7 November 2026, especially **Managed hooks from requirements.toml**. Local and cloud orchestration differ; hooks need trust where supported.
6. OpenAI, [Projects and chats](https://learn.chatgpt.com/docs/projects), accessed 7 November 2026. Shared sources/instructions versus individual transcripts and directory context.
7. OpenAI, [Codex Cloud (Legacy)](https://learn.chatgpt.com/docs/environments/cloud-environment), accessed 7 November 2026. Explicitly separated from the current Cloud guide.
8. OpenAI, [November 2–6, 2026](https://learn.chatgpt.com/docs/whats-new/november-2-6-2026), visible date 4 November 2026. Checked for current product changes; does not establish universal cloud transcript recall.
9. Community report, [openai/codex #56920](https://github.com/openai/codex/issues/56920), opened 25 October 2026, checked 7 November. Bounded reported failure, not independently reproduced platform internals.

Independent source/alternative research: [researcher's report](research/codex-cloud-continuity-agent.md) and [implementation audit](research/continuity-independent-audit.md). Do not import a local-only memory tool or add a database merely because its marketing uses “second brain.” Revisit heavier retrieval only when this project's corpus or concurrent work demonstrates a need.
