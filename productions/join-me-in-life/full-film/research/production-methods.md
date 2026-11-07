# Full-film production methods — research and recommendation

Research date: 6 November 2026. This is a production-method recommendation, not a completed-film review or Dario's creative acceptance. It applies the installed [Be Ambitious skill](https://github.com/robonuggets/be-ambitious/blob/dc116a3ebd8cf772e4d0930626f67369bd60399d/SKILL.md): raise the quality bar, use the raw material, and measure the result independently. No media was generated and no credits were spent for this report.

## Decision

**Selection correction, 6 November, after Dario's clarification:** the availability-based recommendation below is superseded. Existing connections and installed software are accidental, not the selection criterion. The final method must follow demonstrated quality and cost; setup follows that choice. The prepared Runway spending proposal has been withdrawn, without authorization or spending. The source audit of native Blender animation found no adequate full-body/contact rig for this film, so it cannot be promoted as a finished-film route just because it is installed.

The next hosted free candidate is **ChatGPT keyframes → Google Flow → FFmpeg**, selected for reference/first-and-last-frame control and a documented renewable allowance, subject to actual acting tests. Google's current official [credit table](https://support.google.com/flow/answer/16526234?hl=en) gives 50 daily credits; Veo 3.1 Lite costs 10 per 4/6/8-second 720p generation, allowing five daily attempts. The [feature guide](https://support.google.com/flow/answer/16352836?hl=en-1) documents reference-image and first/last-frame input. This is a capability/cost basis, not a claim that its acting has already passed. Plan a whole film across legitimate daily renewals, with rejected takes counted. Google is retiring several older models on 5 December; do not build a sustainable route around those retiring variants.

The quality reference remains an editor-led storyboard/keyframe pipeline, not a particular existing account. [Highdrama's anime music-video breakdown](https://note.com/highdrama/n/ned15425fb1b6?hl=en) documents rejecting character/scene drift and selecting usable portions of generated shots; its reliance on multiple models and retiming is not copied blindly. The open [three-stage GPT Image → Kling → FFmpeg example](https://github.com/0xadvait/ai-video-pipeline) supplies a useful reproducible architecture, but its reported approximately $22 for 72 seconds clearly misses this task's ten-film budget. Its absolute claim to eliminate identity drift is not adopted as a guarantee.

An owned LTX pipeline remains the repeatable low-cost research candidate. Its first CPU result exposed a concrete scheduler integration fault; diagnosis and a corrected retake are underway. Select it for production only if actual acting and acceptable output detail pass independent review. Do not confuse open weights with adequate quality or hardware.

### Earlier candidate, retained as research history

Build the zero-additional-cost version with exactly **ChatGPT's included image model, Blender 5.2.3, and FFmpeg**. Use the existing song, character references and artwork. Make a deliberately directed, limited-animation film: locked character designs, prepared action poses, facial acting, stable contacts, selective camera moves, and an edit shaped by the actual song. Treat research/browser/code utilities as support, not additional media-production services; disclose these three production tools in the delivery manifest.

This is feasible with the current CPU environment. It is not permission to present a succession of zooming paintings as finished character animation. If the acting has not been built and checked, call the output an animatic or motion-comic candidate. A tool count and a complete runtime are necessary constraints, not quality evidence.

If a **verified, usable free video allowance** is found, a better three-tool variant is **ChatGPT image model → that single video provider → Blender for editing/compositing/export**. Blender then replaces the separate FFmpeg finishing stage. Prove the allowance, generation access, usable export and one representative motion shot before adopting it. Do not accumulate several freemium providers merely to consume credits; continuity and retry costs can erase the benefit. The main task's wider free-method investigation should choose between these two variants before production is locked.

## The strongest demonstrated approaches

These are process examples, not a claim that one vendor objectively produces the best videos. I read the creator/process pages and official documentation. Embedded videos were identified, but I did not perform continuous audiovisual viewing of the example films; their movement quality remains to be assessed by playback.

| Demonstration | What the creator actually did | What to borrow here |
| --- | --- | --- |
| [Emily Peng's storyboard-to-video demonstration, 20 August 2026](https://www.kapwing.com/resources/how-to-make-a-full-ai-video-from-a-storyboard-seedance-2-5/) | Character sheet, high-resolution 15-panel storyboard, then a 30-second Seedance 2.5 sequence. The author explicitly describes panel interpretation rather than exact reproduction and recommends multiple takes plus separate generation for precise shots. | Build the entire visual argument before animation. A contact sheet is an economical planning/reference asset; it is not a guarantee of exact timing or anatomy. Budget rejected takes. |
| [Khalil / AI for Real Life, original workflow video](https://www.youtube.com/watch?v=CMPhDepMQS4), indexed with [steps and prompts](https://behindthegen.com/w/contact-sheet-storyboards-and-video-workflow-with-nano-banana-pro-and), December 2025 | Character reference, nine-panel contact sheet covering several shot sizes, selected panels enlarged, short Kling animation, editing in CapCut. | Reuse one identity reference across varied framing; animate selected panels rather than independently reinventing each scene. The original example uses more than three tools, so copy its method rather than its entire stack. |
| [Daito Manabe, “Ore wa Manabe Daito”](https://projects.daito.ws/oreha-manabedaito/en/) | A 192-second music video built from fixed character references, roughly twenty ten-second scenes aligned to lyric timing, selective lip-sync, JSON scene manifests and final scripted composition. The artist also publishes a face-error version and character-reference failures. | Preserve inputs, shot manifests, versions and failures. Generate around a song timeline. Reproducibility is useful; a successful encode does not prove correct faces. |
| [Nicholas Flandro, “LA Witch,” 2026](https://diffuse.runway.com/project/2495f712-1150-4766-8a30-1e230306090f) | Iterated the visual language in stills, refined them, animated with Kling/Seedance, then edited and composited. | Establish a coherent visual system before paying for motion. This is evidence for an iterative production process, not evidence that a no-retry film is cheap. The page's “1 credit” is a personnel credit count, not a generation price. |
| [Blender Studio / Will Anderson / Lucas Zanotto, “Impulse Purchase,” 2025](https://studio.blender.org/projects/impulse-purchase/) and [conference production talk](https://conference.blender.org/2025/presentations/4081/) | An animated OK Go performance built in Blender, with reusable procedural animation and live puppeteering; a production-file article is published. | Reusable authored motion can outperform endless one-off generation for a repeatable studio. Its geometric style is not the existing detailed anime style, so reuse the production principle rather than substitute that look. Full pages were blocked during this research; this row is limited to the official indexed project descriptions. |
| [Dan Streit on A$AP Rocky's “Shittin' Me”](https://runway.com/customers/distorting-reality-with-dan-streit) | Combined real footage, rotoscoping, depth-extruded stills, camera movement and selected AI effects in an editor-led production. | Use source motion when motion matters and reserve still-based techniques for shots that benefit from them. Previsualize the edit before producing assets. A hybrid can be an intentional film, not a concession. |
| [Sasha Kasiuha on Madonna's Celebration Tour](https://runway.com/customers/generating-new-worlds-for-madonnas-celebration-tour) | Explored style first; used source clips with strong motion for video-to-video treatment, and separate designed stills for image-to-video sequences. | Source movement and visual design are separate controllable inputs. This larger production had a team and months; its existence is not proof of instant one-click feasibility. |

A fresh [24 October 2026 Hailuo H3 / Kling 4 comparison](https://behindthegen.com/w/seven-shot-2d-anime-evening-in-one-prompt-hailuo-h3-vs-kling-40) also supports testing short, plainly staged actions from a fixed design sheet. It is a creator's stated comparison, not an independent benchmark: the index itself labels the judgment unverified, and its preview length and described target length differ. It is useful as a test idea, not as proof that either model will deliver this film.

## What the expert starts from

The raw material is [take 49](../../full-song/track-49.mp3), its [final lyric sheet](../../full-song/lyrics.txt), the actual character/art references and the two existing action sources—not an inferred generic song synopsis. The recording is 277.776 seconds. At 24 fps the picture can be 6,667 frames / 277.7917 seconds, with the audio ending 15.7 ms earlier. Verify this against the decoded recording rather than assuming container metadata is exact.

Prepare a song map from waveform/onsets and listening: intro, verses, pre-choruses, choruses, solo, all four screamed bridge pleas, key change and outro. Existing Short timings are anchors, not a full-song structure. Build a timecoded edit/animatic before refining movement. Strong music videos establish visual motifs and develop them; they do not need a literal illustration for every lyric or a cut on every beat.

The story constraints remain material: she is in crisis; he is frightened and stays with her. The waiting-room scene must not accidentally turn into her comforting him, a repeated embrace, or a sudden recovery. The warm summer scene is a memory. The final light can show time passing and continued company without claiming a cure. New full-film story beats are proposals under the current creation request, not retroactive approvals of old candidates.

## Why motion fails, and what to do before rendering 4:38

[Runway's official image-to-video guide](https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide) says the input controls the visual composition while the prompt should primarily direct movement. It warns that blurry hands/faces may worsen during animation and that implied action in an image can conflict with the requested motion. Therefore inspect and repair the source pose first; changing adjectives in a prompt will not reliably repair it. Use one clear action per short shot. Avoid asking a small clip to perform a multi-stage embrace, a turn, walking and a camera orbit together.

[Nicholas De Lotto's professional animation polish tutorial, July 2026](https://www.animationmentor.com/blog/tutorial-how-to-polish-your-animation/) is the most directly useful movement-quality reference. It treats body and face in separate passes, fixes intersections and unstable contacts, then refines timing and offsets between body parts. It cautions against smoothing every arc until the result feels floaty. Apply that method rather than adding sine-wave movement to every layer.

For this production:

1. **Blocking:** Each acting shot needs a readable initial state, intentional action and end state. First approve the poses in a short playblast. A still pan is an establishing shot, not proof of acting.
2. **Contacts:** Keep seated hips on the chair; keep a resting hand on its support; keep planted feet fixed in world space. Make a reach follow an arc with anticipation and a settle. Do not use boomerang playback for irreversible actions.
3. **Faces:** Eyes lead an intentional glance; head/shoulders follow where appropriate. Blinks are brief and varied, not a uniform clock. A closed-mouth reaction shot is preferable to visibly wrong singing.
4. **Exposure:** Use deliberate held drawings and stepped pose changes for limited animation. Smooth camera motion can coexist with animation on twos. Artificial frame interpolation must not melt hands or change faces.
5. **Continuity:** Check facial hair, jewelry, clothes, head-to-torso alignment and room geometry across cuts. A contact sheet helps spot drift but does not prove moving continuity.
6. **Economy:** Repeat motifs with changed stakes or framing; do not conceal a footage shortage by endlessly stretching five-second actions. Reuse environmental cycles only when physically repeatable.

The [Act-Two documentation](https://help.runwayml.com/hc/en-us/articles/42311337895827-Performance-Capture-with-Act-Two) shows another expert route: transfer a recorded performance to a character. It requires a driving performance and distinguishes image-based gesture control from video-based facial transfer. It also warns that a character video shorter than its performance will reverse-loop. This could solve important performance shots, but it is a paid workflow and no matching acting source is currently established; it is not a free substitute we can claim to have used.

## Actual access and sustainable cost

| Route | Evidence and limitation | Decision |
| --- | --- | --- |
| Included ChatGPT image generation | Available in the task; use A01/A02 identity references and one coherent storyboard, then only the pose/plate additions actually needed. | Use for design/preparation; do not generate a separate independent image for every video frame. |
| Blender 5.2.3 + FFmpeg | Existing prepared runtime verified by the primary agent; five CPU cores, no GPU exposed. Both can render/encode without per-second provider fees. | Available baseline; own the scripts, rig and edit. Zero new service spend, but labor and render time remain real costs. |
| Runway connection | Live primary-agent balance reports **1,897 purchased credits, 0 plan credits**. Models are available, but the balance is paid stock. | Do not describe it as free credits or spend without the applicable authorization. Existing source clips remain reusable. |
| Wan 2.2 self-hosting | The [official repository](https://github.com/Wan-Video/Wan2.2) documents 720p 24fps TI2V-5B and a 24 GB GPU route with offload. Larger production configurations need more. | Open weights are not free compute. No suitable GPU is established in this environment. A free remote GPU would need a real tested session and adequate quota. |
| FramePack self-hosting | The [official repository](https://github.com/lllyasviel/FramePack) requires a supported NVIDIA GPU, at least 6 GB VRAM, and over 30 GB of model downloads; its example RTX 4090 speed is 1.5–2.5 seconds per frame. | A plausible owned-GPU method, not a CPU fallback. At 30fps, 277.776s is 8,334 frames: roughly 3.5–5.8 GPU hours at those stated speeds before retries, by calculation. |
| Free provider/demo queues | A public “free” button does not establish authenticated allowance, export access, commercial use terms or throughput. | Test one shot and inspect the actual balance/export first. Do not rely on unverified credits for the full timeline. |

For ten videos of this length, €20 is **€2 per complete video** and 2,777.76 final seconds. A completely generated ten-video batch would require an all-in accepted-footage rate below **€0.00720 per final second**, before retry overhead. At 50% usable yield, the generation rate must be below €0.00360 per generated second. This is arithmetic, not a claim about any provider's current rate. Paid-provider selection and VAT/minimum purchase/renewal terms require the separate cost investigation. Free trials and existing purchased stock cannot establish a sustainable ten-video unit cost.

## Production and review gates

**Storyboard gate:** Inspect every panel at useful resolution against A01/A02. Both characters must retain identity and correct wardrobe; hands/shoulders/head alignment must be plausible; the hospital emotional roles must be correct. The new first act and dawn ending must read as a sequence rather than unrelated art. Each panel needs an assigned song beat and intended action. Reject duplicate/confused panels and repair art defects before animation. The nine-panel sheet is a coherent visual plan, not nine images automatically stretched to fill 277.776 seconds.

**Pilot gate:** Choose a representative action, not only drifting atmosphere. Render 5–10 seconds with the intended soundtrack segment and final cadence. Log start/anticipation/action/settle states; check eyes, hands and physical contacts through the complete clip. Play at 1×, inspect 0.25× and frame-step any doubtful transition. Require stable identity, readable intent, no accidental reverse-loop and a clean endpoint before extending the technique.

**Full-cut gate:** Verify all 6,667 picture frames, full-song coverage and each cut boundary; review all shots in order at 1× with sound. Record timestamped defects and repair them before changing the result from candidate to finished. Recheck affected shots and their two neighboring joins after repairs. An independently written review must distinguish what was actually watched from numerical checks.

Before full rendering, produce a small representative proof: a close reaction, a hand/contact action, and a transition into the bridge. Use the same image treatment, animation system, output fps and audio method as the planned film. Reject or repair visible anatomy drift, sliding contacts and unexplained direction changes at this stage.

Keep a shot manifest with source IDs, start/end frames, motion type, approved pose references and review results. Distinguish character action, environmental action, camera-only movement and intentional still holds so the delivery is honest about how much animation it contains.

The outside judge is a combination of independent technical checks and an unseeded visual reviewer:

- Decode every output frame; verify frame count, dimensions, fps, color/pixel format, continuous timestamps and playable MP4 indexing.
- Verify complete song coverage and audio alignment at the opening, Short anchor, bridge and end. Re-encoding similarity must not be reported as original-packet identity.
- Detect accidental black/frozen stretches and abrupt motion spikes, then inspect each flagged interval. Intended held drawings should be explicitly exempted in the shot manifest; do not hide defects with a blanket exemption.
- Review **every shot at normal speed with audio**, then slow/frame-step hands, contacts, faces and joins. Contact sheets and numerical checks alone cannot establish that movement works.
- Have a reviewer who did not build the animation report timestamped defects without first being told which shots “passed.” Repair them and recheck affected ranges plus neighboring cuts.

A pass means: the entire song is present; every shot has a logged motion review; no unresolved visible anatomy/contact/continuity defects remain in reviewed footage; technical checks pass; and cost/tool counts are documented. If audiovisual playback or a competent visual review cannot be completed, state that limitation and keep the result a review candidate. No finite automated test can guarantee the universal absence of weird movement.

## Ambitious task restatement

```text
Create the complete Join Me in Life film from take 49 and our established characters. First study demonstrated professional and current AI workflows, then use exactly three production tools for a zero-additional-cost version. Build the whole song's visual progression, prepare a coherent storyboard and actual acting poses, and prove the difficult movements in short rendered shots before scaling up. Keep our own editable sources and a record of every generated asset and cost. Prepare the paid alternative only if its real repeatable ten-video cost, including retries and required purchases, fits €20. Judge success through a full decode/audio check and an independent, timestamped normal-speed review of every shot; repair visible motion/continuity failures and report any unmet criteria honestly.
```

The next implementable rung is the full-song edit and representative animation proof using existing accessible tools, with any verified free video service evaluated before locking the three-tool production route. Research is not evidence of a completed film.
