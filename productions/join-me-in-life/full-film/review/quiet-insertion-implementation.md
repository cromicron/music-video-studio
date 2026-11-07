# Quiet arrival and held-contact insertion — implementation evidence

**The two approved source intervals are inserted; exact editorial acceptance remains pending.** No timeline boundary changed. Editor v1.6.1, original/art-only configs, frozen source reviews, earlier source/sequence approvals, the preserved animatic and 1080p cache remain unchanged. Only S013/S030 production descriptions/status and S030’s fallback camera setting changed; selected video uses the existing full-image contain policy.

| Selection | Timeline frames / master time | Source frames | Treatment |
|---|---|---|---|
| A06 → S013 | [1447,1596) / 60.291667–66.500000s | [3,152), 149 frames | Anxious inward pause, retained door-bar grip; sustained eye closure accepted as a pause, not a brief blink. |
| L05 → S030 only | [3526,3624) / 146.916667–151.000000s | [3,101), 98 frames | Tired blink with held contact. Native push-in/pull-back and crown/lap crops retained; not a locked-camera or demonstrated breathing success. |

Both play once at natural 24fps, with **zero additional hold, loop, retiming, crop or zoom**. Full 896×512 sources become 944×540 with 8px symmetric side bands. L05’s release/point/regrip tail and all S032 use are excluded. S032 remains the existing unfinished still. L04 and original full-width L01 are not selected; separate derivative review implies no adoption here.

Configuration SHA256: `526f9c8713c7a8a0ee62cbf5e7701a2fb80964fae6a1386051000de903615db1`. Approval snapshot SHA256: `52865c09fb58be10c76ec3423f079df0f6ba8fda536814549726922ebdccfa4b`. [Exact input snapshot](quiet-insertion-proof/snapshot.json), [bounded config diff](production-continuity-diff.json), [technical checks](quiet-insertion-proof/technical-checks.json).

| Exact original-master proof | Frames / duration | Master start | SHA256 |
|---|---|---|---|
| [Arrival Contain](../exports/Join_Me_in_Life_Arrival_Contain_Proof.mp4) | 149 / 6.208333s | 60.291667s | `8c772116797166ac5a7c1e2d43cc6438f55916c17244bb5733ab5ad3d0fc8fc8` |
| [Arrival Chorus Context](../exports/Join_Me_in_Life_Arrival_Chorus_Context_Proof.mp4) | 451 / 18.791667s | 56.000000s | `eede37caeb2f083b7decd6fed8297d3228383ed39162c328c5d97ef721efa698` |
| [Held Contact S030](../exports/Join_Me_in_Life_Held_Contact_S030_Proof.mp4) | 98 / 4.083333s | 146.916667s | `daf445b7c5108c0ba718b31a944e7f7806e3d338c17a033130aa04a1b5d41b13` |
| [Held Contact Context](../exports/Join_Me_in_Life_Held_Contact_Context_Proof.mp4) | 396 / 16.500000s | 142.666667s | `f3874cfaf2116ae66f8fec4cf5b65881657d591cfb38772e1ab067da4c317230` |

All four exports fully decode at 960×540/24fps with exact frame counts. Original-master waveform correlations are 0.999783378,0.999730350,0.999656895 and0.999550835 respectively; every measured lag is 0.0s. The source audio is encoded once to AAC256k; no packet-identity or subjective listening claim.

An independent frame-index reconstruction explicitly selected each source’s zero-based frame interval, scaled to 944×540 and padded 8px per side. **Every 149/98 decoded standalone frame exactly matches that reconstruction**, and every selected frame also exactly matches its context export at local offsets 103/102. No rejected tail frame is present. [Frame correspondence](quiet-insertion-proof/frame-correspondence.json) verifies selection and cadence, not aesthetic quality.

All four complete proofs actually played at 1×, unmuted, in headless Chromium. They ended normally with 149/451/98/396 reported frames and no media error. The arrival/chorus context reported 2 dropped presentation frames; the other three reported 0. Brief initial waiting events occurred at startup, with no later stalled event. Encoded frames and source correspondence passed independently; browser presentation counters are not encoded-frame loss. [Telemetry](quiet-insertion-proof/playback-telemetry.json) is technical execution, not human-equivalent continuous viewing or listening.

Implementer inspected the actual [arrival cuts](quiet-insertion-proof/arrival-context-cuts.jpg) and [held-contact cuts](quiet-insertion-proof/held-context-cuts.jpg). Containment adds no new source crop; the known native crown/lap limitations remain visible. The hospital exterior separates the newly moving S030 from the still S032, with no rejected pointing/regrip action carried over. Independent reviewers must judge actual pacing, stylistic transition, source-camera movement and adjacent cuts; these frame checks do not promote the edit.

Full candidate stays 6667frames with the original 277.776s song. New accepted/inserted source now totals 31.666667s, of which 21.375s already had scoped placement reviews; these latest 10.291667s still require them. 83.416667s of the 115.083333s target remains without accepted source. M01 contributes 5.041667s historical video; drawings 32.666667s, lead holds 6.458333s, endpoint holds 3.25s and still-camera material 198.708333s stay separately counted. Source and studio structure checks passed. No new broad test suite or provider action was added.
