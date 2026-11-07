# P1L03 source review evidence

The [source review](../ltx23-positive-P1L03-review.md) owns the creative verdict. The exact raw full image passes only `S015` source `[3,104)` at natural 24 fps. These files do not approve a production insertion or neighboring cuts.

- `source-checks.json`: actual source/guide/manifest/provenance/reference hashes and extraction scope.
- `verdict.json`: selected interval, retained limits and compact evidence hashes.
- `overview.jpg`, `face-reflection-phases.jpg`: complete action and sensitive facial phases.
- `eye-detail.png`, `reflection-detail.png`: nearest-neighbor enlargement of decoded source pixels, with no enhancement.
- `selected-end.jpg`: final selected source frame.
- `playback-1.70.jpg`, `playback-4.00.jpg`: captured during actual 1× selected playback. The accompanying telemetry records capture timing; filenames denote requested playback time, not an exact decoded frame claim.
- `playback-summary.json`: playback under the shared review lock; `playback-initial-summary.json` preserves the first uncoordinated runs.

Every one of the 113 decoded frames was inspected in full-frame contacts and native face/reflection contacts. All raw PNGs, dense sheets, the selected playback proxy and complete callback telemetry stay under ignored `build/ltx23-positive-P1L03-review/`; compact evidence is kept here.

Reproduce from the repository root with existing Python/Pillow, FFmpeg/ffprobe, Playwright and `/usr/bin/chromium`:

```sh
python3 productions/join-me-in-life/full-film/review/ltx23-positive-P1L03-review/reproduce_evidence.py
flock build/source-review-playback.lock python3 productions/join-me-in-life/full-film/review/ltx23-positive-P1L03-review/playback_check.py
```

The scripts write only the ignored build folder and verify the pinned source hash before extraction/playback. A later reproduction can have different local playback timing; it does not silently replace the retained reviewed evidence. No listening or human-equivalent continuous viewing is claimed.
