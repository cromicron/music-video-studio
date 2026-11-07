# Selected full-film action plan

7 November 2026. **Keep the original embrace, retain the reviewed male summer performance and matched Short singing, then make seven essential new action/performance takes.** Finish the quieter character coverage with13 separate delivery clips; do not mistake seven successful actions plus the unchanged animatic for a completed film. The selected target is **32.167 s of principal new action +80.917 s of quieter new character motion =113.083 s**. These are editorial deliverables, not a promise of20 successful generation jobs: handles, retries and any split of longer clips add work.

Use **ChatGPT images → owned LTX system → FFmpeg**. Supplied historical Runway clips and drawn performance art are reused source material, explicitly labelled as such. No new Blender rendering. No provider request was made for this plan. Root selected the bounded continuity surgery; implementation now changes only the separate production candidate/editor and review evidence. The113.083s figure remains a delivery target, not completed animation.

Base: [production candidate](../edit-production-candidate.json), snapshot SHA256 `f16ecd7254dbcd1b90a811a60ee38e3125d1ce18edd683f0326030905107ef12`. The [machine-readable companion](action-coverage-plan.json) assigns every one of the58 shot IDs, exact frame intervals, proposed source changes, high-resolution input hashes and work units. Its proposed boundaries remain contiguous through6667frames/277.791667s picture with the original277.776s song intact. Later implementation may change the live candidate hash.

## Seven essential new takes, in priority order

| Priority / take | Exact placement | Selected action and available start frame |
| --- | --- | --- |
| 1 · A01 summer answer | New part of **S026, 122.875–125.875 s**,3s | Her attentive reply, brief shared laugh, then a clean shared smile. Original `current/assets/M02_Summer_Start.png`,1916×1080, plus `assets/summer_identity_end_v2_candidate.png`,1672×941, static eligibility passed (SHA256 `a8568693ace5b316f0ad4e2be5db7501d24e0c094e5183d7382f3a8b980ed01d`); motion remains unapproved. Keep adult face structure, green/hazel eyes, freckles and original earbud/hand positions. |
| 1 · A02 first screamed plea | **S044,207.875–211.250 s**,3.375s | First “Forget your lines” is already a scream. Use P03,1672×941, with the actual original-song excerpt. A2V v5 completed: source[0.125,3.5) is independently scoped-approved for S044; its new wide insertion/cut is being reviewed. The207.75s source start includes a0.125s head handle. |
| 1 · A03 third screamed plea | **S046,215.958333–219.375 s**,3.416667s | A different, more urgent performance with the original gang/crowd vocal. P03 is available; keep the body/hand supported. Do not replay or retime the first plea's mouth cycle. |
| 2 · A04 first chorus appeal | **S014,66.500–70.583333 s**,4.083333s | P02 chorus art,1672×941; a frightened direct vocal appeal with stable microphone contact. This is outside the verified Short timing, so it needs its own actual-song performance. |
| 3 · A05 journey | **S011,50.500–56.000 s**,5.5s | `snow_journey_refined_candidate.png`,1672×941: two or three real supported steps toward the entrance. Source shoe overlap remains a gait-review risk; a camera move over the pose does not count as walking. |
| 3 · A06 arrival | **S013,60.291667–66.500 s**,6.208333s | `his_arrival_refined_candidate.png`,1672×941: tense pause, worried inward look and restrained breath while keeping the existing grip. The minimum plan does not require inventing a moving door mechanism. |
| 4 · A07 final presence | **S058,271.208333–277.791667 s**,6.583333s | `dawn_together_refined_v2_candidate.png`,1672×941: exhausted breathing and settling gaze, continued company, no recovery smile. Preserve motion through the final2s fade. The v2 still passes static ring/identity review; generated hand continuity must still pass independently. Dawn remains proposed creative direction. |

The original M01 is **not another missing generation**. Its [new source review](m01-editor-second-review.md) supports normal-speed reuse. The current S028 composition is92lead-in frames +121original motion frames +78endpoint frames; its new12.125s sequence now has an independent scoped visual pass in [the sequence review](m01-reuse-sequence-review.md). This does not imply actual-song listening or full-film acceptance. Do not reintroduce mandatory hand repair or the rejected generated head-pat action.

For summer, use the [reviewed original M02 male-focused source interval](m02-editor-second-review.md), `[0,2)`s, at **120.875–122.875s**, after the original-start lead-in118.250–120.875s. Then A01 supplies the3s reply, followed by at most the proposed0.875s clean endpoint to126.750s. Root has adopted a separately reviewed **male-only widescreen derivative** for S025, SHA256 `e5d63d2d6e9986e55827680c0195e682ce2bfd319bb8b3bf938e653633615667`; this does not approve the drifting two-person wide source or the new lead/source sequence. This preserves his actual playful performance instead of regenerating the whole exchange. Original M02's later female face and the new rejected LTX summer take are not approved substitutes.

## Bounded editorial changes

| Change | Exact proposed boundary/source | Reason |
| --- | --- | --- |
| S021→S022 | **106.125s / frame2547**, from106.416667/frame2554 | Restore R4 withdrawal close-up S02, then wider distance S01. |
| S022→S023 | **110.125s / frame2643**, from110.166667/frame2644 | Restore the original matched singing entrance. |
| S023→S024 | **114.500s / frame2748**, from114.750/frame2754 | Preserve rounded “you” through the last displayed frame before the original cut; return to original S02 reaction. |
| S025→S026 | **122.875s / frame2949**, from122.458333/frame2939 | Put the cut precisely between original male phrase and new female response. |
| Inside S029 | **145.625s / frame3495**, P02→P01 | Carry over R4's original performance-angle change at the matching song position. |
| S016,S020 | Replace redundant P01 stage plates with S02 hospital reactions | Keep the original song; reuse supplied eye art rather than inventing new unsynchronized singing jobs. |
| S033,S043 | Use the established M01 aftermath | Continue his concern after the chorus and before the screams; reduce repetitive stage cards. |
| S034,S041,S045 | Replace isolated window pose with her reaction **within M01's held contact** | The current candidate fixes S030/S032/S042/S047, but these remaining solo-window returns can still erase the embrace geographically. |

Other shot boundaries and the full-song duration remain unchanged. S007–S008 should read as one continuing room observation; S050–S051 as one continuous indoor dawn observation. The candidate now uses one shared camera curve across each pair, removing artificial camera reversal/reset; actual quiet character motion remains outstanding.

## Reuse the singing knowledge through FFmpeg

The existing aligned P01/P02 mouth drawings and S02 blink drawing are all local1672×941 assets. I evaluated only the pure `exposures()` function against `word_timing.json`, without importing bpy or rendering: **133 constant pose changes**. The rounded “you” drawing begins at zero-based Short frame305 and remains through338—one-based339—before the closure event after the original cut. The selected full-song cut is114.500s, the24fps approximation of114.498s.

**Selected route:** composite those existing local mouth/eye regions in FFmpeg at their original matched song frames for S021–24, S027 and S029. Retain the original separable smootherstep mask—fully exposed inside72% of its radius, fading to zero at the edge—and constant mouth exposures. The companion records exact source hashes, normalized masks and mapping; `current/native_animation.py` and `build_film.py` are read-only implementation evidence. Do not crossfade whole generated portraits or render Blender anew. Check local seams and the vowel cutoff against original R4 frames. This is **reused limited drawn articulation**, not new LTX generation or phoneme-complete sync.

Only the captioned portrait export is local. An archived clean widescreen R4 exists in the release manifest, but has not been recovered/inspected here; it is not the selected dependency. Do not stretch the portrait or carry its baked captions into the wide film. The full-film audio remains the original take49 master, not pasted Short audio.

## Quiet coverage still required

Thirteen bounded quiet-motion deliveries cover the following exact existing slots. They require real, restrained character changes; they are not approval to repeat one blink, freeze a failed endpoint or replay a pull.

| Delivery groups | Shot IDs | Total |
| --- | --- | ---: |
| Three inward window reactions | S003,S010,S015 |15.333s |
| One pre-contact frightened observation | S019 |5.500s |
| Five held-contact clips/continuations | S030+S032; S033+S034; S041; S042+S043; S045+S047 |37.208s |
| One distinct warm-memory aftermath | S037 |5.125s |
| One indoor dawn continuation | S050+S051 |7.958s |
| Two outdoor dawn observations | S053; S056 |9.792s |

Start held-contact footage from the actual1916×1080 M01 endpoint, retaining her passive lap, away gaze and self-supported head. Where a clip supplies two separated timeline slots, use **successive, non-overlapping source portions**, with a deliberate camera distinction and inspected joins. The approved2.033s tail from the rejected generated hospital take may remain a separate candidate, but is not automatically interchangeable with M01's geography and does not fill this37s requirement.

The early doorway portraits can remain brief deliberate held drawings. Empty rooms, corridor, hospital exterior and courtyard can use restrained FFmpeg camera/lighting/snow treatment without generated human action. These are environmental or static-picture choices, not claims that a still person is acting.

## Full-film pressure points and finish gate

The old plan spends **37.583s/eight visits** on one window image. Restoring the Short reactions and keeping post-contact geography reduces that to15.333s/three visits. Stage plates currently consume41.583s; the selected reduction preserves the necessary direct first chorus, matched Short performances and two visible screams rather than ordering a new lip-sync take for every repeated card.

The final dawn/outro is **54.292s**, including29.958s of empty courtyard/room imagery. It cannot be completed by lengthening one quiet bench endpoint. Use the selected indoor→empty exterior→outdoor progression, distinct observed motion in S053/S056/S058 and a continuous final take. Elapsed night permits changed seating/contact by dawn; it does not justify a new embrace or cure. The room is a symbolic return, not an unsupported claim that she has already gone home.

Keep all four screams: **S044 performer/full first scream; S045 her held reaction under scream2; S046 more urgent performer/gang scream3; S047 both still together under scream4.** Original master audio continues through every cut; no truncated phrase or quieter first plea. Their existing boundaries remain provisional outside the known Short until actual-song review.

Completion requires the full277.776s cut with the original song: checked action, faces, hands, contact, gait, reflection, non-repeating quiet motion, ordinary-size cadence, performance exposure joins and ending. Source approval, static-art eligibility, technical playback and an attractive endpoint each establish only their stated scope. This plan does not declare the film finished or hide unmade animation in a hold allowance.

Implementation evidence: [exact production source/timing diff](production-continuity-diff.json). Of the original113.083s new-delivery target,3.375s of first-plea source is now scoped-approved;109.708s still lacks accepted inserted delivery. The recovered drawn exposures are supplied limited animation, separately counted from generated human action.
