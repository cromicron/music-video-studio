# Recovered Short performance/reaction — independent encoded-sequence review

Reviewed 7 November 2026. **The restored P01 mouth treatment, S02 blinks and original cut chronology pass this focused review. One minor S023 camera correction remains before clearing the complete proof: the final push trims the upper hair tips.** A separate, gentler-camera v2 is being prepared; this report and its evidence remain bound to v1.

Reviewed file: [Short performance reuse proof](../exports/Join_Me_in_Life_Short_Performance_Reuse_Proof.mp4), SHA-256 **`25519287823f517943ffc1efd7f2f94aea5408a13c22775c451ce5f1f5619ad3`**. Independently confirmed 960×540 H.264/yuv420p, 429 frames at 24 fps, 17.875 seconds, stereo 48 kHz AAC. This proof contains **P01**, not P02; P02 belongs to the separate later-performance proof and is outside this verdict.

## Chronology and sustained vowel

The encoded cuts and plate order match the first 17.875 seconds of the preserved [Short schedule](../../current/camera_shots_experimental.json), placed at full-song 100.375–118.250 seconds. Frame numbers below are zero-based within this proof; the historical handoff uses one-based Short frames.

| Shot | Proof interval / frames | Finding |
| --- | --- | --- |
| S021 | 0–5.750 s / 0–137 | Withdrawn waiting-room close view; her down/away gaze and his concern remain legible. |
| S022 | 5.750–9.750 s / 138–233 | Wider physical distance, still before the later embrace. No erroneous return from established contact. |
| S023 | 9.750–14.125 s / 234–338 | Supplied limited mouth drawings, then the uninterrupted rounded vowel. |
| S024 | 14.125–17.875 s / 339–428 | Immediate worried waiting-room reaction; no closing performance drawing inserted before the cut. |

[Exact cut frames](r4-performance-sequence/exact-cut-context.jpg) confirm the actual picture boundaries. Independently executing the original pure `exposures()` function from the hash-verified [native source](../../current/native_animation.py), with its original word timings, gives **105/105 agreement** with the selected P01 pose instructions. Inspection of [all 105 encoded performance faces](r4-performance-sequence/all-105-performance-faces.jpg) confirms the rounded drawing remains visible from proof f305 through f338, including the corrected last 19 frames f320–338. The final performance exposure is historical one-based frame339 / full-film zero-based frame2747; reaction begins at full-film frame2748 (114.500 s). This preserves the specific R4 sustained “you” correction.

## Face and eye compositing

At normal 960×540 size and in the sequential face crops, the mouth substitutions remain registered to the face. No conspicuous rectangular patch edge, leftover second mouth, displaced nose/chin, migrating moustache or detached lip was found. The hard exposure changes are deliberate drawn poses; the retained small vocabulary is sufficient for this scoped reuse and is not being judged as continuous phoneme-complete lip sync. Hands, microphone and body are held artwork here, not newly animated performance.

Both original brief blink treatments were inspected through every transition frame in [S021](r4-performance-sequence/s021-blink-frames.jpg) and [S024](r4-performance-sequence/s024-blink-frames.jpg). The endpoints return to the same face with no local patch displacement, rectangular edge or persistent second eye. **The original linear half-opacity transition does produce a briefly blended/doubled eyelid** on local shot frames45/49 and66/70. Each lasts one 24 fps exposure; it is inherited from the source's two-frame fade, not an invented new blink or a lasting compositing ghost. The facial anchors and worried/withdrawn expressions remain stable. A literal “no ghosted pixels anywhere” claim would be inaccurate.

**Remaining framing correction:** [first performance frame](r4-performance-sequence/normal-size-f234.jpg) has visible crown margin; [last performance frame](r4-performance-sequence/normal-size-f338.jpg) clips the top hair tips under the centered 1.015→1.075 push. The [original plate at playback size](r4-performance-sequence/original-p01-at-960.jpg) retains those tips. Preserve all exposure/cut times and reduce or reposition this camera push. This is a small camera defect, not grounds to regenerate the face or reject the recovered drawing method. The original Short camera movement itself was not reproduced exactly, and this review does not claim that it was.

## Actual playback and scope of evidence

An independent local Chromium **154.0.8037.57** run played this exact file at **1×**, audio enabled, in a **960×540 CSS-pixel** video element. It reached 17.875 seconds in approximately 18.016 wall seconds, with no error, zero dropped/corrupted frames, and all 429 media-time frame callbacks. There was one initial `waiting` event at time0 followed about26 ms later by `playing`; no later waiting/stalled event occurred. The cumulative browser counter was433, which is not substituted for the independently decoded 429-frame stream count. [Playback telemetry](r4-performance-sequence/playback.json) records the distinction. Captured player views were inspected at approximately [2 s](r4-performance-sequence/playback-2.0s.jpg), [12.9 s](r4-performance-sequence/playback-12.9s.jpg) and [14.3 s](r4-performance-sequence/playback-14.3s.jpg); exact capture brackets are recorded.

The render manifest reports the original-master excerpt at100.375 s, waveform correlation **0.9997076938** and zero measured lag. Those audio results are attributed to the render's existing check, not independently remeasured here. Browser execution and inspected chronological images establish technical cadence and visual findings; **no human-equivalent continuous audiovisual perception or subjective listening is claimed**. Neither the limited drawings nor 13.875 seconds of exposure-sequence coverage establishes continuous full-body animation, P02 quality, all-film lip sync or completion of the full music video.

[Encoded checks](r4-performance-sequence/encoded-checks.json), [frame reproduction script](r4-performance-sequence/reproduce_review.py) and [playback script](r4-performance-sequence/playback_check.py) make this review reproducible. Evidence uses compact JPEGs and small JSON files. Original sources, code, timing and edit configurations were not changed by this review. No provider call or credit spend occurred.

## V2 camera-only correction — final scoped recommendation

Separately reviewed [v2 proof](../exports/Join_Me_in_Life_Short_Performance_Reuse_Proof_v2.mp4), SHA-256 **`358c833898f0bb6b1aaa0184a5adf8c8bcd6f413cd5a1eb0211e8045f159d817`**. **Use v2 for this S021–S024 sequence: the identified camera defect is corrected, with the restored drawing exposures and narrative cut intact.** This is a bounded sequence recommendation, not approval of the separate P02 proof or completion of the full film.

The sole changed camera is S023, now 1.015→1.035 at center(0.5,0.49). Actual encoded [first](r4-performance-sequence/v2-normal-size-f234.jpg), [middle](r4-performance-sequence/v2-normal-size-f286.jpg) and [last](r4-performance-sequence/v2-normal-size-f338.jpg) performance frames retain visible crown margin, both hands, microphone, mouth and chin. The final rounded vowel remains intact immediately before the unchanged [reaction cut](r4-performance-sequence/v2-normal-size-f339.jpg). No new framing or visible patch-registration defect was found in these focused samples.

Independent decoded frame-hash comparison confirms **exactly105 changed picture frames, f234–338, and zero changed frames elsewhere**. Both files decode to429 frames; manifest drawing/exposure records are equal. Demuxed AAC packet-stream hashes are equal (`a6862c6bf3f7c52b98677917283ed82d811466bf01099636c9a5bef2a7161cc2`). These findings isolate the change to the intended camera shot and retain the original audio. [V2 focused checks](r4-performance-sequence/v2-focused-checks.json) record the results. The full v1 browser run was not repeated or relabeled as a v2 playback/listening test; the inherited blink-blend and limited-animation scope above still apply.
