# Revision 2 action-batch staging

This stages a selected private batch locally. **It makes no remote calls and launches no GPU job.** Root owns actual upload, remote privacy/mount verification and explicit execution. Do not rerun completed v1 queues.

The old story23 runtime already takes first/end images, but its quiet-shot validator requires identical endpoint files and hashes. This adapter changes that contract to independently reviewed, independently hashed, distinct endpoints. It reuses the exact locked `runtime.py`, `run.py`, `bootstrap.py`, dependency/model/source locks and archive from [the retained engine](../../../tools/kaggle-story23/README.md). No duplicated engine fork, midpoint control, sampler change, model upgrade or prompt-cache refactor is introduced. The generated bundle's `common.py` only imports the new validators after defining the original helpers. [Base byte contract](base-runtime-lock.json).

1. Copy [the draft plan](batch-template.json) into a named production plan. Fill in real source PNG paths relative to `full-film`, hashes, an independent endpoint-review record/hash and concrete before/action/after. The template deliberately refuses staging.
2. Select one to five distinct take IDs and explicit private v2 dataset/kernel slugs. Use natural 24 fps, 896×512, seed49 and a bounded `8n+1` frame count between89 and225. The new frame count still needs actual neural/quality verification; 225 is the largest prior successful clip. Use different source drawings for the action's beginning and result.
3. Set exact planned `[source_in,source_out)` intervals and matching optional master intervals. Pilot master intervals may be null. No overlap within one source or retiming is allowed. The separate editor must enforce cross-take/story coverage and review binding.
4. Mark the plan `ready_for_local_staging` only after its real endpoint review passes. This status authorizes local staging only.

From the repository root:

```sh
python3 productions/join-me-in-life/full-film/revision-2/tools/production/test_prepare_batch.py
python3 productions/join-me-in-life/full-film/revision-2/tools/production/prepare_batch.py --plan path/to/selected-plan.json --output build/jml-story-v2-selected-private-v1 --report build/jml-story-v2-selected-private-v1-report.json
```

The stage command verifies original source hashes, frozen engine hashes, source-review evidence, complete package hashes, actual unchanged child `--validate-only`, and selected queue validation. The source ZIP is transported as Base64 because Kaggle recursively expands nested ZIPs. Transport-only `dataset-metadata.json` stays outside the runtime lock; no secret, master audio, model weights or unrelated queue is staged. Local failure preserves its partial directory for diagnosis; choose a fresh name after correcting the input.

The sibling `-kernel` directory contains the private notebook. It retains the exact tested managed CUDA image and serial subprocess scheduler. Installed dependencies and weight files are shared within a job; every take still loads a fresh model. No cache across jobs is promised. A90-minute deadline covers setup and at most five distinct takes; failed takes are recorded, never automatically retried. Keep at most two selected jobs active.

Actual runtime outputs remain `/kaggle/working/jml-ltx-story23-results/<TAKE_ID>/video-silent.mp4`, `render.json`, fitted endpoints, environment/patch evidence and the outer `job.json`. Download into a uniquely named revision2 directory. `render.json` binds the full manifest and exact silent-video SHA; source intervals are in `manifest.editorial.segments`. No model-generated audio is exported. Feed the editor only independently accepted source SHA plus exact intervals. Technical completion and endpoint-source approval do not approve generated acting or cuts.

The [research and pilot plan](../../research/animation-production-research.md) explains action selection, measured resource range and deferred optimizations. Production performance shots use the separate original-song A2V path; this narrative adapter deliberately rejects audio inputs.
