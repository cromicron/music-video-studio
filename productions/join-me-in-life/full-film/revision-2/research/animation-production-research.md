# Revision 2 — directing meaningful animation with the working free pipeline

Checked 7 November 2026. This is production research, measured feasibility and a proposed experiment plan, **not approval of ungenerated animation**. No remote generation or purchase was made for this research. [Reproducible measurements](production-feasibility.json).

## Recommendation

Keep **ChatGPT artwork → owned LTX → FFmpeg**, the tested 2.3 checkpoint and dual-T4 runtime. Rebuild the storyboard around actions that visibly change a situation. Give each shot a clear initial state, one principal action and a different resulting state. Generate meaningfully different first/end poses where an action requires them. The old repeated stills were an editorial scope decision, not evidence that free compute was exhausted: the newly checked account still has 23.84 of 30 GPU hours available.

Approximately 40–50 shots can tell the whole 277.79-second story. Seven-to-nine-second moving takes are already technically demonstrated; they should carry two or three connected phases of **one action**, not a list of unrelated tasks. Use shorter inserts only where the music or an important physical detail earns the cut. Keep a continuous accepted gesture across a cut when appropriate, using disjoint successive source ranges. Never replay it to fill another chorus.

Quiet acting can be purposeful. A character decides, starts to offer something, sees the response and changes how they offer it: this can be restrained and still tell a story. Breathing added to the same tableau cannot replace that development. A 12 fps drawing exposure is also different from padding a missing dramatic beat with a frozen pose; a simplistic “every frame must differ” metric is not our quality target.

## What research establishes

The official [LTX-2.3 prompting guide](https://ltx.io/blog/ltx-2-3-prompt-guide), dated 10 March 2026, recommends chronological physical action, visible emotional cues and sufficient direction for the clip length. Apply that as a clear beginning/action/result with compatible camera motion. Do not fill the positive prompt with every forbidden gesture: the existing distilled path uses one positive context, and the prior local failures show that identical endpoints alone do not control the intervening performance. [Recorded correction evidence](../../research/quiet-motion-correction.md).

The official [previsualization workflow](https://ltx.io/blog/how-to-build-a-complete-pre-visualization-pipeline) describes script, storyboard, moving sequence, review and revision as a production process. We should copy the method in our own files, not buy the interface: approve the emotional and physical sequence against the actual song before the expensive full batch. Character and object references must be carried through the sequence, not reinvented in every request. These are vendor workflow recommendations, not independent evidence of a film's quality.

The official [conditioning documentation](https://github.com/Lightricks/LTX-2/blob/4f521619ae0029e8fbb64d555030c2b121a33b4f/packages/ltx-pipelines/docs/conditioning.md) distinguishes replacement images and positional image guides. The latter can target an interior frame. It separately documents **generated keyframe slots**, which require 2.5 checkpoint support; those are not the same as supplying an intermediate drawing. Current main was independently read as `4f521619ae0029e8fbb64d555030c2b121a33b4f`, committed 4 November. No 2.5 runtime is being substituted for our proven 2.3 setup.

The current [audio-to-video guide](https://docs.ltx.io/open-source-model/usage-guides/audio-to-video) is now a 2.5 example, so its model files and defaults cannot be imported into our 2.3 runtime. Its relevant production principle is exact source-audio conditioning. Our own [performance wrapper](../../tools/kaggle-performance23/README.md) already executed original-song-conditioned 89/105-frame takes; source audio survived review muxing unchanged. Use that path for visible singing or shouted performance. Narrative scenes can use I2V with cuts timed to the original soundtrack. Model-generated audio remains discarded. Neither vendor synchronization claims nor a successful A2V encode establish phoneme-perfect singing.

## Verified capability and the narrow changes needed

| Capability | Actual status | Revision 2 use |
| --- | --- | --- |
| 896×512, 24 fps, eight-step distilled 2.3, dual T4 | Repeated successful local-source/remote-job evidence | Retain the pins, precision fixes and sequential Gemma/video residency |
| 209/225-frame I2V takes | P1/P2 completed; longest 225 frames is 9.375 seconds | Build 7–9-second action takes with genuine temporal handles; do not assume longer clips fit |
| Different first/end pictures | Neural runtime accepts them; **story23 validator currently forbids them** as a quiet-shot contract | Minimal new v2 endpoint validation/provenance; preserve old wrapper and frozen acceptance |
| Intermediate supplied image | Existing pinned WanGP backend exposes `frames_to_inject` and `frames_relative_positions_list`; appends guides to both stages | Not exposed/tested by our wrapper. Leave unimplemented initially; consider one midpoint only if an action pilot demonstrates a need |
| Retain video model across new prompts | Not implemented/tested in this wrapper | Defer. Existing per-shot process isolation is robust and quota suffices for pilots |
| Cache models on disk within a job | Proven | Group about five distinct takes per selected job; installed environment/cache shared |
| Reuse cache across separate Kaggle jobs | Not guaranteed | Include cold setup in estimates; do not count on an old VM |
| Full original-song performance | Exact short excerpts executed; long/full-song conditioning not tested | Use exact phrase-length excerpts for visible performance, preserve original master at final mux |

The pinned backend is [WanGP `b8880bd5`](https://github.com/deepbeepmeep/WanGP/tree/b8880bd5d292edfbe2384f5c951d95757ad59ea0). Inside its retained source ZIP, `models/ltx2/ltx2.py:1096–1116` implements additional image guides. The old `audit_endpoint_guides()` explicitly expects one end guide per stage and would correctly reject an added midpoint. Any extension must audit every image byte hash, frame index, strength and stage rather than disabling that guard.

The same archive's distilled pipeline accepts `precomputed_contexts`. The higher-level `generate()` currently supplies them only through its HDR context path. Our one-use Gemma hook deliberately releases the text model after one encoding. A normal batch cache would require deliberately pre-encoding and transferring multiple prompts, then proving exact context/seed behavior and memory cleanup. This is potentially useful reusable engineering, but it is **not a configuration switch** and should not delay story production.

## Measured capacity, with failure allowance

The ten P1/P2 takes generated **1,642 frames / 68.4167 seconds**. Their summed whole-job time was **7,313.47 seconds / 2.0315 job-hours**; mean whole-job cost was 106.90 elapsed seconds per raw video second. The denoising/generation portion totaled 3,731.34 seconds. Each child incurred about **334.57 additional seconds** for loading, text and other work. Two concurrent jobs can reduce wall time; they do not make summed resource usage disappear.

The first adoption used **1,432 / 1,642 frames, 87.2%**. One later returned-look interval failed and was regenerated separately. That unusually strong batch mostly used restrained action and is not a reliable success probability for new object exchanges or locomotion. Earlier full 13B hospital/summer trials and several quiet/dawn takes failed their intended acting, despite technical success.

The following planning model fits the ten measured generation times, includes measured per-child overhead, about five takes per job, and 12 handle frames per shot rounded to `8n+1`. Equal shot lengths are a planning simplification, not the final edit. The success columns scale complete-shot attempts, not just retained pixels.

| Final shot count | One attempt per shot | 80% successful attempts | 60% | 40% |
| --- | ---: | ---: | ---: | ---: |
| 40 | 8.53 job-hours | 10.66 h | 14.21 h | 21.32 h |
| 48 | 9.50 job-hours | 11.88 h | 15.84 h | 23.76 h |
| 55 | 10.45 job-hours | 13.06 h | 17.42 h | 26.13 h |

These are scenario estimates, not promised account debits or a completion date. The 23.84-hour quota is a rounded account display. Reserve approximately four hours for later corrections rather than consuming it all before editing. A weak 55-shot keeper rate could require the next free weekly allocation on 14 November. The right response is more calendar time or better staging, not silently replacing rejected action with holds.

## First experiment: six takes that prove story action

After the director chooses the new narrative, select **three necessary beats**, with two deliberately distinct staging treatments each. Proposed action classes below are test contracts, not a requirement to insert these props into the story.

1. **An object changes hands or state.** One actor lifts an already visible, well-shaped object, turns it toward the other person and completes the intended offer. Test a medium two-person composition against a carefully designed closer view. Exact hand ownership, object silhouette and beginning/result poses must agree. If a handoff fails, redesign staging while preserving its story function; do not cut from object-on-table to object-in-hand and call the transfer reviewed.
2. **A body changes position for a reason.** One actor rises from a bench or moves through a doorway and arrives in a visibly different relationship to the other. Test locked camera against one simple follow. Keep feet, center of mass and final destination readable. No camera sweep that conceals a body morph.
3. **An appeal receives a meaningful response.** A single reach/offer is followed by a clear permitted response or nonresponse, preserving the song's fear and her withdrawn state. Test a seven-to-nine-second connected action against two motivated shots with their own action endpoints. This tests narrative legibility and interaction, not just blinking.

Use unique take IDs and manifests. Begin with the same tested seed/settings so staging differences remain interpretable. Changing both artwork and wording is a production comparison, not a controlled claim about which factor caused improvement. Later seed variation can be added explicitly if needed; no automatic retry storm. Six pilot takes should use roughly 1.1–1.5 summed job-hours at the observed rates. No more than two selected jobs run simultaneously.

## Acceptance and production sequence

The pilot judge must be independent of its prompt author. Show the original-song excerpt and actual complete generated clip at 1×, then inspect contact/action frames. Ask an unseeded reviewer what changed and who initiated it. A technical pass with no legible action is a failed story pilot. Check identity, age, clothing, finger ownership, object continuity, weight/gait, eye direction and reflections. Review neighboring shots together for action state and screen direction.

Lock the new beat/shot map only after those capabilities are demonstrated. Generate each scene's keyframes from shared character/wardrobe/location references; use complete scene-board sheets for consistency, then refine the particular endpoints needed for production. One coherent action per request is preferable to asking a nine-second clip to cover three locations. Maintain an explicit object/contact/wardrobe state across the edit.

Track two distinct results: whether a shot has accepted moving coverage, and whether it advances its intended dramatic beat. Reject reused source intervals, reversed/looped action and padded endpoints in the new delivery ledger. Frame hashes or optical flow can flag accidental freezes, but meaningful animation is judged from the visible action and musical sequence. The final checks must include the full song, actual cuts and uninterrupted playback, followed by an outside narrative review that is free to reject an anatomically clean but dramatically inert film.
