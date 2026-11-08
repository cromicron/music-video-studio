# Performance-cut private production adapters

These isolated local stagers reuse the tested owned LTX routes while binding only the new adopted [performance-cut generation plan](../../story/shot-plan-v1.json). They never upload or execute a provider job. Old C wrappers, old guards, delivered clips and old notebook versions stay unchanged.

## Local staging

- [prepare_i2v.py](prepare_i2v.py): plan schema `jml-performance-cut-action-batch/v1`; one to five B/O-prefixed takes, P-prefixed queue and new private `darionalis/jml-p-*` dataset/kernel destinations. Paths for endpoint/source-review files are **full-film-relative**. Two distinct independently reviewed PNG endpoints, raw 89–225 frames in 8n+1 steps,896×512, 24 fps, six leading frames and exact natural-speed keepers. The retained neural runtime, runner and bootstrap are copied unchanged; only the selected frozen validation/transport contract is appended to common.py.
- [performance/prepare_bundle.py](performance/prepare_bundle.py): plan schema `jml-performance-cut-performance-plan/v1`; one to five B-prefixed vocal takes, P-prefixed queue, new private `darionalis/jml-p-*` destinations. Image/review paths are **repository-relative**. One first image and exact original stereo48k PCM; raw 89/97/105/113/121/129 frames only, six leading and at least seven trailing frames. B05A/B and B08A/B are all 113 raw frames in adopted v1. Neural runtime/model/backend/dependency pins remain unchanged; proven runner whitelist and isolated output names are the only existing wrapper adaptations.

The [new guard](story_plan_guard.py) checks the exact adopted story bytes/hash, schema, production identity, status/adoption state, fps and full-film extent. It rejects proposals even when their hash is supplied. Each selected shot's timeline, raw frame count, keeper, method, handles and original-audio sample range must match the frozen generation plan exactly. Inherited C slots are **reuse-only**, even though their historical planned-generation metadata remains in the source plan. Cost/queue accounting must select only the 18 new B/O requests, not sum every historical row. [Frozen workload](../../research/operations-frozen-workload-v1.json) records 128.75new raw seconds.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 productions/join-me-in-life/full-film/performance-cut/tools/production/test_prepare_i2v.py
PYTHONDONTWRITEBYTECODE=1 .venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/performance-cut/tools/production/performance/test_pipeline.py
```

Ten I2V and nine A2V offline checks pass. They exercise actual child preflight, source/queue tamper rejection, original PCM samples, private provider metadata, zero retries, stale/proposal/shifted-plan rejection, inherited-source exclusion and real backend audio-shape coverage. Synthetic test reviews are explicitly fixtures and never authorize real artwork. [Verification record](../../research/operations-adapter-verification-v2.json) binds the derived files and unchanged old sources.

To stage an independently reviewed and root-released plan:

```sh
python3 -B productions/join-me-in-life/full-film/performance-cut/tools/production/prepare_i2v.py --plan EXACT_RELEASED_PLAN --output FRESH_BUILD_PATH --report NEW_REPORT
.venv-ltx-cpu/bin/python -B productions/join-me-in-life/full-film/performance-cut/tools/production/performance/prepare_bundle.py --plan EXACT_RELEASED_PLAN --output FRESH_BUILD_PATH --report NEW_REPORT
```

The [pilot draft](plans/pilot-draft-v1.json) originally proposed O01 (209 raw) and B03 (137 raw) in one shared-startup job. Its unready state and placeholder review fields deliberately prevent staging. Preserve that draft; write a new exact released plan only after both actual endpoint pairs pass review. A2V static-source JSON uses the retained `pairs`/`inspection.native_review_crops` contract, recording the exact viewed PNG hash and selected panel.

## Provider release and verification

Only the designated operator submits after root releases the hash-bound payload. Before launch, read official quota and current owned-notebook statuses, check private dataset/notebook metadata and exact remote package/source bytes, then submit the explicit new version once. At most two active account jobs total, provider cap 5400s, no automatic retries. Pilot quota before/after and actual output quality determine whether later batches are released. Four hours is a planning correction margin, not a hard stop: report actual quota and remaining quality needs to root before curtailing authorized free production. Missing local watcher terminals are not failed provider jobs.

The I2V [download verifier](verify_completed_batch.py) and A2V [download verifier](performance/verify_download.py) preserve full source/fitted-guide/render/audio provenance and decode checks. Pass the exact released package-lock hash, downloaded results and a fresh report path. Technical verification grants no motion, musical-fingering, contact, lyric or final-cut acceptance. Review consecutive frames and actual song playback before keeping clips.

## Pilot01 exact payload and naming recovery

The [released-for-staging pilot-v2 plan](plans/pilot-v2.json) binds accepted O01 and B03 sources. [Private deployment proof](../../research/operations-pilot01-deployment-v1.json) records the exact package/manifest/code hashes, actual private dataset version2 and no-run notebook version1. GPU execution state is recorded separately; local staging state does not grant permission to infer.

On the first no-run save, the official CLI warned that the fresh notebook title did not resolve to the requested ID and created `darionalis/join-me-in-life-performance-cut-pilot01`. That private version1 was saved without cell execution and retained unused. Metadata readback confirmed its privacy and expected mount. A new v2 staging plan uses title `JML P Pilot 01`, which resolves exactly to intended `darionalis/jml-p-pilot-01`; its private no-run save and independent readback passed. The new title-to-slug guards reject this mismatch before future staging. Do not run the unused title-derived notebook or treat its no-run404 status as a failed GPU execution.

## Current quota and observation evidence

Pilot01 exact executionv2 completed. [Technical output verification](../../research/operations-pilot01-output-verification-v1.json), [retained sources/quota observation](../../research/operations-pilot01-retention-v1.json) and [completed observer](../../research/operations-pilot01-observer-complete-v2.json) are separate from creative motion acceptance. The official GPU quota changed12.93h to12.49h across the sole active pilot, an observed0.44h debit at0.01h display precision; this is not an invoice or a billing guarantee. Future active watchers write into ignored `build/` and only meaningful snapshots enter research, avoiding constant Git dirt. Four hours is a planning correction margin, not a new user-permission barrier: report actual available quota and quality needs to root before curtailing the authorized free task.

## Followup and vocals execution

Root released both exact private packages in [followup/vocals binary release](../../review/followup-vocals-root-release-v1.json), after [pilot motion adoption](../../review/pilot01-root-adoption-v1.json). [Followup submission](../../research/operations-followup01-submission-v1.json) and [vocals submission](../../research/operations-vocals01-submission-v1.json) each record one successful execution version2 and exact private/code/mount readback. Watch only `darionalis/jml-p-followup-01/2` and `darionalis/jml-p-vocals-01/2`; active observer files are ignored `build/jml-p-followup01-observer-v1.json` and `build/jml-p-vocals01-observer-v1.json`. Their initial observed states are not future completion claims.

The [read-only rate-limit incident](../../research/operations-status-rate-limit-v1.json) occurred before the vocals attempt and did not restart generation. Avoid rescanning every unchanged terminal notebook immediately after a successful full account check. Compare a fresh owned-list latest-run/version record against the cached exact terminal evidence and query changed, new or active refs; resolve unknowns and honor Retry-After. Before any next GPU run, combine that account evidence with fresh exact active-job statuses and quota, preserving the two-job cap.

## Remaining instruments and bounded local dispatch

[Instrument A](../../research/operations-instruments-a-predeployment-v1.json) and [instrument B](../../research/operations-instruments-b-predeployment-v1.json) have exact private no-run version1 readback proofs. Their [conditional root release](../../review/instruments-root-release-v1.json) permits each exact payload once after account slots free, with output retention and fresh quota/max-two checks. [Cached account preflight](../../research/operations-cached-account-preflight-v1.json) demonstrates four fresh status reads across40 owned refs; no SDK list defaults are used as privacy/version/hardware evidence.

The [local dispatcher routing](../../research/operations-conditional-dispatch-routing-v1.json) records its process, bounded scope and stop/recovery controls. It observes existing watcher files, collects actual completed outputs and conditionally starts only the two released instrument notebooks. Temporary scripts and process IDs are convenience state. After interruption, use the canonical exact release/submission/retention records, inspect actual provider statuses first, and never recreate a GPU attempt because a local process vanished. All retained sources still need independent song-paced motion/contact review before binding them into the edit.
