# Join Me in Life

Mercy in Minor's first production, owned by Dario. The song answers HIM's “Join Me in Death” with a plea to stay alive. The long-term project is a full music video; the existing editable production is a roughly one-minute **Revision 4 hybrid Short**.

Start with [STATUS.md](STATUS.md) for the current work and next step, [DECISIONS.md](DECISIONS.md) for constraints, and [SESSIONS.md](SESSIONS.md) for the latest handoff. The [Revision 4 handoff](current/HANDOFF.txt) records the actual current cut. No new creative edit is implied by opening this project.

## The current cut

- [Captioned portrait baseline](current/exports/Join_Me_in_Life_Short_Hybrid_Camera.mp4): 1080 × 1920, 24 fps, 1,439 frames. Picture is 59.958 seconds; supplied audio is 59.950 seconds.
- [Portrait scene](current/Join_Me_in_Life_experimental_vert.blend) and [camera schedule](current/camera_shots_experimental.json). “Experimental” is the archived source filename for the current hybrid, not an instruction to start another experiment. “Simple” is the earlier restrained Revision 3 comparison.
- Three hybrid editions exist: portrait with lyrics, portrait clean, and widescreen. Only the captioned portrait export is tracked in Git; optional alternates are recoverable from the release. Four native scenes (two cuts × two formats) are tracked.
- He is frightened for her and remains beside her. She stays withdrawn during the single embrace. The hospital passage ends unresolved; summer is an earlier memory of warmth. This Short does not depict recovery or a decision to stay alive.

## Where to work

| Work | Start here |
| --- | --- |
| Camera, shot boundaries, or source artwork | [Current source map](current/SOURCES.md), then `camera_shots_experimental.json` and `build_film.py`. |
| Drawn mouth exposures or small torso controls | `current/native_animation.py`. |
| Caption text/timing, titles, logo, encoding | `current/finish.py`; the SRT, ASS and lyric JSON files are generated derivatives. |
| Render a saved scene or source rebuild | [BLENDER.md](BLENDER.md). Check `.venv-bpy` before using system Blender. |
| Browse character references and art proposals | [Art guide](art/README.md) and [visual index](art/Visual_Index.html). |
| Develop the full song | [Full recording, lyrics, and alignment](full-song/README.md). No full-song narrative cut is implemented here. |
| Trace imported packages or old plans | [Historical notes guide](notes/README.md) and [migration inventory](notes/MIGRATION.md). |
| Inspect the eight-second technical study | [Reference guide](reference/README.md). It is a silent 720p pilot, separate from this edit. |
| Restore optional exports or historical art | [Media recovery](../../MEDIA.md). |

Run checks from the repository root:

```sh
python3 tools/studio.py --check
python3 tools/review.py --source-only
```

Use [Render a studio edit](https://github.com/cromicron/music-video-studio/actions/workflows/render-edit.yml) on the branch containing the intended change for preview or full exports. A default workflow run rebuilds from scripts; choose `saved-scene` if the intended work is a direct scene edit. Preserve the original baseline for comparison.
