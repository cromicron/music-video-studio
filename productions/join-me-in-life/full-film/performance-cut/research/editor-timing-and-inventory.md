# Editor timing, source inventory and reconstruction ledger

The actual unchanged take49 file is 277.776 seconds, SHA256`0fe0f566e985a0b028e12543679d3b142ee7b1b62425fcb595799b35ba116cbb`; picture is 6,667 frames/277.791667s at 24 fps. This pass freshly verifies that source hash and exact source/gate/range/cadence bindings. It does **not** claim a new subjective listening review, exact phoneme alignment or a newly authenticated beat grid.

## Timing anchors used

The 14 prior reviewed Short cues transferred by waveform offset 100.373s remain the stronger phrase anchors. The original lyric sheet governs words; ASR misrecognizes some. In particular the bridge lyric is “And our sad songs make it art,” not the later paraphrase “hard.” Preserve the original recording rather than rewriting its words.

| Passage | Seconds / nearest picture frame | Evidence limit |
| --- | --- | --- |
| Opening instrumental/hook |0–33.125; hook onset uncertain12.70–15.36 | Don't claim syllable-level hook sync. |
| Verse1 organising lines |33.125–50.5 /795–1212 | ASR planning section anchor, not exact bar verification. |
| Pre1 / chorus1 |50.5 /66.5 | Planning anchors adopted on24fps grid. |
| Verse2 |100.373 /2409 | Prior reviewed Short alignment. |
| Wrong words |118.253–122.373 | Prior reviewed Short lyric cue. |
| Stupid summer songs |122.473–126.493 | Prior reviewed Short lyric cue. |
| Only summer memory |114.75–134.375 /2754–3225 | C15+originalC16+C17,19.625s; one continuous memory block, no other warm future. |
| Pre2 / waiting-room offer |126.753 /134.353 | Waiting room remains an offer in lyrics, not a required clinic event. |
| Chorus2 |142.653 /3424 | Prior reviewed Short anchor; picture uses3424. |
| Synth instrumental region |171.375–191.583 /4113–4598 | Word gap plus musical texture, not isolated-synth onset proof. |
| Bridge / rehearsal recognition |191.583–207.875; O03 at202.333–207.875 | Original actual audio used; no diagnosed mental state from tidying alone. |
| Four full-force pleas |207.875 /211.25 /215.916667 /219.375; final release223.5 | Distinct previously accepted conditioned source takes at exact original slots. |
| Final chorus / outro |223.5 /247.125 | Band returns briefly after the uninterrupted intimate bridge/pleas. |
| Renewed musical event |261.958 /6287 | Measured mixed-track spectral event; C38 remains at the exact boundary. |
| New tears/look ending |269.875–277.791667 /6477–6667 | O04 replaces old sip/look-down ending; user wants emotional opening with uncertainty. |

## Reuse classification from actual saved motion

[Opening contact evidence](editor-frames/opening.jpg), [world-classification contact evidence](editor-frames/ambiguous.jpg), [short-closing handles](editor-frames/closing-handles.jpg), and [exact C38 exit](editor-frames/C38-exit.png) were extracted from declared source frames for visual classification. They do not replace dense mechanics or full joined playback reviews. Exact frame/sample provenance is in [the inspection record](editor-frame-inspection.json).

- **Exclude the gold-world sources:** C04,C08,C09,C10,C11,C12,C19,C20,C23,C24,C25. C10–12 visibly retain gold planes/alternative worlds; these are not merely blue present clips despite some present action. Their87.0seconds become band footage.
- **Do not overclaim C05:** its real action is a hand sweep across an already clean table; it cannot alone supply the requested fuller organising-place scene. New O01/O02 supply distinct real actions. A previously unused 112-frame C05 subset later punctuates the stage sequence without showing a new imaginary world.
- **Present despite stale draft language:** C21, C26 and C33 sampled frames are the plain blue kitchen. The inherited story text about turning from possibilities/receding gold is reconciled in the built edit rather than fed into new plate prompts. C22 actually raises his own partly open hand toward his face and lowers it, not the old drafted knee-clench.
- **Four pleas:** existing portrait takes have actual kitchen clothing and backgrounds, not literal projected future rooms. Preserve their first full-force entry and different acting. Their old world tags are reconciled to`present`; no source pixels or timings change.
- **Short C35:** accepted raw[6,61) raises clasped hands from lap toward chest. This is self-containment, not tiny thumb release or recovery. A cut to drums can elide the eventual lowering.
- **Short C37:** accepted raw[118,182) gives his settled look toward her while she remains downcast. Avoid earlier upward-gaze fragments that might pre-empt O04's reciprocal look.
- **C38→O04:** exact C38 exit raw195 has mug upright on table, her right hand relaxed beside it (viewer-left), gaze down. New O04 should start from that state; no sip must be assumed.

## Frozen provider plan versus current editorial plan

[Provider plan v1](../story/shot-plan-v1.json) remains immutable, SHA256`420d9e7c086b028f716eff2e90fc0bad093de36c8da508560febb89aeace3b6e`. Its 18 new takes total 128.75 raw seconds, with 87.0 seconds band and 30.291667 seconds new story retained. A2V B05/B08 each split into two 113-frame takes; all raw requests respect 8n+1, 6-frame heads and at least 6-frame tails.

[Editorial plan v2](../story/editorial-plan-v2.json), SHA256`f76d8065d1970a22652910f667267d7b5d5c26c809f445dea4a36459f6524075`, reallocates B06/B09 parts for a later band return without new generation or repeated frames. It has 46 shots. The [current partial edit](../edit/edit-v002.json) removes stale reused-source provider instructions and applies [explicit prose reconciliations](../edit/prose-reconciliations-v2.json), leaving only present/memory/band worlds. Root's late-return choice keeps the whole 191.583–223.5 bridge and four pleas with the pair, returns to band for 9.833 seconds later, then leaves C38/O04 intimate.

The guarded source ledger has 26 inherited reviewed selections and 20 unbound new editorial selections drawn from 18 future takes. Every inherited source SHA/review SHA/accepted range and decoded cadence passed the retained strict engine. All future source recipes have exact lengths, no overlap, and cover their adopted keeper extents once. Those checks do not approve new motion, cuts or the whole film; [initial technical record](editor-initial-validation-v1.json).

## Current full picture ledger

| Shot | Frame interval | Seconds | World | Source selection / production request |
| --- | --- | --- | --- | --- |
|O01|[0,192)|0.000–8.000|present|NEW O01 raw[6,198)|
|C02|[192,384)|8.000–16.000|present|C02_OPENING_B_V2 raw[6,198)|
|C03|[384,588)|16.000–24.500|present|C03_OPENING_B_V2 raw[6,210)|
|B01|[588,795)|24.500–33.125|band|NEW B01 raw[6,213)|
|O02|[795,1007)|33.125–41.958|present|NEW O02 raw[6,218)|
|C06|[1007,1212)|41.958–50.500|present|C06_OPENING_C_V2 raw[6,211)|
|C07|[1212,1404)|50.500–58.500|present|C07_OPENING_C_V2 raw[6,198)|
|B02|[1404,1596)|58.500–66.500|band|NEW B02 raw[6,198)|
|B03|[1596,1716)|66.500–71.500|band|NEW B03 raw[6,126)|
|B04|[1716,1800)|71.500–75.000|band|NEW B04 raw[6,90)|
|B05A|[1800,1897)|75.000–79.042|band|NEW B05A raw[6,103)|
|B05B|[1897,1994)|79.042–83.083|band|NEW B05B raw[6,103)|
|B06_A|[1994,2090)|83.083–87.083|band|NEW B06 raw[6,102)|
|C05_RETURN|[2090,2202)|87.083–91.750|present|C05_OPENING_C_V2 raw[6,118)|
|B07|[2202,2404)|91.750–100.167|band|NEW B07 raw[6,208)|
|C13|[2404,2580)|100.167–107.500|present|C13_MIDDLE_A_V2 raw[2,178)|
|C14|[2580,2754)|107.500–114.750|present|C14_MIDDLE_A_V2 raw[6,180)|
|C15|[2754,2901)|114.750–120.875|memory|C15_MIDDLE_B_V2 raw[6,153)|
|C16|[2901,3021)|120.875–125.875|memory|C_ORIGINAL_M02 raw[0,120)|
|C17|[3021,3225)|125.875–134.375|memory|C17_MIDDLE_B_V2 raw[6,210)|
|C18|[3225,3424)|134.375–142.667|present|C18_MIDDLE_B_V2 raw[6,205)|
|B08A|[3424,3524)|142.667–146.833|band|NEW B08A raw[6,106)|
|B08B|[3524,3624)|146.833–151.000|band|NEW B08B raw[6,106)|
|B09_A|[3624,3696)|151.000–154.000|band|NEW B09 raw[6,78)|
|C01_RETURN|[3696,3820)|154.000–159.167|present|C01_OPENING_A_V2 raw[6,130)|
|C21|[3820,3972)|159.167–165.500|present|C21_MIDDLE_C_V2 raw[6,158)|
|C22|[3972,4113)|165.500–171.375|present|C22_MIDDLE_C_V2 raw[6,147)|
|B10|[4113,4281)|171.375–178.375|band|NEW B10 raw[6,174)|
|B11|[4281,4449)|178.375–185.375|band|NEW B11 raw[6,174)|
|B12|[4449,4598)|185.375–191.583|band|NEW B12 raw[6,155)|
|C26|[4598,4728)|191.583–197.000|present|C26_BRIDGE_A_V2 raw[6,136)|
|C27|[4728,4856)|197.000–202.333|present|C27_BRIDGE_A_V2 raw[6,134)|
|O03|[4856,4989)|202.333–207.875|present|NEW O03 raw[6,139)|
|C29|[4989,5070)|207.875–211.250|present|C29_PERFORMANCE_B_V2 raw[6,87)|
|C30|[5070,5182)|211.250–215.917|present|C30_PERFORMANCE_D_V2 raw[6,118)|
|C31|[5182,5265)|215.917–219.375|present|C31_PERFORMANCE_C_V2 raw[6,89)|
|C32|[5265,5364)|219.375–223.500|present|C32_PERFORMANCE_D_V2 raw[6,105)|
|C33|[5364,5562)|223.500–231.750|present|C33_BRIDGE_A_V2 raw[6,204)|
|C34|[5562,5752)|231.750–239.667|present|C34_BRIDGE_A_V2 raw[6,196)|
|C35|[5752,5807)|239.667–241.958|present|C35_CLOSING_A_V2 raw[6,61)|
|B09_B|[5807,5931)|241.958–247.125|band|NEW B09 raw[78,202)|
|C36|[5931,6111)|247.125–254.625|present|C36_CLOSING_A_V2 raw[6,186)|
|B06_B|[6111,6223)|254.625–259.292|band|NEW B06 raw[102,214)|
|C37|[6223,6287)|259.292–261.958|present|C37_CLOSING_A_V2 raw[118,182)|
|C38|[6287,6477)|261.958–269.875|present|C38_CLOSING_A_V2 raw[6,196)|
|O04|[6477,6667)|269.875–277.792|present|NEW O04 raw[6,196)|
