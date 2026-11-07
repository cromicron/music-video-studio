# Current state — Join Me in Life

Updated: 2026-11-07 (UTC). Current facts belong here; dated experiments remain in [SESSIONS](SESSIONS.md) and their evidence.

## Task and continuity

Complete the original **277.776-second take 49**, building on the published one-minute Revision 4 Short. Use exactly three creative tools for the free production: **ChatGPT images → owned LTX animation → FFmpeg**. Existing supplied footage keeps its historical provenance. Inspect actual motion, identity, anatomy and continuity. The separate paid recommendation must fit **€20 total for ten films**, including retries and charges. Be Ambitious is installed and retained. No new money or purchased Runway credits have been spent.

The knowledge prerequisite is complete: [PR #3](https://github.com/cromicron/music-video-studio/pull/3) merged at `d839a848afc6c8792e526ffe9791767b22531f43`. A fresh clone of merged main, cold artifact checks and a reader without inherited chat recovered the task and unfinished work. [Project memory](../../PROJECT_MEMORY.md), [history coverage](../../docs/HISTORY_INDEX.md), [Cloud continuity research](../../docs/CLOUD_CONTINUITY.md). This does not establish access to every private chat or automatic first-turn loading in a newly provisioned Cloud task. The observed starting→ready transition delivered the workspace entrypoint; it was not a proven new VM.

Dario reports approximately 600 views in less than a week for the [published Short](PUBLICATION.md). Build on it. The view count is user-reported. Current work is on `feat/join-me-in-life-motion-pilots`; latest root checkpoint `b74923c` is pushed. Preserve ongoing local work and fetch all heads before continuing.

## Run already in progress — check before submitting

**A2V notebook version 5 was submitted at 02:13:47 UTC on 7 November**: `darionalis/join-me-in-life-private-supplied-song-diagnostic`, frozen source bundle v5. It requests one **97-frame, 24-fps, 896×512** bridge performance with the actual song excerpt beginning at 207.75 seconds. [Exact deployment](full-film/research/kaggle-a2v-v5-deployment.json), [source/audio provenance](full-film/assets/audio/bridge-a2v-conditioning.json). Root owns provider operations. Check the existing job; do not duplicate it. The read-only monitor downloads notebook `/5` to `build/jml-kaggle-a2v-results-v5` on completion. Process/provider caps are 90/95 minutes.

The preceding run, notebook v3 / bundle v4, passed actual dual-T4 quantization tests, verified all 35.38 GB of weights and encoded sufficient original-song audio. It then exhausted GPU1 memory during Gemma prompt encoding, before video diffusion. [Failure evidence](full-film/research/kaggle-a2v-v4-failure/render.json). V5 preserves all inputs and 1,024 context positions, keeps video modules on CPU during text encoding, disables unused KV cache and releases Gemma before staging video modules. Twenty offline tests pass; actual generation remains unproven until the running job returns.

Latest displayed free Kaggle quota before v5: **29.09 / 30 hours**. Earlier overlapping jobs prevent assigning individual debits by subtraction. [Usage ledger](full-film/research/usage-ledger.json). No 13B or local CPU generation is currently running.

## Available picture and current edit

- **Preserved baseline:** `current/` contains Revision 4, its portrait export, source footage, art, lyrics and scripts. Read [HANDOFF](current/HANDOFF.txt) before dependent changes. `experimental` means R4; `simple` means the R3 comparison. Original timing, logo, rounded vowel and source assets remain unchanged.
- **Full-song animatic:** [4:38 / 58 shots](full-film/exports/Join_Me_in_Life_Full_Animatic.mp4), 6,667 frames, fully decoded, original-audio correlation 0.999659 at zero detected lag. This is a planning film, not the completed music video. Browser completion is telemetry, not subjective listening or acting approval.
- **Refined art:** [art candidate](full-film/edit-art-candidate.json) replaces seven small panels across 23 shots. Eleven portrait uses have locked wide framing after crop review. [6.5-second opening proof](full-film/exports/Join_Me_in_Life_Opening_Refined_Animatic_Proof.mp4) preserves the original logo and fade, fully decodes and has audio correlation 0.997765 at zero lag. Sources are 1672×941, so a 1080p export does not create native 1080p detail. Dawn finger-ring continuity remains a documented art caveat.
- **Original embrace recovered:** independent [M01 source review](full-film/review/m01-editor-second-review.md) passes the original 121 frames at natural 24 fps and ordinary viewing size. Brief turning-hand softness is not a persistent contact failure. JML-020 supersedes its blanket exclusion through exact source/review hashes; it is not user creative sign-off.
- **S028 placement rendered:** [12.125-second candidate](full-film/exports/Join_Me_in_Life_S028_Original_Reuse_Candidate.mp4) contains 92 lead frames, all 121 source frames once, and 78 exact endpoint frames. The action starts at full-song 134.375 seconds, matching the Short mapping within 2 ms. No loop, reversal or retiming. Full decode and audio alignment pass; independent review of the new holds and sequence remains pending. [Technical evidence](full-film/build/m01-reuse-candidate/technical-checks.json).
- **Production candidate:** [separate configuration](full-film/edit-production-candidate.json) uses that M01 source and retains contact in four later hospital returns, avoiding a reset to separated poses. Original edit/art candidate/animatic remain preserved. Renderer v1.4 records source dimensions, named configuration hash, new generation, historical footage, lead holds and endpoint holds separately. All **31 repository tests** pass, including a real 92+121+78-frame cadence test.
- **Summer:** the original [M02 second review](full-film/review/m02-editor-second-review.md) retains the responsive performance but requires sustained female-face correction from about 0.5 seconds onward. Blue eyes and rounder proportions persist between laughs. Faithful local inpainting needs a different model/offload and sampling path; [bounded contract](full-film/research/ltx-m02-face-repair-contract.md). A separately generated corrected end-keyframe is under static review, and a smaller first/end-guided LTX2.3 wrapper is being prepared. No video repair or whole-take approval is claimed.

## Completed motion tests and stopped routes

| Test | Result and next implication |
| --- | --- |
| Owned 13B bridge, 121 frames / 4.033 s | Rejected: finger fusion, lost rings, final mouth/chin ghosting. Identity and stage were relatively stable. [Review](full-film/review/ltx13b-bridge-pilot-review.md). |
| Owned 13B hospital, 241 frames / 8.033 s | Full action rejected for a head pat, lifted gaze and early hand artifacts. Only **6.000–8.033333 s** passes visually as later already-established-contact aftermath; no extra hold or song join approved. [Review](full-film/review/ltx13b-hospital-pilot-review.md). Prefer the recovered original M01 action. |
| Owned 13B summer, 185 frames / 6.167 s | Responsive exchange, but persistent identity/style drift and lost raised-hand ring. No approved interval. [Review](full-film/review/ltx13b-summer-pilot-review.md). |
| Google Flow | Private first/end upload and saved login work. Initial attempt and one official delayed retry both failed “unusual activity”; 50 credits remained, no output. **Stop this automated route**; do not repeat setup or alter required proxy/security settings. [Evidence](full-film/research/flow-pilots/F01-hospital-embrace.json). |
| Anonymous hosted LTX / local CPU | Hosted take failed direction; next request exceeded its legitimate quota. Four CPU tests failed representative motion despite a corrected scheduler. No active job; do not rerun unchanged experiments. |

Kaggle CLI authentication and actual dual-T4 execution are verified. Hugging Face login/email/model agreement are complete. TinyFish setup sessions were saved and closed. Do not ask Dario to redo those steps. [Access and recovery](full-film/ACCESS_SETUP.md). Purchased Runway credits remain untouched; the earlier 1,800-credit proposal was withdrawn.

## Next production work and remaining limits

1. Retrieve and review the existing A2V v5 output, or fix the specific evidenced runtime failure. Keep original soundtrack provenance and distinguish frame/telemetry review from listening.
2. Finish independent S028 sequence and original M02 reviews. Build the smallest necessary new-action set against the actual full-film timeline, preserving all four screamed “Forget your lines” pleas.
3. Complete and inspect the full edit. Still-camera animation, one approved supplied embrace and an aftermath fragment do not yet constitute the requested finished film. No full-film phoneme/lip-sync acceptance is claimed.
4. Keep the proposed dawn emotionally unresolved: companionship and exhaustion, not a sudden cure. It remains a creative proposal, not a user-approved resolution.

[Paid recommendation](full-film/research/paid-budget.md) distinguishes a hybrid workflow from fully generated coverage. No ordinary per-output API has been verified to deliver ten fully generated 277-second films within €20. No purchase is queued.

Run `python3 tools/studio.py --check` and `python3 tools/review.py --source-only` after relevant changes. Before handoff, commit/push coherent work and run `python3 tools/studio.py --checkpoint`; local checks alone do not establish remote persistence. The prepared bpy 5.2.3 route, not system Blender 4.3.2, opens original native scenes; verify with `--runtime` if needed.
