# Repository structure and ownership

## Top level

| Location | Responsibility |
| --- | --- |
| [README.md](../README.md) | Human entry point: what the studio is, current work, and useful actions. |
| [AGENTS.md](../AGENTS.md) | Mandatory instructions for agents, including safe checkout synchronization. |
| [studio.json](../studio.json) | Registry of productions and the active production ID. Paths are `productions/<id>/`. |
| [docs/SESSION_GUIDE.md](SESSION_GUIDE.md) | How to start, record decisions, finish, and persist work across sessions. |
| [band/](../band/) | Shared band identity. Song-specific art stays in its production. |
| [productions/](../productions/) | One independent directory per song; start with that production's README and STATUS. |
| [tools/](../tools/) | Repository-wide orientation, validation, recovery, and runtime setup. Production scripts remain beside their data. |
| [.github/](../.github/) | CI, render/review workflows, and the PR template. |
| [templates/production/](../templates/production/) | Four starting documents for the next song. Template text is not an active production. |
| [MEDIA.md](../MEDIA.md) | Recovery of optional originals and alternate baseline exports from the release. |
| `work/` | Ignored scratch, draft scripts, and temporary transfers. |
| `build/` | Ignored reproducible check outputs, contact sheets, tool caches, and downloaded packages. |
| `.venv-bpy/` | Ignored optional local Python/bpy environment. Verify it; never rely on its existence in a fresh clone. |

## Within a production

| Location | Meaning and maintenance |
| --- | --- |
| `README.md` | Song brief, scope, folder map, authoritative sources, and production-specific work routes. |
| `STATUS.md` | Current baseline/candidate, present task, pending review, blockers, and next action. Update it instead of adding competing “latest” files. |
| `DECISIONS.md` | Confirmed creative constraints and technical choices with evidence and scope. Explicitly label proposals and superseded decisions. |
| `SESSIONS.md` | Dated continuation log, newest first; checks, results, and where work is saved. |
| `BLENDER.md` | Native scene and candidate-render procedure when Blender is used. |
| `current/` | Active edit source and the baseline that supports it. Keep the existing script-relative layout. |
| `art/` | Visual development, approved references and candidates, with provenance and indexes. Presence here does not mean approval for use in a cut. |
| `audio/` | Preserved supplied excerpt(s). `current/audio.mp4` is the portable working copy for the existing Short. |
| `full-song/` | Full recording, final lyric sheet, source links, and alignment to an excerpt. |
| `reference/` | Technical studies and earlier experiments, clearly labelled as references. |
| `notes/` | Imported historical handoffs, prompt records, inventories, and source mapping. Read its README before relying on an old plan. |
| `archive/` | Optional restored historical material; ignored and recoverable through the media guide. |
| `Revision_4/` | Existing Join Me in Life encoder/package output; ignored. A future production documents its own delivery path. |

Create folders only when they have content. The four maintained production documents are required for every registered production; media folders and Blender are not required for an idea-stage song.

## Organization review — 3 November 2026

The review covered tracked source, scenes/media inventories, all repository instructions and handoffs, source/finishing/recovery scripts, validation records and four GitHub workflows. The existing `band/`, song, art and portable edit boundaries already serve the production, so their working asset paths are retained.

The gaps addressed were a missing production-level entry point and current-state record; historical handoffs that could restart superseded plans; undocumented source-versus-generated file ownership; a working bpy setup described only in ignored local build files; and no repeatable continuation or new-song structure. The registry, four production records, folder/source guides, templates and CI layout check provide those missing parts. Runtime and render procedures are now linked from startup rather than rediscovered per chat.

This organization does not change the film or infer new creative approvals. The source checker, runtime probe and document checks establish technical readiness; the production STATUS retains outstanding creative review and full-song work.

## Source authority

Dario's latest request governs the task. Use `STATUS.md` to locate the current cut and `DECISIONS.md` to recover the current constraints and their evidence. For the existing Short, the Revision 4 handoff and camera schedule govern over the older v1/v2 planning documents. The old art package's manifest still governs the identity and approval status of its individual assets.

Technical validation, proposed ideas, and user acceptance are different facts. Preserve each in its proper scope. If two current instructions conflict, inspect their evidence and resolve the specific ambiguity before a dependent creative change.

The existing duplicate art/audio files serve different roles: the original selection with checksums and the portable edit's adjacent runtime assets. Do not deduplicate them or move `.blend`, `assets/`, scripts, audio, or validation files without updating and checking all dependent paths. [Current edit source map](../productions/join-me-in-life/current/SOURCES.md) lists the exact file roles.

## Add a production

1. Choose a unique lowercase, hyphenated song ID, for example `next-song`. Copy `templates/production/` to `productions/next-song/` (never over an existing directory).
2. Replace every `{{...}}` placeholder in the four copied documents. State the actual brief, what exists, which ideas are proposals, and the next concrete task. Unknowns should remain explicit.
3. Add `{ "id": "next-song", "title": "Actual Song Title" }` to the `productions` array in `studio.json`. Change `active_production` only if the new song is the work to resume by default, and update the root README's current-production links at the same time. Multiple productions may remain available; do not rename an existing production to switch songs. Keep song-specific agent rules scoped to their song.
4. Add only the media and source folders needed for that production. Record origins, approval status, and checksums for imported art/audio. Do not copy Join Me in Life's cast, timings, locked shots, or validation records as a new song's decisions. Existing render and recovery tools are song-specific until explicitly adapted.
5. Run `python3 tools/studio.py --check`. Add appropriate source/render checks when source exists, and update the session log. Commit and share the new registry and documents with the production.

## Add or accept a revision

Work on a focused branch; record the edition, shot and inclusive frame range before changing source. Render a short affected range, encode with existing audio, and record the comparison and actual review. Baseline checking with `tools/review.py` checks the original Revision 4 export, not arbitrary new encodes. See [BLENDER.md](../productions/join-me-in-life/BLENDER.md) for candidate checks.

Keep the original baseline, validation evidence and identity available. Dario's acceptance must be recorded before calling a candidate accepted. Give an accepted revision its own reference/tag and validation record; update STATUS and the production source map if its paths or authority change. Routine frames, preview encodes, ZIPs, and environment files stay out of Git. A durable accepted delivery belongs in a release or versioned media storage with provenance, rather than repeated binary replacements in history.
