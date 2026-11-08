# Mercy in Minor — consolidated anime band v1

[Open the16-page reference book in Google Drive](https://drive.google.com/file/d/1dxvZTDOmWkAzDl5LCBczMtzENqM8xALD/view?usp=drivesdk) · [All individual PNGs](https://drive.google.com/drive/folders/1S_nYDZsVbwUb30bbLjHZOgYifxpB7Dqj) · [Full-band stage preview](https://drive.google.com/file/d/12JwYkYp8_c3IQBxarrFgpv01dBlNbIx2/view?usp=drivesdk).

This is the current reusable band reference pack for the Join Me in Life performance revision. The newly supplied lineup overrides the earlier all-male proposal. The keyboardist's four photographs are one person, supplemented by his supplied anime face. The previous silver-streak keyboardist concept is historical. User-selected references are distinct from approval of every generated realization; this pack is a production proposal with independent static review.

## Members and authority

| Stable ID | Member | Identity / costume | Instrument / poses |
| --- | --- | --- | --- |
| keys | Dario-inspired keyboardist | [Four views + four expressions](sheets/keys.png): supplied anime face, spiky dark-brown hair, full short beard, black leather biker jacket and printed black tee, jeans/boots, silver cross. | [Standing, seated and detail](poses/keys.png): silver Tyros-inspired arranger, black central display, outer speakers, X stand; stool/pedal in seated view. |
| guitar | Blonde guitarist; name not supplied | [Four views + four expressions](sheets/guitar.png): long pale-blonde hair, lace corset/sleeves, asymmetric lace overskirt and strapped trousers/boots, neutral circular flower ornament. | [Three playing poses](poses/guitar.png): right-handed black cream-bound six-string single-cut guitar, two humbuckers, four knobs, six tuners. |
| bass | Dirty-blond bassist; name not supplied | [Four views + four expressions](sheets/bass.png): tied-up hair, small goatee, embroidered black coat over cream shirt, ragged tails, chains and boots. | [Three corrected poses](poses/bass.png): right-handed dark figured-wood four-string bass, four tuning machines in2+2 configuration. |
| drums | Black-haired drummer; name not supplied | [Four views + four expressions](sheets/drums.png): long loose black hair, small pointed goatee, hoops, ornate brass-button jacket. | [Three playing poses](poses/drums.png): black five-piece kit, exactly two sticks per view; upper-body contact reference. |
| vocal | Yaro; older records also spell Jaro | [Established angles](../../productions/join-me-in-life/art/01_Characters/C04_Man_Angles.png) and [expressions](../../productions/join-me-in-life/art/02_Expressions/E02_Man_Expressions.png) retain priority: brown tousled hair, blue-grey eyes, light stubble and round silver disc. | Original [verse](../../productions/join-me-in-life/art/04_Performance/P01_Verse_Performance.png), [chorus](../../productions/join-me-in-life/art/04_Performance/P02_Chorus_Performance.png) and [plea](../../productions/join-me-in-life/art/04_Performance/P03_Bridge_Plea.png) art reused. |

**Only the keyboardist wears a cross.** This is Dario's explicit character direction; he alone is a person of faith in the band for now. Other members have neutral jewelry and no religious motifs. The blonde guitarist is a band member and distinct from the red-haired narrative woman. The latter remains outside the performing band.

The leather stage outfit is selected from the user's wardrobe references. The plain black templates supply body/playing reference rather than overriding that outfit; denim remains an unused alternate, not a silent costume change.

## Fixed stage and reuse

The [stage wide](stage/wide.png) and editable [plot](stage/plot.svg), [PNG](stage/plot.png) and [coordinate/camera record](stage/plot.json) distinguish audience-left/right: Yaro downstage centre, guitar front left, bass front right, keys rear left, drums on a shallow rear-centre riser. Numerical planning coordinates are illustrative, not a calibrated reconstruction of the painted wide. Keep drummer visibility and instrument neck clearance when choosing cameras. The neutral identity lineup's left-to-right ordering is not the stage order.

[Manifest](manifest.json) gives stable asset IDs, exact image hashes, file sizes, role locks, source paths and verified Drive links. Turnaround sheets own faces/major costume construction; corrected pose sheets own broad instrument hardware; original Yaro art owns his identity. Fine lace/embroidery and keyboard button layouts vary slightly. Choose one panel's hardware when preparing a shot. Sheet panels are montages for reference, not ready-to-animate whole frames: compose a single clean shot with the chosen character, hands and instrument before animation.

The pack contains11 new retained PNGs plus five reused Yaro sources. The four new members have16 full-body angle views,16 expressions and12 performance poses collectively. [Exact generation prompts](prompts/lineup.txt) and all companion prompt files remain in `prompts/`. Original raw chat attachments were not available as portable local files; the derived canonical references and their provenance are retained. [Development images](development/) preserve rejected prop versions; do not use them as current instrument references.

## Method and verification

The applied Be Ambitious goal is a reusable cast that survives different shots and sessions, rather than unrelated attractive portraits. Professional methods are lineup, turnaround, action/expression reference, fixed stage geography and independent review; [primary-source research](research.md) records the basis. The production instruction is: preserve each supplied identity and selected costume in the existing anime language, keep the keyboardist's cross unique, prepare coherent right-handed instrument poses, and bind a reviewed reusable library to exact sources before new animation.

[Independent static-art review](review.md) passes the final pack after correcting excess sticks, missing bass tuners and cross-like pendant drift. Static anatomy/contact plausibility does not establish exact fingering, keyboard key grouping, drum pedal mechanics, musical note sync or motion quality. Those require song-specific single-shot plates and consecutive-frame/playback review during animation. New paid video-provider spending is€0; only the included ChatGPT image tool was used for new art. The delivered film is preserved and no new band animation has been inserted yet.

The [book](Mercy_in_Minor_Anime_Band_Reference_Book.pdf) embeds whole original images without source editing/cropping. Rebuild from the repository root with `python3 band/lineup-v1/build_book.py`; dependencies are ReportLab and Pillow in the existing environment. The builder verifies all image hashes and image bounds; [build record](book-build.json) binds its source manifest. [Drive verification](delivery.json) records completed upload/readback and critical exact-download checks.
