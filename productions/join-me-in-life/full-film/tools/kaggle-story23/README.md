# Remaining story motion: three explicitly selected queues

One reusable wrapper prepares **Q2, Q3 or Q4 only when explicitly selected**. Each frozen package contains only that queue's source images, manifests, specifications and provenance. The queue catalog is shared configuration; it never launches all queues. Root owns private uploads and execution, after reviewing the current 201-frame trial. No provider action, model download, GPU job or motion acceptance occurs in local preparation.

All eleven takes use the same reviewed source at their first and last semantic guide, seed 49, 896×512 at natural 24 fps. Total frames are the next `8n+1` count covering the exact editorial use plus three head and at least four tail frames. Same-image guidance does not prove motion, preserve original pixels, or guarantee that the last generated frame matches the guide.

## Exact editorial contract

All source ranges below are zero-based, end-exclusive and native-speed. Each multi-shot take uses successive, disjoint source sections, even when a different shot intervenes on the master timeline. No earlier motion section is replayed.

| Queue / take | Placement | Total | Used source frames | Head / tail |
| --- | --- | ---: | --- | --- |
| Q2 · L02 | S010 | 121 | `[3,116)` =113 | 3 / 5 |
| Q2 · L03 | S015 | 113 | `[3,104)` =101 | 3 / 9 |
| Q2 · L06 | S033, S034 | 209 | `[3,102)` =99; `[102,198)` =96 | 3 / 11 |
| Q2 · L07 | S041 | 105 | `[3,99)` =96 | 3 / 6 |
| Q3 · L08 | S042, S043 | 209 | `[3,101)` =98; `[101,199)` =98 | 3 / 10 |
| Q3 · L09 | S045, S047 | 225 | `[3,116)` =113; `[116,215)` =99 | 3 / 10 |
| Q3 · L10 | S037 | 137 | `[3,126)` =123 | 3 / 11 |
| Q3 · L11 | S050, S051 | 201 | `[3,99)` =96; `[99,194)` =95 | 3 / 7 |
| Q4 · L12 | S053 | 97 | `[3,92)` =89 | 3 / 5 |
| Q4 · L13 | S056 | 153 | `[3,149)` =146 | 3 / 4 |
| Q4 · A07 | S058 | 169 | `[3,161)` =158 | 3 / 8 |

L09 is **225 frames / 9.375 seconds**; L06/L08 are **209 / 8.708333 seconds**. These exceed the current 201-frame trial and require new remote memory/time evidence. They are not silently shortened, split, retimed or retried. Q2 contains 548 generated /505 used frames, Q3 772/722, Q4 419/393; total intended new editorial coverage is 1620 frames /67.5 seconds. These are requested deliveries, not accepted motion.

**A07 has no fade in its generated source.** The editor alone applies the existing final two-second fade at master frames `[6619,6667)`, corresponding to A07 source `[113,161)`. The source must maintain continuous breathing through that region and its remaining tail, without a frozen ending pose. The exact mapping is validated as metadata; it does not render a fade or change the edit.

## Inspected references and prompt intent

All five native source images were viewed. Their full SHA-256, dimensions, fitting offsets/RGB hashes and review links are recorded in [local-validation.json](local-validation.json) and per-take `provenance/`. Exact prompts are retained in [takes-template.json](takes-template.json); the compact intent below is for root's review.

| Take(s) | Unchanged native source | Distinct requested motion and constraints |
| --- | --- | --- |
| L02 | [Window redraw](../../assets/her_window_refined_candidate.png), 1672×941 | One weary exhale, brief defocus, slightly pressed lips; gaze stays down/inward, reflection moves in synchrony. |
| L03 | Same window source | Brief worried eyelid/brow tightening, soft blink and a small breath; unresolved response without a head turn or hopefulness. |
| L06 | [Original M01 endpoint](../../../current/assets/M01_Embrace_End.png), 1916×1080 | His worried breath/brow first, then her tired blink/exhale; hold the original outer-upper-arm grip and passive lap. |
| L07 | Same original endpoint | Her breath briefly catches and eyelids lower; his continued attentive presence has only a small breath. |
| L08 | Same original endpoint | His inhalation/pause and growing brow/jaw tension, then partial blink while she exhales. No staged singing. |
| L09 | Same original endpoint | Her shallow uneven breath/tired blink early; his brief eyelid closure/reopening and independent breathing later. The second section continues instead of restarting. |
| L10 | [Corrected summer v2](../../assets/summer_identity_end_v2_candidate.png), 1672×941 | Gentle relaxed breaths and brief eye attention; preserve small shared smiles without replaying the laugh or mouthing a new phrase. Earbud grip, wires, rings, narrow wristband and summer clothing stay fixed. |
| L11 | [Original indoor S06 dawn](../../../art/03_Story/S06_Still_Here_At_Dawn.png), 1672×941 | His long quiet exhale, then her slow blink/breath. Preserve the source's close seating and original hands/arms, her away gaze and his concern; no invented shoulder grip or new embrace. One continuous shot across both IDs. |
| L12 | [Outdoor dawn v2](../../assets/dawn_together_refined_v2_candidate.png), 1672×941 | Small concerned breath from him, brief blink from her as the outdoor seating is established. No new contact. |
| L13 | Same corrected outdoor source | Her slow exhale/settling shoulders, then his blink and only slight easing of brow; continued concern, with distinct breath spacing. |
| A07 | Same corrected outdoor source | Exhausted uneven breaths throughout; her away gaze settles slightly, he stays attentive. No smile, cure, source fade or final freeze. |

The [window review](../../review/her-window-refined-review.md) warns of existing tight crown framing and reflection risk. [M01 contact review](../../review/aftermath-edit-candidate.md) supports the outer-upper-arm hand ownership, passive lap and self-supported heads; every held-contact prompt preserves those features and rejects a new pull, stroke, squeeze, hand lift or hug. [Summer v2 review](../../review/summer-identity-anchor-review.md) clears the corrected adult eyes/freckles and narrow wristband for static use. The indoor S06 drawing remains the selected original source; its earlier [workprint review](../../review/full-workprint-v1-review.md) concerns continuity, not proof of moving anatomy. The [outdoor v2 review](../../review/dawn-refined-review.md) resolves the old exposed-finger ring omission. Dawn remains an unresolved proposed ending, not recovery or a role reversal.

No source was redrawn or edited. All sources fit within 896×512 without stretching/cropping. Existing source occlusions and framing limits remain. Motion prompts use natural, uneven breath/expression changes instead of a repeated gesture; actual performance and variation still require review.

## Runtime, resources and limits

`runtime.py` is **byte-identical to the frozen quiet wrapper**: model loading, precision/attention patches, sequential Gemma/video residency, exact endpoint byte/index/strength audit in both stages, joint generation and model-audio discard are unchanged. Source/dependency/model/patch locks are byte-identical too. No new engine, model, sampler or prompt cache is introduced. The serial scheduler and managed-Torch pipless bootstrap functions are unchanged. Only selected queue specifications, paths and allowed frame counts vary.

Each queue gets a separate 5400-second cap covering installation, downloads and its serial children. The installed environment and verified weight cache are reused **within that queue's job**, not promised across separate Kaggle jobs. Each take has a fresh child/model/text encoding and separate output/backend/failure records. A failed take is never retried; later distinct takes may continue inside the remaining deadline. Timeout kills the process group and marks unstarted takes. Existing job/render records are not overwritten.

No audio is supplied, uploaded or exported. The backend still jointly generates audio/video, and model audio is discarded; the MP4 must have exactly one video stream. The full master stays unchanged for later editorial mux. The same 18 allowlisted model files total 35,379,235,525 bytes; initial cache space needs 39,674,202,821 bytes including reserve, plus 2 GiB output reserve at preflight. Source/hardware/CUDA/quantization checks precede large weights. Source notices and model terms remain in [NOTICE.md](NOTICE.md) and `vendor/`.

The prior 145-frame summer success establishes this runtime's technical execution at that size. The current 201-frame trial must be inspected by root before submission; this package makes no claim that 209/225 frames fit or that matching endpoints produce useful quiet action. Prompt token counts are measured by the real pinned tokenizer remotely, without truncation and retaining all 1024 padded positions. Independent normal-speed and frame review must check faces, reflections, breath variation, anatomy, contact, jewelry and joins.

## Explicit preparation and private staging

From the repository root, run the offline tests once:

```sh
PYTHONPATH=build/ltx-a2v-check-packages:build/ltx-kaggle-check-packages .venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/tools/kaggle-story23/test_pipeline.py
```

Prepare one selected queue per invocation; `--queue` has no default and accepts only Q2, Q3 or Q4:

```sh
python3 productions/join-me-in-life/full-film/tools/kaggle-story23/prepare_bundle.py --queue Q2 --output build/jml-kaggle-story23-q2-private-20261107-v1 --report build/jml-kaggle-story23-q2-private-20261107-v1-report.json
python3 productions/join-me-in-life/full-film/tools/kaggle-story23/prepare_bundle.py --queue Q3 --output build/jml-kaggle-story23-q3-private-20261107-v1 --report build/jml-kaggle-story23-q3-private-20261107-v1-report.json
python3 productions/join-me-in-life/full-film/tools/kaggle-story23/prepare_bundle.py --queue Q4 --output build/jml-kaggle-story23-q4-private-20261107-v1 --report build/jml-kaggle-story23-q4-private-20261107-v1-report.json
```

Each creates an independent frozen bundle/ZIP and sibling `-kernel/` containing the generated private notebook/metadata. Existing destinations are refused. Local validation for a child uses its selected frozen path, for example `python3 build/jml-kaggle-story23-q2-private-20261107-v1/run.py --manifest build/jml-kaggle-story23-q2-private-20261107-v1/L02.json --validate-only`.

| Queue | Private dataset ID | Private notebook ID/title slug |
| --- | --- | --- |
| Q2 | `darionalis/jml-ltx-story23-q2-private-inputs` | `darionalis/join-me-in-life-private-story-q2` |
| Q3 | `darionalis/jml-ltx-story23-q3-private-inputs` | `darionalis/join-me-in-life-private-story-q3` |
| Q4 | `darionalis/jml-ltx-story23-q4-private-inputs` | `darionalis/join-me-in-life-private-story-q4` |

Root must verify actual remote privacy and mounted files before GPU execution. The canonical source ZIP stays recoverable in Git and travels as strict Base64 at `vendor/wangp-source.zip.b64`, avoiding Kaggle's recursive ZIP expansion. Transport-only `dataset-metadata.json` is excluded from runtime integrity because Kaggle consumes it. Inputs shared by multiple takes within one queue are stored once. No `__pycache__`, other queue's artwork/manifests/provenance, audio or model weights is staged.

## Local verification

[Test log](local-tests.log) covers exact selected frame counts/guide indices, consecutive non-reused source portions, editor-only A07 fade metadata, invalid inputs/scope, explicit selection without auto-all, isolated private packaging, metadata-absent mounts, Base64/source/patch integrity, unchanged inference snapshots, actual pinned endpoint construction and stage-helper calls for every take, changed/missing guide failures, synthetic CPU wrapper shapes, real FFmpeg encode/full decode at every selected duration, audio-track rejection, serial failure continuation, timeout cleanup and no-CUDA early stop. Synthetic wrapper tensors are not neural inference. [Validation and frozen hashes](local-validation.json) separate these checks from the still-unproven remote memory/time and motion quality.

## Bounded positive-prompt corrections R1W / R1H

After the initial quiet review rejected unrequested hand actions, root selected two separate one-take comparisons. `R1W` contains `R1L04` at the same 145 frames and `R1H` contains `R1L05` at the same 201 frames. Only the positive prompt changes semantically: exact original first/end images, seed 49, 896×512, 24 fps, eight distilled steps, guidance, schedules and runtime remain unchanged. Queue/take names change solely to retain the original results and prevent accidental overwrite. Each uses its own explicitly selected private dataset/notebook; preparation does not submit either. At most two free batch jobs may run. No automatic retry or later queue launch.

[Correction research](../../research/quiet-motion-correction.md) distinguishes the tested failures from the unproven wording hypothesis. The pinned distilled runtime does not use a negative context at the present NAG setting; changing that setting would violate the validated single-prompt Gemma residency path. Intermediate image guides are supported upstream but are deliberately excluded from this comparison. A successful encode is not acceptance: both full planned intervals need new independent hand/contact, motion, identity and framing review. Existing source/sequence keepers remain scoped and unchanged.
