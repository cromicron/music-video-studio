# Join Me in Life — full-song work

Current deliverable: [the complete 4:38 animatic](exports/Join_Me_in_Life_Full_Animatic.mp4). This is a reviewed planning cut, **not the finished animated music video**. It preserves all of take 49, with 58 shots and zero approved generated-action seconds.

The first hosted LTX-2.5 acting take and four local CPU tests are complete, with zero accepted motion clips. CPU integration was repaired, but actual motion still failed direction/reflection checks. No CPU inference is running. Kaggle phone verification, two-T4 CUDA execution and official CLI OAuth have succeeded; private model generation and Flow shot generation remain untested. Read [current access](ACCESS_SETUP.md) before asking for setup again.

## What to open

- [Brief and applied Be Ambitious skill](BRIEF.md).
- [Researched production methods](research/production-methods.md).
- [Actual free access, tests and quota evidence](research/free-access.md).
- [Paid options and the €20 / ten-film arithmetic](research/paid-budget.md).
- [Editable shot list](edit.json) and [render/reproduction guide](EDIT_NOTES.md).
- [Independent frame review](review/independent-cut-review.md) and [browser playback evidence](review/browser-playback.json).

The exact reviewed MP4 has SHA-256 `d3f66f4feebc401438218345d61889650418a65a5d3f6afb014720c8369550cb`. All 6,667 frames decode. Audio comparison gives zero detected lag and waveform correlation 0.999659. A Chromium player completed the entire file at 1×, unmuted, without a media error or stall; it dropped 90 displayed frames under concurrent workload. This does not constitute listening by a human or approval of acting. Independent inspection closed the three reported framing/continuity defects.

## Production boundary

The first hosted free candidate is **ChatGPT image generation → Google Flow → FFmpeg**, chosen for reference/start/end-frame control and renewable free generation. An owned LTX route is being tested separately for quality and repeatable cost. The final version will use one animation provider, not combine both while claiming a three-tool count. Python only orchestrates production tools and checks outputs. The current animatic uses ChatGPT images and FFmpeg; rejected or unused tests do not satisfy the three-tool finished-video requirement. Existing R4 sources remain intact.

No new money or purchased credits have been spent. Four included image-generation calls and one successful public free video generation were used, alongside local CPU tests. The Runway proposal was withdrawn after Dario corrected its availability-based rationale: connected tools are accidental. Its prepaid inventory does not determine the method and is not a renewable free allowance. Choose on quality and cost, then obtain access.

## Continue

1. Read the active production's STATUS and latest SESSIONS entry before working; preserve this branch's local files.
2. Finish the continuity verification recorded in production STATUS, then test the prepared private Kaggle model bundle and supported Flow image transfer. The CPU experiments are already complete; do not restart them without a changed hypothesis. Record actual temporal failures as rejected.
3. Use the prepared motion proposals only within the confirmed account and spending scope. No account cycling, automatic purchases or quota bypass.
4. Supply only independently reviewed selections to `review/approved-motion.json`, following EDIT_NOTES. Re-render, inspect all affected joins and motion, then play the complete final cut with the original song.
5. Record actual generated seconds, holds, resolution, retries and cost. Keep the unfinished label until the intended film quality has been achieved.

## Local setup and recovery

Current browser access uses the three authenticated TinyFish profiles documented in [ACCESS_SETUP](ACCESS_SETUP.md). Their live calls are verified. Older Playwright signup/CAPTCHA notes describe an earlier attempt, not current account blockers. Local browser processes and Kaggle CLI credentials may need recovery in a new environment; test actual access first and follow the supported recovery instructions. Never commit browser state, tokens or password files.

The CPU model environment is `.venv-ltx-cpu` at repository root; its multi-gigabyte model cache is under ignored `build/ltx-cpu`. ASR tooling is in `.venv-jml-asr`, with its cache under ignored `build/asr-model-cache`. Full-film shot caches are ignored under `work/`. These are runtime setup, not portable source artifacts. Consult the benchmark scripts and saved provenance before restarting a job.
