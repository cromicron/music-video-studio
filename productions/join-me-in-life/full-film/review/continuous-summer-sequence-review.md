# Continuous summer — actual sequence review

**Visual pass for these exact exports, including the held lead, continuous action and surrounding cuts.** The wide insertion preserves the reviewed shared exchange without a new crop, identity, hand-contact or shot-boundary defect. It contains **five seconds of animation plus a noticeable 2.625-second still lead**; acceptance does not reclassify that lead as motion or establish musical/phoneme sync.

| Reviewed export | Exact picture | Master interval | SHA-256 |
| --- | --- | --- | --- |
| [Summer proof](../exports/Join_Me_in_Life_Continuous_Summer_Proof.mp4) | 183 frames / 7.625s | [118.250,125.875)s | `bac1fdcfe19b9b0c832aa11a60c11773abdb893824d5f60a0875dbd2c33b3f41` |
| [Context proof](../exports/Join_Me_in_Life_Continuous_Summer_Context_Proof.mp4) | 385 frames / 16.041667s | [114.500,130.541667)s | `c58d1d3d8f869167bdd7fe3b4f924b9821ea7dbab63dd19a59ebddeb79d74cac` |

Both are 960×540 at 24 fps. The [source review](ltx23-summer-pilot-review.md) remains unchanged at SHA-256 `6ad7686d1a41100e4b10e06b34079a3dd12de35637748fdc0c859b06d3f20f29`; its all-frame source assessment is not repeated or expanded here.

The centered, aspect-preserving wide crop keeps both crowns, faces, his earbud grip and free hand, her lap clasp and their supported seated bodies. Her green-hazel eyes remain readable when open. The brief chuckle and his responding turn/smile survive at ordinary size. The selected tail retains the previously disclosed facial softness around source 4.375–5.0s, but does not reach the later guide sharpening. No new deformation, disconnected hand or obscured acting beat was introduced by the export. [Wide sequence](continuous-summer-sequence-review/wide-sequence.jpg) · [actual shared response](continuous-summer-sequence-review/proof-136.jpg).

The **63 added first-frame lead frames** occupy master 118.250–120.875s. This is plainly a held establishing picture, with eyes and background still. It works as a quiet memory setup rather than a gesture frozen halfway through; it is the least lively part of the excerpt and should remain counted honestly. At source playback's start the matching pose begins moving without a framing or bodily jump. No additional motion is implied by this judgement.

At master **122.875s**, S025→S026 is only an administrative split: **proof f111→112 / source zero-based f47→48**. The same scale, position, bodies and action continue. There is no repeated start, visible camera reset, jump in hand placement or extra hold. At **125.875s**, source f119 (zero-based) cuts directly to P01; there is no frozen summer tail. [Native lead and split evidence](continuous-summer-sequence-review/native-boundaries.jpg).

The **waiting room→summer** cut clearly changes time/place and tone: the same couple becomes relaxed in the courtyard. Their exchanged screen positions are understandable across that location change, not an accidental spatial jump within one action. The **summer→singer** cut follows the settled shared smile and clearly returns to his fragile present performance. The summer softness gives way to sharper stage artwork, but identity remains readable and the cut is not a face morph. [Surrounding cuts](continuous-summer-sequence-review/context-cuts.jpg).

P01's earlier entrance keeps visible crown clearance and the microphone/contact hand plus chest hand inside frame. All **112 actual P01 face frames** were inspected: the initial closed-mouth exposure and subsequent supplied mouth changes stay registered, without a new patch seam, beard tear or dislocated jaw. The first open exposure appears at master **126.708333s** (P01 f21), consistent with the manifest's unchanged absolute timing. This is limited drawn-mouth performance with a gentle camera move, not new animated body acting. It is not evidence of phoneme-complete sync. [Earlier entrance face sequence](continuous-summer-sequence-review/performance-faces-001-028.jpg).

Independent checks fully decoded both exports, verified every timestamp and compared **all 183 summer output frames** with the expected scaled source: 63 added first-frame lead frames followed by source f0–119. Mean RGB absolute error was **3.282/255**, maximum **3.684/255**, from lossy encoding/color conversion; this is correspondence evidence, not pixel identity or anatomy proof. The summer frames in the context export decode **pixel-identically** to the standalone proof. [Frame checks](continuous-summer-sequence-review/checks.json). Visual inspection used full-frame chronological samples, native boundary/contact detail, all P01 faces and actual browser captures.

Independent sandboxed Chromium **154.0.8037.57** playback at **1×, unmuted, 672×378** completed **183/385 frames**, with **zero dropped or corrupted frames, errors, waits or stalls**. Wall times were 7.726s and 16.146s, including screenshot overhead. [Telemetry](continuous-summer-sequence-review/playback.json) · [ordinary shared response](continuous-summer-sequence-review/playback-proof-5.60.jpg) · [ordinary stage entrance](continuous-summer-sequence-review/playback-context-11.60.jpg). This records executed playback and inspected screenshots, not continuous human-equivalent perception or subjective listening.

The [implementer's waveform checks](continuous-summer-implementation.md) report original-master correlations **0.999503 / 0.999514**, both with zero measured lag; those audio checks were not repeated here. They do not establish musical pacing or lip sync. The visible joins inside this context are accepted; cuts before 114.5s or after 130.541667s and the complete film remain outside this review.

Reproduce the independent evidence from the repository root:

```sh
python3 productions/join-me-in-life/full-film/review/continuous-summer-sequence-review/reproduce.py
```

Dependencies: Python, NumPy, Pillow, FFmpeg/ffprobe, Playwright and `/usr/bin/chromium`. Raw/temporary evidence goes only to ignored `build/continuous-summer-sequence-review/`; selected portable files are retained beside the script. No provider, production configuration, approval manifest or prior source review was modified.
