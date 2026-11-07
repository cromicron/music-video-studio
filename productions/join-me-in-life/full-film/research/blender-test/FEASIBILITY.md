# Native Blender fallback: source audit, 6 November 2026

**Verdict: the prepared native animation cannot be extended directly into a convincing complete 58-shot film.** Blender can produce proper limited animation, but the current material does not contain the acting assets or rigs needed here. Selecting it because it is installed would repeat the availability-first error. No new pilot was rendered and no current source or export was modified. This directory records the evidence and the specific prerequisite for a useful future pilot, not a selected production route.

## What the existing code actually does

The inspected source hashes and edit coverage are in [source-audit.json](source-audit.json).

| Source | Implemented capability | Limit that matters for this film |
| --- | --- | --- |
| `current/native_animation.py:35–55` | Four mouth exposures using existing drawn variants | A 1,440-frame Short exposure list and a special sustained-vowel correction. It is not an alignment for the 6,667-frame full song. |
| `current/native_animation.py:57–80` | Constant mouth substitutions on P01 and P02 | A mouth changes inside a locally masked face. There is no head, jaw, torso or gesture performance. P03 bridge has no such variants. |
| `current/native_animation.py:88–127` | Compact shape-key displacement inside three garments, maximum below 1.1 source pixels | The script deliberately fixes faces, silhouettes and background. At the full-width 960-pixel review scale, 1.1 pixels of the 1,672-pixel drawing would be only 0.63 output pixels before any crop zoom. This is not a breathing body or a changing pose. |
| `current/build_film.py`, S02 material | Independent eye-region mixes from a supplied closed-eye drawing | Only one waiting-room composition has this treatment. A blink is useful acting punctuation but does not supply body action. |
| `current/build_film.py:186–205` | Camera coverage and source checks | Validation explicitly asserts zero deformation modifiers. Passing proves coverage and the small-deformation limit, not believable movement. |
| `reference/blender-pilot/build_scene.py:117–160` | A four-bone portrait mesh: Breath, Head, Left hair, Right hair | No shoulder, elbow, hand, hip, knee or foot controls. Small whole-image deformation is possible, but articulated interaction is absent. |
| `reference/blender-pilot/build_scene.py:112–115,177–191` | Alternate three-quarter artwork at frame 97 | The scene itself labels this as an editorial cut, not a continuous head turn. It cannot be counted as proof of a rigged turn. |

The P01, P02 and S02 source images used by the full-film manifest are byte-identical to the current assets, so the existing controls are relevant to those images. They match **12 shots / 52.208 seconds / 18.8% of the timeline**. This is source compatibility, **not accepted motion coverage**. All other shots lack these controls. The full edit contains 38 character shots totalling 178.917 seconds and 20 environment shots totalling 98.875 seconds. Eighteen distinct source plates are used.

`BLENDER.md` correctly documents a working bpy 5.2.3 route and restoration of the original Short. That removes a runtime obstacle. It does not establish a new acting capability. CPU emission rendering is a plausible delivery method after authoring; it is not the missing part.

## The hardest actions are precisely the unsupported ones

| Film requirement | Existing material | What is missing |
| --- | --- | --- |
| Four urgent pleas, especially S044 and S046 | P03 has a large foreshortened palm, bent wrist, microphone contact, open mouth, overlapping sleeves and hair, all painted into one opaque image | A coherent arm/hand volume across the gesture, shoulder and torso counter-motion, maintained microphone grip, facial changes and clean revealed background. Scaling or rotating a cut-out palm would look like a paper prop. |
| Night journey and arrival, S011 and S013 | One flat snow-travel plate and one arrival plate | Contact/down/pass/up poses, planted feet, weight transfer, coat/hair overlap and clean background. A drifting plate with moving snow would leave the walking person frozen. |
| Summer memory, S025–S026 and S037 | One shared seated composition | Distinct gaze/head poses with consistent faces, asymmetric timing, stable hands and seat contact. A mesh sway cannot invent the missing side of a head. |
| Hospital closeness and dawn | Flat two-person drawings with overlapping limbs, hair and furniture | Separate body regions, occluded artwork, contact constraints and expression changes that preserve her exhaustion. Matching blinks alone cannot carry these scenes. |
| Repeated solitary window shots | One small storyboard crop with reflected figure | The character and reflection must move coherently. Deforming the whole image drags the architecture; separating a flat face does not provide a real turn. |

The isolated full-body character PNGs and expression/angle sheets are references, not production puppets. They have no painted hidden joints, aligned replacement states, depth order for articulated limbs, or guaranteed correspondence to the shot perspectives. They are useful starting material for an animator, not ready animation controls.

## A bounded route that would genuinely test the method

The three-tool method could be **ChatGPT image generation → Blender cel/mesh animation → FFmpeg**. Python would automate Blender and FFmpeg, not add another image/video generator. This is only a feasible authoring architecture; it has not been demonstrated to finish this film with the current inputs.

1. Choose the five-second bridge plea as the gate, because it exposes the missing capability. Do not start with another easy blink. Use the existing P03 drawing as the identity and staging anchor.
2. Obtain a clean stage and separated torso, head, hair, microphone arm, extended upper arm, forearm and palm. Paint the areas uncovered by moving them. Author consistent anticipation, extension and settle drawings for the foreshortened hand/forearm. Existing assets alone do not provide these layers or poses.
3. In Blender, hold painted volume where possible and use genuine drawn replacements where perspective changes. Preserve the microphone grip and palm anatomy. Key one deliberate chest/shoulder initiation, delayed forearm action, a small settle and intentional facial exposure. Keep the camera locked so it cannot disguise the result.
4. Render 120 frames at 24 fps, with the image at full review size. Use drawn exposures on twos where appropriate; do not synthesize texture morphs or blanket smooth interpolation. Include a five-second static source alongside the candidate for comparison.
5. Independent review must see purposeful body/arm acting at normal speed; stable face and hand identity; unchanged finger count; correct wrist/shoulder connection; no detached limb, sliding contact, stretched print, revealed hole or background warp; and emotional urgency. Frame-step the anticipation, peak and settle. A successful decode, blinks, or moving pixels alone is a fail.
6. Only if that passes, build a separate walk/contact pilot and a two-person reaction pilot before authoring the remaining compositions. Reuse the character system, not a repeated canned action over unrelated story moments. A bridge pilot by itself cannot qualify walking or interaction.

This would require new art authoring, rigging, pose correspondence and animation direction. The prepared renderer helps with delivery, but there is no evidence-based estimate that this work is cheaper in effort or produces a better full film than a demonstrated storyboard-to-video workflow. No completion time or quality claim is made.

## Independent challenge

The `audio_story_map` reviewer independently inspected the native code and portrait pilot. They agreed that the existing material does not directly provide foreshortened-hand acting, planted-foot walking or two-person contact, and that a blink-only pilot would not test those actions. They also challenged an overbroad inference: this does **not** mean every one of the 58 shots needs full-body animation, or that Blender itself is infeasible. Environmental shots, deliberate holds and small head/hair motion within one view can be valid limited animation. A selective film could share fewer acting systems across the 18 used compositions. The missing evidence is at least one successful difficult-action gate with authored poses, occlusion and contact, followed by the other required action types. This was independent source review, not playback review of a newly rendered pilot.

## Why no new five-second movie is attached

The requested pilot was conditional on feasibility with existing source art. Rendering the existing blink or four-bone breathing treatment again would reproduce a capability already known to be insufficient. Animating an unsupported bridge gesture by warping the flat drawing would test the wrong method and risk presenting paper motion as finished anime acting. The useful next native test requires the actual layered/alternate-pose material above; it cannot be honestly replaced with a decorative loop.

The existing full animatic remains unchanged at SHA-256 `d3f66f4feebc401438218345d61889650418a65a5d3f6afb014720c8369550cb`. The Runway proposal was separately marked withdrawn/nonselected after Dario's correction; this Blender audit does not replace it with an installed-tool preference.
