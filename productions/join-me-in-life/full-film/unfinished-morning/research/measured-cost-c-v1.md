# Unfinished Morning — measured runtime and cost supplement

Snapshot: 2026-11-07T23:46:48.117819+00:00. **INCOMPLETE_SOURCE_COVERAGE**.

8 verified completed notebooks generated 22 takes in **4.768478 summed notebook wall-hours**. The binding ledger accepts 19/39 shots: 18 distinct new sources and 1 existing source(s). This is scoped source acceptance, not final-film approval.

Only exact locally verified completed C jobs. Running jobs, failed/pre-verification sessions, earlier concept tests, image/browser work, editing and review time are outside this measured subtotal.

Current bindings include 4/4 planned performance shots. Earlier failed takes remain charged to runtime even when repaired sources are now accepted; the earlier paid report is a dated snapshot.

Concurrent notebooks overlap. Whole-job timers include setup/download/CPU overhead and are not provider billing or account quota measurements. Billed GPU hours and project-specific quota debit are unknown.

| Completed record | Takes | Raw frames | Notebook wall-hours |
|---|---:|---:|---:|
| bridge-a-v2-output-verification.json | 5 | 869 | 1.079739 |
| opening-a-v2-output-verification.json | 1 | 209 | 0.270936 |
| opening-b-v2-output-verification.json | 3 | 651 | 0.715227 |
| opening-c-v2-output-verification.json | 5 | 1085 | 1.140296 |
| performance-a-v3-output-verification.json | 2 | 226 | 0.383498 |
| performance-b-v2-output-verification.json | 1 | 97 | 0.208527 |
| performance-c-v2-output-verification.json | 3 | 339 | 0.564576 |
| performance-d-v2-output-verification.json | 2 | 242 | 0.405679 |

**Ten-film sensitivity from these completed records only:**

Scale each planned narrative/A2V raw frame by that method's measured completed-job wall-seconds per generated frame, then multiply by ten films and explicit attempt scenario. Fixed batch overhead is averaged over current batch sizes; no keeper-rate extrapolation.

| Scenario | Forecast notebook wall-hours | Notional 30-hour blocks* |
|---|---:|---:|
| one_initial_take | 84.215 | 3 |
| three_total_takes_plus_10_percent_pool | 277.909 | 10 |

*Only if notebook wall-hours equalled provider quota hours, which this evidence does not establish. Sensitivity only: no quota admission, future throughput, acceptance yield or calendar guarantee. The 30h blocks are not actual quota debit or weeks. Each future film needs its own accepted five-second existing source or extra free generation. No still/loop fallback.

**The cap remains €20 total for ten complete films.** The dated root report of 2026-11-07 records no new paid video-provider purchase; this tool does not refresh account billing. Chat-credit replenishment cost is unknown; existing TinyFish browser usage is unpriced. **Total user cost is unknown, not €0; all-in compliance with €20 is not proven.** The three creative tools remain ChatGPT images, owned LTX and FFmpeg, plus the retained original summer source.

The dated [paid recommendation](paid-budget-c.md) remains unchanged. Its prices and conditional upgrade are research, not purchases or demonstrated improvement.

Rerun from the repository root after all outputs and bindings are verified; choose a fresh version for saved snapshots:

```sh
python3 productions/join-me-in-life/full-film/unfinished-morning/tools/cost/summarize.py --format json
python3 productions/join-me-in-life/full-film/unfinished-morning/tools/cost/summarize.py --format markdown
```

Both commands only read local evidence and print to stdout. Duplicate actual package/job identities, malformed completion data, changed hashes or accepted sources without exact completion evidence cause a nonzero exit rather than a plausible total. Running or queued jobs never count as completed. Distinct executions of the same package count separately.
