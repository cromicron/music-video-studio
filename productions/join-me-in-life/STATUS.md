# Current state — Join Me in Life

Updated: 2026-11-04 (Europe/Berlin). This is the maintained continuation record; older handoffs remain evidence of their own stage.

## Existing work

The working reference is the **Revision 4 hybrid Short** in `current/`. Its source names use `experimental`; the exports use `Hybrid`. The tracked portrait export has lyrics. The restrained `simple` scenes are Revision 3 comparison material. See [the production guide](README.md) and [current source map](current/SOURCES.md).

The four native scenes, active artwork, two source movie clips, supplied Short audio, captions and scripts are present. The full take 49 and final lyric sheet are in `full-song/`. Optional alternate exports and v1 art are recoverable through [MEDIA.md](../../MEDIA.md).

Revision 4 is the recovered working baseline, **not a newly recorded final creative sign-off**. Prior review records describe frame, geometry, audio-hash and decode checks; they do not establish normal-speed audiovisual review or acceptance of the whole cut.

## Present task

Short recreation preparation is documented in [PRODUCTION_PLAN.md](PRODUCTION_PLAN.md). Scope is the existing one-minute excerpt first, not a full-length film. The baseline film, sources and historical evidence remain unchanged. No footage, generation credits, uploads, purchases or subscriptions were used.

## Next action

Select `prep/join-me-in-life-recreation` (until merged) and read the plan. Provisional route: reference-directed Runway shots, Hedra supplied-audio singing, local finishing; fallback is performance-driven/animator hybrid. Runway auth and 1,995 purchased workspace credits were verified read-only on 2026-11-04; supplied-audio singing is absent from its exposed video tool. Connect/authorize Hedra in the actual Codex client and verify model schema, billing and output rights. Obtain explicit test spending and private-media transfer authorization; proposed cap is 600 Runway credits plus $5 Hedra, combined $15 reference equivalent. Run the three planned tests only then. Full production waits for normal-speed review with original sound and Dario's acceptance.

## Verified setup and checks

- Preparation base: `bda13a971da3e7ab9265ab66af71ba054d86fa90`, matching live GitHub main after ordinary fetch. Compare live main at each new session; this is a dated observation, not a fixed sync target.
- Prior session runtime observation (not rechecked or repaired in preparation): `.venv-bpy/bin/python`, Python 3.13.5 and bpy 5.2.3 LTS. It opens the original 1080 × 1920 portrait scene. System `/usr/bin/blender` is 4.3.2 and must not be used to open the original 5.2 scene. Verify anew in each environment using `python3 tools/studio.py --runtime`.
- `python3 tools/review.py --source-only` passes: 19 hybrid segments, 16 restrained segments, 1,439 contiguous frames each, 14 ordered lyric cues.
- Production rendering is available in `.github/workflows/render-edit.yml` (“Render a studio edit”). It supports preview/full mode, three editions, and source rebuild or saved scene. Jobs must run on a branch containing their intended source changes.

## Open review and limits

- Normal-speed viewing with sound and Dario's creative feedback remain separate from automated validation. No new playback or creative approval is claimed by the organization task.
- The existing reach has brief source hand blur; singing uses limited drawn mouth poses, not complete phoneme lip sync.
- Full-song narrative sequencing and bridge visuals remain undeveloped here. [Full-song timing and source](full-song/README.md) and [DECISIONS.md](DECISIONS.md) preserve the known context.
- A new charge for generation needs the specific shot, reason and expected cost before spending; small edits can reuse local rendering; recreation method selection follows the production plan.
