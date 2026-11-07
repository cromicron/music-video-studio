# Current state — Join Me in Life

Updated: 2026-11-07 (UTC). This is the maintained continuation record; older handoffs remain evidence of their own stage.

## Existing work

The working reference is the **Revision 4 hybrid Short** in `current/`. Its source names use `experimental`; the exports use `Hybrid`. The tracked portrait export has lyrics. The restrained `simple` scenes are Revision 3 comparison material. See [the production guide](README.md) and [current source map](current/SOURCES.md).

The four native scenes, active artwork, two source movie clips, supplied Short audio, captions and scripts are present. The full take 49 and final lyric sheet are in `full-song/`. Optional alternate exports and v1 art are recoverable through [MEDIA.md](../../MEDIA.md).

Revision 4 is the recovered working baseline, **not a newly recorded final creative sign-off**. Prior review records describe frame, geometry, audio-hash and decode checks; they do not establish normal-speed audiovisual review or acceptance of the whole cut.

## Present task

Dario authorized completing the shared knowledge setup and then resuming production on 7 November. PR #3 was merged successfully into main at `d839a848afc6c8792e526ffe9791767b22531f43`; the knowledge base is no longer stranded on a task branch. See [project memory](../../PROJECT_MEMORY.md), [history coverage](../../docs/HISTORY_INDEX.md), and [researched implementation](../../docs/CLOUD_CONTINUITY.md). A fresh independent clone of merged main passed remote/cold verification, and a second reader with no inherited chat recovered the task and unfinished pilot correctly; the original film goal remains unfinished. Dario reports the existing one-minute Short is published on YouTube with about 600 views in less than a week. Preserve that foundation; view count is user-reported, not independently retrieved analytics.

Dario requested the entire music video, extensive method research, a free version using exactly three production tools, movement checks, and a sustainable paid recommendation capped at €20 for ten films. Be Ambitious is installed in the environment and retained in the repository. Active new work is in [full-film](full-film/README.md), separate from the unchanged R4 baseline.

A [complete 4:38 animatic](full-film/exports/Join_Me_in_Life_Full_Animatic.mp4) now covers the original song with 58 shots. Independent review found and then verified repairs to chorus/bridge framing, summer camera continuity and dawn chronology. This is **not the finished animated video**: no generated acting take has passed review. The first free hosted LTX test was rejected; the next request hit the daily quota. Four local CPU tests are complete: an owned scheduler correction fixes incoherent output, but representative motion fails direction/reflection checks. No CPU job remains running.

The paid research distinguishes renewable generation from prepaid inventory, includes retries/tax assumptions and does not falsely claim ten fully generated films fit €20. See [the recommendation](full-film/research/paid-budget.md). No new money or purchased credits have been spent.

## Next action

Repository consolidation, fresh-reader recovery, cold artifact checks and remote checkpoint verification are complete. [PR #3](https://github.com/cromicron/music-video-studio/pull/3) is merged. Merged-main recovery passed; the repository knowledge setup is ready for production continuation. A newly provisioned Cloud task has not yet tested automatic first-turn loading. No new generation was started during consolidation.

TinyFish is installed and live browser calls work. Google Flow is signed in and shows 50 daily credits. Kaggle phone verification is complete. A real private notebook successfully ran CUDA on two Tesla T4 GPUs; the official CLI independently downloaded its saved outputs and metadata. CLI OAuth is authenticated, with 29.95 of 30 GPU hours remaining at the last check. Hugging Face is signed in with verified email; the agent accepted the free LTX-2.5 access agreement and verified the explicit access-granted message and model file listing. See [access setup](full-film/ACCESS_SETUP.md) and [GPU evidence](full-film/research/kaggle-readiness/verified.json). Do not ask the user to redo completed sign-ins, phone verification or the model agreement.

Finish and test the owned private Kaggle LTX pilot bundle. Its [frozen handoff](full-film/tools/kaggle/README.md) explicitly marks the runner unfinished: notebook/bootstrap are absent, GPU stages untested, and the old local ZIP is stale and must not be uploaded. Run the prepared Flow motion pilots after supported private image transfer is configured; compare actual shot quality before production. The Kaggle infrastructure test succeeded, but no Kaggle model generation or Flow generation is claimed yet. A short labelled [story check](full-film/exports/Join_Me_in_Life_Story_Check.mp4) gives Dario immediate evidence of retained narrative direction; it is an animatic excerpt, not a motion pass.

The Runway plan was **withdrawn** after Dario corrected the reasoning: existing connections are accidental and must not determine tool selection. The [pilot plan](full-film/RUNWAY_PILOT_PLAN.md) remains research only. His reply did not authorize spending; zero purchased credits were used. Select the method from demonstrated quality and cost, then obtain the necessary access. Google Flow's published daily allowance and own-model LTX are being compared on that basis; the final three-tool route is not yet proven.

## Verified setup and checks

- Studio source base at this task's start: `dead4f4b545f13aa2776e539cfe439d047e7df83` on GitHub main. Compare live main at each new session; this is a dated observation, not a fixed sync target. Current local branch: `feat/join-me-in-life-motion-pilots`, based on merged main `d839a84`.
- Prepared local environment: `.venv-bpy/bin/python`, Python 3.13.5 and bpy 5.2.3 LTS. It opens the original 1080 × 1920 portrait scene. System `/usr/bin/blender` is 4.3.2 and must not be used to open the original 5.2 scene. Verify anew in each environment using `python3 tools/studio.py --runtime`.
- `python3 tools/review.py --source-only` passes: 19 hybrid segments, 16 restrained segments, 1,439 contiguous frames each, 14 ordered lyric cues.
- Production rendering is available in `.github/workflows/render-edit.yml` (“Render a studio edit”). It supports preview/full mode, three editions, and source rebuild or saved scene. Jobs must run on a branch containing their intended source changes.

## Open review and limits

- Full-film technical checks: 6,667 frames fully decode; audio waveform correlation 0.999659 with zero detected lag; only the intentional final fade is black. Chromium completed the exact reviewed animatic at 1× unmuted with no media error/stall, dropping 90 displayed frames under concurrent workload. This telemetry is not human listening or acting approval.
- The seven smaller new storyboard panels need higher-resolution final artwork. Full-song lyric/section estimates outside the known Short still need listening review; no fabricated lip sync is claimed.
- The existing reach has brief source hand blur; singing uses limited drawn mouth poses, not complete phoneme lip sync.
- Full-song narrative and all four bridge plea beats are now planned in the animatic. The proposed dawn ending is companionship and exhaustion, not a cure or accepted creative resolution.
- A new charge for generation needs the specific shot, reason and expected cost before spending; use supplied assets and local rendering by default.
