# Mercy in Minor Studio

Music-video production for Mercy in Minor. **Join Me in Life** is the first production in this repository. Its working baseline is the one-minute Revision 4 hybrid edit. Play the [captioned portrait Short](productions/join-me-in-life/current/exports/Join_Me_in_Life_Short_Hybrid_Camera.mp4) or open the [native portrait scene](productions/join-me-in-life/current/Join_Me_in_Life_experimental_vert.blend). Keep the scene beside its `assets/` directory.

![Twelve timestamped frames from the captioned Revision 4 Short](docs/revision4-contact-sheet.jpg)

## Review from GitHub

Open **Actions → Review the Revision 4 Short → Run workflow**. Choose the branch and run it. When it finishes, open the run summary and download **join-me-in-life-r4-review** under **Artifacts**. The ZIP contains the full-cut contact sheet shown above and an 11.92-second portrait clip of the waiting-room sequence with sound. Each run checks the tracked baseline against its recorded file and audio hashes and decodes all 1,439 frames. [Open the review workflow](https://github.com/cromicron/music-video-studio/actions/workflows/review-short.yml)

To render your branch after changing a shot, choose an edition and a time range or the full cut in [Render a studio edit](https://github.com/cromicron/music-video-studio/actions/workflows/render-edit.yml).

## Start a session

Select **cromicron/music-video-studio** when configuring the GitHub repository for a Codex cloud environment. For local work, clone the repository and open its folder in Codex. [Creative decisions and editing instructions](AGENTS.md) · [Official Codex Cloud guide](https://developers.openai.com/codex/cloud/)

```sh
git clone https://github.com/cromicron/music-video-studio.git
cd music-video-studio
```

For a Codex cloud snapshot that opens on an older commit, follow the [saved-checkout sync instructions](AGENTS.md#sync-a-saved-codex-checkout). GitHub supplies the verified update inside each successful main-branch source check.

Run the source check from the repository root with Python 3.11 or newer.

```sh
python3 tools/review.py --source-only
```

For a time-labelled contact sheet, install FFmpeg with the drawtext filter, ffprobe and a monospace font, then run:

```sh
python3 tools/review.py
```

Open `build/join-me-in-life/revision4-contact-sheet.jpg`. To check every decoded frame of the available baseline videos, run `python3 tools/review.py --full-decode`. On Windows, `py -3` can be used in place of `python3`. For native scene work on Linux x86-64, run `bash tools/setup-blender-linux.sh` to install the production version or locate a matching Blender on PATH. The [native render guide](productions/join-me-in-life/BLENDER.md) has the two-frame test and source rebuild commands.

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

The repository includes the current portrait baseline and the source needed for the three Revision 4 formats. Alternate finished MP4s and earlier visual development are available from the [Revision 4 release](https://github.com/cromicron/music-video-studio/releases/tag/join-me-in-life-r4). Rebuild the frame cache locally when editing a cut. Plain Git stores the initial source assets and editable Blender scenes so the first clone can work offline. Keep frame caches and routine delivery exports out of commit history. For a larger catalogue with frequently revised binary masters, move those masters to Git LFS or a versioned media store before committing successive large versions.

## A useful first Codex task

> Run the project checks and show me the Revision 4 waiting-room passage at its source joins. Give me a short playback clip with the existing audio and identify which source controls the portrait camera from 30.167 to 42.083 seconds. Keep the edit itself intact.

For the full-length film, begin from take 49 (4:37.776). The existing Short occupies approximately 1:40.373–2:40.323 in that recording. The full-length lyric video and the final lyric sheet are linked in the full-song guide. Build the next section on a branch and review a short sequence in motion before scaling up.
