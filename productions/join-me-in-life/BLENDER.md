# Editing the Rev 4 Short

The current portrait edit is `current/Join_Me_in_Life_experimental_vert.blend`. The archive calls it “experimental” in native files and “Hybrid” in exports. Its widescreen sibling has the suffix `experimental_wide`. The `simple` scenes are the earlier comparison cut.

Use **Blender 5.2.3** for the archived production, plus Python 3.10+ with FFmpeg and ffprobe on your PATH for finishing. Blender supplies its own Python and `bpy`. Finishing uses libx264, libass and the DejaVu Sans and DejaVu Serif fonts. Keep the project’s `assets/` directory beside the scenes. It contains the two external movie textures and original logo.

## Linux and Codex Cloud

The setup command below fetches the official Linux x86-64 release of Blender 5.2.3, verifies its published SHA-256 checksum and caches it in `build/tools/`. A matching Blender already on PATH is reused. The first download needs HTTPS access to `download.blender.org`. Rendering uses local files after setup.

```sh
blender_bin=$(bash tools/setup-blender-linux.sh)
"$blender_bin" --version
```

Use the path in `$blender_bin` for Blender commands. To run a render check on GitHub, open **Actions → Native Blender review → Run workflow**. The run renders two frames from the tracked scene, checks their dimensions, fully decodes the baseline video and saves the JPEGs and the contact sheet as a review artifact.

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

## Rebuild with Blender 4.3.2

If only Blender 4.3.2 is installed, create the separate worktree described above. Rebuild the scene there from the camera schedule and artwork before opening it. Blender 4.3.2 cannot read the supplied 5.2 scene header. This build uses the earlier Blender animation-curve and sound-strip APIs and writes a new native scene into the worktree.

```sh
blender -b --factory-startup --python-exit-code 1 --python build_film.py -- --cut experimental --format vert
blender -b --factory-startup --python-exit-code 1 --python render_existing.py -- --cut experimental --format vert --ranges 339:339,841:841
```

The 4.3.2 portrait rebuild passed all 1,439 per-frame coverage checks and rendered both 1080 × 1920 JPEGs on CPU. A central crop from each render matched the corresponding finished Revision 4 reference frame with RGB correlation above 0.998. The comparison excludes the caption area. The archived production handoff records a build with bpy 5.2.3, Python 3.13 and FFmpeg. The original 5.2.3 scene binaries remain the production baseline.
