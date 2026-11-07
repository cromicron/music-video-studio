# Private keyframe transfer into Flow — handoff, 7 November 2026

**Execution update, 7 November:** Root completed this route. The ordinary TinyFish dashboard reused its existing personal key (dashboard had Regenerate, not Create; no rotation). The exact existing Flow profile matched through REST. Private PNG byte upload through Flow's actual chooser succeeded and persisted in project `8bcfabef-47cf-4414-a180-1a256150973f` across saved/new sessions. The [proxy-preserving CDP bridge](tinyfish_cdp_bridge.py) was necessary because direct Playwright WSS failed on the unavailable direct route. Key/session data remain outside Git in private files. Both setup sessions were explicitly saved/closed with HTTP 200. Generation is a separate result: two submissions were refused for unusual activity, no output, balance50 after both; the automated Flow generation route is stopped. [Access record](../ACCESS_SETUP.md), [initial attempt](../research/flow-pilots/F01-hospital-embrace.json), [retry](../research/flow-pilots/F01-hospital-embrace-retry1.json). The investigation below preserves what was known before execution.

**Finding:** TinyFish's documented profile setup API plus Playwright can provide a private local-PNG-to-browser transfer. The available TinyFish MCP automation tool does not expose a file attachment parameter. This is a documented implementation route, **not a completed Flow upload**. No browser session, generation, account write, private Drive upload, credential inspection or spending was performed in this investigation.

Root reports that Flow is authenticated in profile `prof_c6ddfc0a3d2c4524` and shows 50 daily credits. Root also checked the actual MCP setup response: it returns a `setup_url`, but no CDP URL. Those are parent observations, not independent checks by this researcher. Root owns browser runs and the unified access record.

## What was verified

| Evidence | Actual observation | Consequence |
| --- | --- | --- |
| Available `tinyfish_run_web_automation` tool schema | URL, goal, profile, agent configuration and related fields; no file/attachment/source-bytes parameter | A local `/workspace/...png` path in its goal is not a supported file transfer. |
| Public [TinyFish OpenAPI](https://agent.tinyfish.ai/v1/openapi/main), fetched read-only | Run request has no asset-file field or upload endpoint. `/v1/profiles/{profileId}/upload` is browser state upload | Do not mistake cookie/storage upload for media upload. |
| Official [profile setup reference](https://docs.tinyfish.ai/api-reference/browser-context-profiles/create-a-profile-setup-session) | REST response includes `session_id`, `cdp_url`, `base_url`, `timeout_seconds`, `expires_at` | This is the supported endpoint for a controller connection associated with the existing profile. |
| Published `@tiny-fish/sdk` **0.11.0**, downloaded into memory and inspected | `client.profiles.setup.start(profileId, params)` calls the documented setup-session endpoint and parses a CDP URL; no media-upload resource | SDK supports the same route. No SDK installation or account invocation occurred. [Package metadata](https://registry.npmjs.org/@tiny-fish/sdk/latest), [inspected tarball](https://registry.npmjs.org/@tiny-fish/sdk/-/sdk-0.11.0.tgz). |
| [Playwright upload documentation](https://playwright.dev/python/docs/input#upload-files) | `set_input_files` accepts an in-memory `{name, mimeType, buffer}` payload; dynamically created inputs can use a file-chooser event | Local bytes can be sent through the controller to the real browser input without public hosting or copying cookies. This method was not executed against Flow. |
| [Flow's own creation guide](https://support.google.com/flow/answer/16353334?hl=en) | Documents uploaded project assets, local-device drag/drop and upload via Add; start/end frame input | Local upload is supported. The guide does **not** establish a Drive picker. |
| Connected Drive upload tool schema | Accepts an absolute local path as `file_uri` | Private Drive staging is possible in principle, but the remaining Drive→Flow/browser-file step is unverified. No staging was done. |

A public read of `agent.tinyfish.ai/api-keys` redirected to its sign-in page. A shell presence-only check found no `TINYFISH_API_KEY` environment variable; no credential values or stores were read. Public sign-in HTML did not establish whether the currently rendered login page offers Google sign-in. Official TinyFish material mentions Google sign-in as an account option, but actual SSO reuse into this user's existing TinyFish account remains a UI check.

## Smallest supported setup

1. Use the ordinary [TinyFish API Keys page](https://agent.tinyfish.ai/api-keys), under the **same TinyFish user and account/organization context** as the existing profile. The [authentication guide](https://docs.tinyfish.ai/authentication) explicitly instructs **Create API Key** there; an API key is shown once. Use a personal key, not an organization workflow key. [Organization documentation](https://docs.tinyfish.ai/key-concepts/organizations) says profiles belong to each person and require a personal key.
2. If the dashboard offers **Continue with Google**, normal SSO may reuse the saved Google sign-in. This is conditional: a Google login to Flow does not itself prove a matching TinyFish login or identical account context. Do not create a different account to work around access. Confirm the exact existing profile is visible in the dashboard and, with the new key, through `GET /v1/profiles`; this is a stronger identity check than assuming matching email is enough.
3. Keep the key in an approved private secret/environment mechanism, outside the repository and reports. The plugin's OAuth session is not an API key and should not be extracted. A secure transfer of the newly created key into the executor is still a setup requirement; this report does not claim the current MCP tool can write a secret into the local filesystem.
4. Once root's active browser work has finished, open an API setup session for the **existing** profile. Connect Playwright to the returned `cdp_url`. Verify that Flow is actually authenticated in that session before proceeding; profile metadata alone is insufficient. Do not substitute the generic Browser API, whose sessions are documented as isolated and whose creation schema has no `profile_id` parameter.
5. Through Flow's actual upload UI, inspect the current file input or capture its file-chooser event. Supply the exact hashed PNG bytes, then verify the resulting asset thumbnail and dimensions. Uploading an asset is separate from Generate: stop before any generation button. Four distinct keyframes serve the three tests; their selected paths and hashes are in [flow-pilot-requests.json](flow-pilot-requests.json).
6. Save or discard only this newly created setup session using its returned session ID. Do not touch root's automation runs, another user's session or the stored profile itself. Verify upload persistence in the same Flow project before declaring transfer complete.

## Exact documented endpoint scope

REST base: `https://agent.tinyfish.ai`; header: `X-API-Key` from the private personal-key mechanism. No invented API-key-creation REST endpoint is proposed; key creation is the documented dashboard action.

| Method and path | Request / use |
| --- | --- |
| `GET /v1/profiles` | Confirm `prof_c6ddfc0a3d2c4524` belongs to this authenticated key/context; returns metadata, not cookie values. |
| `GET /v1/profiles/prof_c6ddfc0a3d2c4524` | Optional profile/domain-count metadata check; not a credential export. |
| `GET /v1/wallet` | Inspect actual browser-session rates and allowance before creating a session. TinyFish browser usage and Flow generation credits are different budgets. No top-up or auto-reload change. |
| `POST /v1/profiles/prof_c6ddfc0a3d2c4524/setup-session` | JSON: `{"url":"https://flow.google.com/","timeout_seconds":300}`. Keep the returned session and connection data privately; do not print the CDP URL. |
| `POST /v1/profiles/prof_c6ddfc0a3d2c4524/save` | JSON: `{"session_id":"<returned session ID>"}`. Captures setup browser state into the profile and closes that browser. Optional `signed_in_sites` must describe actual observed sign-in; do not invent it. |
| `POST /v1/profiles/prof_c6ddfc0a3d2c4524/setup-session/cancel` | JSON: `{"session_id":"<returned session ID>"}`. Closes this setup browser and discards unsaved setup state. It does not undo assets already uploaded into Flow. |

Choose save after a successful, verified session if refreshed state should persist; choose cancel to leave stored state unchanged after a failed/unused setup. Check cleanup results. A local Playwright disconnect is not proof the remote session stopped billing. Do not call `/profiles/.../upload`, export cookies, delete profile domains, change wallet settings, or generate video as part of this transfer-only operation. Exact API definitions: [create setup](https://docs.tinyfish.ai/api-reference/browser-context-profiles/create-a-profile-setup-session), [save](https://docs.tinyfish.ai/api-reference/browser-context-profiles/save-a-profile-setup-session), [cancel](https://docs.tinyfish.ai/api-reference/browser-context-profiles/cancel-a-profile-setup-session), [profile lifecycle](https://docs.tinyfish.ai/agent/api/profiles/browser-context-profiles).

## Transfer primitive

This snippet is illustrative and deliberately requires an already connected authenticated page plus a real inspected upload locator; it does not start sessions or guess Flow selectors:

```python
from pathlib import Path
from hashlib import sha256

source = Path(source_path_from_selected_request)
payload = source.read_bytes()
assert sha256(payload).hexdigest() == expected_sha256
await observed_file_input.set_input_files({
    "name": source.name,
    "mimeType": "image/png",
    "buffer": payload,
})
# Inspect the resulting Flow asset. Do not click Generate here.
```

If Flow creates its input only after clicking Upload, use Playwright's documented `expect_file_chooser` and `file_chooser.set_files` with the same payload. No base64 PNG belongs in an agent goal, a public paste, or a public URL. No account/session result in this report establishes successful end-to-end transfer yet.

## Handoff state

**Documented and inspected:** API-key dashboard procedure, personal-key requirement, setup-session/CDP response, SDK implementation, Playwright file-byte upload, Flow device upload, exact save/cancel endpoints. **Still to verify by root:** same-user dashboard SSO, secure key handoff, actual setup-session sign-in, live Flow input, private upload success and retained project assets. **Not established:** direct Drive picker or native TinyAgent download-then-upload capability. This investigation changed only this report; it did not edit STATUS, SESSIONS, ACCESS_SETUP or usage ledgers.
