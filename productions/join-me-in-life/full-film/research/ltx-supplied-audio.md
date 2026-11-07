# LTX supplied-song conditioning: supported mode and bounded comparison

Research: **7 November 2026 UTC**. Public documentation and source inspection only; no account calls, model downloads, GPU execution, implementation or spending in this investigation. Builds on [free GPU research](free-gpu.md) and the [actual 13B pilot review](../review/ltx13b-bridge-pilot-review.md).

**Yes: LTX-2.5 can generate video conditioned on an existing song excerpt.** This is a distinct audio-to-video pipeline, not merely generated audio attached to video. The current official public HF Space does **not** expose this input. A dedicated community LTX-2.3 dual-T4 notebook supplies a concrete lower-memory implementation, but its published notebook has no saved execution outputs. Neither proves good anime singing, clean hands, or superior performance on our shot.

## Verified contracts

| Route | Existing audio and image inputs | What is established |
| --- | --- | --- |
| Official 2.5 open-source A2V | Audio file; optional image/keyframes; prompt and explicit frame rate. | Audio is encoded as conditioning and frozen during **both** generation stages. Original decoded waveform is returned; audio is not resynthesized. |
| Current official 2.5 HF Space | Prompt, one image, dimensions, frames, seed, decoder and duration controls. | **No supplied-audio input**, last-frame input or multi-reference input in its `generate` contract. Generated audio in its output is not evidence of A2V support. |
| Dedicated community 2.3 Q4 Kaggle A2V notebook | Prompt, optional **first image**, input audio, seed, duration/resolution/aspect and match-audio-duration switch. | Real waveform-to-audio-latent conditioning verified in the pinned backend. This wrapper exposes no end-image control. Output muxing may use decoded model audio, so it must not replace our original stereo master. |
| Official hosted A2V API | Required `audio_uri`; optional `image_uri`; optional `last_frame_uri` requires first image. Prompt required without image. | Supported, separately billed API; not part of the free recommendation. No API call was made. |

### Official open-source 2.5

The [official Audio-to-Video guide](https://docs.ltx.io/open-source-model/usage-guides/audio-to-video) describes `LoadAudio → TrimAudioDuration → LTXVAudioVAEEncode`, retaining that audio latent in both stages, decoding only video, then attaching the trimmed original waveform. Its [2.5 distilled ComfyUI graph](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/2.5/LTX-2.5_A2V_Two_Stage_Distilled.json) uses guidance 1 in both stages. This is a music/speech/ambience input, not just a reference voice.

The current official Python implementation is [`A2VidPipelineTwoStage`](https://github.com/Lightricks/LTX-2/blob/4f521619ae0029e8fbb64d555030c2b121a33b4f/packages/ltx-pipelines/src/ltx_pipelines/a2vid_two_stage.py), pinned to `4f521619ae0029e8fbb64d555030c2b121a33b4f` (4 November 2026). Its call takes:

```text
prompt, negative_prompt, seed, height, width, num_frames, frame_rate,
num_inference_steps, video_guider_params, images,
audio_path, audio_start_time=0.0, audio_max_duration=None, ...
```

At the inspected revision, lines 241–287 load and encode the supplied audio; lines 474/483 set `freeze_audio=True` in both stages; line 488 disables the audio decoder; line 496 replaces output audio with the original decoded source waveform. A stale class comment says stage two refines audio: the actual implementation and current guide establish the opposite. Returning the decoded source waveform does not mean a later MP4 AAC encode is bit-identical to the input file.

The [CLI argument implementation](https://github.com/Lightricks/LTX-2/blob/4f521619ae0029e8fbb64d555030c2b121a33b4f/packages/ltx-pipelines/src/ltx_pipelines/utils/args.py) exposes required `--audio-path`, `--audio-start-time`, and either `--audio-max-duration` or `--num-frames`. Frames follow the `1 + 8k` grid; two-stage image dimensions must be multiples of 64. Verify actual decoded duration rather than assuming an audio duration maps to an identical video duration.

Repeatable `--image PATH FRAME_IDX STRENGTH [BINDING] [CRF]` supports actual timeline keyframes. In automatic binding, frame zero replaces the initial latent and later frames are guide keyframes. Thus a first frame and an end guide at frame 96 can accompany a 97-frame audio-conditioned clip. A guide is not a guarantee that the final drawing is copied exactly. This is not an arbitrary identity-reference/ingredients contract. The official Python dev-checkpoint plus distilled-LoRA route and the distilled ComfyUI graph are different setups; do not mix their load requirements or infer identical sampling schedules.

### Access and hardware limits

The official [system requirements](https://docs.ltx.io/open-source-model/getting-started/system-requirements) list **32 GB+ NVIDIA VRAM, 32 GB RAM and 100 GB disk**, with A100/H100 recommended. The Python A2V pipeline hardcodes BF16. Two 16 GB T4 cards are not a shared 32 GB allocation and do not provide native BF16/FP8/NVFP4 execution. CPU/disk offload and community precision adaptations can alter the minimum; the official guide does not demonstrate a dual-T4 A2V runtime.

The [official Space source](https://huggingface.co/spaces/Lightricks/LTX-2.5/blob/c42e4cd512ec0a861024699f031538eb7bf093a7/app.py) was read without calling it. At revision `c42e4cd512ec0a861024699f031538eb7bf093a7`, its signature is `generate(prompt, image_path, height, width, num_frames, seed, decoder, auto_len=False, progress=...)`. Source SHA-256: `9cb16da2545228511423c0d3394519445ddc035f9e7a3e4410eddf04afbeecdb`. The existing public endpoint cannot perform this experiment unchanged.

The [hosted API](https://docs.ltx.io/api-documentation/api-reference/async-video-generation/submit-audio-to-video) supports `POST /v2/audio-to-video` on `ltx-2-5-fast`, `ltx-2-5-pro` and `ltx-2-3-pro`; 2.3 Fast is excluded. Supplied audio determines duration, minimum two seconds; supported maximum varies by model/resolution. [Published pricing](https://docs.ltx.io/pricing) is $0.09/$0.12/$0.06 per second respectively at 720p. These are paid API prices, not free Space or Kaggle access. No API provisioning is needed for the proposed free test.

## The specific T4 implementation, and its evidence limits

The already-cited TeamAIQ repository contains a dedicated [`ltx-2-3-a2v-q4-kaggle.ipynb`](https://github.com/TeamAIQ/Colab-notebooks/blob/04923c1446bc32f01e3649a526e3a8e19c5607a6/kaggle_notebooks/ltx-2-3-a2v-q4-kaggle.ipynb), inspected at repository commit `04923c1446bc32f01e3649a526e3a8e19c5607a6` (29 October 2026). It has ten cells and **zero saved outputs**, so its title and code are implementation evidence, not a measured successful run.

It uses a roughly 11.8 GB Q4_K_M converted transformer from `DeepBeepMeep/LTX-2`, Gemma on the second T4, FP16 transformer handling, FP32 VAE/upsampler fixes, audio-VAE dtype alignment and numerous device/precision patches. This is not the official unmodified BF16 checkpoint. It pins WanGP to `b8880bd5d292edfbe2384f5c951d95757ad59ea0` and documents failures with other revisions; preserve those pins and audit patches rather than installing latest blindly. Remove public Gradio sharing when adapting to our private batch controller.

Its wrapper reads the audio with SoundFile, averages stereo to mono, and passes `input_waveform`, `input_waveform_sample_rate`, and `audio_scale=1.0` to `ltx2_model.generate`, alongside `image_start`, prompt, dimensions, frames, 24 fps, seed, two stages and eight sampling steps. This is substantive conditioning: the [pinned backend](https://github.com/deepbeepmeep/WanGP/blob/b8880bd5d292edfbe2384f5c951d95757ad59ea0/models/ltx2/ltx2.py#L1125) encodes the waveform and creates `AudioConditionByLatent` at line 1210. A too-short waveform instead selects `AudioConditionByLatentPrefix`, potentially leaving a tail without full audio conditioning. Assert the actual encoded audio covers the requested latent span. A blank `audio_prompt_type` in this direct wrapper does not disable the waveform path.

The wrapper exposes only a first image. It offers matching frame count to audio, but no end-image field; do not advertise last-frame control without an explicitly reviewed extension. Its resolution helper rounds to 32 while the backend rounds to 64, so choose dimensions divisible by 64 explicitly and record any source fitting. Its mux prefers returned model audio and only falls back to the input waveform; preserve our original song separately in FFmpeg.

The existing TeamAIQ **2.5** notebook at the same commit supports first/end images but does not expose supplied audio in its generation wrapper. The current [WanGP LTX handler](https://github.com/deepbeepmeep/WanGP/blob/f0b54e02aa32b539e7be5c65cf4ada67db69da26/models/ltx2/ltx2_handler.py) (6 November 2026 revision) does expose soundtrack conditioning and start/end controls. That is a possible 2.5 adaptation, not a verified T4 run of the older notebook. MSR image-reference modes impose additional combinations/LoRA constraints and are unnecessary for this first diagnostic.

No inspected source supplies a measured T4 A2V speed or acceptance yield for our material. The earlier jigs10 estimate of 15 minutes per five seconds concerns its general 2.5 workflow; it cannot be relabelled an A2V benchmark. Our measured 13B time, 146.681 seconds generation / 815.988 seconds cold total for 4.033 seconds, also cannot predict 2.3/2.5 A2V speed.

## Demonstrated singing: useful precedent, not acceptance

A [30 January 2026 creator post](https://www.reddit.com/r/comfyui/comments/1qrgro0/ltx2_full_i2v_lipsync_video_local_generations/) describes an entire local LTX-2 music video, “Carved My Heart,” generated from an existing Suno song with per-shot audio offsets and an [AudioSync I2V workflow](https://github.com/RageCat73/RCWorkflows/blob/main/011426-LTX2-AudioSync-i2v-Ver2.json). The creator reports useful mouth/breath synchronization but also face-color/eye drift, background people lip-syncing, and increasingly static choices; discussion specifically criticizes acting energy in a high-energy section. This is a primary workflow account for older LTX-2, **not** a 2.5, T4 or screamed-anime benchmark. This research read the account/workflow references; it did not independently play and approve that film.

A current [2.5 lip-sync implementation](https://github.com/UCHIJ/LTX2.5-LipSync/tree/42bde0a0773b59c96cc4aaac019e238ccd3081fa) (4 September 2026) explicitly retains the supplied audio latent through both stages to prevent second-stage drift. It supplies implementation corroboration, not a measured T4 or metal-performance result. No source inspected establishes reliable hand anatomy or our character's singing quality.

## Recommended next comparison — one clip, not production

For the actual available dual T4s, **choose the dedicated pinned 2.3 Q4 A2V path as the next bounded diagnostic**. Its exact supplied-audio plumbing and smaller transformer make it a more concrete T4 starting point than assuming the general 2.5 notebook already implements A2V. This is an engineering-risk choice, not a claim that 2.3 looks better. Retain 2.5 as a subsequent same-input comparison once a compatible runtime is demonstrated; do not claim a newer model wins without its clip.

1. Use the actual take-49 song excerpt for one bridge plea, not a synthetic voice or a text instruction to sing. The edit places S044 at **207.875 s**, but that is an editorial boundary, not verified phoneme timing: inspect/listen to the phrase and record the chosen exact offset. Save a PCM conditioning excerpt, its hash/sample rate and relationship to the untouched stereo master.
2. Request **97 frames at 24 fps (4.041667 s)**, seed 49, explicitly **896×512**, fitting the source without stretching or clipping the hand. This is close to the previous 864×480 diagnostic while obeying the two-stage grid. Check runtime memory first; an OOM is a technical failure, not permission to silently shrink frames or change the comparison. Assert full audio-latent coverage rather than the prefix fallback.
3. Use the existing reviewed bridge start drawing `bridge_plea_start_candidate.png`, SHA `2fa46ef059bc3e0327c08b2252df5757140e92e97a1496f5cc5c1d9a4cba2840`. The dedicated wrapper is first-frame-only: state that difference from the 13B endpoint-conditioned test. Ask for one restrained, supported pleading action and articulation matching the supplied performance; **do not force the mouth permanently open**. Keep microphone/hand geometry visible enough to judge. No new MSR/voice LoRA is needed.
4. Preserve source master audio for the review mux and eventual edit. Record exact code/model revisions, converted-weight provenance, dimensions, frame count, first-frame binding, precision patches, duration, cold/generation time and actual quota. Stop after this single result for independent review. If it succeeds technically, an optional matched 2.3 audio-disabled control can isolate the effect of audio conditioning; changing model, fps and conditioning together otherwise does not establish causation.
5. Judge actual 1× playback with song plus every suspect frame: phrasing/consonants, direction/energy of the plea, face/chin stability, finger count, rings, supported shoulder/elbow, grip and endpoint. Do not infer correct singing from rhythmic mouth movement. Do not turn a valid still or source waveform preservation into motion approval.

The existing 13B take (SHA `32e20fd1388ea390b910541384beb79808b958ea5eccab9ff8f5223f2f3c0a29`) proves an executable free pipeline and substantial arm movement. Its independently sufficient defects are finger/ring discontinuities and final mouth/chin ghosting. Its silent mouth articulation has **not** been matched against song phonemes, so ordinary closures alone do not establish bad lip sync. Audio conditioning addresses that untested temporal-control question; it does not inherently repair anatomy. No clip from either newer model is accepted yet, and no full-film capacity estimate should assume otherwise.
