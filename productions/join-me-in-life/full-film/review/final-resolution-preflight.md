# 1080p production preflight — scoped pass, incomplete film

Rendered the unchanged production snapshot from checkpoint `2af7d097b8bbef483257dd364bf12aca4cd14a40` to `build/production-1080-preflight.mp4`, using dedicated reusable `build/production-1080-cache`. No production configuration, editor, approval or provider changed for this task. The current snapshot still contains 209.0 seconds of still-camera material; later sources and the complete-film review remain outstanding.

| Record | SHA256 |
|---|---|
| 1080p MP4 | `c8fb590f3b84d6d62901d31874c28d8e97188435ed5956212034f2739f32b98c` |
| Production config | `ad8047b88e94267a02ffdd25b3d3d7a16cf2c382e98b89422fc412e8fe6abb10` |
| Approval manifest | `332ba9ab71d3a07e1fe789c8e67329b5a47d7c7b83cd8b1714287814bf48f704` |
| Editor v1.6.1 | `eafd6b5a38a916f72295c86a6605e856437f8b7c445a0ddfc25d68ad26f0a124` |

**Output-specific visual findings.** The original silver logo and title directly beneath it are legible on the dark upper facade at native resolution. Neither is cropped; the entrance remains unobstructed. Chronological frames show both absent at 0.333s, partially visible at 0.5s, fully visible by 0.75s, fading together at 4.5s and absent by 4.833s. This matches shared 0.35–0.75s fade-in and 4.15–4.80s fade-out. See [fade sequence](final-resolution-preflight/opening-fade-contact.jpg) and [native branding crop](final-resolution-preflight/branding-native-crop.jpg).

S014 preserves the complete 896×512 source at 66.5–70.583333s. FFmpeg scales to 1892×1080 and pads 14 pixels on each side; no added crop or camera push. Divisible-by-four rounding changes aspect by 0.106%, without losing source edges. Shoes and reaching hand remain within frame in the inspected first/middle/last samples. The existing native crown grazing persists; contain cannot add missing source headroom. Enlarged moving detail remains visibly soft: this is 1080p delivery, not newly generated 1080p detail. See [chronological whole frames](final-resolution-preflight/s014-first-middle-last-contact.jpg) and [native crown sample](final-resolution-preflight/s014-native-crown.jpg).

**Technical evidence.** Full decode passed at 1920×1080, 24fps, 6667 frames / 277.791667s. Original master SHA256 `0fe0f566e985a0b028e12543679d3b142ee7b1b62425fcb595799b35ba116cbb` was encoded once to AAC256k from source time 0. Waveform correlation is 0.999658987, measured lag 0.0s. No packet-identity or subjective listening claim. Thirteen selected decoded frames from the full MP4 exactly match the inspected shot cache; [correspondence](final-resolution-preflight/frame-correspondence.json) binds the frame evidence to this complete output.

Opening and S014 spans played at 1×, unmuted, in headless Chromium at native 1920×1080 with zero dropped frames, stalls or media errors. [Telemetry](final-resolution-preflight/playback-telemetry.json) records technical execution only; it is not continuous human-equivalent viewing/listening. The first harness attempt lacked HTTP seeking support; fetching the exact same MP4 into a seekable Blob resolved that harness issue. Playback callback counts include boundary/prebuffer frames and do not replace the exact encoded count.

[Snapshot](final-resolution-preflight/snapshot.json) and [verification](final-resolution-preflight/verification.json) retain the exact inputs and accounting: 21.375s new generated video, 5.041667s historical M01, 32.666667s supplied drawing sequences, 6.458333s lead holds, 3.25s endpoint holds, 209.0s still-camera material. This report does not approve missing acting, audio/phoneme synchronization, new source intervals, future joins, or the finished film. The cache is ready for subsequent bounded insertions; changed shot fingerprints will rerender on the next named-config export.
