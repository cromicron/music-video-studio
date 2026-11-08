# Performance-cut GPU readiness — 8 November2026

[Machine-readable observation and budget scenarios](operations-readiness-v1.json) retain the exact observation time. This is a read-only inspection; no generation, purchase, account change or new login occurred.

## Actual access and capacity

- The official Kaggle CLI at `/workspace/.tools/jml-kaggle/bin/kaggle` succeeds with the existing OAuth. No credential value was read or printed.
- A fresh `kaggle quota` reports **12.93 free GPU hours remaining of30**, refreshing14 November2026 at00:00UTC. The historical12.93 figure happens to remain current; it was not simply copied.
- Fresh owned-notebook listing returns34 entries. Actual status reads find32 terminal notebooks and no reported active status. Two old setup/2025 notebooks return the same404 as prior capacity records, so their active/inactive state is not claimed. Do not cancel or restart them to obtain a tidier report. Official job admission remains authoritative.
- Exact old middle-a/2 and middle-c/2 are COMPLETE. All12 old C production jobs remain completed and must never be resubmitted for this revision.
- Every retained I2V and A2V base-runtime lock file matches. The local32GB workspace has about4.9GB free at inspection; use bounded downloads and avoid raw whole-film RGB dumps.

## Frozen runtime contracts to preserve

The current narrative adapter stages one to five serial fresh children per private job, max5400s,896×512 at24fps, raw8n+1 lengths89–225frames, seed49, **two distinct reviewed PNG endpoints**, six leading frames and explicit keeper/tail handles. The current A2V adapter takes one reviewed image plus exact original-song48k stereo PCM, raw lengths89/97/105/113/121/129frames, six leading and at least seven trailing frames.129-frame A2V has actual GPU success; longer A2V is outside the tested adapter. Neither mode proves playing/phoneme quality merely by decoding successfully.

Both old wrappers hard-bind C IDs/private `jml-c-*` destinations and the frozen old C story hash. Create a separate derived performance-cut wrapper and guard after the new shot plan is adopted; preserve the old adapters/guard bytes and retain the pinned neural/runtime code unchanged. Never relabel the new story as a successful old queue.

## Bounded production proposal

Measured old rates are96.35875 wall seconds per raw I2V second and149.31523 per raw A2V second, including recorded notebook overhead. At120 raw seconds (90I2V/30A2V), this gives3.65 summed notebook hours. A stated2×wall quota-debit stress leaves5.62 free hours from12.93, above the4h correction reserve. At130 raw seconds with30A2V, the stress leaves5.09h. At150 raw seconds with40A2V, it leaves3.72h and fails the reserve. These are workload scenarios, not observed billed GPU hours or a completion/keeper guarantee.

Start only after root binds reviewed single-shot plates and an immutable timeline/payload. Select small representative pilots (wide band, keys and drums or equivalent chosen roles), verify exact private remote source/package readback, and read official quota immediately before and after those jobs. Use the observed new debit/rate to release subsequent batches. Keep at most two active account GPU jobs, counting unrelated work, retain at least4h free quota in the revised projection, and never auto-retry failed takes. Motion/instrument-contact review, not runtime success, decides keepers.

## Actual read-only commands

```sh
/workspace/.tools/jml-kaggle/bin/kaggle quota
/workspace/.tools/jml-kaggle/bin/kaggle kernels list --mine --page-size 100 --format json --sort-by dateRun
/workspace/.tools/jml-kaggle/bin/kaggle kernels status OWNER/SLUG
/workspace/.tools/jml-kaggle/bin/kaggle kernels status darionalis/jml-c-middle-a/2
/workspace/.tools/jml-kaggle/bin/kaggle kernels status darionalis/jml-c-middle-c/2
```

All34 listed notebooks were checked with bounded four-way concurrent read-only subprocess calls; no unrelated notebook contents were opened.
