# Provenance and licenses

This is a private four-take quiet-motion adaptation of the studio's successful
I2V v1 / A2V v5 runtime, itself adapted from AIQUEST Academy / TeamAIQ's
`ltx-2-3-a2v-q4-kaggle.ipynb` at Colab-notebooks commit
`04923c1446bc32f01e3649a526e3a8e19c5607a6`, notebook SHA-256
`17e4b2b325eaccb6d2e540be65f8bf6b76e82f640381f9f637cb7a933e697913`.
The unchanged notebook is retained as attribution/engineering evidence only;
none of its UI, launch, shell setup or public Gradio code is executed.
No LICENSE/COPYING file was found in the complete pinned repository tree.
Do not describe it as MIT/Apache licensed or remove its creator attribution.

The backend is DeepBeepMeep's WanGP/Wan2GP, pinned to
`b8880bd5d292edfbe2384f5c951d95757ad59ea0`. The source-only vendor ZIP preserves
original notices and the **WanGP Community License 2.0** in `LICENSE.txt`, plus
the retained third-party license texts. A separate copy is in
`vendor/LICENSE.WanGP.txt`. This license allows private use/modification and
requires credit when directly selling/licensing outputs; its limitations on
paid hosted/white-label resale remain. This diagnostic offers no such service.
Lightricks/Alibaba and other upstream source notices remain in their files.

The converted weights are from **DeepBeepMeep/LTX-2**, exact revision
`1798f80b3340d2f87cffae42f9fa5367d0963d0c`; this is community Q4_K_M / Quanto
conversion, not an official byte-identical checkpoint. `model-lock.json`
records every selected file's size/SHA-256 from public Hub metadata or actual
small JSON metadata bytes. Neither LTX nor Gemma weights were fetched in local
preparation. The LTX-2.3 model card identifies the **LTX-2 community license**;
the official text is retained as `vendor/LICENSE.LTX-2.txt` with pinned source
URL/hash in `vendor/license-fetch.json`. Gemma retains its separate
[Gemma Terms](https://ai.google.dev/gemma/terms); its converted model card is
preserved. These model terms are not replaced by the backend's license.

Adaptations: private CLI and four selected 145/161/201-frame quiet-motion jobs; managed-Torch
pipless bootstrap; strict source/patch/weight/input hashes; hard failure on
missing dual-T4 layout, precision patch failure, non-finite latents or changed
first/last guide bytes/index in either stage; fixed 512-pixel/64-frame VAE tiling;
sequential Gemma/video residency from v5; no automatic OOM retry; no public
server, prompt enhancement, NIM/chat call, account token or new model. The
source notebook's dynamic resolution, duration snapping, UI and model-audio
mux choices are not used. No waveform is supplied. The backend still performs
joint audio/video generation, but the model audio is discarded and the only
output movie must have exactly one video stream and no audio stream. The A2V
source and all its strict full-audio coverage checks remain unchanged.

The first source archive retrieval unexpectedly included an unrelated 28 MB
SeedVC binary. It and the downloaded archive were removed immediately; neither
was executed, used, retained in this package or fetched again. The 260-file
source-only allowlist excludes all model binaries. This incident is not
misreported as an intentional LTX/Gemma weight download.

Project artwork remains the studio's supplied material. Only four reviewed source PNGs are staged, each reused as its own first/end
guide. Per-take source provenance and non-overlapping editorial portions are retained.
No song excerpt, master, or model audio is staged or written by this package.
No motion output has been accepted by preparing this diagnostic.
