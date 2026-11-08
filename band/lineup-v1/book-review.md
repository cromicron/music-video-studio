# Independent reference-book check

**PASS for the checked PDF and scope below.**

Book SHA256: `75e15bda1fa5685bdd7ec099f58d30fd19de1b2b8c0664942d607809955579a0`.

- Visually inspected rendered pages2 (full band on stage) and5 (keyboardist poses) from `build/band-book-review/`. Headers, captions and page numbers are legible, whole source images fit without new visible clipping, and the corrected circular guitar pendant / sole keyboardist cross remain visible. The renderer's nonfatal font-cache warning did not prevent readable text in these two outputs.
- Extracted titles/captions from all16 PDF pages. Order matches the manifest: lineup, stage, plot, keyboard identity/poses, guitar identity/poses, bass identity/corrected poses, drums identity/poses, then five retained Yaro references. Captions distinguish static references from future animation checks, identify corrected bass hardware and retain established Yaro identity. No historical rejected image is listed as a current page.
- Independently decoded the embedded image on every page with pypdf/Pillow and compared dimensions and SHA256 of RGB pixels against that page's source file from `manifest.json`. All16 pages contain exactly one image, all16 have the expected title, and all16 decoded images match their source pixels exactly. Thus the book embeds the retained source artwork without an image-content transformation.

This is not a claim that all16 pages were newly rasterized and visually re-reviewed end to end, or that a matching embedded bitmap by itself proves page-placement geometry. The two requested rendered pages were inspected, all page content/order and embedded pixels were checked, and root separately checks all placement bounds. Static art review and its limits remain in the unchanged [review.md](review.md). No motion, musical fingering or final video synchronization is established by this PDF check.

## Exact checked page order

| Page | Manifest ID | Embedded pixels / title |
| --- | --- | --- |
| 1 | `lineup` | PASS / PASS |
| 2 | `stage_wide` | PASS / PASS |
| 3 | `plot` | PASS / PASS |
| 4 | `keys` | PASS / PASS |
| 5 | `keys_poses` | PASS / PASS |
| 6 | `guitar` | PASS / PASS |
| 7 | `guitar_poses` | PASS / PASS |
| 8 | `bass` | PASS / PASS |
| 9 | `bass_poses` | PASS / PASS |
| 10 | `drums` | PASS / PASS |
| 11 | `drums_poses` | PASS / PASS |
| 12 | `yaro_angles` | PASS / PASS |
| 13 | `yaro_expressions` | PASS / PASS |
| 14 | `yaro_verse` | PASS / PASS |
| 15 | `yaro_chorus` | PASS / PASS |
| 16 | `yaro_plea` | PASS / PASS |
