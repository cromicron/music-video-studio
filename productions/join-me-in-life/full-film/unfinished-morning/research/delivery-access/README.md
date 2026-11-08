# Private Drive delivery verification — 7 November 2026

The accepted 48-second climax preview can be downloaded through the existing private Drive file. Both the viewer’s **Herunterladen** button and the stable [direct download](https://drive.google.com/uc?export=download&id=1ZutXZIwMvvy1Tugh8dCvrucoDlOrIdwN) produced an actual Chromium `Browser.downloadProgress` event with `state: completed` and `receivedBytes = totalBytes = 32127341`.

The original [viewer](https://drive.google.com/file/d/1ZutXZIwMvvy1Tugh8dCvrucoDlOrIdwN/view) remains private. Existing Google sign-in was reused. No sharing permissions, profile settings, account credentials or source media were changed. The remote browser suggested filename `download`, but a bounded follow-up established that Drive supplies the proper `.mp4` filename in `Content-Disposition`. See the header check below; no Drive file rename was made.

## What the player failure establishes

TinyFish’s reviewer browser reports Chromium **147.0.7727.6**. Its `HTMLMediaElement.canPlayType()` returns an empty string for H.264 High (`avc1.640028`), H.264 Baseline (`avc1.42E01E`) and AAC (`mp4a.40.2`), but `probably` for VP9 and Opus. This browser lacks the codecs in the accepted H.264/AAC export. That makes it unsuitable for verifying this MP4’s playback and is a concrete browser limitation; it does not establish a failure in Dario’s browser or a global Drive outage.

This CDP pass observed the embedded video at currentTime 0, readyState 0 and networkState 0, with no populated media error. Its attempted click did not obtain an HTML media error code. Earlier independent visual runs recorded Drive’s unexpected-error message. We do not claim that codec support alone proves every cause of Drive’s generic error, nor that changing cookie settings was necessary. No settings were changed and no re-encode was made.

## Evidence and limits

- [Viewer download and codec observations](browser-v1.json).
- [Direct URL download completion](direct-download-v1.json).
- [Exact temporary session cleanup](session-cleanup-v1.json): documented cancel returned HTTP 200 and `cancelled: true`. Unsaved review state was discarded and the saved sign-in profile remained untouched.
- [Prior connector upload and byte verification](../bridge-48s-delivery-v1.json) independently matched the source SHA-256 `3f07a9182d945a12483e2e375c00556829183893ed1d13c8a3d3e2930c3d4052`.

The CDP download evidence proves browser completion and exact expected byte count; it does **not** independently hash the remote browser’s downloaded file. The connector comparison supplies the separate hash evidence. Root’s local Chromium playback review is also separate from this remote browser diagnosis.

## Recovery method

Use the existing supported TinyFish profile setup API and the proxy-preserving [CDP bridge](../../../tools/tinyfish_cdp_bridge.py), as documented in [access setup](../../../ACCESS_SETUP.md). Keep API key, temporary CDP endpoint and setup-session response in mode-0600 files outside Git. Never export Google cookies to a second machine. For a future delivery, connect Playwright through the loopback bridge, record `canPlayType()` and browser version, enable `Browser.setDownloadBehavior` with `eventsEnabled: true`, then listen to `Browser.downloadWillBegin` and `Browser.downloadProgress` before clicking the download button or navigating to the stable Drive download URL. A click alone is not completion. Require `completed` and both byte counts matching the exported file size.

Store only the stable file ID/URL, suggested filename, downloaded byte counts and status. Strip query strings from redirects and network diagnostics; never retain bearer/signed URLs, cookies, account-frame contents or keys. When done, POST the exact session ID to `/v1/profiles/{profileId}/setup-session/cancel` and retain its sanitized HTTP status and `cancelled` result. Closing a CDP connection or local bridge alone is not provider cleanup. Preserve the existing profile rather than saving incidental diagnostic state.

## Follow-up: response headers and filename

A single fresh, read-only setup session tested the stable `/uc` URL and its observed stable [usercontent endpoint](https://drive.usercontent.google.com/download?id=1ZutXZIwMvvy1Tugh8dCvrucoDlOrIdwN&export=download). Both returned HTTP 200 with `Content-Type: video/mp4`, `Content-Length: 32127341`, and `Content-Disposition: attachment; filename="Join Me in Life — Unfinished Morning — Climax Preview (48 seconds).mp4"`. Both downloads again completed with all 32,127,341 bytes, while this remote Chromium continued to report suggested filename `download`.

Thus the response supplies a named MP4; the generic name appears downstream in this reviewer browser. The CDP raw extra-info representation renders the UTF-8 em dashes as mojibake, while the normal response event decodes them correctly. This does not by itself establish whether the reviewer ignores the disposition generally or handles this Unicode header differently. No comparison with an ASCII filename and no account file rename was performed. We do not claim that Dario's actual browser was tested or that a manual rename is necessary there.

[Sanitized headers and two completed downloads](download-headers-v1.json) contain only response MIME/filename/length, stable URLs and byte events. [Exact second session cleanup](header-session-cleanup-v1.json) confirms HTTP 200 / `cancelled: true`; no profile changes were saved. No cookies, request authentication headers or signed redirect URLs were exported.


## Summer viewing proof — 8 November 2026

The first live execution of the retained [download checker](../../tools/delivery/check_drive_download.cjs) passed against the private 44-second summer proof. The tested [stable download](https://drive.google.com/uc?export=download&id=1tbuHWxLdAObAP_5MGQQjQfywtaOOTxRv) completed all **14,432,807 bytes**. Its separately verified response headers are HTTP 200, `video/mp4`, Content-Length `14432807`, and `attachment; filename="Join Me in Life - Unfinished Morning - Summer Preview (44 seconds).mp4"`. The browser also suggested that full `.mp4` filename, with no manual rename needed in this observed run.

[Wrapper output](summer-download-wrapper-v1.json), [exact script provenance](summer-wrapper-provenance-v1.json) and [session cleanup](summer-session-cleanup-v1.json) record one successful attempt, exit 0, no wrapper changes/retry, and HTTP 200 / `cancelled: true` from exact provider-session cleanup. The bridge was then stopped. No sign-in/account/profile changes or sharing changes were made. This does not hash the remote browser download or establish playback; H.264/AAC remain unsupported in the reviewer browser and root's connector hash review is separate.


## Complete film — 8 November 2026

The final [private full-film download](https://drive.google.com/uc?export=download&id=10QCgXl_APKkg3BCfJNCP00IYUtflv2o7) passed the retained checker on its first attempt: **89,163,714 received / 89,163,714 total bytes**, browser state `completed`, exit 0. Header verification independently passed HTTP 200, `video/mp4`, exact Content-Length and `.mp4` Content-Disposition. The browser suggested the correct filename `Join Me in Life - Unfinished Morning (Full Music Video).mp4`.

[Exact download/header evidence](full-film-download-wrapper-v1.json), [script SHA and run provenance](full-film-wrapper-provenance-v1.json), and [successful provider cleanup](full-film-session-cleanup-v1.json) are retained. The exact temporary session was cancelled through the documented API (HTTP 200, `cancelled: true`), followed by stopping the bridge. No sign-in, profile, sharing or account changes were made. This validates browser transfer and headers; root owns the separate authenticated content-hash comparison and actual playback review. The codec-limited remote browser was not used to claim MP4 playback.
