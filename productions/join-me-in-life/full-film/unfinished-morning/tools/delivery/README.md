# Repeatable private Drive download check

[check_drive_download.cjs](check_drive_download.cjs) checks an already uploaded, private Drive file through an authorized reviewer browser. It records browser version, codec capability, sanitized response filename/MIME/length headers, and actual download completion. Exit code 0 requires `completed` with both received and total bytes matching the expected export size and no contradictory observed download headers. `download_verification` records the transfer result separately from `header_verification`, which checks HTTP 200, `video/mp4`, expected Content-Length and an `.mp4` Content-Disposition filename. Missing header evidence is explicitly `unverified`; a byte-count pass never implies header verification. Observed header contradictions, byte mismatch, timeout, cancellation or error return 1; invalid arguments return 2.

This is a transfer check, not a content hash, actual playback or creative review. Keep independent source/download SHA-256 verification and normal-speed playback evidence. A reviewer browser's codec limitation does not describe Dario's browser.

## Reproduce from the repository root

Use an isolated, temporary, already signed-in TinyFish profile setup session obtained through the documented API in [access setup](../../../ACCESS_SETUP.md). Keep its session response in a mode-0600 file outside Git. Do not export cookies or repeat a working Google sign-in. Start the existing [proxy-preserving bridge](../../../tools/tinyfish_cdp_bridge.py), pointing `--session` at that private response file, on loopback port 8878. The script does not create, save or cancel sign-in sessions.

```sh
node productions/join-me-in-life/full-film/unfinished-morning/tools/delivery/check_drive_download.cjs \
  --cdp ws://127.0.0.1:8878 \
  --file-id 1ZutXZIwMvvy1Tugh8dCvrucoDlOrIdwN \
  --expected-bytes 32127341 \
  --output build/delivery-check.json
```

Replace the stable file ID and byte count for a new export. Choose a new output filename for each check: an existing path is rejected before connecting, and exclusive creation prevents overwriting evidence if a file appears during the run. The default completion deadline is 30 seconds; `--timeout-ms` permits up to 60 seconds. Playwright is resolved from the local installation or the existing `/workspace/.tools/browser/node_modules/playwright`; use `--playwright /absolute/module/path` in another environment. No packages are installed automatically. Only plain loopback `ws://` endpoints are accepted; never supply the provider's temporary bearer CDP endpoint directly.

The script opens one temporary tab and enables browser download events into a temporary directory in the reviewer browser. Use a dedicated diagnostic session because download behavior applies to that browser. It records only the three selected response headers and redirect host/path, excluding query strings, authentication headers and cookies. It closes its tab and disconnects CDP afterward. **Always cancel/close the exact provider setup session separately through its supported API and retain the sanitized cleanup result.** Stopping the bridge is not remote-session cleanup. If the process is interrupted or times out, the same cleanup obligation remains.

## Validation provenance

On 7 November 2026, the predecessor logic was exercised live through supported CDP in Chromium 147.0.7727.6: the viewer button, stable `/uc` route, and observed usercontent route downloaded all 32,127,341 bytes. Network events captured HTTP 200, `video/mp4`, the `.mp4` Content-Disposition filename and exact length; this browser's codec API reported no H.264/AAC support. See [live observations and limits](../../research/delivery-access/README.md).

At its initial 7 November implementation checkpoint, this parameterized wrapper had **not** been run in another live session solely for validation. `node --check`, `--help`, and offline assertions passed for invalid remote/token-bearing CDP endpoints, invalid byte counts, valid inputs, removal of URL queries and exclusion of cookie/authentication headers. Additional offline checks confirmed existing-output rejection and exclusive-write preservation, missing-header `unverified` status, contradictory MIME/status/length/filename failure, and exclusion of redirect headers from the final-download verdict. The captured live header fixture passes against 32,127,341 bytes and fails against a one-byte-wrong expected size. These are offline validations only. Those earlier prototype runs are not execution of this exact wrapper. The first live wrapper run is now recorded below.


## First live retained-wrapper execution — 8 November 2026

The exact retained script ran once against the privately uploaded 44-second summer proof, file ID `1tbuHWxLdAObAP_5MGQQjQfywtaOOTxRv`, expected size 14,432,807 bytes. It exited 0 with `download_verification: pass` and separate `header_verification.status: pass`. The browser completed all bytes and suggested the proper full `.mp4` filename. HTTP 200, `video/mp4`, exact Content-Length and `.mp4` Content-Disposition all passed. No wrapper fix or retry was needed.

[Actual wrapper output](../../research/delivery-access/summer-download-wrapper-v1.json), [script SHA-256 and run provenance](../../research/delivery-access/summer-wrapper-provenance-v1.json), and [successful exact-session cleanup](../../research/delivery-access/summer-session-cleanup-v1.json) preserve the evidence. The later final-film delivery check is recorded below. This browser pass did not hash the remotely downloaded file or establish playback; root's connector hash comparison and local motion review remain separate.

## Independently hash a larger connector download

The generic Sediment materializer caps files at32MiB. For a larger final MP4, use only the authenticated top-level `file_uri.download_url` actually returned by the connected Drive raw fetch, after grounding its MIME/URL. [download_reference.py](download_reference.py) streams that reference, enforces the expected byte count and SHA256, refuses an existing destination, and atomically publishes only an exact result. It retains no URL or credentials and reports network error classes without potentially secret exception messages. The500MiB bound is a local transfer guard, not a claim about connector upload limits.

Provide one JSON line containing `download_url` through stdin. Never put the URL in command arguments, logs, Git, or a user-facing link. In this executor plain-pipe stdin closes immediately; the tested route starts an echo-disabled PTY, runs the script with `--output`, `--expected-bytes`, and `--expected-sha256`, then supplies the fresh JSON through `write_stdin`. Restore terminal echo on exit. The live14.43MB summer transfer matches the separate Sediment download exactly; existing-output, bad-hash and oversized-transfer failures were also checked offline. [Validation](../../research/authenticated-reference-downloader-validation-v1.json). Larger final-film execution remains pending.


## Complete-film delivery check — 8 November 2026

The retained checker passed on its first attempt for private full-film file `10QCgXl_APKkg3BCfJNCP00IYUtflv2o7`, expected size **89,163,714 bytes**, with a 60-second deadline. Actual browser download completion and the separate HTTP/MIME/length/filename header checks all passed; exit code was 0. Both the response header and browser suggested filename were `Join Me in Life - Unfinished Morning (Full Music Video).mp4`.

[Actual full-film wrapper output](../../research/delivery-access/full-film-download-wrapper-v1.json), [script provenance](../../research/delivery-access/full-film-wrapper-provenance-v1.json), and [exact session cleanup](../../research/delivery-access/full-film-session-cleanup-v1.json) retain this run. The session was cancelled with HTTP 200 / `cancelled: true` and the loopback bridge stopped. No unsupported MP4 preview retry was attempted; content-hash verification and local playback review remain separate.
