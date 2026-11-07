# Positive window sequence evidence

This folder accompanies [the scoped review](../positive-window-sequence-review.md). The exact proof covers S009–S016, master `[998,1896)`, 898 frames at 24 fps. Local frame zero is master frame 998. All intervals are zero-based and half-open; JPEG labels give local and master indices and local media time.

`frozen-manifest.json` and `frozen-edit.json` are exact historical snapshots. The manifest's pending sequence-review text records its state before this review, not a current verdict. The full configuration hash is pinned even if the live edit file later changes other shots.

`checks.json` records independent integer-frame reconstruction of both insertions, prior-neighbour comparisons, source/export hashes and timestamp checks. The four `cut-*.jpg` sheets preserve the two actual 960×540 boundary pictures at native output dimensions. `S010-native-face-phases.jpg` and `S015-native-face-phases.jpg` use native-scale output crops solely for inspection; those crops are not production framing. `sequence-overview.jpg` and `S016-exposure-phases.jpg` are compact thumbnails. Reproduction keeps all extracted PNGs, all 214 inserted frames in contact sheets, native face sheets and cut-phase sheets in ignored `build/positive-window-sequence-review/`.

From the repository root:

```sh
python3 productions/join-me-in-life/full-film/review/positive-window-sequence-review/reproduce.py
python3 productions/join-me-in-life/full-film/review/positive-window-sequence-review/verify_audio.py
flock build/source-review-playback.lock python3 productions/join-me-in-life/full-film/review/positive-window-sequence-review/playback_check.py
```

Dependencies are FFmpeg/ffprobe, Python with NumPy/Pillow/Playwright, and `/usr/bin/chromium`. Each script checks its exact media inputs before proceeding. Reproduction writes only to this review's separate ignored build directory. The playback server selects an ephemeral localhost port and Chromium uses a separate temporary profile; no provider or network service is involved. The checked run was capture-free and audio-enabled. Browser execution and waveform alignment are recorded separately from visual inspection and do not constitute a subjective listening or phoneme-sync claim.

`verdict.json` records SHA-256 values for the report, retained evidence, original frozen source reports and operative media inputs. Large frame grids and playback callbacks remain reproducible in ignored build storage rather than being copied into this compact folder.
