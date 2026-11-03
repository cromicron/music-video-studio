# Mercy in Minor Studio

Music-video production for Mercy in Minor. **Join Me in Life** is the first production in this repository. Its working baseline is the one-minute Revision 4 hybrid edit. Play the [captioned portrait Short](productions/join-me-in-life/current/exports/Join_Me_in_Life_Short_Hybrid_Camera.mp4) or open the [native portrait scene](productions/join-me-in-life/current/Join_Me_in_Life_experimental_vert.blend). Keep the scene beside its `assets/` directory.

## Start a session

Open this folder as a local project in Codex. Once the repository is on GitHub, you can also select it in a Codex cloud environment. The root [AGENTS.md](AGENTS.md) carries forward the creative decisions and the review workflow.

From the repository root, with Python 3.11 or newer:

```sh
python3 tools/review.py --source-only
```

For a time-labelled contact sheet, install FFmpeg with the drawtext filter, ffprobe and a monospace font, then run:

```sh
python3 tools/review.py
```

Open `build/join-me-in-life/revision4-contact-sheet.jpg`. To check every decoded frame of the available baseline videos, run `python3 tools/review.py --full-decode`. On Windows, `py -3` can be used in place of `python3`.

## Put the initial checkout on GitHub

The starter ZIP contains a Git working tree, a `main` branch and a `join-me-in-life-r4` tag on the original production import. Extract the folder before opening it. With GitHub CLI signed in to the intended account, run inside that folder:

```sh
git status
gh repo create mercy-in-minor-studio --private --source=. --remote=origin --push
git push origin join-me-in-life-r4
```

If you use GitHub Desktop, add the extracted folder as a local repository, choose **Publish repository**, and keep it private. Push the baseline tag as well if the remote does not show it. The project includes unpublished production art and music.

In Codex Cloud, choose the repository in the environment setup, run the source check, and publish the environment after reviewing the setup result. Configure Python 3.11+ and FFmpeg for shot review. Native scene work also needs a compatible Blender build. Existing assets render offline. [Official Codex Cloud guide](https://developers.openai.com/codex/cloud/)

## Where to work

| Task | Source |
| --- | --- |
| Read the last edit decisions | [Revision 4 handoff](productions/join-me-in-life/current/HANDOFF.txt) |
| Change a shot or camera path | [Hybrid schedule](productions/join-me-in-life/current/camera_shots_experimental.json) |
| Edit a mouth exposure, title or lyric | [Native animation](productions/join-me-in-life/current/native_animation.py) · [Finishing and captions](productions/join-me-in-life/current/finish.py) |
| Render with Blender | [Scene and render guide](productions/join-me-in-life/BLENDER.md) |
| Find approved character references or browse the 22-image selection | [Local visual index](productions/join-me-in-life/art/Visual_Index.html) · [Art handoff](productions/join-me-in-life/notes/Music_Video_Anime_Content_v2_Handoff.md) |
| Work on the full-length film | [Final recording, lyrics and Short-to-song timing](productions/join-me-in-life/full-song/README.md) |
| Find the other export versions or older artwork | [Media recovery](MEDIA.md) · [Attachment inventory](productions/join-me-in-life/notes/MIGRATION.md) |
| Use the band identity on a different song | [Band banners](band/) |

The repository includes the current portrait baseline and the source needed for the three Revision 4 formats. Alternate finished MP4s, earlier visual development and render caches have separate recovery paths. Plain Git stores the initial source assets and editable Blender scenes so the first clone can work offline. Keep frame caches and routine delivery exports out of commit history. For a larger catalogue with frequently revised binary masters, move those masters to Git LFS or a versioned media store before committing successive large versions.

## A useful first Codex task

> Run the project checks and show me the Revision 4 waiting-room passage at its source joins. Give me a short playback clip with the existing audio and identify which source controls the portrait camera from 30.167 to 42.083 seconds. Keep the edit itself intact.

For the full-length film, begin from take 49 (4:37.776). The existing Short occupies approximately 1:40.373–2:40.323 in that recording. The full-length lyric video and the final lyric sheet are linked in the full-song guide. Build the next section on a branch and review a short sequence in motion before scaling up.
