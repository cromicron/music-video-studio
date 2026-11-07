# Actual free-generation access, tested 6 November 2026

**Latest setup update, 23:13 UTC:** TinyFish actual browser calls verify Flow signed in with 50 daily credits, Kaggle phone verified, with two Tesla T4 GPUs and CLI OAuth tested (29.95/30 GPU hours remained at the last quota read), and Hugging Face signed in with verified email. The agent has enabled official LTX-2.5 model access and verified the access-granted message and file list. Details and exact profiles are in [access setup](../ACCESS_SETUP.md). No Flow generation or Kaggle model generation is claimed; the private Kaggle CUDA infrastructure test succeeded and its session was stopped. Four CPU benchmarks are complete with zero accepted motion clips; see [CPU findings](local-cpu-test/README.md). Earlier signup/CAPTCHA/browser observations below are historical, not current blockers.

An anonymous request to the official **Lightricks/LTX-2.5 Hugging Face Space succeeded**. This is a usable free video-generation path in this environment, not an untested signup offer. A second production request then hit the daily quota. The remaining allowance cannot admit even the smallest supported job, so this route cannot supply the whole 277.776-second film today without a legitimate quota reset or additional authorized access.

## Tested accounts and capabilities

| Route | Live observation | Consequence |
| --- | --- | --- |
| Hedra configured MCP | Authenticated; only one workspace; credit balance 0, subscription 0, credit pack 0; API wallet USD 0.00; billing mode `usd`. Library video query returned no assets. | No available free generation or reusable library footage. No billing mode change or generation submitted. |
| Runway connector | Parent's live account inspection found 1,897 purchased credits, zero plan credits. | Existing purchased credits cannot be described as free credits; no spending by this investigation. |
| Official LTX-2.5 public demo | Runtime `RUNNING`; public Gradio API; anonymous image upload and generation succeeded with no credentials or purchase. | Real image-to-video available now, within the provider's quota. |
| Local environment | Parent verified 5 CPU cores, no NVIDIA GPU, working Blender bpy 5.2.3 and FFmpeg. A real distilled LTX 2B CPU benchmark is now being prepared in an isolated environment. | Local editing works. Full-film neural generation speed and quality on this CPU are not yet established. |
| Browser-only free plans | The prepared Microsoft Playwright CLI was recovered and tested. It controls a cloud browser, not the user's local Chrome. Google Flow is at Google sign-in. Free Hugging Face signup reached a human CAPTCHA. | Browser automation works; authenticated generation through either service has not been established. No purchase or completed account creation. |

The Hedra read-only client at [hedra_readonly.py](../tools/hedra_readonly.py) preserves inherited proxy/CA configuration, sends the configured token only to `https://mcp.hedra.com`, rejects redirects, and exposes only read-only discovery tools. It does not print or save credentials.

## Actual LTX smoke test

- Source: existing `current/assets/S02_Waiting_Closeup.png`; two established characters seated in the hospital waiting room.
- Request: subtle breathing and one blink; camera, heads, arms and mouths held still; same art, faces and clothing. Full parameters are preserved in [the request JSON](free-test/ltx-2.5-request.json).
- Model/demo: [Lightricks/LTX-2.5](https://huggingface.co/spaces/Lightricks/LTX-2.5), demo source commit `c42e4cd512ec0a861024699f031538eb7bf093a7` observed before generation.
- Settings: 896×512, requested 5 seconds, 24 fps, seed 49, convolutional decoder, fixed duration, prompt enhancement off.
- Actual output: [LTX25_waitingroom_free_5s.mp4](free-test/LTX25_waitingroom_free_5s.mp4), **121 frames / 5.041667 seconds**, H.264/yuv420p, 418,142 bytes. Generated AAC is also present and must be discarded if the shot is used with the song.
- API acknowledgement: event `15f18bee002840ada80759bbe8760e89`; [event log](free-test/ltx-2.5-events.txt) and [result](free-test/ltx-2.5-result.json) preserve success independently of the written assessment.
- Observed submission-to-completion walltime: **16.929 seconds**, from saved-file timestamps `21:24:46.725006 UTC` to `21:25:03.654158 UTC`. GPU quota debit was not returned, so this is not a measured quota-cost figure.
- Cost: no credentials, billing account, card, subscription change or monetary payment used. A public anonymous ZeroGPU quota was consumed.

## Quality verdict: reject this take for its requested dramatic action

Full FFmpeg decode completed without error. A [20-frame contact sheet at 4 fps](free-test/contact.jpg) was inspected in chronological order. This is frame-based visual inspection, not a claim of normal-speed audiovisual playback.

The model moved the man's head from his original worried sideways gaze to facing the viewer during roughly the first half second, despite the requested fixed pose. The resulting frontal expression is harder and less vulnerable. The woman closes her eyes and keeps them closed for the latter portion, rather than performing a brief blink. The sampled frames show no gross arm/limb deformation, but that does not establish frame-perfect anatomy or clean motion in unsampled intervals.

This proves free generation works; it does **not** clear the take for the film. Use a simpler positive action brief, compare identity against the source, and reject or trim unwanted action. Do not repeat this take for four minutes or call a sequence of still-camera moves complete character animation.

## Reusable endpoint and limits

[ltx_free_client.py](free-test/ltx_free_client.py) uses the public demo's supported upload and Gradio API. It submits one clip, saves the event before polling, and resumes that event when its output directory is reused. It has no credential support, billing, automatic retry, alternate identities or quota bypass. A failed or quota-limited result is a stop, not a trigger to switch accounts.

The tested calls were:

1. `POST https://lightricks-ltx-2-5.hf.space/gradio_api/upload` with multipart field `files`.
2. `POST /gradio_api/call/v2/run` with the named parameters shown in the saved request.
3. `GET /gradio_api/call/run/{event_id}` for the SSE result.
4. Download the exact output URL from the successful result.

The live [API schema](https://lightricks-ltx-2-5.hf.space/gradio_api/info) permits a 1–5 second requested duration; dimensions must be divisible by 64 for the two-stage pipeline. The official demo uses an `xlarge` ZeroGPU allocation. The Space's own current source estimates each job's required GPU time; exceeding the allowance can refuse a job even when some quota remains.

### Follow-up: quota refusal and smallest-job check

The parent's next five-second request for the woman at the window was refused. Its [saved event](../assets/motion/her_window_take1/events.txt) reports **150 seconds requested versus 72 seconds left**, with a wait of **23:55:36**. This is the first explicit quota result observed; no further generation was submitted after that error.

Read-only inspection of the official Space's [current source](https://huggingface.co/spaces/Lightricks/LTX-2.5/blob/main/app.py) confirmed the admission calculation:

```python
reservation = int(min(400, max(60, 30 + height * width * frames / 1_500_000 + decode)))
# decode = 8 for conv, 20 for diffusion; xlarge multiplies quota by 2
```

Even the minimum supported **1-second, 512×512** job reserves **60 GPU seconds / 120 weighted quota seconds**. Two seconds at 768×512 and three seconds at 896×512 have the same 120-second minimum. None fits the observed 72 seconds. Reducing a dimension to 384 or 448 is outside the public schema's 512-pixel minimum and would not remove the hard floor. Changing identity, rotating hosts or bypassing the quota is not an acceptable recovery method.

Legitimate options are to wait for the reported renewal or use an authorized Hugging Face account's normal allowance. No account/token access was established here, and no new account, subscription or billing change was made. The successful rejected smoke test remains research evidence, not an accepted production shot.

### Access setup update, 21:53 UTC

Dario explicitly asked the agent to create the necessary free setup and handle the browser itself. The prepared `/workspace/.tools/browser/playwright-cli` works without disabling TLS checks or the Chromium sandbox. Its `jml-access` session has Google Flow's Google sign-in page and the Hugging Face signup form. The latter was filled with the user's connected email identity and reached an hCaptcha challenge. Account creation is **pending**, not successful; no challenge was bypassed. A newly generated signup password is kept in a private mode-0600 file outside the repository and is never logged in this project. No existing Google credential was requested, extracted or reset.

TinyFish was suggested as a possible user-controlled browser handoff, but its connection is not confirmed. A suggestion alone does not establish usable access. The native cloud-browser activation separately failed because its platform runtime token was absent; no platform secret was fabricated. These are dated capability observations, not instructions to repeat failed setup on each continuation.

[Hugging Face's official ZeroGPU documentation](https://huggingface.co/docs/hub/spaces-zerogpu) currently lists **2 minutes/day unauthenticated, 5 minutes/day for a free account, and 40 minutes/day for PRO**, with daily renewal 24 hours after first GPU use. `xlarge` costs twice the quota of `large`. Paid users can spend prepaid credits beyond quota, so any future paid setup must explicitly avoid that spillover when enforcing the €20 ceiling. Quotas, queues and demo availability prevent promising the entire film in one day.

The [LTX-2.5 model card](https://huggingface.co/Lightricks/LTX-2.5) says commercial/production use is available without a model-license fee for entities below USD 10 million annual revenue under the linked community license. This is not a claim that every hosting plan is unlimited, that model redistribution has identical terms, or that every user automatically qualifies.

## Recommendation for the parent production

The evidence supports a three-tool candidate for production over multiple quota windows: **ChatGPT image generation for the consistent storyboard/keyframes → LTX-2.5 for selected real movement → FFmpeg for editing, audio and technical review**. It is blocked for further anonymous generation in today's quota window. Blender would be excluded from that version's production tool count. Existing assets are inputs, not an extra newly operated tool.

Start with a few crucial acting tests and accept clips only after source comparison and sequential review. Use free quota over legitimate daily resets if needed. The paid-budget researcher has been notified to examine whether one month of Hugging Face PRO can fund enough daily generation quota for ten films under €20; that proposal needs current price, tax and retry arithmetic, and must not silently become a purchase.

If the production instead proceeds immediately with ChatGPT image generation, Blender and FFmpeg, describe the result according to the actual animation it contains. An unused, rejected LTX research take does not make LTX a production tool, and it does not justify calling a film fully generated character animation.
