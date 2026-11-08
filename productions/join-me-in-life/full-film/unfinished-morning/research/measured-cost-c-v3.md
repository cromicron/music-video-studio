# Unfinished Morning — measured runtime and cost supplement

Snapshot: 2026-11-08T01:36:52.428775+00:00. **ALL_SOURCES_BOUND_FINAL_FILM_NOT_VERIFIED_HERE**.

12 verified completed notebooks generated 42 takes in **9.068002 summed notebook wall-hours**. The binding ledger accepts 39/39 shots: 38 distinct new sources and 1 existing source(s). This is scoped source acceptance, not final-film approval.

Only exact locally verified completed C jobs. Running jobs, failed/pre-verification sessions, earlier concept tests, image/browser work, editing and review time are outside this measured subtotal.

Current selection is 38/42 generated takes (90.48%). Current chosen sources divided by generated takes, including rejected/unused attempts; not a future or cross-model keeper probability.

Current bindings include 4/4 planned performance shots. Earlier failed takes remain charged to runtime even when repaired sources are now accepted; the earlier paid report is a dated snapshot.

Raw workload comes from the frozen generation plan. Accepted keeper lengths come from the hash-verified adopted current edit; a reviewed redistribution of existing frames does not create another generated take or GPU charge.

Concurrent notebooks overlap. Whole-job timers include setup/download/CPU overhead and are not provider billing or account quota measurements. Billed GPU hours and project-specific quota debit are unknown.

| Completed record | Takes | Raw frames | Notebook wall-hours |
|---|---:|---:|---:|
| bridge-a-v2-output-verification.json | 5 | 869 | 1.079739 |
| closing-a-v2-output-verification.json | 5 | 997 | 1.061565 |
| middle-a-v2-output-verification.json | 5 | 1029 | 1.081077 |
| middle-b-v2-output-verification.json | 5 | 1021 | 1.124060 |
| middle-c-v2-output-verification.json | 5 | 869 | 1.032821 |
| opening-a-v2-output-verification.json | 1 | 209 | 0.270936 |
| opening-b-v2-output-verification.json | 3 | 651 | 0.715227 |
| opening-c-v2-output-verification.json | 5 | 1085 | 1.140296 |
| performance-a-v3-output-verification.json | 2 | 226 | 0.383498 |
| performance-b-v2-output-verification.json | 1 | 97 | 0.208527 |
| performance-c-v2-output-verification.json | 3 | 339 | 0.564576 |
| performance-d-v2-output-verification.json | 2 | 242 | 0.405679 |

Separate account snapshot at 2026-11-08T01:22:22.957735+00:00: 12.93 free GPU hours remaining, 0 listed active jobs. Separate official account-capacity snapshot, not the GPU hours charged to these jobs. Unreadable notebook statuses are not assumed active or inactive.

**Ten-film sensitivity from these completed records only:**

Scale each planned narrative/A2V raw frame by that method's measured completed-job wall-seconds per generated frame, then multiply by ten films and explicit attempt scenario. Fixed batch overhead is averaged over current batch sizes; no keeper-rate extrapolation.

| Scenario | Forecast notebook wall-hours | Notional 30-hour blocks* |
|---|---:|---:|
| repeat_this_observed_complete_source_process_ten_times | 90.680 | 4 |
| one_initial_take | 82.592 | 3 |
| three_total_takes_plus_10_percent_pool | 272.554 | 10 |

*Only if notebook wall-hours equalled provider quota hours, which this evidence does not establish. Sensitivity only: no quota admission, future throughput, acceptance yield or calendar guarantee. The 30h blocks are not actual quota debit or weeks. Each future film needs its own accepted five-second existing source or extra free generation. No still/loop fallback.

**The paid-video option has a hard actual checkout cap of €20 total across ten complete films.** The dated root report of 2026-11-08 records no new paid video-provider purchase and no purchased Runway credits consumed for selected C; this tool does not refresh account billing. **Already-paid subscriptions, included credits, machines and cloud accounts count as zero additional cost under the user’s rule.** Existing included TinyFish browser usage follows that rule; its underlying price is not audited. Separately purchased chat-credit replenishment is unpriced and excluded from the paid-video-tools budget. It prevents a claim about total personal spending, without changing the scope of the €20 paid-video cap. The three creative tools remain ChatGPT images, owned LTX and FFmpeg, plus the retained original summer source.

The dated [paid recommendation](paid-budget-c.md) remains unchanged. Its prices and conditional upgrade are research, not purchases or demonstrated improvement.

Rerun from the repository root after all outputs and bindings are verified; choose a fresh version for saved snapshots:

```sh
python3 productions/join-me-in-life/full-film/unfinished-morning/tools/cost/summarize.py --format json
python3 productions/join-me-in-life/full-film/unfinished-morning/tools/cost/summarize.py --format markdown
```

Both commands only read local evidence and print to stdout. Duplicate actual package/job identities, malformed completion data, changed hashes or accepted sources without exact completion evidence cause a nonzero exit rather than a plausible total. Running or queued jobs never count as completed. Distinct executions of the same package count separately.
