# Editing the Rev 4 Short

The current portrait edit is `current/Join_Me_in_Life_experimental_vert.blend`. The archive calls it “experimental” in native files and “Hybrid” in exports. Its widescreen sibling has the suffix `experimental_wide`. The `simple` scenes are the earlier comparison cut.

Use **Blender 5.2.3** for the archived production, plus Python 3.10+ with FFmpeg and ffprobe on your PATH for finishing. Blender supplies its own Python and `bpy`. Finishing uses libx264, libass and the DejaVu Sans and DejaVu Serif fonts. Keep the project’s `assets/` directory beside the scenes. It contains the two external movie textures and original logo.

## Render two frames from the saved scene

From the repository root, in a fresh clone with its media present, run the following. The script opens the saved scene read-only and writes into its frame cache.

```sh
cd productions/join-me-in-life/current
blender --version
blender -b --factory-startup --python-exit-code 1 --python render_existing.py -- --cut experimental --format vert --ranges 339:339,841:841
```

Open `frames/experimental/vert/frame_0339.jpg` and `frame_0841.jpg`. The first is the last singer frame with the rounded sustained vowel. The second lands 35 seconds into the timeline, during the embrace movie. Check that both are 1080 × 1920, with visible artwork and the expected action. The clean Blender frames precede the FFmpeg logo and caption overlay. The renderer skips existing JPEGs. Use a fresh worktree or clear the named stale frames before repeating an edit check.

## Change a shot and produce the captioned Short

Create a working branch from the repository root if you want to keep the baseline checkout open alongside the revision.

```sh
git worktree add -b edit/waiting-room ../mim-waiting-room
cd ../mim-waiting-room/productions/join-me-in-life/current
```

Edit `camera_shots_experimental.json` for camera travel and shot boundaries, `native_animation.py` for the drawn mouth exposures or `finish.py` for caption timing and branding. Direct Blender edits belong in a working copy of the appropriate `.blend`. Use the command that corresponds to the source you changed.

| Change | Action |
| --- | --- |
| Edits in a saved Blender scene | Render that scene using `render_existing.py`. A scene rebuild would replace the direct edits. |
| Camera schedule or native animation code | Run the builder first. It recreates the named scene, its shot list and its validation report. |
| Captions or logo only | Reuse the complete clean JPEG sequence for the same cut and format and run the encoder. A fresh clone needs to render that frame sequence once. |

In the shell below, run the first command only after changing source that drives the scene. The remaining commands render the clean sequence and encode the captioned portrait cut.

```sh
blender -b --factory-startup --python-exit-code 1 --python build_film.py -- --cut experimental --format vert
blender -b --factory-startup --python-exit-code 1 --python render_existing.py -- --cut experimental --format vert --ranges 1:1439
python3 finish.py --cut experimental --format vert --lyrics
```

Open `../Revision_4/Join_Me_in_Life_Short_Hybrid_Camera.mp4`. Check the held vowel and camera joins at playback speed with sound. The encoder copies the source AAC and requires 1,439 picture frames. The portrait clean edition uses the same frame sequence with `--lyrics` omitted. For the widescreen edition, use `--format wide` throughout. The checked-in exports in `current/exports/` are reference copies. Both the original packaging script and six-output delivery validator expect all six finished files together under `../Revision_4/`.

## Migration verification

Blender 4.3.2 in the migration environment rejected the 5.2 scene header before rendering. The native two-frame smoke test therefore remains to run under Blender 5.2.3. The archived production handoff records a successful build with bpy 5.2.3, Python 3.13 and FFmpeg. During migration the builder's argument handling was corrected so Blender options before `--` are excluded. Rebuilds also save repository-relative artwork, audio and output paths. The corrected CLI help, FFmpeg subtitle filter and font lookup were exercised locally. The four supplied scene binaries were retained as received.
