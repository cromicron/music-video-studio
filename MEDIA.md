# Restoring production media

A normal clone includes the four native Blender scenes, their active artwork and audio, the final full song, and the Revision 4 portrait Short with lyrics. The [Revision 4 release](https://github.com/cromicron/music-video-studio/releases/tag/join-me-in-life-r4) holds the alternate renders and the earlier visual-development materials.

| Release asset | What it restores |
| --- | --- |
| [Join_Me_in_Life_Camera_Blender.zip](https://github.com/cromicron/music-video-studio/releases/download/join-me-in-life-r4/Join_Me_in_Life_Camera_Blender.zip) | Six videos under `current/exports/`. The three hybrid exports contain the Revision 4 corrections. The three restrained exports are the Revision 3 comparisons. |
| [Join_Me_in_Life_Waiting_Room_Fix.mp4](https://github.com/cromicron/music-video-studio/releases/download/join-me-in-life-r4/Join_Me_in_Life_Waiting_Room_Fix.mp4) | The original 11.917-second preview of the waiting-room correction, under `current/exports/`. |
| [Music_Video_Consolidated_Package.zip](https://github.com/cromicron/music-video-studio/releases/download/join-me-in-life-r4/Music_Video_Consolidated_Package.zip) | Historical illustrations, the visual index and notes under `archive/visual-development-v1/`, plus the original checksums. It contains the standalone `Join_Me_in_Life_Full_Package.zip` also accepted by the restore script. |

Download the assets you want and keep the filenames shown above. From the repository root, point the restore command at your download folder. If you use the GitHub CLI, the following downloads and restores all three from the private release.

```sh
gh release download join-me-in-life-r4 --repo cromicron/music-video-studio --dir build/release-inputs --pattern 'Join_Me_in_Life_Camera_Blender.zip' --pattern 'Join_Me_in_Life_Waiting_Room_Fix.mp4' --pattern 'Music_Video_Consolidated_Package.zip' --skip-existing
python3 tools/restore_media.py build/release-inputs
```

You can also pass one or more individual file paths to `tools/restore_media.py`. On Windows, use `py -3` in place of `python3` if needed. The script restores into `productions/join-me-in-life/`. It verifies each input and restored file against SHA-256, skips matching local files and preserves differing local files for review.
