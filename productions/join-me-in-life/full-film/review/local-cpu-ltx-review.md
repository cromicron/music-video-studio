# Independent second review: local CPU LTX output

6 November 2026. Source: `research/local-cpu-test/ltx_cpu_2b_49f.mp4`.

SHA-256: `b30ee7111732fe39530f9ae5a58422c55d54af4df4539bc372af39ea5e1eb815`.

Observed metadata: H.264, 384 × 256, 24 fps, 49 frames, 2.041667 seconds. Inspected 20 chronological samples from frame 0 through frame 48 in the [sequence contact sheet](local-cpu-ltx-sequence.jpg).

**Reject this output; no usable range.**

- **Frame 0 / 0.000 s:** the source woman/window composition is only partly recognizable beneath a noisy, ghosted texture. It is already below a usable clean conditioning frame.
- **Frame 3 / 0.125 s:** the face, anatomy and setting have broken down into unresolved multicolour/grey texture. No coherent eye, mouth, hand or supported head can be evaluated.
- **0.208–2.000 s:** subsequent sampled frames remain incoherent textured noise, with no recognizable controlled character action or stable background. This is a generation/inference failure, not a subtle motion-quality dispute.

The run's metrics record 207.2 seconds for the video stage, but elapsed runtime is not useful output throughput when no frame sequence is usable. This result does not support a claim that the local CPU route can currently produce the finished film.

The conclusion applies to **this file and tested configuration only**. It does not prove every local video model or CPU configuration is inherently incapable. Conditioning, model/scheduler compatibility, and denoising configuration may need diagnosis before another long run. Those implementation checks belong with the producing agent; this reviewer has not identified a specific root cause from the video alone.

Review limitation: chronological frame inspection only, not normal-speed playback. No new generation, account change or credit spending was performed by this review.
