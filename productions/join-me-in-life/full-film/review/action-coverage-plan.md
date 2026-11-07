# Selected full-film action plan

7 November 2026. **Keep the original embrace and matched Short singing, use the reviewed continuous new summer exchange, then finish the remaining action/performance coverage.** Finish the quieter character coverage with13 separate delivery clips; do not mistake seven successful actions plus the unchanged animatic for a completed film. The selected target is **34.167 s of principal new action +80.917 s of quieter new character motion =115.083 s**. These are editorial deliverables, not a promise of20 successful generation jobs: handles, retries and any split of longer clips add work.

Use **ChatGPT images → owned LTX system → FFmpeg**. Supplied historical Runway clips and drawn performance art are reused source material, explicitly labelled as such. No new Blender rendering. No provider request was made for this plan. Root selected the bounded continuity surgery; implementation now changes only the separate production candidate/editor and review evidence. The115.083s figure remains a delivery target, not completed animation.

Base: [production candidate](../edit-production-candidate.json), snapshot SHA256 `f16ecd7254dbcd1b90a811a60ee38e3125d1ce18edd683f0326030905107ef12`. The [machine-readable companion](action-coverage-plan.json) assigns every one of the58 shot IDs, exact frame intervals, proposed source changes, high-resolution input hashes and work units. Its proposed boundaries remain contiguous through6667frames/277.791667s picture with the original277.776s song intact. Later implementation may change the live candidate hash.

## Seven essential new takes, in priority order

| Priority / take | Exact placement | Selected action and available start frame |
| --- | --- | --- |
| 1 · A01 continuous summer exchange | **S025/S026,120.875–125.875s**,5s, after63lead frames | Root adopts independently reviewed new LTX source`[0,5)`: subtle male phrase, her attentive turn/chuckle, his warm response and shared smiles. Source uses original M02start and reviewed v2end guides; the exact continuous summer/context exports now have scoped visual passes. Historical male crop stays an inactive alternate. |
| 1 · A02 first screamed plea | **S044,207.875–211.250 s**,3.375s | First “Forget your lines” is already a scream. Use P03,1672×941, with the actual original-song excerpt. A2V v5 completed: source[0.125,3.5) is independently scoped-approved for S044; its exact wide insertion has a scoped visual pass. The207.75s source start includes a0.125s head handle. |
| 1 · A03 third screamed plea | **S046,215.958333–219.375 s**,3.416667s | A different, more urgent performance with the original gang/crowd vocal. P03 is available; keep the body/hand supported. Do not replay or retime the first plea's mouth cycle. |
| 2 · A04 first chorus appeal | **S014,66.500–70.583333 s**,4.083333s | P02 chorus art,1672×941; a frightened direct vocal appeal with stable microphone contact. This lies outside the original Short span; its own generated performance and contained v2 placement/current neighboring cuts now have scoped visual passes. |
| 3 · A05 journey | **S011,50.500–56.000 s**,5.5s | `snow_journey_refined_candidate.png`,1672×941: the adopted source now supplies about seven supported exchanges toward the entrance. Root accepts the cadence departure from the rough3–5target; no slowdown, loop or hold. Initial/passing shoe overlap is a recorded source limitation. The exact wide insertion and current S010–S013 cuts pass [independent sequence review](walk-sequence-review.md). |
| 3 · A06 arrival | **S013,60.291667–66.500 s**,6.208333s | Root adopts A06 source `[3,152)`: anxious inward pause, sustained eye closure and head/chest dip with the existing grip retained. Full-source contain; exact insertion/cuts pending. |
| 4 · A07 final presence | **S058,271.208333–277.791667 s**,6.583333s | `dawn_together_refined_v2_candidate.png`,1672×941: exhausted breathing and settling gaze, continued company, no recovery smile. Preserve motion through the final2s fade. The v2 still passes static ring/identity review; generated hand continuity must still pass independently. Dawn remains proposed creative direction. |

The original M01 is **not another missing generation**. Its [new source review](m01-editor-second-review.md) supports normal-speed reuse. The current S028 composition is92lead-in frames +121original motion frames +78endpoint frames; its new12.125s sequence now has an independent scoped visual pass in [the sequence review](m01-reuse-sequence-review.md). This does not imply actual-song listening or full-film acceptance. Do not reintroduce mandatory hand repair or the rejected generated head-pat action.

For summer, use the [independently reviewed continuous new LTX exchange](ltx23-summer-pilot-review.md), source`[0,5)`, across S025/S026. Hold its exact first frame for63frames at118.250–120.875, then play all120consecutive source frames once through125.875. S025contains source`[0,48)`; S026continues`[48,120)` with the identical fixed wide crop. **No reset, retiming, repeat or endpoint hold.** The source recommendation favors this continuous progression over the original male/new-response join, whose broad smile/head angle/cuff differed. Original male-only derivative and its reviewed proof remain preserved as an inactive alternate; this does not reapprove original M02’s drifting female face.

## Bounded editorial changes

| Change | Exact proposed boundary/source | Reason |
| --- | --- | --- |
| S021→S022 | **106.125s / frame2547**, from106.416667/frame2554 | Restore R4 withdrawal close-up S02, then wider distance S01. |
| S022→S023 | **110.125s / frame2643**, from110.166667/frame2644 | Restore the original matched singing entrance. |
| S023→S024 | **114.500s / frame2748**, from114.750/frame2754 | Preserve rounded “you” through the last displayed frame before the original cut; return to original S02 reaction. |
| S025→S026 | **122.875s / frame2949**, from122.458333/frame2939 | Internal administrative split between consecutive new source frames47/48; identical wide framing, no visible reset. |
| S026→S027 | **125.875s / frame3021**, from126.750/frame3042 | Remove the planned.875s frozen summer tail; enter existing P01earlier with absolute mouth timing preserved. |
| Inside S029 | **145.625s / frame3495**, P02→P01 | Carry over R4's original performance-angle change at the matching song position. |
| S016,S020 | Replace redundant P01 stage plates with S02 hospital reactions | Keep the original song; reuse supplied eye art rather than inventing new unsynchronized singing jobs. |
| S033,S043 | Use the established M01 aftermath | Continue his concern after the chorus and before the screams; reduce repetitive stage cards. |
| S034,S041,S045 | Replace isolated window pose with her reaction **within M01's held contact** | The current candidate fixes S030/S032/S042/S047, but these remaining solo-window returns can still erase the embrace geographically. |

The summer update additionally moves **S026→S027 from3042/126.750 to3021/125.875**, removing the planned21-frame endpoint hold. Existing P01S027starts21frames earlier; its mouth drawings retain absolute original-song timing. All later boundaries and6667total frames remain unchanged. S007–S008 share one continuing room camera curve; S050–S051 share one indoor dawn curve. Root’s subsequent locked1.0S019/S042camera repairs are preserved.

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

Implementation evidence: [exact production source/timing diff](production-continuity-diff.json). The selected target is now115.083333s of new delivery,2s more because the new5s summer exchange replaces the former new3s reply plus historical2s male segment. Active adopted new intervals now total 38.083333s (the previous 21.375s plus A06 arrival 6.208333s, S030 held contact 4.083333s and fixed window close-up 6.416667s), leaving 77s without accepted source. The previous 21.375s have scoped placement reviews; the latest 16.708333s and their changed neighbouring cuts remain pending independent review. Active historical video is M01only5.041667s. Original mouth/eye drawing sequences remain separately counted. Sequence acceptance and musical listening do not follow automatically from source approval.


Latest bounded performance update: root adopts [first chorus source](ltx23-first-chorus-review.md) frames`[3,101)` for S014and [third plea source](ltx23-third-plea-review.md) frames`[3,85)` for S046. No shot boundaries change. S014must remain wide and uses opt-in **contain**, preserving full896×512source with narrow symmetric side padding at16:9; its native crown grazing is a source limitation, not reconstructed detail. S046uses existing wide fill; root accepts its higher palm as distressed escalation while retaining hand-exit, moving detail softness and repeated upward-motif caveats. No new loop, retiming or hold. Exact original-master insertion/context proofs, rather than source approval alone, govern promotion.


Current review reconciliation: S014 has a scoped pass for the final contained v2 and its current neighboring cuts; S046 has a scoped pass for the wide insertion and four-plea staging. S028 has both its exact sequence pass and the pinned incoming/outgoing cut pass in [the placement review](short-reuse-placement-review.md). These do not certify subjective musical pacing or later replacement footage. The creation-time base-config record above remains unchanged.

The latest addition is [reviewed snowy-walk source](ltx23-walk-pilot-review.md) frames `[3,135)`:132frames /5.5s at50.5–56.0, covering the whole S011slot with standard fixed wide fill. Approximately seven support exchanges were accepted despite the rough three-to-five target. No additional freeze, repetition or retiming. Separate S011 and S010–S013 original-master proofs check actual crop and journey/arrival continuity; source review alone does not promote the edit.

[Walking insertion/context proof evidence](walk-insertion-implementation.md) records the exact new outputs and their current review scope.

The exact walking insertion and current cuts now pass [independent sequence review](walk-sequence-review.md), including all 132 reconstructed frame matches, preserved head/feet/ground and actual 1× context playback with zero dropped frames or media errors. Future window and arrival motion require new seam checks.


Latest quiet-source selection (JML-026): **S013 uses A06 `[3,152)`, 149 frames / 6.208333s; S030 alone uses L05 `[3,101)`, 98 frames / 4.083333s.** Every timeline boundary stays fixed. Both use full-image contain with no additional crop, zoom, retiming, loop or hold. A06 supplies an anxious inward pause with sustained eye closure, not the originally requested brief blink. L05 retains its conspicuous native push-in/pull-back and crown/lap cropping; it preserves contact and supplies a tired blink, not proven uneven breathing. The rejected later release/point/regrip is excluded. **S032 remains unfinished and receives none of L05; L04 and original full-width L01 are not selected.** The original full-width window source remains rejected; the later separately adopted fixed derivative is described below. Standalone and S012–15/S029–32 original-master proofs require independent exact-sequence review.

[Quiet insertion proofs and technical evidence](quiet-insertion-implementation.md) retain exact export/config hashes and the unreviewed sequence scope.


The separately reviewed **fixed window close-up now fills S003**, source `[3,157)` / 154 natural24fps frames at12.791667–19.208333s. It preserves the derivative’s entire672×378 picture (original x224/y0/w672/h378 crop), without additional crop, zoom, hold or timeline change. Faulty reflected eyes/mouth stay excluded; faint peripheral reflected ear/rear cheek/neck/hair remains. The larger head rise/turn and lowered gaze are accepted as withdrawn acting rather than the original minimal-breath request. Native crown limitation and distant passersby remain disclosed. Original full-width L01 is still rejected. Exact insertion and S002–S004 cuts need independent sequence review; prior proofs are preserved.

[Exact window insertion proofs and technical evidence](window-insertion-implementation.md) retain the snapshot and outstanding independent sequence-review scope.
