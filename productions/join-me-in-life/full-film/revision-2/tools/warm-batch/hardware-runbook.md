# Private H01/C01 warm-cache experiment

**Root/ops have saved and read back private no-run version 1; no GPU execution or neural equivalence result is claimed.** The [deployment record](../../research/warm-ab-v1-deployment.json) owns current provider state and scheduling. Do not repeat the dataset creation or no-run save instructions below for this already verified candidate. The current gate gives the gait/coat test the next slot after an acceptable initial handoff result; warm follows only when another real slot frees. Count unrelated account work toward the maximum of two batch GPU sessions and preserve existing jobs.

## Frozen inputs and local validation

The [staging record](staging-v1.json) is the exact file manifest for this candidate:

| Item | Value |
| --- | --- |
| Bundle | `build/jml-story-v2-warm-ab-private-v1` |
| Notebook directory | `build/jml-story-v2-warm-ab-private-v1-kernel` |
| Complete archive | `build/jml-story-v2-warm-ab-private-v1.zip` |
| Package-lock SHA-256 | `ea896cf0f05569031a624b42e01f8050f788af0a078486daeeca24519888e697` |
| Archive SHA-256 | `af528fd33023ebe665b15adfb67989c58192fa497026370d661387df226603b7` |
| Private dataset ID | `darionalis/jml-story-v2-warm-ab-inputs` |
| Private notebook ID | `darionalis/jml-story-v2-warm-ab` |
| Sequence | Fresh cold A, fresh cold B, fresh warm process A1 → B → A2 |
| A | H01, 169 frames; experimental ID `V2WH01` |
| B | C01, 193 frames; experimental ID `V2WC01` |
| Fixed rendering | Original reviewed endpoint bytes, exact prompt, seed 49, 896×512 at 24 fps; original engine/model/runtime pins |
| Attempts | One job, five generations, no automatic retry or production promotion |

Only take IDs and corresponding provenance paths differ from the two original bundles. The immutable `experiment.json` records both original package hashes, manifests, prompt hashes and image hashes. Neither original pilot bundle is modified. The archive ending `-base.zip` is a preserved intermediate and **must not be uploaded**; it lacks the hardware-experiment additions.

From the repository root, this performs only local package and experiment-policy validation:

```sh
python3 -B build/jml-story-v2-warm-ab-private-v1/experiment_driver.py \
  --bundle build/jml-story-v2-warm-ab-private-v1 --validate-only
python3 -m unittest discover \
  -s productions/join-me-in-life/full-film/revision-2/tools/warm-batch \
  -p 'test_*.py' -v
```

Expected: `valid: true`, `planned_generations: 5`, `cap_seconds: 5400`, `new_gpu_jobs: 0`, and 15 passing offline tests. These tests cannot establish GPU memory viability or equality of generated frames.

[Local verification record](local-validation-v1.json) records the completed checks, including every locked archive member and absence of extra files in the frozen bundle. Use `-B` when checking that bundle to avoid adding Python bytecode caches to its upload directory.

## Private save and readback, only when root/ops schedule it

Commands below are operational instructions, **not a record that they ran**. They use the existing verified account tools without putting credentials in the bundle. Stop on a mismatched file, privacy setting, notebook source or provider response. Do not replace or retry an existing candidate remotely.

```sh
/workspace/.tools/jml-kaggle/bin/python tools/kaggle_auth_refresh.py
/workspace/.tools/jml-kaggle/bin/kaggle datasets create \
  -p build/jml-story-v2-warm-ab-private-v1 -t -r zip -q
/workspace/.tools/jml-kaggle/bin/kaggle kernels push \
  -p build/jml-story-v2-warm-ab-private-v1-kernel \
  --no-run --accelerator NvidiaTeslaT4 -t 5400
mkdir -p build/jml-story-v2-warm-ab-remote-evidence-v1/inputs
/workspace/.tools/jml-kaggle/bin/kaggle datasets metadata \
  darionalis/jml-story-v2-warm-ab-inputs \
  -p build/jml-story-v2-warm-ab-remote-evidence-v1
/workspace/.tools/jml-kaggle/bin/kaggle kernels pull \
  darionalis/jml-story-v2-warm-ab/1 -m \
  -p build/jml-story-v2-warm-ab-remote-evidence-v1
/workspace/.tools/jml-kaggle/bin/kaggle datasets download \
  darionalis/jml-story-v2-warm-ab-inputs --unzip \
  -p build/jml-story-v2-warm-ab-remote-evidence-v1/inputs -q
python3 tools/kaggle_verify_bundle.py \
  --bundle build/jml-story-v2-warm-ab-private-v1 \
  --evidence build/jml-story-v2-warm-ab-remote-evidence-v1 \
  --expected-lock ea896cf0f05569031a624b42e01f8050f788af0a078486daeeca24519888e697 \
  --notebook-version 1
python3 build/jml-story-v2-warm-ab-remote-evidence-v1/inputs/experiment_driver.py \
  --bundle build/jml-story-v2-warm-ab-remote-evidence-v1/inputs --validate-only
```

Dataset creation is private by default; the notebook declares `is_private: true`. The verification must confirm **actual retrieved privacy**, all package-locked bytes, decoded engine archive, exact normalized notebook cells, attached dataset, pinned container and T4 settings. Save console responses and the resulting `verified.json`. If the provider assigns another version, retrieve and verify that exact version rather than assuming version 1. A no-run notebook displaying `COMPLETE` means the notebook was saved, not that any generation ran.

After successful readback, a free slot, chair priority and root scheduling, the only execution command is:

```sh
/workspace/.tools/jml-kaggle/bin/kaggle kernels push \
  -p build/jml-story-v2-warm-ab-private-v1-kernel \
  --accelerator NvidiaTeslaT4 -t 5400
```

The **provider timeout is 5,400 seconds (90 minutes)**. Do not reuse the older pilots' `-t 5700`. The driver separately permits 5,390 seconds of active work and reserves ten seconds for process-group teardown. Environment preparation, initial model downloads, both cold baselines, all three warm generations and comparison share that deadline. A timeout preserves available evidence and ends the experiment; it is not permission to retry or lengthen the job. The notebook's longer emergency subprocess watchdog is subordinate to the provider's 90-minute environment cap.

Parse the provider's actual message: its CLI may return exit code 0 while saying `Maximum batch GPU session count of 2 reached`. That response is an admission failure, not a queued experiment. Pull the actual submitted notebook version, verify its normalized cells/settings again and record its real status. Do not cancel other work to create room.

## Expected outputs and interpretation

Retrieve the notebook output into a new local evidence directory. Its main folder is `/kaggle/working/jml-v2-warm-ab-results`:

```text
job.json                       whole-job state, caps, exact input hashes, stage clocks
bootstrap.log                  managed-PyTorch-preserving environment setup
setup/                         preflight, backend patch and verified weight-cache setup
cold-A/                        fresh unchanged standalone A
cold-B/                        fresh unchanged standalone B
warm/warm-summary.json         load/prefill clocks, cache counts, memory and complete timing
warm/A1/                       first warm A
warm/B/                        warm B
warm/A2/                       repeated A, solely a retained-state test
comparison.json                exactness, decode, memory and timing gates
comparison.log                 comparison stdout/errors
```

Each of the five generated-take directories contains `video-silent.mp4`, `render.json`, `raw-rgb.json` and `context-observation.json`. Cold directories preserve the unchanged runner's fitted guides, environment and patch logs; warm shared input/environment/patch evidence sits in `warm/`. Each subprocess has `child.json` and its driver-captured `runner.log`. Raw RGB hashes are taken **before encoding**; the unchanged encoder and full decoder also validate the delivered files. The two warm contexts are the final video/audio conditioning tensors, even though no generated audio is delivered.

The initial model download/cache setup is common and excluded from both throughput branches, but included in the job cap. Fresh-process cold A + B is compared with warm process startup + both prompt encodes + A1 + B + exports. Warm A2 is excluded from that speed ratio because its purpose is to detect state carryover. Every context/RGB comparison must be exactly equal, all five files must fully decode, Gemma must remain released, the final context CPU cache must stay within 256 MiB, and A2 must show no increase in live allocated GPU bytes versus A1. No positive byte tolerance is hidden. The fixed speed target is warm A/B at most 80% of cold A/B elapsed time.

Failure of any gate blocks adoption. An exact match with less than 20% gain also fails the proposed speed target. No file claims production promotion, even when every numeric check passes. Root still reviews actual normal-speed motion, guide behavior and memory traces. If cold GPU arithmetic proves nondeterministic, investigate with a separately authorized test; do not silently weaken equality to obtain a speed claim. The repeated A is diagnostic evidence and cannot be inserted twice into the film.
