# Quiet arrival and held contact — exact insertion review

Reviewed 7 November 2026 UTC. **Both contained insertions and their current adjacent cuts pass this scoped visual review.** A06 `[3,152)` supplies S013 once; L05 `[3,101)` supplies S030 once. I found no added crop, doubled camera move, repeated action, pose reset or leaked rejected hand gesture. The accepted native limitations remain visible, especially L05's push-in/pull-back and crown/lap cropping. This does not accept L05's later action, add motion to unfinished neighboring stills, or clear future replacements of those neighbors.

## Exact reviewed exports

All filenames below are under `full-film/exports/` and begin `Join_Me_in_Life_`. All four are 960×540 at 24 fps.

| Export | Frames | SHA-256 |
| --- | --- | --- |
| [Arrival_Contain_Proof.mp4](../exports/Join_Me_in_Life_Arrival_Contain_Proof.mp4) | 149 | `8c772116797166ac5a7c1e2d43cc6438f55916c17244bb5733ab5ad3d0fc8fc8` |
| [Arrival_Chorus_Context_Proof.mp4](../exports/Join_Me_in_Life_Arrival_Chorus_Context_Proof.mp4) | 451 | `eede37caeb2f083b7decd6fed8297d3228383ed39162c328c5d97ef721efa698` |
| [Held_Contact_S030_Proof.mp4](../exports/Join_Me_in_Life_Held_Contact_S030_Proof.mp4) | 98 | `daf445b7c5108c0ba718b31a944e7f7806e3d338c17a033130aa04a1b5d41b13` |
| [Held_Contact_Context_Proof.mp4](../exports/Join_Me_in_Life_Held_Contact_Context_Proof.mp4) | 396 | `f3874cfaf2116ae66f8fec4cf5b65881657d591cfb38772e1ab067da4c317230` |

These proofs belong to configuration snapshot `526f9c8713c7a8a0ee62cbf5e7701a2fb80964fae6a1386051000de903615db1`, recorded in the [implementation evidence](quiet-insertion-implementation.md). The source verdicts remain frozen: [A06](ltx23-quiet-A06-review.md), [L05](ltx23-quiet-L05-review.md). This report is bound to the actual export hashes, not any later state of the production configuration.

## Arrival, chorus and window

The 451-frame context begins at master 56.000000 s. Local frames 0–102 show the hospital exterior; 103–251 contain S013; 252–349 contain the first chorus; 350–450 show the existing window still. Cuts occur at master **60.291667, 66.500000 and 70.583333 s**.

The exterior-to-arrival cut establishes the entrance, then moves to his apprehensive face and planted bar grip without inserting a fresh reach. The head/chest dip and strained eye closure remain readable at 960×540. He looks back up before the chorus cut; no final frame freezes or resets him. The cut to the wide stage makes a clear change of setting and performance mode. The subsequent window portrait keeps her down-away and withdrawn, so the passage does not imply reassurance or recovery. The darker blue stage and hospital palette join coherently, with normal intentional changes of shot scale.

Containment preserves the available crown, face, pendant and gripping fingers. The native crown graze and softened eyelid detail remain; neither is worsened by an extra edit crop. The previously reviewed chorus source keeps its full picture, shoes and existing upper-hair limit. S015 is the **still window image in this exact proof**, not the new cropped L01 motion. No moving-reflection acceptance is implied. [Arrival cut sheet](quiet-insertion-sequence-review/arrival-context-cuts.jpg), [ordinary-size arrival capture](quiet-insertion-sequence-review/arrival-context-playback-4.40.jpg), [chorus capture](quiet-insertion-sequence-review/arrival-context-playback-10.70.jpg).

## Stage, held contact, exterior and wider still

The 396-frame context begins at master 142.666667 s. Local frames 0–70 show the wide stage performance, 71–101 its closer performance view, 102–199 contain S030, 200–299 show the hospital exterior, and 300–395 return to the existing wider held-contact still. The internal stage cut is **145.625000 s**; the subsequent cuts are **146.916667, 151.000000 and 155.166667 s**. S031 is the hospital exterior, not another stage shot.

The stage-to-S030 cut enters an already established hold. The camera then makes one conspicuous push-in and partial pull-back within the source; the edit adds no second push. His crown and her lap leave the source frame at the tighter phase, but both faces and the hand on her upper arm stay visible. The enlargement reads as a camera move rather than bodies swelling. Her tired blink is visible; this remains no proof of independently resolved breathing. At ordinary size, this moving two-shot is usable with the disclosed framing limitation.

Across all 98 inserted frames, his grip persists and her arms remain lap-directed. No release, pointing, regrip, new embrace or head pat enters the selection. Her head stays supported and directed down/away. The shot ends while contact remains intact and before the rejected later action. [Tight native picture](quiet-insertion-sequence-review/held-native-058.jpg), [late inserted picture](quiet-insertion-sequence-review/held-context-native-199.jpg).

The **100-frame / 4.166667-second exterior** provides a distinct separation before the wider still. The return changes composition and drawing detail but preserves the same relationship: his arm remains around her, and she remains passive. It therefore reads as a later view of continued waiting, not an on-screen rewind or a new pull into contact. The S032 still is visibly less animated and remains unfinished motion coverage; the separation does not promote it to a completed performance. [Held-contact cut sheet](quiet-insertion-sequence-review/held-context-cuts.jpg), [exterior playback capture](quiet-insertion-sequence-review/held-context-playback-8.50.jpg), [return capture](quiet-insertion-sequence-review/held-context-playback-12.70.jpg).

## Verification and limits

I inspected every encoded insert frame, phase overviews of both contexts, dense frames surrounding each cut, and complete 960×540 pictures at the tightest framing and boundaries. Both full contexts actually played at 1×. The narrower task was placement review; unaffected neighboring source performances were not re-reviewed exhaustively.

Independent checks confirm **149/149 arrival and 98/98 held-contact decoded frames exactly match their context counterparts**, at offsets 103 and 102. Both inserts show a 944×540 picture with 8px side bands on every frame. A direct same-index comparison with the full-source contain transform is retained in [encoded checks](quiet-insertion-sequence-review/encoded-checks.json). Nearly still adjacent frames can be ambiguous in a lossy thumbnail comparison, so that heuristic is explicitly not treated as an exact order certificate. The author's separate [exact encoded reconstruction](quiet-insertion-proof/frame-correspondence.json) establishes the frame-index selection, natural cadence and absence of holds/rejected tails; my independent context matching confirms that those same pictures occur here without substitution.

| Actual Chromium 154.0.8037.57 run, displayed 960×540 | Media / wall seconds | Reported total / dropped / corrupt frames |
| --- | --- | --- |
| Arrival/chorus context | 18.791667 / 18.9041 | 451 / 1 / 0 |
| Held-contact context | 16.500000 / 16.6137 | 396 / 0 / 0 |

Both ended at rate 1 with no media error, waiting or stalled event. The arrival run's single presentation drop is a browser counter, not an encoded missing frame. Supplied audio was enabled; no subjective listening or phoneme/music-sync judgment is claimed. This is actual player execution and inspected captures plus sequential frame review, not a claim of human-equivalent continuous audiovisual perception.

[Portable evidence index](quiet-insertion-sequence-review/README.md), [playback telemetry](quiet-insertion-sequence-review/playback.json), [frame/crop reproduction](quiet-insertion-sequence-review/reproduce.py), [playback reproduction](quiet-insertion-sequence-review/playback_check.py). No source, provider, configuration, approval record or earlier review was changed. Changed neighboring takes or added camera treatment require new cut checks.
