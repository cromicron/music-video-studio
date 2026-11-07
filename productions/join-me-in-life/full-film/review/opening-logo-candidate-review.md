# Opening logo candidate — independent review

Reviewed 2026-11-07 UTC. This is a 6.5-second opening **animatic excerpt**, not finished character animation. Reviewer did not change the editor, source artwork, or protected full animatic.

## First candidate

Current SHA-256: `d3403488a6ddc05d8eae3bb0a26555aa6441d7c18422a6f4b5da679ef2f41d9e`. Native-frame inspection initially used `900a3166680e25b10b35ef6ba09de4bf09c5ac63dedf41232d8b3abe79e807a7`; editor owner confirms the replacement corrected container/report labeling only, with cached picture/audio unchanged. The first label called this a full animatic; the current label correctly calls it a review excerpt.

**Verdict: original graphic and fade restored; revise placement and title grouping before adopting the opening.**

- The exact silver original `current/assets/Band_Logo_Original.png` (SHA-256 `44be7217a5624970a97841af3d2e2971a04378300bf796068be055f1c99e602f`) is scaled and screen-composited, rather than replaced by ordinary type. Its proportions are intact, with no visible clipping.
- Source comparison with `current/finish.py` confirms the original wordmark fade: starts 0.35 s, fully visible 0.75 s; fades out 4.15–4.80 s, screen opacity 0.94. Extracted frames at 0.333, 0.500, 0.750, 2.000, 4.500 and 4.833 s agree with that envelope. R4 portrait placement/relative size is not literally copied to this landscape frame.
- At native 960×540 the wordmark can be read, but thin silver strokes overlap similarly bright snowy branches in the upper left. Recognition falls sharply in the 480-pixel-wide comparison images. This is a contrast/composition weakness, not a malformed logo.
- The song title is unclipped and readable at native size. However, lower-center placement separates it from the upper-left logo, and its later 0.7–5.2 s envelope leaves the title behind after the logo disappears. R4 used the title beneath the logo and the same 0.35–4.80 s envelope for both. Restoring that compact grouping is the better continuation of the existing identity.
- The hospital entrance remains visible; there are no characters or anatomy in this opening to assess. The underlying still camera move is planning motion only.

Evidence: `opening-logo-candidate-contact.jpg`, `opening-logo-independent-timing.jpg`, six `opening-logo-independent-*.png` native extracts, and source compositor/title definitions. These are chronological image inspection and code timing checks. No normal-speed perceptual playback, audio listening, or animation acceptance is claimed for this candidate.

Protected full animatic independently remains SHA-256 `d3f66f4feebc401438218345d61889650418a65a5d3f6afb014720c8369550cb`.

## Revised candidate v2 — targeted pass

File: `exports/Join_Me_in_Life_Opening_Logo_Candidate_v2.mp4`, SHA-256 **`d25f20318fe517f15257025b4d464aec967d04d313ad3e8c8ce0cc3141e099a8`**. 960×540, 24 fps, 156 frames, 6.5 seconds.

**Pass for this opening branding treatment.** The original silver wordmark is now over the darker upper façade, clear of the main white branches. The serif song title sits directly beneath it. Both are readable in the native frame and remain identifiable in the 480-pixel comparison images; the finer silver details naturally become less distinct at thumbnail size. Neither graphic is clipped, distorted, or masking the hospital entrance. This arrangement is an appropriate landscape adaptation of R4's logo/title grouping, not a claim of identical coordinates or relative scale. The actual R4 export at 2 seconds was also extracted and visually compared (`opening-logo-r4-reference-2s.png`).

Chronological frames at 0.333, 0.500, 0.750, 2.000, 4.500 and 4.833 seconds confirm that the pair now appears and disappears together. Both are absent before the fade, visible together during it, fully established by 0.750 seconds, and gone at 4.833 seconds. The current compositor confirms the shared original 0.35–0.75 and 4.15–4.80 second fades. The former late, detached title has been removed. Evidence: `opening-logo-v2-independent-timing.jpg`, `opening-logo-candidate-v2-2s.png`, and `opening-logo-v2-browser-2s.png`.

Independent local Chromium **player telemetry** ran this exact file at 1×, unmuted, volume 1, through `ended` at 6.5 seconds (6.62 seconds wall time). It reported 156 presented/processed video frames, zero dropped frames, no media error, and no waiting/stalled event. See `opening-logo-v2-browser-telemetry.json`. This establishes successful playback in that player and supplements image inspection; it is not a subjective normal-speed audiovisual viewing/listening claim. The six extracted frames do not independently inspect every temporal transition, and the underlying still shot offers no character movement to accept.

The pass applies only to this separate 6.5-second branding excerpt. The existing full animatic is still a planning cut, and its file remains unchanged at SHA-256 `d3f66f4feebc401438218345d61889650418a65a5d3f6afb014720c8369550cb`. V1 and the source logo also retain their recorded hashes. No production footage or source assets were altered by this reviewer.
