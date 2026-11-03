# What came across from the ChatGPT project

The six project attachments supplied on 3 November 2026 contained 60 distinct files after unpacking the nested archives. The table below uses paths relative to `productions/join-me-in-life/`. The recovered Rev 4 edit is in [current/](../current/) and takes priority for work on the existing Short. Use this inventory to trace its supporting materials.

| Location | Contents and use |
| --- | --- |
| `audio/Join-Me-in-Life-Short.mp4` | Original 59.950-second AAC-LC stereo music excerpt, 48 kHz. The MP4 contains a single audio stream. |
| `art/` | Supporting v2 art selection. Open `Visual_Index.html` locally to browse all 22 illustrations, or use `Visual_Index.pdf` on a phone. `FILE_MANIFEST.json` gives the identity, path, status, dimensions and checksum of each original. |
| `reference/blender-pilot/` | Eight-second silent Blender study, including the packed editable scene, original build script, five external PNGs, original README and rendered 1280 × 720 H.264 MP4 at 24 fps. The original handoff reports Blender 5.2.3 LTS. The build script writes a scene and preview beside itself. Work on a copy when rebuilding. |
| `notes/` | Latest v2 visual handoff, earlier master handoff, source lyrics, prompts and curation notes. The unedited handoffs retain their original archive names and historical links. |
| `archive/visual-development-v1/` | Twelve earlier illustrations, including the two identity portraits, plus the historical visual index, prompts, manifest and handoff. The old and current sets reuse some shot IDs. Use the complete path to distinguish them. |
| `archive/Consolidated_Package_CHECKSUMS.sha256` | Original list of checksums for files inside the consolidated package. It uses the old archive filenames. |

## Finding the original

`source-map.csv` records the six original filenames, every nested entry, its exact byte length and SHA-256, and the corresponding file in this production. The separator `!/` marks an entry inside an archive. An empty production path identifies a ZIP container whose entries follow in the map. Duplicate source entries resolve to one working copy. For example, all three copies of the short have the same SHA-256, and both editions of the lyrics map to `notes/Full_Lyrics_and_Performance.txt`. The current index PDF matches the standalone project attachment byte for byte. All 34 current and historical illustration files matched their original manifest checksums during import.

## Reading the v2 art selection

A01 and A02 define the approved identities and drawn style. A03 supplies her withdrawn crisis expression. The other 19 images are candidates. S02 is the waiting closeup with her gaze lowered. S04 is the revised summer memory with a short-sleeved shirt and charcoal jeans. S05 was deliberately dropped from v2. Use the original manifest to look up each exact filename.

## Limits of these six attachments

The production audio and eight-second technical study are different works. These six attachments contain no rendered narrative Short, editable scene for that edit, phrase or mouth timings, isolated stems, full-length master recording, or standalone band wordmark. The v2 handoff also mentions a separate `Latest_Character_Corrections` folder outside this selection. The separately recovered Rev 4 edit has its own production files and timing. Start there for changes to the actual Short.
