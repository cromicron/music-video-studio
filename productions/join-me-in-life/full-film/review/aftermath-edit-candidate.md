# Preserve the embrace aftermath in later hospital returns

Editorial configuration and framing check, **7 November 2026 UTC**. This document describes work prepared and checked by the configuration author; it is not a separate independent motion approval. New configuration: `edit-production-candidate.json`, copied from the reviewed `edit-art-candidate.json`. Both prior configurations and all source artwork remain unchanged.

**S030, S032, S042 and S047 now use the preserved embraced endpoint instead of returning to separated poses.** This fixes the planned physical-state regression identified in [Short-to-full continuity](short-to-full-continuity.md). It does not supply the missing reach/pull in S028 or turn the still-art plan into a finished film.

## Reused source and intended continuity

New source key **`hospital_after_contact`** points directly to `../current/assets/M01_Embrace_End.png`, **1916×1080**, SHA-256 **`466bccb17c8862b61c6e84792d46bb6a0730c2222a7aa9d32d5316e90e9c0f10`**. The source was viewed at native size and reused unchanged. No new art, copied/repainted hand, generated frame or provider call was introduced.

His right arm runs behind her, with the visible hand resting on her outer upper arm. Her forearms/hands remain passive in her lap and her gaze stays down and away. Her head remains supported by her own neck; he watches her with concern, without putting his head in her care. The already established contact persists, without a second reach or an emotional cure. The endpoint's slightly different rendering/detail is inherited from the preserved Short; this is not a newly invented character/room plate.

The source already clips a little of his upper hair and distal fingers at the lower image edge. It shows enough wrist/lap and arm contact to establish the intended held state, but it cannot certify unseen fingertips, a complete crown, or the movement into/out of that state. No crop can restore those missing pixels. The upper arm's partly occluded path remains acceptable as a held-pose source; a generated transition still has to prove ownership and contact frame by frame.

## Scoped shot changes

| Shot | Unchanged full-song interval | New framing and intent |
| --- | --- | --- |
| S030 | 146.916667–151.000000 s, 98 frames | Locked **1.045** centered two-person crop. Return to his continuing outer-arm contact and her away gaze. |
| S032 | 155.166667–159.166667 s, 96 frames | Locked **1.000** centered widest framing. Keep the shared held aftermath and passive lap visible. |
| S042 | 199.708333–203.791667 s, 98 frames | Same locked **1.045** framing. His presence continues under the quieter bridge; no pre-contact reset. |
| S047 | 219.375000–223.500000 s, 99 frames | Same locked **1.000** framing. The fourth scream returns to the ongoing hospital contact without suggesting recovery. |

The “closer” view is deliberately only 4.5% tighter than the full-width view, **not a face-only close-up**. A larger crop would discard too much passive lap/hand evidence and further cut the inherited crown. Both cameras are locked: no artificial new push within a held still, no reverse, no loop and no invented body motion. Changes in camera size occur only at the existing editorial cuts.

All 58 shot IDs/order, frame boundaries, seconds, sections, opening title flag, original full-song audio and final fade remain unchanged. The original seven refined-source selections and all unrelated shot objects remain as in the art candidate. The only other shot change is S028's explicit unfinished-action purpose/status notes.

## S028 is still an unresolved production requirement

S028 remains the same **291-frame / 12.125-second separated still placeholder** at 130.541667–142.666667 seconds. Its previous purpose text implying that remaining beside her *without* the embrace was sufficient has been replaced with the required **one continuous reach/contact → torso pull → held aftermath**. It is labelled `UNFINISHED REQUIRED ACTION`; its source/timing/camera are not secretly replaced with the endpoint.

Consequently, rendering this preparation as-is would still jump from an unperformed action to a later held state. **Do not approve that jump as the completed embrace, hide it with another cut, or mark S028 finished because later sources now match the intended aftermath.** Repair and independently review the single uninterrupted action before final sequence approval. This configuration resolves what the later shots should preserve once that action is restored.

## Actual framing verification

The unchanged `edit.py` was imported and its real `still_filter` rendered first/middle/last frames at **960×540** for both distinct camera paths: S032 frames **0/47/95** and S030 frames **0/48/97**, zero-based. The same locked paths apply to their paired later uses. All six frames were visually inspected in compact JPEG contacts, with full-size representative JPEGs also inspected. Exact decoded RGB hashes confirm first/middle/last identity for each locked path; no temporal character movement is claimed.

Both views preserve the entire visible supporting hand and arm contact, both faces from brows/eyes through chin, their neck/shoulder support and the passive lap. The tighter view removes a small further strip of already cropped hair and lower lap, but does **not** cut an eye, mouth, chin or contact fingers. It does not make the source's incomplete fingertips complete. No framing change introduces a head-in-her-care or reciprocal-embrace reading.

Evidence and reproducible script: `build/aftermath-candidate-review/` contains `wide-first-middle-last.jpg`, `closer-first-middle-last.jpg`, two representative JPEGs, `framing-manifest.json`, and `render_frames.py`. No duplicate lossless PNG series or new film export was made.

## Planned tools and model limits

The configuration names **ChatGPT → Owned LTX animation → FFmpeg** as the planned three-tool route. These labels do not claim that the resulting film has been animated or that a particular model has passed quality review. No fake approved-motion manifest was created or modified.

LTX-Video 0.9.8 13B is a video-only pipeline; it does not become supplied-song conditioning by changing a prompt. LTX-2.3/2.5 audio-to-video is a separate supported mode with different weights, runtime and image controls; documented capability is not proof of singing accuracy, T4 throughput, hands, contact or identity on our material. Each actual take still needs its own verified source hash, temporal review and song-aligned performance check where relevant. The four new after-contact entries remain static planning material.

Preserved base identities: `edit.json` SHA-256 `f8d78f4b665ac8ccd51b0fd2e8ac41bfbb2e542501cf15c21db779699a45cc30`; `edit-art-candidate.json` SHA-256 `432c675ce395ac0c11219cf03d02e116b12dc7ab68ac64ffc0041789ba6bdce2`. The new configuration's exact hash is recorded in the framing manifest. No new generation, credits, source artwork, production-editor change or full-cut approval is part of this preparation.
