# P1L09 — fourth-plea held-contact source review

7 November 2026. Independent source review under the retained Be Ambitious outside-review gate. **PASS S045; FAIL S047 and the complete take as a withdrawn continuation.** Her later chin lift and returned gaze toward him add a response that contradicts the required down/away reaction. Stable grip and technically valid playback do not rescue that change.

| Intended use | Zero-based, end-exclusive source frames | One-based frames | Source seconds | Judgment |
| --- | --- | --- | --- | --- |
| S045 | `[3,116)` | 4–116 | 0.125000–4.833333 | **PASS**, 113 frames / 4.708333 s |
| S047 | `[116,215)` | 117–215 | 4.833333–8.958333 | **FAIL**, 99 frames / 4.125000 s |
| Whole take | `[0,225)` | 1–225 | 0.000000–9.375000 | **FAIL** as continuous withdrawn acting |

S045 is cleared only at natural 24 fps with full-image contain framing, once, without extra crop, retiming, loop or hold. S046's stage plea intervenes between the proposed selections. Source approval does not approve the actual S044→S045→S046 cuts, the later replacement/return, or song-context meaning; those remain separate edit reviews.

The [reviewed silent source](../assets/motion/ltx23-positive-continuation/P1/P1L09/video-silent.mp4) is SHA-256 `94c105fb16c8cfdae7ee7e00793b48d7e6dd36196e0689fb8ab3a46e1e4adbd2`: 225 frames, 896×512, 24 fps, 9.375 s.

## Decisive failure and bounded partial candidates

The [native returned-look phases](ltx23-positive-P1L09-review/her-returned-look.jpg) show her starting down/away, lifting her chin clearly by one-based f145 / 6.000 s, rotating toward him through f153–169 / 6.333–7.000 s, and looking up into his direction for roughly f169–188 / 7.000–7.792 s. She then closes her eyes and lowers again, with the down/away pose restored by f209 / 8.667 s. The action is also plainly visible at normal display size in the [S047 playback captures](ltx23-positive-P1L09-review/captured-S047-1.jpg).

For editorial exclusion, use the conservative **`[136,208)` / 5.666667–8.666667 s** region, including the movement's lead-in and return. This is a safe exclusion envelope, not a claim that the first unmistakable upward eye contact occurs at frame 136. The core failure is her new response toward him; there is no need to invent a smile, cure, comforting gesture or complete role reversal to reject it. She remains physically self-supported, but her gaze no longer remains withdrawn away during this passage.

After the passed S045 portion, clean-looking residual candidates are **`[116,136)`**, 20 frames / 0.833333 s, before the head-lift lead-in, and **`[208,225)`**, 17 frames / 0.708333 s, after the return. Within the originally proposed S047 bounds, only `[208,215)` of that tail is available. These are frame-reviewed partial candidates, **not adopted replacements**; they have no dedicated placement/cut or separately trimmed playback verdict. They cannot supply the required 99-frame S047 naturally without reusing earlier action, adding a hold or altering duration. Do not salvage the failed full slot through those devices.

## Why S045 passes, and what remains limited

He rotates from watching her through a near-frontal outward scan around f25–49 / 1.0–2.0 s, then lowers his gaze and closes his eyes around f65–73 / 2.7–3.0 s; his head remains down/turning back at the S045 endpoint. The [native gaze phases](ltx23-positive-P1L09-review/his-gaze-phases.jpg) retain the frontal angle rather than hiding it. His tense brows and subdued mouth read as frightened checking and an inward pause, not confidence or an address/sung line to the viewer. This larger head/gaze movement is accepted as a scoped acting deviation, consistent with the precedent in [R1L05](ltx23-correction-R1L05-review.md); screen direction and motivation still require the actual cut review.

Throughout S045, she remains down/away, depleted, with passive hands in her own lap. Her early eyelid narrowing is subtle; a fully shut brief early blink is not established. His later eye closure is sustained, rather than a quick closed-and-open cycle entirely within S045. Small shoulder/cloth/hair changes are present, but independently timed breathing cycles cannot be isolated confidently. [Her eyelid detail](ltx23-positive-P1L09-review/her-eyelid-detail.jpg) prevents the conspicuous later eye closure inside the rejected action from being counted as an earlier prompt success.

His arm stays behind her and the visible bare hand maintains the upper-arm grip throughout all 225 frames, including the rejected gaze exchange. No release, point, regrip, pull, stroke, head pat or new embrace appears. His other hand stays on his own thigh; both heads stay self-supported and her lap hands do not reach toward him. [Native contact/lap phases](ltx23-positive-P1L09-review/contact-lap-phases.jpg) show the contact and the original bare grip hand. Silver ring detail is on his other hand and becomes partly hidden below the native lower frame edge; that is distinct from an accessory disappearing off the grip hand.

The auburn hair, his light facial hair, wardrobe and pendants remain recognizable. Fine facial/finger detail softens and varies with head angle; there is no gross duplicate person, detached neck or new fused contact hand. The background/composition drifts slightly, so perfectly fixed camera behavior is not established. The native crown and lower-finger edges are tight; [guide/endpoints](ltx23-positive-P1L09-review/guide-endpoints.jpg) distinguish that source framing from a new anatomical loss. Keep the full image; no additional enlargement/crop is cleared.

## Evidence, playback and limits

I inspected all 225 decoded frames chronologically in full-sequence sheets, then native head/eye, contact and lap phases, original/fitted guides, endpoints and actual playback captures. [Overview](ltx23-positive-P1L09-review/overview.jpg) and [S045 captures](ltx23-positive-P1L09-review/captured-S045-1.jpg) preserve both the usable earlier action and the later failure. This is frame/capture inspection, not continuous human-equivalent visual perception.

Error-failing full decode, every timestamp and the silent-stream check pass. Sandboxed Chromium 154.0.8037.57 played all three files at 1×, displayed at 672×384 without seeking:

| Run | Frames | Media duration | Measured wall duration |
| --- | --- | --- | --- |
| Full source | 225 | 9.375000 s | 9.3906 s |
| S045 proxy | 113 | 4.708333 s | 4.7345 s |
| S047 proxy | 99 | 4.125000 s | 4.1607 s |

All ended with zero dropped/corrupt frames and no media error, stall or waiting event. [Telemetry summary](ltx23-positive-P1L09-review/playback-summary.json) and [complete compressed callbacks](ltx23-positive-P1L09-review/playback-full.json.gz) retain source/proxy hashes and screenshot time bounds. Smooth playback is a technical result; the S047 acting still fails. These clips are silent; no subjective listening, audio-sync or phoneme-sync judgment is claimed.

[Checks](ltx23-positive-P1L09-review/checks.json) verify the actual source, all 225 timestamps, identical fitted start/end pixels and all four guide records. Original M01 endpoint SHA-256 is `466bccb17c8862b61c6e84792d46bb6a0730c2222a7aa9d32d5316e90e9c0f10`, 1916×1080. Matching endpoint guidance did not prevent the intervening gaze response.

Reproduce with [reproduce.py](ltx23-positive-P1L09-review/reproduce.py), then [retain_evidence.py](ltx23-positive-P1L09-review/retain_evidence.py). Raw frames, native full sheets and trim proxies live in ignored `build/ltx23-positive-P1L09-review/`. No provider operation, edit configuration or adoption record was changed by this review.
