# Current state — Join Me in Life

Updated: 2026-11-03 (Europe/Berlin). This is the maintained continuation record; older handoffs remain evidence of their own stage.

## Existing work

The working reference is the **Revision 4 hybrid Short** in `current/`. Its source names use `experimental`; the exports use `Hybrid`. The tracked portrait export has lyrics. The restrained `simple` scenes are Revision 3 comparison material. See [the production guide](README.md) and [current source map](current/SOURCES.md).

The four native scenes, active artwork, two source movie clips, supplied Short audio, captions and scripts are present. The full take 49 and final lyric sheet are in `full-song/`. Optional alternate exports and v1 art are recoverable through [MEDIA.md](../../MEDIA.md).

Revision 4 is the recovered working baseline, **not a newly recorded final creative sign-off**. Prior review records describe frame, geometry, audio-hash and decode checks; they do not establish normal-speed audiovisual review or acceptance of the whole cut.

## Present task

Dario requested a technology approach for producing usable music-video clips across songs, ordered from free/cheap through highest quality and making use of the confirmed ChatGPT Pro subscription. The [technology guide](../../docs/VIDEO_GENERATION.md) records current routes, published price examples, Pro image-generation use, local hardware needs and a bounded comparison proposal. It is a proposal, not a new creative decision or generation authorization. The existing Short remains the reference production.

## Next action

Choose two approved reference shots for a small local-versus-hosted motion comparison. The guide proposes a subtle face/cloth shot and a two-person contact shot; quote the actual selected shots and workspace cost before committing credits. Its $6.80 arithmetic uses published Runway Dev prices and is not a confirmed workspace charge. No new generation, image creation, render, subscription purchase or creative edit was submitted. A singing/lip-sync test remains a separate requirement.

For a direct edit to the existing Short, identify the requested shot/time range, inspect it, and render a short candidate on a focused branch using the existing source and sound.

## Verified setup and checks

- Studio source base at this task's start: `4d35644` on GitHub main. Compare live main at each new session; this is a dated observation, not a fixed sync target.
- Prepared local environment: `.venv-bpy/bin/python`, Python 3.13.5 and bpy 5.2.3 LTS. It opens the original 1080 × 1920 portrait scene. System `/usr/bin/blender` is 4.3.2 and must not be used to open the original 5.2 scene. Verify anew in each environment using `python3 tools/studio.py --runtime`.
- `python3 tools/review.py --source-only` passes: 19 hybrid segments, 16 restrained segments, 1,439 contiguous frames each, 14 ordered lyric cues.
- Production rendering is available in `.github/workflows/render-edit.yml` (“Render a studio edit”). It supports preview/full mode, three editions, and source rebuild or saved scene. Jobs must run on a branch containing their intended source changes.

## Open review and limits

- Normal-speed viewing with sound and Dario's creative feedback remain separate from automated validation. No new playback or creative approval is claimed by the organization task.
- The existing reach has brief source hand blur; singing uses limited drawn mouth poses, not complete phoneme lip sync.
- Full-song narrative sequencing and bridge visuals remain undeveloped here. [Full-song timing and source](full-song/README.md) and [DECISIONS.md](DECISIONS.md) preserve the known context.
- A new charge for generation needs the specific shot, reason and expected cost before spending; use supplied assets and local rendering by default.
