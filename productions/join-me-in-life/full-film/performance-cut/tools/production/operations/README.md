# Retained operator reference and recovery

These Python files are exact credential-free execution snapshots. [Initial snapshot](snapshot-v1.json) records the two original correction launches; [current snapshot](snapshot-v2.json) adds the controller with three registered packets after B10-only BAND-FIX/2 also passed actual launch/private/code/mount checks. The current dispatcher reference is `dispatch_corrections_snapshot_v3.py`; its registered-packet guard is3 while the actual concurrent-job limit remains2. Active processes and temporary files were not changed by retaining these copies. They are specific to this recreation, its `/workspace/music-video-studio` root, prepared official CLI and ignored build layout. They are not a general service or new authority to generate.

The [vocal execution release](../../../review/vocal-fix01-root-execution-release-v1.json), [action execution release](../../../review/action-fix01-root-execution-release-v1.json) and [B10 band execution release](../../../review/band-fix01-root-execution-release-v1.json) own the exact plans, package locks and versions. The [production guide](../README.md) owns setup. Credentials remain outside Git with the official CLI; no credential file is copied by these helpers. Actual source acceptance, musical/acting review and final-film approval remain separate.

## Recover the state before any action

Read the exact submission, retention and latest routing records in `performance-cut/research/`. A submission record means an attempt already happened, even if a later local check failed. Never delete it or repeat a push because a watcher/process vanished. In this run a local filename mismatch occurred **after** vocal version3 was submitted; reading the existing returned code completed verification without another push. Vocal no-run1 also had an empty mount: accepted no-run2 replaced it, making actual GPU version3. Action's accepted no-run1 makes its GPU version2.

From repository root these are read-only actual-status checks:

```sh
/workspace/.tools/jml-kaggle/bin/kaggle kernels status darionalis/jml-p-instruments-a/2
/workspace/.tools/jml-kaggle/bin/kaggle kernels status darionalis/jml-p-instruments-b/2
/workspace/.tools/jml-kaggle/bin/kaggle kernels status darionalis/jml-p-vocal-fix-01/3
/workspace/.tools/jml-kaggle/bin/kaggle kernels status darionalis/jml-p-action-fix-01/2
/workspace/.tools/jml-kaggle/bin/kaggle kernels status darionalis/jml-p-band-fix-01/2
```

Base instrument sources already retained under `assets/motion/instruments-{a,b}-v2` must not be regenerated. If a completed correction lacks retained output, use `kaggle kernels output EXACT_VERSION --path NEW_DIRECTORY --page-size 100 --quiet`, then the existing A2V or I2V download verifier with its exact package lock. Output download is not inference. Preserve partial downloads/proofs and inspect them before choosing a new readback destination.

Restore read-only watchers with [watch_jobs.py](../watch_jobs.py), one exact version per process, a fresh report and 60-second polling. Archive an old observer before replacing its expected build pathname; a stale report is not remote failure. The dispatcher expects `build/jml-p-instruments-{a,b}-observer-v1.json`, `build/jml-p-vocal-fix01-observer-v1.json` and `build/jml-p-action-fix01-observer-v1.json` and `build/jml-p-band-fix01-observer-v1.json`. For a cold workspace, obtain actual terminal base snapshots with the same read-only watcher rather than fabricating them. Keep continuous observer/cache/log writes in ignored build storage.

## If the local controller must be restored

First inspect actual process commands and ensure no controller is still running. There must be only one mutation owner. Current routing records give historical PIDs; verify a PID's command before stopping it. Stop/restart of a local observer never cancels a remote notebook.

The helpers still refer to their original `/tmp/pcut_launch_correction.py` path. Only after the old controller has stopped, restore the exact retained copies there, using the current v3 dispatcher snapshot for the controller. Do not replace an active helper.

```sh
install -m700 productions/join-me-in-life/full-film/performance-cut/tools/production/operations/launch_correction_snapshot.py /tmp/pcut_launch_correction.py
install -m700 productions/join-me-in-life/full-film/performance-cut/tools/production/operations/dispatch_corrections_snapshot_v3.py /tmp/pcut_dispatch_corrections_v3.py
``` The launcher also needs the exact local bundles named by the predeployment proofs. If caches were lost, recreate those bundles locally from their frozen plans with the owned preparation adapters, then compare the resulting package-lock hashes to the immutable release records before any operation.

If the ignored account cache was lost, seed it only from the frozen [observed account preflight](../../../research/operations-cached-account-preflight-v1.json), preserving that snapshot as historical evidence. The launcher's next fresh owned-list/latest-run comparison and active-status reads remain mandatory; this seed is not a claim of current account state. This also avoids dependence on an old temporary baseline file.

```python
from pathlib import Path
import json
root = Path('/workspace/music-video-studio')
cut = root / 'productions/join-me-in-life/full-film/performance-cut'
cache = root / 'build/jml-p-account-status-cache-v1.json'
assert not cache.exists()
saved = json.loads((cut / 'research/operations-cached-account-preflight-v1.json').read_text())
rows = saved['account']['statuses']
assert all('last_run_time' in row and 'ref' in row for row in rows)
cache.parent.mkdir(exist_ok=True)
cache.write_text(json.dumps({row['ref']: row for row in rows}, indent=2) + '\n')
```

If its ignored config was lost, reconstruct it from the three exact release records as below. This creates only a local routing file, not a provider job. Preserve any existing config rather than overwriting it.

```python
from pathlib import Path
import hashlib, json
root = Path('/workspace/music-video-studio')
cut = root / 'productions/join-me-in-life/full-film/performance-cut'
output = root / 'build/jml-p-correction-release-routing-v1.json'
assert not output.exists()
rows = []
for tag, slug, kind in [('vocal-fix01', 'vocal-fix-01', 'a2v'),
                         ('action-fix01', 'action-fix-01', 'i2v'),
                         ('band-fix01', 'band-fix-01', 'i2v')]:
    relative = f'review/{tag}-root-execution-release-v1.json'
    file = cut / relative
    release = json.loads(file.read_text())
    assert release['status'] == 'released_for_one_exact_job_when_actual_account_slot_free'
    rows.append(dict(tag=tag, slug=slug, kind=kind, release=relative,
                     release_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
                     version=release['expected_execution_version']))
output.parent.mkdir(exist_ok=True)
output.write_text(json.dumps(dict(jobs=rows, expected_total_jobs=3), indent=2) + '\n')
```

After state recovery, one controller may resume the existing exact attempts. It must not be run alongside another copy. Its launcher refuses an existing/incomplete attempt, checks every locked file and root release, performs fresh cached-account/quota/max-two checks, and submits only an unattempted exact released payload. Neither helper retries failed inference. Any discrepancy requires inspection and a changed, explicitly scoped next hypothesis under the current task. Existing success records remain immutable; output retention does not clear motion quality.

The new private-dataset readiness checks also matter: a fresh resource can initially return403 while creation propagates. Keep the successful create record, wait for actual official READY, download/verify private metadata and locked files, **then** save no-run code and verify its real mount. Do not repeat account sign-in or dataset creation for that observation. The current action setup followed this order and passed on its first no-run save.
