# Technology for producing music video clips

Research date: 3 November 2026, Europe/Berlin. Scope: how to produce the actual pictures once a song's intended shots are known. Dario confirmed ChatGPT Pro. This is a proposed production approach; it does not approve a new cut, vendor subscription, generation charge or visual direction.

The recommended starting point is **Pro image generation for approved artwork, Blender for controlled animation and assembly, and selective image-to-video generation for natural movement**. Route each shot to a method that can deliver it. A camera pan across artwork, an articulated puppet and generated human acting solve different problems.

## Ambitious goal and method

Build a repeatable way to obtain usable, consistent clips for multiple songs, with a measured cost for footage that actually survives the edit.

- Altitude: first produce one reliable shot; then establish routes for the recurring shot types; finally reuse the tested routes across songs with a shot manifest, bounded retries and saved editable sources.
- Depth: start from approved reference images, the actual song master, intended motion, and original generated clips. A production animator would test articulation, contact, identity, timing and export before committing a whole song. Use Blender, FFmpeg/ffprobe, aligned image layers, recorded performance references and controlled comparisons. Proposed hard target: a 20-second representative test sequence with every selected frame usable and all spending recorded, before scaling to a full song.
- Range is skipped as a separate exercise: this request already has a clear technical scope. No story expansion or additional creative deliverables are needed.
- Outside checks: ffprobe/full decode for technical delivery, and a model-blind review by an independent animator/editor for motion and identity. Neither an assistant's self-rating nor a generic leaderboard establishes that our clips pass.

## Free through highest control and quality

| Route | Additional cash requirement | What creates the motion | Useful for | Main limitation |
| --- | --- | --- | --- | --- |
| Existing artwork plus Blender/FFmpeg | No new generation fee; rendering uses compute | Keyframed camera, layers, masks, particles, lighting and compositing | Atmospheric shots, graphic passages, lyric treatments, slow pushes and reusable environments | A pan/zoom does not create body movement or a new viewpoint |
| Pro images plus an articulated 2D rig | Image creation uses included allowance; local rendering has compute cost | Mesh/bone deformation, replacement mouths/eyes and hand-keyed poses | Repeatable stylized performance, controlled expressions and precisely timed actions | Rigging and drawing cleanup take work; large turns/contact need additional art or animation |
| Local open-weight image-to-video | Model access can be free; suitable hardware, electricity and setup are required | Video diffusion, optionally pose/depth/performance control | High iteration volume and experiments when hardware is already available | GPU memory, setup, render time and temporal defects; not free on an ordinary CPU cloud machine |
| Hosted budget image-to-video | Pay per generated attempt | Model synthesizes movement from an approved frame | Short inserts, subtle motion, first motion tests | Hands, faces and precise action may fail; low-resolution tests do not guarantee final-resolution results |
| Premium image/video-to-video | Higher generation cost and retries | Stronger reference conditioning, start/end guidance or performance-driven generation | Important acting, interaction, richer movement and difficult shots | No guarantee of exact choreography, identity or singing synchronization |
| Authored 2D/3D animation and compositing, with selective generated material | Highest labor/setup; software can still be free | Editable rigs, staged performances, animation and cleanup | Exact choreography, recurring band performance, instrument contact and demanding continuity | Requires animation skill and time; higher spend on a model alone cannot buy this control |

[Blender](https://www.blender.org/features/animation/) provides animation and rigging. A beautiful image is useful source material, but it is not automatically a rig, layered scene or 3D character.

## Make the Pro subscription do the artwork work

Use image generation available here to create and revise:

1. Consistent identity and wardrobe references, with existing accepted art attached.
2. The actual composed starting image for each shot, at its intended aspect ratio.
3. Clean backgrounds and foreground cutouts; use transparent-background generation for isolated parts and inspect their edges.
4. Additional poses, expressions and mouth shapes for controlled local animation. Align and clean them before use: an expression sheet is not a registered animation strip.
5. A final target frame when a video model supports start/end guidance. This guides the result; it does not constrain every intermediate frame.

Refine faces, hands, clothing, composition and drawn environments at this stage. Once approved, send the image to the chosen video service and ask primarily for motion. Preserve a master reference rather than repeatedly editing already drifted derivatives. Separately generated images must not be assumed to form a stable frame-by-frame animation.

Pro is already paid for, so using its included image allowance can avoid a second image bill. It is not unlimited compute: [Codex pricing](https://learn.chatgpt.com/docs/pricing) says image generation draws on included usage and consumes it faster. External Runway generation has its own billing. OpenAI's [current Sora notice](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation) gives 26 April 2026 for web/app discontinuation and 24 September 2026 for API discontinuation; do not build this workflow around Sora access.

There is also a potentially valuable [API-credit benefit for eligible Pro subscriptions](https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions). The documented full-period grants are $100/$200/$500 for the corresponding Pro tiers. Activation, eligibility and the receiving API organization must be checked; Dario's exact tier and grant are unverified. These are OpenAI API credits, not Runway credits. They could help a later image-automation pipeline; direct image creation here needs no API-key setup.

## Concrete hosted generation costs

These are **Runway Dev published rates**, USD before tax, checked on the research date. They are a comparison baseline, not a quote for the connected workspace's next submission. Creative-plan allowances and developer billing are separate products; confirm the relevant route's charge before generation. The Runway connection is authenticated and lists the following candidate models as available. No new generation was submitted.

| Candidate | Published credits per second | Example raw attempt | Proposed role |
| --- | --- | --- | --- |
| Gen-4 Turbo | 5 | 5 s: 25 credits / $0.25 | Low-cost image-to-video baseline, 720p through the connected tool |
| Seedance 2 Mini, 480p | 7 | 5 s: 35 credits / $0.35 | Cheap reference/control experiments; upgrade resolution only after testing |
| Gen-4.5 | 12 | 5 s: 60 credits / $0.60 | Compare for important motion shots |
| Kling O3 Pro | 17 | 5 s: 85 credits / $0.85 | Existing project precedent; test identity and two-person interaction |
| Veo 3.1, no generated audio | 20 | 6 s: 120 credits / $1.20 | Compare natural movement/realistic shots if appropriate to the song's look |
| Seedance 2.5, 1080p | 68 | 5 s: 340 credits / $3.40 before video-reference charges | Reserve for a demonstrated advantage or a longer shot requirement |

Source: [Runway Dev pricing](https://docs.dev.runwayml.com/guides/pricing/). The Veo example uses a supported duration rather than pretending every model generates five seconds. Availability can still be subject to account and operation checks. Newer versions are comparison candidates, not an established quality ranking for our drawn style.

Creative subscriptions currently list Standard at $15 monthly, Pro at $35 and Max at $95; annual-billing equivalents shown are $12/$28/$76. The respective monthly allowances are 625/2,250/9,500 credits. Compare an actual recurring workload before adding one. Avoid relying on old advice about an unlimited plan. See [current Creative pricing](https://runway.com/pricing).

The supplied song remains the music master. Disable generated audio where supported; remove it during assembly otherwise. Audio-off only reduces the price on models whose pricing distinguishes it. Generate short shots with clear action and edit them to the track; generated speech or singing does not establish synchronization with our recording.

## The number that matters is cost per usable second

Use `all attempt costs / accepted seconds in the final edit`, including rejected generations and trimmed sections. Keep labor and compute in separate columns so a nominally free route is not mistaken for free production.

Illustrative assumptions, not measured results: a five-second attempt costs $0.60, three attempts are needed, and three seconds survive. Effective cost is $0.60 per usable second. At the same yield a $0.25 attempt costs $0.25 per usable second. A more expensive model can still be cheaper overall if it produces far more usable footage.

For an illustrative three-minute video, 180 final seconds from five-second attempts with three seconds retained and three attempts per accepted shot require 180 attempts, or 900 generated seconds. That is $45 at $0.05/s, $108 at $0.12/s, or $153 at $0.17/s. At a $0.68/s rate it is $612. These exclude tax, references, cleanup, upscaling and labor. A 50% locally animated mix halves the generation portion under the same assumptions. A difficult singing close-up may have a much worse yield.

## Local generation without misleading free claims

[Wan2.2](https://github.com/Wan-Video/Wan2.2) offers Apache-2.0 models and image-to-video. Its documented 5B 720p route uses at least 24 GB VRAM with offloading; documented large-model commands can require 80 GB. Quantized/community workflows have different requirements and must be evaluated separately.

[LTX Desktop](https://github.com/Lightricks/LTX-Desktop) offers local generation. Its recommended Windows/Linux setup is an NVIDIA GPU with at least 24 GB VRAM, 32 GB recommended. For Apple Silicon, its current full-local recommendation is macOS 26+ with at least 48 GB memory; 32 GB is limited to 540p and five seconds. The application license and downloaded model licenses are distinct.

ComfyUI provides repeatable workflows; it is an orchestration interface, not itself a video model. [Comfy's motion-control work](https://blog.comfy.org/p/wan22-animate-and-qwen-image-edit-2509) shows how a driving performance can control body motion. Match any current model version to its own hardware requirements and model license. For our own performance material, recorded acting or a Blender blockout is often a better starting input than increasingly elaborate text instructions.

This environment has a working CPU-accessible Blender runtime, but no NVIDIA device or `nvidia-smi` was found. Local video diffusion was not installed or benchmarked. First establish Dario's available desktop GPU/memory before investing in that route. Renting GPU time is paid compute, not free model usage.

## Route shots according to the motion needed

- Camera movement, graphic effects and held atmospheric art: local Blender compositing. Layer separation enables parallax within limits; a large camera orbit requires geometry or newly drawn views.
- Blinks, gaze, subtle posture and repeating drawn singing: articulated cutouts, aligned replacement drawings and timed visemes. Use the actual vocal for timing and manual cleanup; do not assume a speech lip-sync tool will handle sung vowels and screams.
- Walking, embraces, hair/clothing movement and emotionally nuanced acting: approved images plus short image-to-video tests. For precise blocking, supply a recorded or rendered motion reference to a compatible video-to-video/performance route.
- Playing instruments or choreographed hands: stage or animate the actual contact. Generated footage can be attractive while the fingers, strings, keys or beat are wrong.
- Highest-fidelity recurring characters: invest in editable animation assets and compositing. Use premium generative shots where their output passes the same acceptance criteria.

## Fit with our current studio

The [Join Me in Life manifest](../productions/join-me-in-life/current/generation_manifest.json) records two approximately five-second Kling O3 Pro clips, 85 credits each, 170 total. Revision 4 added zero video-generation credits. These figures are historical source costs, not the total labor or whole-film cost and not proof of unrestricted reuse for other songs. The existing mix demonstrates feasibility; it does not establish that every shot or future song is solved.

Existing references, source movies, schedules, FFmpeg and the bpy 5.2.3 runtime are available. The native portrait scene opened successfully during this research. Existing artwork contains flattened cutout and expression candidates, not production-ready full articulation. Preserve the current cut; build tests separately.

## Proposed test before scaling

Start with two approved images representing a subtle face/cloth shot and a harder two-person contact shot. Compare two five-second attempts each with Gen-4 Turbo, Gen-4.5 and Kling O3 Pro; also make a local animation of the subtle shot. Published Dev generation arithmetic is 2 images × 2 attempts × (25 + 60 + 85) = **680 credits / $6.80**, before taxes or route-specific differences. Quote the actual workspace charge and the exact shots before spending. Do not silently add retries. Singing requires a separate synchronized performance test after this initial comparison.

Record source checksum, motion instructions, tool/model version, settings, billed credits, wait time, retained time range, export metadata and failure reason for every attempt. Use the same image and action for each candidate, strip provider labels for review, and compare at the intended viewing size. Low-resolution drafts are evaluated as drafts, not mislabeled as 1080p tests.

Pass criteria: decode without errors; correct aspect/dimensions/timebase and song alignment; at least three consecutive useful seconds per selected take; no visible identity, hand-contact or environment instability in that range; required action happens in its agreed timing window. Have an independent animator/editor score motion, identity and style at least 4/5 for the selected footage. Select by cost per passing second. If no model passes, change the motion method or use authored animation rather than repeatedly escalating text prompts. These are proposed tests; no new comparison clips or scores exist yet.

## Reusable task prompt

```text
Develop our music-video production method for actual usable clips once the shots are known. Use our ChatGPT Pro image generation to refine reference art and shot frames. Compare local animation, local open-weight generation where suitable hardware exists, cheap image-to-video and premium performance/reference-driven generation. Preserve the intended look, characters and original song recording. Do not expand into story development.

For each route give the motion it can deliver, required inputs/hardware, current billing route, expected cleanup and editable outputs. Start with the approved representative shots, quote their exact cost before paid generation, cap retries, and keep a shot-level manifest. Evaluate every attempt by independent technical checks and a model-blind animator/editor review. Pass only footage with the intended action, consistent identity/style, correct timing and at least three consecutive usable seconds; report total spending per accepted second, including failures. Scale only a route that passes.
```
