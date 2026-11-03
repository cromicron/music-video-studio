# Automation and review

| Workflow | Trigger and purpose | Result |
| --- | --- | --- |
| [Production source check](workflows/source-check.yml) | Push (excluding generated `codex-sync`), PR, or manual. Checks repository structure/maintained links and the original Join Me in Life source. Runs the studio checker tests. On main, bundles verified updates since the R4 baseline. | `studio-main-update` bundle (30 days); on the private repository, connector-readable manifest/parts on generated `codex-sync`. |
| [Review the Revision 4 Short](workflows/review-short.yml) | Manual. Verifies the **original** baseline, decodes available hybrid exports and makes a contact sheet and a phone-size waiting-room playback sample. | `join-me-in-life-r4-review` artifact (7 days). |
| [Native Blender review](workflows/native-review.yml) | Manual. Renders original portrait frames 339 and 841, checks their dimensions, and runs baseline full-decode review. | `join-me-in-life-native-review` artifact (7 days). |
| [Render a studio edit](workflows/render-edit.yml) | Manual on the selected source branch. Edition: portrait-captioned, portrait-clean or widescreen. Mode: preview (up to 288 frames) or full (1–1439). Source: rebuild from scripts (default) or saved scene. | Finished MP4(s) in `studio-edit-<run-id>-<attempt>` (7 days). This is the candidate-production path. |

At 24 fps, the inclusive range for a time interval `[start, end)` is `round(start * 24) + 1` through `round(end * 24)`. For the 34–39 s embrace preview, choose start **817**, frames **120**, `portrait-captioned`, `preview`. This preserves the full-cut caption clock and selects matching audio; preview AAC is re-encoded. Full Short exports copy the source AAC.

Use a branch containing the intended source changes. Rendering from `main` does not include an unpushed local edit. Choose `saved-scene` for direct `.blend` work so a default rebuild does not replace it. Downloaded Actions artifacts expire: retain an enduring review/delivery reference when future sessions need it and link it in the session log. Successful CI is technical evidence, not Dario's approval or a claim of playback review.

`codex-sync` is a generated transport branch, not a place for human edits or a separate production. [AGENTS.md](../AGENTS.md#sync-a-saved-codex-checkout) documents pinning its manifest/parts and verifying the reconstructed bundle before a clean fast-forward.
