# Revision 2 editing boundary

The existing [editor](../../edit.py) deliberately substitutes still artwork when no approved clip exists and clones the first/last frame to fill a longer shot. That is useful for an animatic, but cannot enforce the newly requested animation scope. Keep that editor and all v1 records unchanged.

The small [strict v2 adapter](../tools/editor/strict_edit.py) reuses the original editor's process, probe, hashing and original-song correlation helpers. It uses an explicit frame-index trim and full-image contain for every picture interval, with no `fps` conversion filter, `tpad`, repeated source interval, silent still fallback or speed field. After proving source cadence, it normalizes container timestamp rounding to exact 24 fps and encodes at that rate; the real fixture proves no selected picture is added or dropped. It refuses a selected clip shorter than its exact timeline slot. A missing take is unresolved production, not permission to fill its slot. No generated source audio enters the result.

This does not detect all frozen or repeated pictures *inside* a generated take, nor discover that two differently encoded files reproduce the same performance. Raw take identity, review-bound SHA and the independent source review must catch that. It also does not infer story quality, contact continuity or whether an intentionally quiet shot earns its duration. Those are [outside-review questions](../review/acceptance-rubric.md), not coding scores.

## Plan and continuity schema

Start from [plan-template.json](../tools/editor/plan-template.json). Its empty shots intentionally fail until a full story has been entered. All file paths in a populated plan are relative to `full-film/`, even if the plan itself is saved below revision-2. Full plan validation requires exactly 6,667 contiguous frames at 24 fps, including an explicitly described action/consequence and entry/exit continuity for every shot. A draft has no source approval merely because it passes its timeline checks.

One source record, under `sources`, has this form (placeholder values must be replaced):

```json
{
  "TAKE_A": {
    "kind": "video",
    "path": "revision-2/assets/motion/TAKE_A/video-silent.mp4",
    "sha256": "EXACT_VIDEO_SHA256",
    "take_id": "unique_original_generation_id",
    "review": {
      "status": "accepted",
      "path": "revision-2/review/TAKE_A.md",
      "sha256": "EXACT_REVIEW_SHA256",
      "accepted_ranges": [[3, 171]]
    }
  }
}
```

The external source review must name the exact video SHA and support its declared accepted ranges. The adapter checks the bindings and containment, but cannot establish that the critic actually performed the review. Source selection uses zero-based, end-exclusive decoded frame indices. Sources are completely decoded to establish actual frame extent and natural 24 fps cadence. Selecting different non-overlapping intervals from the same accepted take is allowed; selecting any frame twice is refused even through a source ID alias.

One shot record has this shape:

```json
{
  "id": "V201",
  "start_frame": 0,
  "end_frame_exclusive": 168,
  "section": "intro",
  "world": "present",
  "story": {
    "before": "Describe the established situation.",
    "action": "Describe the visible playable action.",
    "after": "Describe what the action changes."
  },
  "continuity": {
    "entry": {
      "location": "Named set and time",
      "blocking": "Characters, screen direction, gaze and contact",
      "props": {"named_object": "position/possession/state"}
    },
    "exit": {
      "location": "Named set and time",
      "blocking": "Characters, screen direction, gaze and contact",
      "props": {"named_object": "position/possession/state"}
    },
    "cut_to_next": "Motivation and what the next shot must inherit"
  },
  "source": {"id": "TAKE_A", "in_frame": 3, "out_frame_exclusive": 171},
  "framing": "contain",
  "fade_out_frames": 0
}
```

This is a schema example, not an invented scene in the new treatment. `world` and additional editorial notes can be used without changing generation. The core ledger fields are required; their correctness remains a visual judgment. Cropping is not added silently. If a deliberate reframed derivative is selected, preserve its original take provenance and review the exact derivative before registering it as a new source. Only the final moving shot may have an explicit fade; the fade does not add frames. Titles, drawings or intertitles are not implemented as motion fallback; an intentional future drawn sequence needs explicit reviewed source footage and a separately recorded editorial reason.

## Commands

From the repository root, first validate the full timeline and ledger without requiring pending motion assets:

```sh
python3 productions/join-me-in-life/full-film/revision-2/tools/editor/strict_edit.py PATH_TO_PLAN --draft
```

Validate accepted source bindings with the same command without `--draft`. Use `--shots V201:V204` to validate or render a contiguous excerpt while later source records are still pending. Its resulting manifest declares partial coverage and its exact original-song offset. Full output is refused until every shot has sufficient accepted source footage.

```sh
python3 productions/join-me-in-life/full-film/revision-2/tools/editor/strict_edit.py PATH_TO_PLAN --render --output build/v2-review-candidate.mp4 --work-dir build/v2-review-render
```

Output is 1920×1080 by default, H.264 yuv420p and AAC256k encoded once from the complete original take49 MP3, with `faststart`. No lyric, mix, tempo or soundtrack change occurs. “Unchanged song” here means content and alignment, not byte-identical audio compression. The default is portable AAC rather than MP3-in-MP4. No `-shortest` trims the full song. Original audio SHA, waveform alignment, source selections, every review binding and output SHA are retained in the adjacent manifest. The manifest labels the film a candidate: source validation is not final-cut or music-pacing approval.

Use a new output path and an empty render work directory. Existing results are not overwritten and stale source renders are not implicitly trusted. Partial source approval is insufficient for a longer planned shot. All final frames must decode, and the whole original song must correlate at the expected offset. Publish/Drive delivery and final independent viewing review remain separate from this adapter.

## Verification

Run `python3 -m unittest discover -s productions/join-me-in-life/full-film/revision-2/tools/editor -p 'test_*.py' -v`. The focused cases reject timeline gaps, missing motion, short coverage, out-of-bounds intervals, overlapping selections behind aliases, changed review hashes, unreviewed ranges and non-24-fps sources. A real FFmpeg fixture renders two consecutive frame-index trims and proves every selected decoded picture equals the source sequence across the join. It does not claim that synthetic test footage is a reviewed music-video shot.

On 7 November 2026 all nine focused tests passed. A separate actual CLI smoke run validated a complete draft ledger with later sources still pending, rendered only its two selected synthetic intervals at 640×360, and joined them to the original song at frame792 /33 seconds. The 24-picture-frame excerpt fully decoded, declared partial coverage and zero padding/reused intervals, and measured original-song correlation0.9995036556 with zero detected lag. The temporary fixture was removed afterward; it is not a proposed story shot. The first frame-order test caught an end-packet duration problem in passthrough timestamp mode; explicit validated 24fps encoder timing resolved it, with exact picture equality retained.
