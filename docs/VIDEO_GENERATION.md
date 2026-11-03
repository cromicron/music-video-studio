# Technology for producing music video clips

Research checked 3 November 2026, Europe/Berlin. Scope: producing the actual footage after the intended shots are known. Dario confirmed ChatGPT Pro. Prices below are USD before tax unless specified. Public documentation, independent benchmarks, local source inspection and account/tool availability were checked; this is not a measured benchmark of new clips made for our songs.

The strongest approach to test is **Pro-generated visual assets plus motion supplied by the method appropriate to the shot**. For atmosphere, use ordinary image-to-video or local compositing. For precise acting, film or block the movement first, then transfer or restyle that performance. For singing, test actual-audio/performance-driven tools. Keep the original song as the delivery master.

## What the research supports

The useful objective is a repeatable way to obtain consistent, usable footage across songs at a known production cost. A list of video models is not enough: an I2V model, a performance-transfer model, a lip-sync model and a rigged animation system accept different controls and solve different problems.

Be Ambitious is applied through three methods:

- **Altitude:** one repeatable shot, then validated routes for recurring shot types, then a reusable shot-production system. Do not assume one model can generate the entire film accurately.
- **Depth:** use original reference art, source song, exact action and real performance references; compare methods through technical delivery, motion/contact, identity/style and retained footage. Treat vendor examples as capability evidence, not our acceptance results.
- **Range:** combine production animation, model/hardware engineering and production-cost analysis. Their independent research found additional free routes, song-specific tools and a different quality shortlist.

The target is a representative 20-second proof sequence covering the hard requirements before a whole-song production commitment. Public independent benchmarks guide the shortlist; clip-level technical checks and an independent animator/editor review, if available, establish whether our particular footage passes. No reviewer has been recruited and no new clips have been scored.

## Free and included routes first

| Route | What it actually gives us | Conditions and limits |
| --- | --- | --- |
| **ChatGPT Pro image generation already here** | Reference packs, composed shot frames, precisely edited performance keyframes, alternate poses and layered-animation source art | Included usage allowance, not unlimited frames or a video service. No second image subscription is needed to begin. |
| **Google Flow documented free allowance** | Google's credits page says 50 credits/day without subscription; Lite is 10 credits and Fast 20 per 4/6/8-second generation | Potentially five Lite or two Fast attempts/day. Free access can be unavailable at peak demand. Other Google setup documentation still mentions a subscription requirement; verify the account's actual eligibility. This account has not been inspected. |
| **Comfy Cloud new-user trial** | Current pricing advertises five free GPU workflow runs and free agent credits | A practical way to screen a supported local-model workflow without owning a GPU. The older 400-credits-every-month announcement is not the current pricing promise. |
| **Blender/FFmpeg and authored 2D animation** | Camera motion, parallax, particles, compositing, exact mouth exposure timing; articulated movement if suitable rigs/art are built | No per-generation fee. Compute and animation labor remain costs. A pan across a drawing does not create a walking or embracing performance. |
| **Open-weight video models** | Local I2V, audio-driven generation or motion transfer, depending on the exact model | Free model access is not free GPU infrastructure. Requirements and licenses differ sharply between variants. See hardware section. |
| **Vendor free trials** | Small opportunities to inspect a tool before buying | Do not assume free-tier commercial rights, ongoing credits or watermark-free delivery. Pika's current Free plan has no included monthly credits and excludes a commercial license. |

Google sources: [credit allowances and model rates](https://support.google.com/flow/answer/16526234?hl=en), [setup and watermark rules](https://support.google.com/flow/answer/16353333?hl=en), [current US subscription offers](https://gemini.google/us/subscriptions/?hl=en). Daily and monthly credits expire rather than accumulating indefinitely. Flow always embeds invisible SynthID; current visible-watermark rules vary by setting/region. [Comfy's current pricing](https://comfy.org/pricing/) supersedes reliance on its [March free-tier announcement](https://blog.comfy.org/p/free-tier-arrives-in-comfy-cloud). Free trials are a way to screen motion, not a guaranteed commercial production entitlement.

## Use Pro to direct the footage

The largest opportunity is to use included image generation as a **visual direction and control layer**, not just to generate attractive starting pictures.

1. **Identity pack:** retain the accepted master references and make the additional angles/expressions the chosen motion system accepts. Specify identity, wardrobe and style separately. Multi-angle references improve conditioning but are not an identity guarantee.
2. **Exact shot frame:** fix composition, anatomy, clothing, hands, props, lighting and drawn background before paying for motion.
3. **Edited performance frame:** take a frame from our own filmed performance or Blender blockout and use image generation here to give it the intended character and treatment. Propagate that change through a compatible video-editing route.
4. **Timed pose anchors:** create a small set of chosen action/keyframes for a route that accepts timed guide frames. For example: initial pose, contact, final hold. Intermediate images guide synthesis; they do not prove every intervening frame will be correct.
5. **Local animation assets:** create clean backgrounds, transparent parts and replacement expressions. Register their scale/position and clean overlaps before rigging. A generated expression sheet is not automatically an aligned mouth strip or a 3D rig.

OpenAI documents reference-based editing and multiple references in [image generation](https://learn.chatgpt.com/docs/image-generation) and reusable character references in [image prompting](https://developers.openai.com/api/docs/guides/image-prompting). Keep masters rather than building an endless chain of drifted edits. Generating each animation frame independently is not a reliable substitute for temporal video generation or animation.

Image generation here draws on included usage; bulk API generation is a separate billing route. Eligible Pro subscriptions can also have an [API-credit benefit](https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions), subject to activation and tier. Dario's exact grant has not been verified. OpenAI credits do not pay external providers. [Sora's current discontinuation notice](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation) rules it out as a current route, regardless of older Pro/Sora comparisons.

## Actual control and motion methods

| Method | Required source and control | Best reason to test it | Limits that affect production |
| --- | --- | --- | --- |
| **Ordinary image-to-video** | Approved opening image plus motion instructions; some endpoints add ending frames or identity references | Atmosphere, short independent actions, camera/cloth/hair movement | Exact choreography and contact remain synthesized; prompt length is not equivalent to control |
| **Runway Act-Two** | Driving performance video + character image/video; image mode permits body/hand gesture transfer | Single-character expressive performance timed to a real take | 3–30 s, 24 fps, 720p. Single subject, waist-up, visible face. Image mode adds environmental/camera motion; character-video mode preserves source movement but disables gesture transfer. Short source video can boomerang |
| **Kling 3 Motion Control** | Character image + driving video; optional facial element reference | Full-body/hand transfer and stylized character performance | 3–10 s image-orientation or up to 30 s video-orientation. With multiple people it targets the largest subject; not independent control of two interacting people. Facial binding does not lock wardrobe/props |
| **Luma Ray 3.2 guide-frame generation** | 1–64 timed guide images, placed on a 24 fps output grid | More directed action progression from Pro-created pose frames | The exact resolution/duration/keyframe combination needs endpoint validation; parts of the documentation have differing generic restrictions |
| **Luma Ray 3.2 whole-scene editing** | Filmed or rendered source action, visual guides and preservation controls for pose/depth/normals/trajectory/face | Preserve the staging of two-person contact while changing appearance | A serious candidate, not a proven solution for our specific anime identities/contact |
| **Runway Aleph 2 / Edit Studio** | Existing moving shot and an edited/reference frame | Propagate a specified appearance change while retaining source performance | Documented source range 2–30 s, 480–1080p, 24–30 fps, at most ten cuts. Product features and exposed connector controls are not identical |
| **Seedance 2.5 multimodal reference/edit** | Images, driving video and optional audio via supported product/API | A benchmark-supported general model with richer reference control | Direct APIs expose controls that the current chat connector does not. Audio reference does not automatically preserve the supplied master unchanged |
| **Authored rigged 2D/3D** | Separated art or geometry, rig, actual timing and animation | Exact contact, instrument performance, recurrent characters and editable motion | Labor and asset-building replace inference uncertainty; highest control does not mean lowest production effort |

Primary control documentation: [Act-Two](https://help.runwayml.com/hc/en-us/articles/42311337895827-Performance-Capture-with-Act-Two), [Kling Motion Control](https://help.runwayml.com/hc/en-us/articles/50280558448147-Creating-with-Kling-3-0-Motion-Control), [Kling element constraints](https://kling.ai/quickstart/motion-control-user-guide), [Luma generation](https://docs.agents.lumalabs.ai/guides/videos/generation/), [Luma editing](https://docs.agents.lumalabs.ai/guides/videos/editing/), [Edit Studio](https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio), [Seedance 2.5](https://docs.byteplus.com/en/docs/ModelArk/seedance-2-5).

For a known embrace or instrument action, record/block the movement before visual conversion. Two independently animated characters do not automatically preserve their shared contact. Use a whole-scene control route or authored interaction. Keep difficult camera moves separate when possible; fixing action, camera, appearance and lip sync simultaneously makes failure diagnosis expensive.

## Singing is a separate production route

| Route | How it uses our actual song | Published cost evidence | Qualification |
| --- | --- | --- | --- |
| **Hedra Character 3** | Character starting image + required audio; explicitly supports singing | 540p $0.025/s, 720p $0.05/s, 1080p $0.0625/s; raw 5 s at 1080p is $0.3125 | Avatar/portrait route, up to ten minutes. Our anime proportions, screams and desired acting are not tested |
| **Sync Labs** | Existing video + isolated vocal; explicitly documents song lip-sync | At 25 fps: lipsync-2 $0.04–0.05/s; sync-3 $0.107–0.133/s | lipsync-2/-pro need natural speaking motion already present. sync-3 can open silent lips. Human-like faces; stylized compatibility requires a test |
| **Act-Two** | Film a performer lip-syncing to the exact excerpt; transfer the timed take | Published Dev rate 5 credits/s, or $0.05/s | Transfers performance rather than inferring all acting from audio. Preserve the original recording in final assembly |
| **LTX 2.5 Audio-to-Video** | Optional opening image + supplied audio; audio tokens are frozen while video is generated | Local compute or the selected hosted endpoint's rate | Official workflow saves the original trimmed audio unchanged. Timing/motion following sound is not proof that every sung phoneme is correct |
| **Authored mouth/face animation** | Mark visemes, sustained vowels and beats against the actual recording | No inference fee; animation labor | Most precise timing control; requires drawn poses and acting, not merely random mouth opening |

Sources: [Hedra specifications/prices](https://www.hedra.com/models/video/hedra/character-3), [Sync models and song FAQ](https://sync.so/docs/models/lipsync), [LTX Audio-to-Video](https://docs.ltx.io/open-source-model/usage-guides/audio-to-video/), [Runway Dev rates](https://docs.dev.runwayml.com/guides/pricing/). These rates have different billing/account conditions; they are not interchangeable subscription credits.

Use an isolated vocal to drive a singer where recommended, then align/composite back to the untouched master. Preserve the excerpt's start offset and inspect sustained vowels, consonant closures, screams and visual beat alignment. Stem isolation, if needed, is preparation; it does not replace the delivered song master. A speech demo or generated dialogue does not establish song performance.

## Current quality evidence and what it cannot tell us

[Artificial Analysis I2V v2.1](https://artificialanalysis.ai/video/leaderboard/image-to-video), retrieved 3 November, shows Seedance 2.5 first on the audio board at 1157 ±16 and MiniMax H3 768p fourth at 1131 ±16. Kling O3 Pro and Veo 3.1 are seventeenth and twenty-first on that particular board. Its silent-board FAQ lists Utopai X, Seedance 2.5 and H3 Max as the leading three. Silent footage is the more relevant broad comparison when our recording supplies the soundtrack.

A separate [Arena I2V snapshot dated 21 September](https://arena.ai/leaderboard/video/image-to-video?rankBy=models) puts MiniMax H3 first and Seedance 2.5 fourth. These sources justify including **H3-family and Seedance candidates**. They do not justify equating MiniMax H3, H3 Max, Hailuo endpoints or model versions, or assuming a generic budget model is a good baseline simply because it is cheap.

[AA methodology](https://artificialanalysis.ai/methodology/video) uses blind preference comparisons, separate pools for silent/audio/editing, and mostly photorealistic material despite including anime/illustration. Default evaluation is generally ten seconds at 16:9, 1080p or closest supported. Its Elo values are not comparable to another site's scale; overlapping intervals also limit exact adjacent-rank claims. Our portrait anime, recurring identities, hand contact and recorded singing require separate checks. A silent model's absence from the audio leaderboard says nothing about its quality.

[VBench-2.0](https://arxiv.org/html/2503.21755v1) provides useful anatomy/contact/identity categories, but its face-identity metric excludes multi-person intervals and its [documented custom-video mode](https://github.com/Vchitect/VBench/blob/master/VBench-2.0/README.md) does not expose every dimension. It is not a turnkey independent judge of our two-person anime contact. [Hi-Singers](https://arxiv.org/html/2609.22264v1) studies the speech-to-singing gap; [AnimeShooter](https://arxiv.org/abs/2506.03126) and [MSVBench](https://arxiv.org/abs/2602.23969) motivate separate reference and multi-shot consistency evaluation. None certifies a commercial tool for this project.

## Cost ladder across providers

These are raw-generation examples, not costs of accepted footage. Subscription equivalents assume the entire allowance is used on that route. Actual initial cash outlay can therefore exceed the displayed per-clip allocation. No account was purchased or charged. Direct provider plans, APIs and resellers can expose different controls and rates.

| Route and billing basis | Raw clip example | Cash/usage qualification |
| --- | --- | --- |
| Google Flow daily allowance | Potentially $0 for Lite/Fast trials within the documented allowance | Eligibility/availability must be checked; credits page and setup page differ |
| Comfy Cloud supported open-model workflows | Five free new-user runs; Standard $20 monthly, Creator $35 monthly | Charges active GPU workflow time; importing own models requires Creator or higher. Advertised cheap clip counts use a small accelerated draft, not final 1080p |
| Pika Starter native H3 Flex, 768p | 5 s, 10 of 900 credits: about $0.11 allowance-equivalent | $10 monthly subscription floor; not the same as independently ranked full H3 |
| Pika Starter Pika 2.5, 720p | 5 s, 20 credits: about $0.22 allocation | Same $10 floor; motion quality untested |
| Runway Dev Gen-4 Turbo | 5 s: $0.25 | 720p via current tool; low price does not establish adequate quality |
| Luma Ray 3.2 API, SDR 720p | 5 s, 100 credits at $0.003: $0.30 | Default list-rate conversion; selected contract governs. Ten seconds is $0.90, not twice $0.30 |
| Hedra Character 3, 1080p | 5 s: $0.3125 | Audio-driven avatar generation, not a general-action comparison |
| Google AI Pro Flow Fast | 8 s, 20 of 1,000 monthly credits: about $0.40 allocation | US $19.99/month example, fully used monthly pool; Google plan is separate from ChatGPT Pro |
| Kling direct VIDEO 3, silent 1080p | 5 s, 40 credits: about $0.53 at published Standard renewal allocation | $8.80/660-credit example is from a dated official guide, not a verified live checkout quote |
| Runway Dev Gen-4.5 / Kling O3 Pro | 5 s: $0.60 / $0.85 | Different models and controls; existing project uses O3, not a proof of comparative quality |
| Luma Ray 3.2 API, SDR 1080p | 5 s: $1.20 at default list conversion | Four times the 720p rate in this table |
| Pika Starter Seedance 2.5, 720p / 1080p | 5 s: about $1.36 / $3.32 allocation | 122/299 credits; same model family can be far pricier than native budget routes |
| Adobe Firefly Standard, own model | 5 s: about $0.50 at 540p / $1.25 at 720p / $2.50 at 1080p | $9.99/month for 2,000 credits. Marketing maximum clip counts use lowest resolution |
| Runway Dev Seedance 2.5, 1080p | 5 s: $3.40 before video-reference charges | Published rate 68 credits/s; input/reference video billed additionally |

Price sources: [Pika plans and model consumption](https://pika.art/pricing), [Runway Dev](https://docs.dev.runwayml.com/guides/pricing/), [Luma API pricing](https://docs.agents.lumalabs.ai/guides/pricing/) and [credit conversion](https://docs.agents.lumalabs.ai/guides/usage/), [Google US plans](https://gemini.google/us/subscriptions/?hl=en), [Kling rate guide](https://kling.ai/quickstart/klingai-video-3-model-user-guide) and [dated plan example](https://kling.ai/blog/kling-video-3-0-credit-cost-guide), [Adobe plans](https://www.adobe.com/products/firefly/plans.html) and [resolution-specific consumption](https://helpx.adobe.com/creative-cloud/apps/generative-ai/generative-credits-faq.html).

Commercial/export details affect usable cost. Pika paid plans include commercial use; its Free plan does not. Adobe's own-model unlimited promise on its Premium plan does not cover every partner model. Luma web-plan pricing was not reliably retrieved and is not inferred from older Lite/Unlimited articles. Region, tax, promotional period, credit expiration, input-reference charges, resolution and subscription minimum must stay attached to a price comparison.

The highest advertised resolution is not automatically the best production choice. Generate and inspect a short shot at the final intended size before paying for a whole sequence; upscaling cannot repair incorrect fingers, identities or performance timing.

## Local models need specific hardware, not a generic free label

| Model/workflow | Official documented setup | Implication |
| --- | --- | --- |
| Wan2.2 TI2V 5B | At least 24 GB VRAM with offloading for the documented 720p route | Consumer GPU candidate; says nothing about larger motion/audio models |
| Wan2.2 S2V | Image + audio + optional pose video; documented single-GPU command needs 80 GB VRAM | Singing example exists, but this is not the 24 GB 5B workflow |
| Wan-Animate-2 | Default 8×A800 at 720p; tested 2×A800 at 480p | Not a verified ordinary-desktop route; community optimizations need separate evidence |
| LTX 2.5 open reference stack | 32 GB+ VRAM, 32 GB RAM, 100 GB storage; A100/H100 recommended | Exact A2V/control workload must be benchmarked on selected hardware |
| LTX Desktop | Windows/Linux recommendation 24 GB+ NVIDIA VRAM, 32 GB recommended; supported Apple Silicon tiers also documented | Product/runtime-specific optimizations; not interchangeable with reference-stack requirements |

Sources: [Wan2.2](https://github.com/Wan-Video/Wan2.2), [Wan-Animate-2](https://github.com/Wan-Video/Wan-Animate-2/blob/main/README.md), [LTX system requirements](https://docs.ltx.io/open-source-model/getting-started/system-requirements), [LTX Desktop](https://github.com/Lightricks/LTX-Desktop). Wan repositories specify Apache-2.0; LTX application and model-weight licenses are separate. Check the actual selected model license and any checkpoint/adapter terms.

No NVIDIA device or nvidia-smi was found in this environment. Blender's bpy runtime works; that is not evidence of a diffusion-capable GPU. Buying/renting hardware requires an expected workload first.

[Comfy Cloud](https://comfy.org/pricing/) is an alternative to building the runtime ourselves: it documents 96 GB RTX PRO 6000 workflow machines, supported preinstalled models/nodes, and a 30-minute Standard job limit. Creator adds own-model import. Its large advertised clip counts are based on Wan2.2 at 640×640, 18 fps and a four-step sampler; they are not evidence of equal-cost final-resolution film footage. Its separately priced Cloud API lists a 48 GB partition at $1.75/hour and a 96 GB machine at $3.49/hour. Check which product/workflow is actually being billed.

[Runpod's RTX 4090 page](https://www.runpod.io/gpu-models/rtx-4090) itself shows $0.89/hour in its heading while retaining $0.34/hour in body copy. Neither is treated as a verified deployable quote here. For rented compute use the actual available instance quote and measure the exact model's wall time, including loading and failures. An hourly price alone cannot establish a per-clip price.

## What is already operational here

- Native image-generation and editing tool: available here; Pro confirmed by Dario. Exact remaining allowance and Pro API grant were not inspected.
- Blender 5.2.3/Python 3.13.5 module route and FFmpeg: available. Original portrait scene opened successfully; source checks pass.
- Existing film: [manifest](../productions/join-me-in-life/current/generation_manifest.json) records two roughly five-second Kling O3 Pro clips at 85 credits each. The wider Short uses camera, image planes, blinks, drawn mouth substitutions and very small garment deformation. It is **not** a fully articulated character rig. The 170 credits are historical source-generation costs, not whole-film costs or a measured acceptance rate.
- Runway connection: authenticated. However, account-listed models are broader than the current generic generation tool's accepted model enum. Act-Two and some newly listed models have no dedicated callable operation exposed in this chat. Product/API/browser access may be needed; account availability is not proof of every connector control.
- Flow, Pika, Luma, Hedra and Sync: public capabilities researched; no connected account entitlement, commercial checkout or end-to-end execution verified here.

Web research was available and no approval rejection blocked it. Some pages produced fetch/content-type errors; those are specific retrieval limits, not evidence that research broadly requires more permissions. No paid-generation attempt was made.

## Evaluation and next production decision

Do not test only three ordinary I2V models and call that a music-video system. Use four discriminating shot types:

| Requirement | First comparison | Pass must include |
| --- | --- | --- |
| Atmospheric/subtle movement | Documented free or budget I2V versus H3/Seedance candidate and existing route | Stable identity/background and the required movement at intended framing |
| Two-person contact | Existing source versus whole-scene filmed/Blender action restyle or guide-frame route | Correct arm ownership, occlusion, passive hands/gaze where specified, full action and final hold |
| Singing close-up | Pro portrait + actual vocal through Hedra/LTX A2V versus a filmed Act-Two performance; Sync if source video is suitable | Sustained vowel, consonant closure, scream/expression and exact master alignment |
| Instrument/hand action | Actual playing reference or authored animation versus compatible motion transfer | Correct instrument contact and beat timing, not merely plausible hand movement |

Use a staged screen rather than buying every route. Preserve existing clips as baselines, choose approved input material and one difficult excerpt, then make a short, bounded trial only on the relevant routes. One or two attempts eliminate obvious failures; they do not estimate a dependable success rate. Stress-test survivors and repeat enough to expose variance before committing a full song budget. Quote the concrete shot, billing route and bounded charge before a paid submission, as required by the existing studio instructions.

Record each attempt's source checksum, action specification, model/version/provider, controls, native resolution/fps, song offset, wait time, billed cost, cleanup time, rejection reason and retained range. Technical decode/timebase checks are necessary but cannot grade acting or identity. Review at normal speed and inspect contact/phoneme frames; use blinded independent animation review if available. No such review is claimed yet.

The correct cost metric is:

`all generation charges + subscription allocation + compute + paid cleanup, divided by accepted seconds`

Keep initial cash outlay and labor hours alongside that metric. A $0.30 attempt that passes is cheaper than three $0.11 attempts that still fail. Conversely, the latest expensive model is not justified when a free/local route supplies the intended motion.

A transparent sensitivity scenario: for a 180-second final film, if each five-second attempt yields three usable seconds and three attempts are required per selected shot, 900 seconds are generated. At $0.05/$0.12/$0.17 per generated second, raw generation is $45/$108/$153; at $0.68 it is $612. These are assumptions, not measured yields. Adapt the model for reference charges, nonlinear duration pricing and subscription floors. Our 277.776-second full song is longer than this example.

The next evidence needed is a **shot-type test with the actual approved art and vocal**, not another general provider list. No additional story development, subscription purchase or production alteration is implied.

## Reusable ambitious production prompt

```text
Build a technically reliable way to produce our intended music-video shots across songs. Use our ChatGPT Pro image generation for character references, composed frames, edited performance keyframes and suitable animation assets. Compare genuinely free options, cheap native hosted models, keyframe-conditioned generation, recorded/Blender-driven performance transfer and actual-audio singing routes. Use independent current evidence to choose candidates rather than assuming expensive or newer means better.

Start with the original art, recording and precise action. For each representative shot choose the method that gives the required control. Keep the original song master, identity, style, timing, contact and instrument behavior. Distinguish documented capability, account/tool availability and results actually tested. Quote a specific bounded charge before paid generation and preserve every attempt and rejection.

Pass only clips that satisfy technical delivery and the full required action, preserve identities/contact/style, and align with the supplied performance. Use independent animation review where available; do not treat a generic benchmark or self-rating as clip acceptance. Report cost per accepted second, cleanup time and uncertainty before scaling to the full song.
```
