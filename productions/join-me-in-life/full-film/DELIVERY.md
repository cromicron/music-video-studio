# Join Me in Life — completed film

**Historical first hybrid film. The current selected C version is [Unfinished Morning — complete-film delivery](unfinished-morning/DELIVERY.md).** The records below preserve the earlier film and must not be mistaken for current creative acceptance.

[Watch the complete film in Google Drive](https://drive.google.com/file/d/1bzwoKWyRFhf677XgDP5a3qmuHTTZ_OCC/view?usp=drivesdk). This private 1080p viewing copy is 70.3 MB, with the same 6,667 frames, timing and unchanged AAC audio. Its picture is compressed for delivery. If Drive is still processing its preview, use its Download button. A workspace-path link failed for Dario; use this hosted link in chat. [Viewing-copy verification and reproduction](research/viewing-copy-delivery.json).

[Download the complete film and verification files from the private production archive](https://github.com/cromicron/music-video-studio/releases/tag/join-me-in-life-full-v1). Local playback file: `exports/Join_Me_in_Life_Full_Music_Video.mp4`. This is the delivered 1080p hybrid film; the older animatic, story check and workprint remain historical references.

**1920×1080 · 24 fps · 6,667 frames · 277.791667 seconds.** The complete original take 49 song is277.776 seconds, encoded once as256kb/sAAC for portable playback. MP4 SHA-256: `865b8a620c5905b239f0665c1019d42d2f9f38280dc298e49a78d3f02d9e71d4`. [Delivery manifest](exports/Join_Me_in_Life_Full_Music_Video.manifest.json) · [acceptance record](review/final-acceptance.json).

The three new creative production tools are **ChatGPT image generation → owned LTX animation → FFmpeg**. Supplied historical M01 footage retains its Kling O3 Pro/Runway provenance; the earlier drawing exposures are composited with FFmpeg. No new Blender rendering or paid video generation was used. Actual new cash and purchased Runway-credit spend are both **zero**.

| Picture source | Seconds |
| --- | ---: |
| Newly generated, reviewed LTX footage |115.083333|
| Supplied original embrace footage |5.041667|
| Supplied drawing-exposure sequences |32.666667|
| First-frame holds |6.458333|
| Endpoint holds |3.250000|
| Still artwork with camera movement |115.291667|

This is a complete hybrid music video. The table does not claim continuous body animation or complete phoneme synchronization throughout. LTX source frames are 896×512 and enlarged for the 1080p export; enlargement does not create native detail. Slight moving face/hand softness, tight native crown framing and source-cropped lower hands remain documented. No unresolved blocking movement/contact/cut finding remains in the delivery reviews.

## Verification

[Whole-film review](review/final-full-film-review.md), [final native-picture review](review/final-positive-1080-review.md) and [four-plea sequence](review/positive-four-pleas-sequence-review.md) bind the actual output. All 6,667 decoded pictures match independently reconstructed new shots or previously reviewed stable shots. All planned new source intervals have exact placement/current-cut reviews. One continuous embrace, maintained contact, withdrawn reaction, original branding, original-song coverage, all four pleas and final fade are retained.

Full unseeked 1× playback completed with audio enabled, no errors/stalls/corruption and three browser presentation drops among 6,667 frames. Original-song correlation is0.99965899 at zero detected offset. This is instrumented playback plus inspected frames, not human-equivalent continuous watching, subjective listening or verified phoneme sync. The final metadata-only remux preserves every video/audio packet and timestamp from that reviewed candidate and passes full decode. Thirty-five repository tests pass.

## Recover in a new environment

From the repository root, with the existing authorized GitHub account:

```sh
gh release download join-me-in-life-full-v1 --repo cromicron/music-video-studio --pattern 'Join_Me_in_Life_Full_Music_Video.mp4' --pattern 'Join_Me_in_Life_Full_Music_Video.manifest.json' --pattern SHA256SUMS --dir productions/join-me-in-life/full-film/exports --skip-existing
cd productions/join-me-in-life/full-film/exports
sha256sum -c SHA256SUMS
```

The 125 MiB movie exceeds GitHub's ordinary 100 MiB single-file limit. Its exact bytes are retained in three verified Git archive parts, with a single-file private release for convenient download. Its manifest, checksum, editable sources and reviews are also retained in Git. [Archive verification](research/final-delivery-archive.json) tracks private upload and independent download verification. No public YouTube upload is part of this delivery.

If the release download is unavailable, the repository alone can restore the exact film without any account or network request:

```sh
python3 productions/join-me-in-life/full-film/tools/restore_delivery.py
```

The helper verifies each part and the combined SHA-256, preserves an existing different file, and reconstructs the accepted bytes without re-encoding. This route was tested into a fresh output directory. [Archive index](exports/archive/index.json).

## Rebuild or revise

Read [STATUS](../STATUS.md) and [the source approval record](review/approved-motion-production.json). Render from the repository root:

```sh
python3 productions/join-me-in-life/full-film/edit.py --edit productions/join-me-in-life/full-film/edit-production-candidate.json --render --width 1920 --height 1080 --crf 18 --work-dir build/production-1080-cache --output build/Join_Me_in_Life_Full_Music_Video_QC.mp4
```

The immutable configuration's render-time pending annotations are historical; current acceptance is in STATUS and the hash-bound acceptance record. A changed shot, source, codec or byte-different rebuild needs appropriately scoped review. [Finalization tool](tools/finalize_delivery.py) refuses to overwrite a file or finalize a candidate whose hash/reviews differ from the explicit acceptance. Never relabel the old workprint.

The [paid production recommendation](research/paid-budget.md) is separate: an optional single$10 API allocation across ten comparable complete hybrids, stress-budgeted at€12.257 including 19% tax and 3% payment/FX allowance, with an absolute€20cash ceiling. It adds a small Runway Gen-4 Turbo upgrade only when better than the free source. No paid version has been generated or purchased; paid-only full generation at this cap is not established.
