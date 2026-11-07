# History coverage and provenance

Consolidation checked 7 November 2026. This index says what was actually recovered, how it affects current work, and what remains unavailable. Read [PROJECT_MEMORY](../PROJECT_MEMORY.md) first; do not load every historical file into every task.

## Covered sources

| Source | Coverage and authority |
| --- | --- |
| Repository main through `dead4f4b545f13aa2776e539cfe439d047e7df83` | Twelve main-history commits from the 3 November R4/band import through the 5 November global research instructions. Includes recovered sources, art inventory, media recovery, validation and the first session-memory structure. This is the observed main head during this audit, not a permanent sync target. |
| Six imported historical packages | [Source map](../productions/join-me-in-life/notes/source-map.csv), [migration inventory](../productions/join-me-in-life/notes/MIGRATION.md), original 1 November master/v2 handoffs and curation. Their caveats are package-specific; later recovery resolved several missing assets. |
| Recovered R2/R3/R4 production | [R4 handoff](../productions/join-me-in-life/current/HANDOFF.txt), [review history](../productions/join-me-in-life/current/REVIEW_NOTES.txt), source manifests, scenes and actual baseline. Later R4 emotional/continuity corrections govern that Short. |
| Unmerged 3–4 November branches | [Pinned branch recovery](history/2026-11-07-branch-recovery/README.md) covers `research/video-generation-approach`, PR #2's `prep/join-me-in-life-recreation`, and `codex/hedra-mcp-registration`. Useful research/setup lessons retained; old Short-first scope, access blockers and paid proposals are not current authorization. |
| Current full-film work, 6–7 November | [Full-film sources/results](../productions/join-me-in-life/full-film/README.md), [STATUS](../productions/join-me-in-life/STATUS.md), [DECISIONS](../productions/join-me-in-life/DECISIONS.md), [SESSIONS](../productions/join-me-in-life/SESSIONS.md). The active task's messages supply recent user corrections; these files preserve the operational facts rather than pretending to be a verbatim transcript. |
| Connected Drive project sources | The [band folder](https://drive.google.com/drive/folders/1vUCLK5ssIqYCGi-B0ALeltV5OpR0WGM_) was inventoried; the [current handbook](https://drive.google.com/file/d/1JgROTdjfMNssOTwK34fF24IRHfhXpEw8/view) was fetched (source last modified 29 October 2026). It confirms take 49 is final, band context and prior Suno lessons. Its old “do not worry about costs” statement concerns that music-making stage; it does not override this film's explicit budget. Final lyrics/remake sheet/rights/fingerprints were located; do not imply every one was freshly read. |
| Independent reconciliation | [Historical audit with exact source-line citations](history/2026-11-07-branch-recovery/historical-audit.md). Differentiates rejected work, proposals, technical checks, implemented revisions and acceptance. |

PR #1 was merged and its discussion had no comments. PR #2 was open and its fetched discussion had no comments at inspection. Branch snapshots preserve evidence without merging conflicting copies of STATUS or duplicate decision IDs. `codex-sync` is generated transport, not another creative session.

## Concrete gaps

- No general ChatGPT/Claude transcript-history API is exposed in this task. Searches of accessible local Codex/Claude history locations found no raw session exports. Connected Pages searches found no matching studio memory. These observations do **not** establish that the private chats do not exist.
- The master handoff says an animation-conversation transcript was consulted, but that raw transcript was not included in the imported files.
- The parallel `output/Latest_Character_Corrections` contribution is explicitly outside the old 22-image review and was not found in this checkout. Later image pointers are not blanket evidence of recovery or approval.
- The old custom `anime_pilot` renderer and separate 1080p experiment were not recovered. The preserved silent Blender pilot is a different artifact.
- Local-machine Codex memories and Claude web project histories are not automatically synchronized into this cloud task. Do not claim they were read or silently replace their contents with a summary.

These gaps do not justify asking again for the already-recovered full song, R4, references or logo. If missing history becomes necessary for a specific decision, identify that exact source and import it once with provenance.

## Maintaining coverage

At startup fetch and list remote branches, inspect relevant unseen commits and records, then reconcile them into current owners. Keep a source/commit/date for changed facts. Preserve contradictory evidence and its scope. At each coherent checkpoint update current state and lessons, append the session result, and verify the remote branch contains the commit. Main and a task branch are different persistence states; never say “saved for every session” merely because local files exist.
