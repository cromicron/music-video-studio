# S053 early dawn prefix — implementation evidence

**Only the reviewed A07 prefix is inserted at S053; exact sequence acceptance remains pending.** JML-027 reassigns this source to the shorter early outdoor slot. The full A07 ending and original L12/L13 full-slot takes remain rejected. No source frame is reused elsewhere. Original configs, earlier proofs/reviews/approvals, editor code, the 1080p cache and active provider jobs remain untouched.

Source `assets/motion/ltx23-dawn-pilots/A07/video-silent.mp4`, SHA256 `1eb004c3e7306da55b479af550481c0fbbb7cf269913e9db16e2ccdc3fc90582`. Select zero-based `[0,89)` only: **89 frames at natural 24fps**, last included index 88, first excluded index 89. This fills S053 `[5842,5931)` / 243.416667–247.125000s. The [frozen salvage review](ltx23-dawn-A07-salvage-review.md) accepts this prefix before foreground walker intrusion, not the obstructed ending. Tired settling/head lowering and passive lap/knee hands remain the accepted action; no claim of proven uneven breathing.

Contain preserves the full 896×512 source as 944×540 plus symmetric 8px side bands at 960×540. There is no added zoom/crop/hold/loop/retiming or fade. Every timeline boundary remains fixed. The full assembled plan selects this exact source only in S053; S056 and S058 remain unfinished stills with no adopted source. Native moving-detail softness is not repaired by enlargement.

Configuration SHA256 `c8470942090e8b10799f135a25710f8947daa3d523fa62fe42fbc396559db832`; approval snapshot SHA256 `c7ed6843ac769e71b92a0eb5b5e9c395b48d161aa7dbf8aafcb87d86700a43d7`. [Snapshot](dawn-s053-insertion-proof/snapshot.json), [bounded diff](production-continuity-diff.json), [technical checks](dawn-s053-insertion-proof/technical-checks.json).

| Original-master export | Frames / duration | Master start | SHA256 |
|---|---|---|---|
| [Dawn Early Company](../exports/Join_Me_in_Life_Dawn_Early_Company_Proof.mp4) | 89 / 3.708333s | 243.416667s | `568f194d3e2a4576262730502647748a1845098e917e84ee71fdffe665b65deb` |
| [Dawn Early Company Context](../exports/Join_Me_in_Life_Dawn_Early_Company_Context_Proof.mp4) | 327 / 13.625000s | 239.666667s | `f69402b57c8fd426debf41b9d19a74508562dfe863e4204e6e49f06f78f9e2f3` |

Both exports fully decode at 960×540/24fps with exact frame counts. Original-master waveform correlations are 0.999582836 and 0.999564606, each at 0.0s measured lag. Audio is AAC256k encoded once from the corresponding original master positions, not packet-identical MP3 or subjective listening evidence.

Every 89 decoded standalone frame exactly matches an independent integer-frame `[0,89)` reconstruction, explicitly scaled/padded and encoded identically. Those same frames equal context `[90,179)` exactly. Thus no later walker frame, repeated frame, extra hold or frame interpolation was introduced. [Frame correspondence](dawn-s053-insertion-proof/frame-correspondence.json) verifies order, crop and cadence, not acting quality. Implementer inspected [actual phases](dawn-s053-insertion-proof/source-phases.jpg) and [both adjacent cuts](dawn-s053-insertion-proof/context-cuts.jpg): the final included picture is unobstructed; courtyard→seated company→empty morning room remains the original order. Independent review must judge its pacing and placement; these checks do not promote the sequence.

The exact standalone and complete S052–S054 context each played at 1×, unmuted, in headless Chromium, ending normally with 89/327 reported frames, zero dropped frames and no media error. Brief waiting occurred at startup, with no later stall. [Playback telemetry](dawn-s053-insertion-proof/playback-telemetry.json) records technical execution, not human-equivalent continuous viewing/listening.

Full candidate remains 6667frames with the original 277.776s master. Accepted new source totals 41.791667s; 38.083333s has prior scoped placement reviews, and this 3.708333s awaits its own. 73.291667s still lacks accepted source. M01 contributes 5.041667s historical video; drawing sequences 32.666667s, lead holds 6.458333s, endpoint holds 3.25s and still-camera material 188.583333s remain separate. No new broad test suite or provider call was added. Render caches stay in separate ignored root `build/` directories; [commands](dawn-s053-insertion-proof/render-commands.txt) reproduce both diagnostics from the named config.

Original-source and studio structure checks pass.
