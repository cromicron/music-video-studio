# Fixed window close-up — implementation evidence

**S003 now contains only the separately reviewed fixed-crop derivative. Actual sequence and neighboring-cut acceptance remain pending.** No source review, approval record, editor code, earlier proof, original/art-only config or 1080p cache changed. Every timeline boundary remains intact.

The selected source is `assets/motion/ltx23-quiet-window-closeup/video-silent.mp4`, SHA256 `5e61ec0d2b686a750e5c36f73fccc646544939dc10673f606153e3d098f8ec20`. Its native 672×378 image is the fixed original crop x224/y0/w672/h378. S003 uses zero-based source `[3,157)` / 154 frames once at natural 24fps, placed at master `[307,461)` / 12.791667–19.208333s. The editor scales the whole 16:9 derivative to 960×540; **no added crop, zoom, hold, loop or retiming**.

The original full-width L01 remains rejected. The fixed crop excludes the faulty reflected eyelids and mouth, while faint peripheral reflected ear/rear cheek/neck/hair remains. This is exclusion, not a repaired reflection. The accepted larger head rise/three-quarter turn and lowered gaze exceed the original minimal-breath request. Native crown limitation and small distant passersby remain disclosed. The [frozen source review](ltx23-window-closeup-review.md) governs only that exact derivative/interval.

Config SHA256 `e32955750fb6c65dcaf81e4304e5896f8d39b1e9c37ab1d397f69fd4095dcec2`; approval snapshot SHA256 `5fd8666276257dccfb2b6de43c1a3aedb488bf4764061b84923daad85052220b`. [Snapshot](window-insertion-proof/snapshot.json), [bounded diff](production-continuity-diff.json), [technical checks](window-insertion-proof/technical-checks.json).

| Original-master export | Frames / duration | Master start | SHA256 |
|---|---|---|---|
| [Window Closeup](../exports/Join_Me_in_Life_Window_Closeup_Proof.mp4) | 154 / 6.416667s | 12.791667s | `dd1c70082c7ccd5bcc0f2dd5df147df0aee340e46695cf66a99c8ee322d8a9b6` |
| [Window Closeup Context](../exports/Join_Me_in_Life_Window_Closeup_Context_Proof.mp4) | 425 / 17.708333s | 6.500000s | `3f42a3a6dcda31c121a6263a2883a743d1273d5bf8d6c425f701731552f0c646` |

Both outputs fully decode at 960×540/24fps with exact frame counts. Original-master waveform correlations are 0.999932130 and 0.999940917, both at 0.0s measured lag. Audio is AAC256k from the original master; no packet-identity or subjective listening claim.

Every 154 decoded proof frame exactly matches an independent reconstruction using frame-index trim `[3,157)` and simple full-frame resize, encoded identically. All 154 also match their context positions at local frames `[151,305)`. [Frame correspondence](window-insertion-proof/frame-correspondence.json) proves selected cadence and absence of an extra crop/hold, not acting quality. Implementer inspected [actual phases](window-insertion-proof/window-phases.jpg) and [adjacent cuts](window-insertion-proof/context-cuts.jpg); the known native framing limit remains, without an added crop from the editor.

Complete standalone and S002–S004 context exports played at 1×, unmuted, in headless Chromium: 154/425 reported frames, normal end, zero dropped frames and no media errors. Brief initial waiting occurred at startup; no later stall was recorded. [Playback telemetry](window-insertion-proof/playback-telemetry.json) is technical execution, not human-equivalent continuous audiovisual perception. Independent reviewers still judge the actual close-up progression, distant background movement, musical placement and cuts.

Full candidate stays 6667frames with original 277.776s master. New accepted/inserted source totals 38.083333s; 21.375s had prior scoped placement review and 16.708333s now awaits it. 77s of targeted new picture remains without accepted source. Historical M01 remains 5.041667s; supplied drawing sequences 32.666667s, lead holds 6.458333s, endpoint holds 3.25s and still-camera material 192.291667s retain separate accounting. This is not a finished-film claim.

Original-source and studio structure checks pass. No editor-code change or new broad test suite was needed.
