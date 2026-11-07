# First scream — actual wide insertion review

**Pass for this exact standalone S044 insertion.** The 960×540 export preserves the useful face, microphone contact and rising plea from the adopted source interval. It cuts before the damaged settling, with no added hold, reset, loop or camera push observed. This does **not** approve its joins to the surrounding shots, which are absent from the excerpt, or establish phoneme sync.

Reviewed [actual proof](../exports/Join_Me_in_Life_First_Scream_A2V_Proof.mp4), SHA-256 `62e0300a732c43aee6304cd711f083f6fd197ead38a96bac086fc77f65ed9e90`: **81 frames at 24 fps, 3.375 seconds**, corresponding to source **f4–84 / [0.125,3.500) s** and master **207.875–211.250 s**. The [prior source review](ltx23-a2v-bridge-pilot-review.md) remains unchanged at SHA-256 `89a341ac000767516c29f310566db5cc1e8a062c3f548c22cf396988c945fb92`.

The aspect-preserving resize is 896×512 → 960×549, followed by a centered 9-pixel total vertical trim to 16:9. His face, hair, microphone hand and connected shoulder/arm remain readable. The top crop does not create a new significant framing problem: the high fingertips already exit the source frame, and the face/palm/forearm still communicate the plea. The brief soft moving-finger/ring detail remains the previously adopted limitation, without a new enlargement or crop failure. [Wide sequence](first-scream-sequence-review/wide-sequence.jpg) · [first frame](first-scream-sequence-review/proof-001.jpg) · [moving hand](first-scream-sequence-review/proof-031.jpg) · [last frame](first-scream-sequence-review/proof-081.jpg).

The last proof frame is the raised, coherent source f84. It does not reach source f86's settling or f89–91's conspicuous face/hair/hand breakup. The first frame's brief mouth closure is inherited from the source; this review does not interpret it as a whispered first plea or claim a verified sung consonant.

Verification was focused on the insertion: full decode and all 81 timestamps at exactly 1/24-second spacing; comparison of every output frame with the consecutively advancing source after the same resize/crop; visual inspection of nine wide samples and native first/moving-hand/last frames. Lossy compression and colour conversion prevent pixel equality, and near-held poses give ambiguous nearest-frame matches in some samples; the comparison is not advertised as an exact pixel match. Together with the exact interval/frame accounting and inspected endpoints, it supports preservation of native cadence with no extra holds or reset. [Frame checks](first-scream-sequence-review/checks.json).

Actual sandboxed Chromium 154.0.8037.57 playback of this export at **1×, unmuted, 960×540** completed all **81 frames**, with **0 dropped, 0 corrupted, no error/stall** and 3.375 seconds media duration. [Telemetry](first-scream-sequence-review/playback.json). This records browser execution, not subjective listening or continuous human-equivalent perception. The delivery manifest's original-master correlation **0.999592**, offset **0**, is acknowledged as root's waveform check; it was not repeated here and is not lip-sync acceptance.

Reproduce this focused check with:

```sh
python productions/join-me-in-life/full-film/review/first-scream-sequence-review/reproduce.py
```

The script writes only to ignored `build/first-scream-sequence-review/`. No provider, production configuration, approval manifest or prior review was changed.
