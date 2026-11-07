# Private A05 walking diagnostic — prepared, not submitted

One take for **S011, full-song 50.500–56.000 s / frames `[1212,1344)`**. Seed 49, 896×512, 24 fps, **145 generated frames**. Proposed use is source `[3,135)`: 3 head frames  + 132 used frames (5.5 s)  + 10 tail frames. Export the full silent take for review; this preparation neither trims/inserts it nor approves its motion.

The [exact two-guide static review](../../review/snow-walk-anchor-review.md) passes eligibility only. Both images are 1672×941; the end figure is smaller, farther screen-right and higher on the ground plane. Both anchors show screen-left leg trailing / screen-right supporting. The prompt therefore targets **roughly four natural alternating steps** toward the entrance. A physically plausible three–five-step result is acceptable; exact count, metric distance and percentage shrink are not promised. His hands stay in his pockets, rear view is retained, camera stays fixed and snowfall remains subtle. Reject gliding, a translated/shrunk frozen pose, changing architecture/footprints, foot sliding, a stop/turn/restart or face reveal. Starting support-foot occlusion remains a review risk; the end support shoe is clearer.

| Input | SHA-256 |
| --- | --- |
| `assets/snow_journey_refined_candidate.png` | `58198431a0673f8fabe4f0728d6f53b337542cf6518f132d067e83f032cca0e1` |
| `assets/snow_journey_end_candidate.png` | `bf94d17c837ce88cf3833e8498ffd9620e899e27b08f2ab55c7523ddabac9792` |
| Independent static review | `3c8170e8c4abeaf5b33a33051e2f0f84e31c8362546b95b3f562394f4dac5874` |

The preparer requires that exact review and both image hashes before freezing. First and last guides enter **both stages at indices 0 and 144**, with the same runtime audit as the summer diagnostic. Both images fit without stretch/crop onto an 896×512 canvas, using 896×504 content and 4-pixel top/bottom padding. The guide at 144 lies beyond the proposed used interval; it is directional conditioning, not proof that frame 134 already matches it.

## Frozen runtime, bounded execution

`common.py`, `bootstrap.py`, `run.py`, `runtime.py`, requirements and all source/model/patch locks are **byte-identical** to the frozen [summer I2V wrapper](../kaggle-i2v23/README.md). Inference, loader, precision patches, quantization, full 1024-position text encoding and sequential residency are unchanged. The copied runner's historical summer docstring/output names do not select its scene; the pinned walking manifest and images do. No model redesign, extra model, audio conditioning or prompt truncation was added.

The actual [summer render record](../../assets/motion/ltx23-summer-pilot/render.json) confirms 145 frames at 896×512 / 24 fps, four guide audit events, silent export and full decode: 333.190 s generation, 746.989 s runner, approximately 804.044 s whole job; peak allocated GPU bytes 11,143,011,840 and11,524,473,856. This is technical execution evidence for the retained 145-frame path, **not demonstrated walking or automatic acting acceptance**. Walking prompt token count is measured by the actual tokenizer at runtime; no local neural/tokenizer claim is made.

No audio is supplied or uploaded. The unchanged backend still jointly generates video/audio; generated audio is discarded and the output must contain one video stream with zero audio streams. The original master stays separate. The unchanged hardware/preflight/disk gates require two T4s, the 18 allowlisted files totaling 35,379,235,525 bytes plus 4 GiB cache reserve, and 2 GiB output reserve. Bootstrap/install/download/inference share the existing 5400-second limit and child-process cleanup. Root adds the provider 95-minute cap. Exactly one take; no automatic retry or batch.

## Local freeze and handoff

From the repository root:

```sh
PYTHONPATH=build/ltx-a2v-check-packages:build/ltx-kaggle-check-packages .venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/tools/kaggle-walk23/test_pipeline.py
python3 productions/join-me-in-life/full-film/tools/kaggle-walk23/prepare_bundle.py --output build/jml-kaggle-walk23-private-20261107-v1 --report build/jml-kaggle-walk23-private-20261107-v1-report.json
python3 build/jml-kaggle-walk23-private-20261107-v1/run.py --manifest build/jml-kaggle-walk23-private-20261107-v1/pilot.json --validate-only
```

Those v1 destinations are already frozen locally. Preparation refuses existing bundle/kernel/archive destinations; use a new version for changes. [Local validation](local-validation.json) records exact package/manifest/notebook hashes and [11 passing reused checks](local-tests.log), including actual pinned guide-construction/call ASTs, both-stage guide identity, source/patch integrity, private metadata, no-audio gates, mounted-dataset transport, timeout/no-CUDA failure and a real 145-frame synthetic H.264 encode/full decode. The synthetic backend test is an interface check, not neural inference.

Distinct private IDs:

- Dataset: `darionalis/jml-ltx-walk23-private-inputs`.
- Notebook: `darionalis/join-me-in-life-private-walking-i2v`.
- Frozen local bundle/report stem: `build/jml-kaggle-walk23-private-20261107-v1`.
- The unchanged bootstrap writes `/kaggle/working/jml-ltx-i2v23-results/` inside this separate walking job. Preserve its full records and `video-silent.mp4` under a distinct walking result directory when recovered; do not overwrite summer evidence.

Only root submits. Verify actual private dataset/notebook visibility, exact mounted files, free dual-T4 quota and the one-take manifest before execution. Local privacy flags do not prove remote visibility. The bundle excludes credentials, audio and weights; the canonical backend ZIP is transported as strict ASCII Base64 to avoid Kaggle recursive archive expansion. The notebook has no outputs. No provider calls, weight downloads or GPU jobs occurred in this preparation. Review the full result and proposed source interval for real alternating ground contact and natural-speed gait before deciding whether it can enter S011. No production config/source has been changed.
