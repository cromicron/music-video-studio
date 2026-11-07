# Paid recommendation for ten complete hybrid music videos

Updated **7 November 2026** against the [selected action plan](../review/action-coverage-plan.md), actual LTX2.3 run and [usage ledger](usage-ledger.json). This supersedes the earlier six-action-shot / 24-second-per-film proposal. The limit is **€20 total for all ten completed films**, including tax, fees, deposits, storage and transfer. It is not €20 each, and it does not require every final frame to be newly generated.

**Recommendation: keep our selected ChatGPT images → owned LTX → FFmpeg workflow, use renewable free Kaggle time as the base, and conditionally buy one tightly bounded GPU rental through Vast only when it demonstrably accelerates the same work. Cap all new provider spending at $15 net and €20 actually paid, whichever limit is reached first.** A subscription is not presently justified. No purchase, paid generation or account change was made for this update; no further access is requested. Existing free production can continue. A paid burst still needs Dario's spending authorization, which is absent from the ledger.

This is a conditional way to complete the **hybrid** batch with optional paid acceleration, not a promise that €20 buys all generation commercially. At the observed dual-T4 speed, the all-paid batch misses the cap. A faster rental must pass the cost gate below; otherwise finish the outstanding work through legitimate free quota renewals. A paid service does not solve an acting failure merely by returning a valid video.

## The workload being priced

**Scope revision v3:** root adopted the independently accepted continuous summer source `[0,5)` across S025/S026 at 120.875–125.875 seconds. It replaces the planned two-second historical male crop plus three-second new female reply, adding **two new-picture seconds per film** without adding a delivery. The former male derivative remains an inactive alternate. The previous **113.083333-second** target and **136.5-second** one-take generation set are retained as prior-scope history in budget.json; the current targets below govern. The source pass does not itself approve the new 63-frame lead / 120-frame motion insertion or phoneme sync.

| Editorial delivery | Per film | Ten films |
| --- | ---: | ---: |
| Principal new action/performance | 7 takes / 34.166667 s | 70 / 341.666667 s |
| Distinct quiet character motion | 13 deliveries / 80.916667 s | 130 / 809.166667 s |
| **Total retained new picture** | **20 deliveries / 115.083333 s** | **200 / 1,150.833333 s** |
| Original soundtrack | 277.776 s | 2,777.76 s |

New picture is approximately **41.43%** of the song. The remaining **162.692667 seconds per film** use supplied performances, existing matched drawing exposures, environmental camera work and deliberate reviewed holds. The 24 fps picture is 277.791667 seconds, so its complementary picture interval is 162.708333 seconds. Neither remainder is described as new generated acting. Existing paid subscriptions, local rendering and supplied media add no new cash under Dario's accounting; the 1,897 **purchased** Runway credits are finite prepaid inventory, remain untouched, and are not renewable free credits.

The ten-film calculation assumes comparable new-picture requirements and adequate legitimate source material for each film. Another song cannot reuse this song's mouth timings. If a later film needs more new performance or lacks supplied footage, recalculate its allocation before claiming the ten-film target. For this film, producing the seven principal actions alone is insufficient: the thirteen quiet deliveries and whole-cut review are part of completion.

A working generation allowance includes **one second of trim handles per delivery**, then rounds up to LTX's `8n+1` frame grid at 24 fps:

`requested_frames = 8 × ceil((round(retained_seconds × 24) + 24 − 1) / 8) + 1`

This gives **138.5 generated seconds per one-take set**, across twenty requests ranging from 4.375 to 10.041667 seconds. Longer settings must pass actual memory/runtime checks; the existing four-second A2V success does not establish ten-second feasibility. If a delivery must be split, budget the extra handles and inspect the new join. Splitting does not authorize repeating or retiming movement.

| Retry allocation | Attempts across ten films | Generated seconds before reviewing/trim |
| --- | ---: | ---: |
| Three **total** takes per delivery: initial attempt + two retries | 600 | 4,155 |
| Same allocation + shared 10% extra-take pool | 660 | 4,570.5 at the same duration mix |
| Sensitivity: initial attempt + three retries | 800 | 5,540 |

The recommended envelope includes the 60-attempt shared pool, subject to the cash/runtime limit; a longer extra take consumes more of it. These are workload allowances, **not observed keeper rates**. All rejected takes count. There is no guarantee that three tries produce an acceptable performance. Exact per-delivery lengths, arithmetic and evidence dates are in [budget.json](budget.json).

## What the production test actually established

The [LTX2.3 A2V render record](../assets/motion/ltx23-a2v-bridge-pilot/render.json) contains **97 frames / 4.041667 seconds at 896×512, 24 fps**, with **255.161 seconds of generation**. Its internal renderer elapsed time is 701.964 seconds; the outer [job record](../assets/motion/ltx23-a2v-bridge-pilot/job.json) and usage ledger record **774.901 seconds for the complete cold job**, including bootstrap/setup. Do not confuse these clocks or treat them as an isolated account-quota debit.

Independent [source review](../review/ltx23-a2v-bridge-pilot-review.md) accepted **source [0.125, 3.500) seconds, 81 frames / 3.375 seconds**, for the first screamed plea. The terminal face/hand/hair breakup is rejected. This is a scoped visual source pass, not phoneme-sync, edited insertion or full-film approval. The render record's original `unreviewed` label is historical; the later signed review supplies the scoped result. The first-plea fragment and separate summer source pass cannot establish a one-in-three success probability across walking, reflections, summer identity, contact and quiet breathing. Earlier 13B and hosted tests include genuine failures; a short 13B aftermath fragment is not a replacement for the required new performances.

The independently reviewed [summer source](../review/ltx23-summer-pilot-review.md) now supplies a separate accepted `[0,5)` interval. Together with the first plea this makes **8.375 seconds of scoped accepted new source**, leaving **106.708333 seconds** of the selected target without completed accepted coverage. Sequence/context review remains separate. This budget update retains the measured A2V rate as its explicit sensitivity proxy; it introduces no new I2V speed measurement or inferred keeper rate.

The **saved quota observation used for this estimate**, at **02:29:55 UTC on 7 November**, was **28.868530556 of 30 GPU hours remaining**, zero reserved, **pay-to-scale disabled**. It precedes the subsequent summer I2V submission; it is not a fresh live balance. The saved reset is **14 November 00:00 UTC**. [Raw quota evidence](kaggle-quota-after-a2v-v5.json). Overlapping earlier jobs prevent attributing individual debit by subtraction. This update made no account calls.

Dividing the measured generation time by output length gives **63.1327 generation seconds per output second**. Applying that rate linearly is a sensitivity model, not a measured mixed-scene batch:

| Allowance | Warm generation at the pilot's rate | With the observed cold overhead repeated for every request |
| --- | ---: | ---: |
| 600 attempts | 72.87 h | 159.49 h |
| 660 attempts including pool | 80.15 h | 175.44 h |
| 800 attempts | 97.15 h | 212.65 h |

Warm batching, prompt reuse and retaining loaded models matter enormously. The current tested wrapper is a bounded diagnostic; production batching has not yet proved this amortization. Long-clip memory and temporal attention can make scaling nonlinear. The 660-attempt warm scenario plus modest setup fits roughly **three weekly 30-hour allocations**; repeated cold jobs push it toward six. This is a planning range, not a promised completion date or an assertion that all twenty deliveries have passed. There is no recurring fee for the observed free quota, and no need to buy compute merely to consume the remaining allowance sooner. [Official Kaggle GPU guide](https://www.kaggle.com/docs/efficient-gpu-usage) · [retained free-GPU research](free-gpu.md).

## Conditional paid rental and hard stop

An hourly GPU is the paid option that preserves our actual supplied-song and first/end-image control, source locks, original audio and local editor. The public Vast documentation confirms separately charged compute, continuing storage and transfer. The **6 November** read-only snapshot found verified RTX 4090 offers around **$0.383–0.402/hour**, with variable storage and bandwidth; it remains historical evidence in budget.json. On **7 November**, unauthenticated searches for dual T4 and single 4090 offers returned HTTP 403. **No current offer or capacity has been verified.** A fresh exact quote must satisfy the envelope; the old offer is not reserved.

| Whole ten-film paid envelope, including pilot | Limit/assumption |
| --- | ---: |
| Compute quote | ≤ $0.40/hour |
| Allocated disk/storage | ≤ $0.02/hour |
| Total setup/download/load time | 1.5 hours |
| All transfer | $1 |
| Extra contingency | $1 |
| **Total net allocation** | **$15** |
| Stress conversion: €1/$1, 19% VAT, 3% payment/FX fee | **€18.3855** |
| Margin to absolute €20 cash cap | **€1.6145** |

VAT and exchange values are conservative planning assumptions, not the actual invoice or a guarantee of the user's tax treatment. All providers' invoices/deposits count against the same €20; unspent prepaid credit does not disappear from cash spent. Reject a minimum deposit or tax/fee total that breaches the cap. Benchmark charges are inside the $15 allocation, not an extra purchase. No annual commitment, second subscription, paid storage plan or automatic top-up is included.

With these assumptions, available warm generation time is:

`(15 − 1 transfer − 1 contingency) / (0.40 compute + 0.02 storage) − 1.5 setup = 29.452381 hours`

To cover all 660 planned attempts commercially, the actual mix must average **≤160.65 seconds per attempt**, including unsuccessful generations but excluding only the explicitly budgeted setup. Equivalently it must be **at least 2.72× faster** than the measured A2V seconds-per-output-second rate. Without the extra pool the 600-attempt gate is 176.71 seconds / 2.47×; with three retries after the first take it is 132.54 seconds / 3.30×. The allowed seconds per attempt stay unchanged because the attempt count and cash envelope are unchanged; the longer duration mix raises the required relative throughput. These are **required thresholds**, not a claimed RTX 4090 benchmark. Even dual-T4 rental at the observed speed would need compute below approximately **$0.1548/hour for both cards together** to fit the 600-attempt envelope after the stated storage/fixed costs; no such current offer is established.

The tested runner explicitly requires **two T4s**. A single 24 GB 4090 is not a drop-in replacement for two separate 16 GB allocations. Its device placement, quantization kernels, long-clip memory and cold loading must first be adapted and smoke-tested. The current pinned weights occupy approximately **35.38 GB**, with a roughly 39.67 GB fresh-cache requirement before other runtime files. Price the actual disk allocation and model transfer, not an empty instance. Our own retained implementation remains useful whether it runs free or rented. [Runtime/source requirements](../tools/kaggle-a2v/README.md).

Before any paid batch, the outside test is several representative principal **and** quiet shots at their required lengths, with independently accepted motion and a ledger covering failures, loading, disk and transfer. The free route can establish quality first; a paid hardware test must stay within a small **$3 net first-stage limit**, counted inside $15. Continue only when measured remaining work fits the remaining cash and runtime. Otherwise stop the rental and use free quota; do not lower the movement standard or secretly replace required acting with holds to make the arithmetic pass.

At each submission, reserve the full in-flight timeout cost plus storage, transfer and teardown. Download and hash-check useful outputs, **destroy** rented instances and attached volumes, and verify that nothing remains billable. Merely stopping a GPU continues storage billing. Vast can charge a saved card for a negative balance, so a prepaid wallet is **not** a hard cap. Disable optional auto-top-up, avoid reaching zero, and stop before committed costs could exceed the ledger. [Vast pricing](https://docs.vast.ai/guides/instances/pricing) and [billing](https://docs.vast.ai/guides/reference/billing), rechecked 7 November.

## Why the previously researched managed options are not selected

These lower bounds now use **1,150.833333 retained new seconds across the ten hybrid films**, not all 2,777.76 song seconds. They omit handles, model-duration rounding, tax and minimum payments, so they favor the APIs. Even on that basis three total takes exceed the ceiling.

| Paid API | Rate/source | One take, no handles | Three takes, no handles |
| --- | --- | ---: | ---: |
| Hedra / Seedance 1.5 Pro, 480p, audio off | Actual saved 5s quote $0.061227; extrapolated $0.0122454/s | $14.09 | **$42.28** |
| LTX2.3 Fast 720p I2V | $0.03/s, official pricing rechecked 7 Nov | $34.53 | **$103.58** |
| Runway Gen-4 Turbo API | $0.05/s, official pricing checked 6 Nov | $57.54 | **$172.63** |
| Kling 2.5 Turbo Pro via fal | $0.07/s, endpoint checked 6 Nov | $80.56 | **$241.68** |

[Hedra catalog](https://www.hedra.com/models/video) · [saved estimate](hedra-seedance-15-estimate.json) · [LTX pricing](https://docs.ltx.io/pricing) · [Runway pricing](https://dev.runwayml.com/pricing) · [Kling endpoint](https://fal.ai/models/fal-ai/kling-video/v2.5-turbo/pro/image-to-video). The Seedance estimate omitted the actual reference-image upload, so it is not a final I2V quote. LTX's I2V rate is not substituted for its supplied-audio endpoint. At Seedance's extrapolated rate the 4,155-second handle budget alone becomes **$50.88 before tax**, even before the extra pool. The previous $12.85767 / 210-attempt proposal only bought **24 retained seconds per film**, and is withdrawn as an answer to the selected 115-second plan.

**HF PRO has plausible quota volume, but is not an equivalent tested production method.** Its $9/month price and 40 minutes/day were rechecked on 7 November. At the same tax/FX stress assumptions, one month is €11.0313. The official LTX2.5 Space currently accepts prompt, **first image**, dimensions, frame count, seed and decoder. Its inspected interface provides **no supplied-song audio or end-image conditioning input**, unlike the selected A2V/first-and-end workflow. Model-generated audio is not a substitute for the original song. Our one hosted test also failed the intended acting. A custom compatible private Space would be new engineering with unmeasured quota/runtime, not a capability already bought by PRO.

Quota admission still matters. The observed five-second request reserved **150 weighted seconds** and the subsequent request was refused with **72 remaining**. Initial balance was not measured; the often-used **48-second debit is inferred** from a nominal 120-second allowance and remains unresolved, not measured. The 16.929-second walltime is not the quota debit. Current Space code uses `xlarge` at 2× quota and a 60-second reservation floor. For this proposed 896×512 length mix, its formula gives reservations of **140–222 weighted seconds with the fast/VAE decoder**, or **164–246 with the diffusion decoder**.

With 2,400 daily weighted seconds and the conservative fast-decoder reservation of 222, a *hypothetical constant* debit of 48 / 75 / 100 / 150 seconds would admit 46 / 30 / 22 / 15 attempts daily: **1,380 / 900 / 660 / 450 across thirty complete daily cycles**. Thus one month could cover 660 attempts only in some scenarios. The actual longer-job debits, model fit, thirty usable daily cycles and keeper rate have not been measured; a debit observed for a five-second take cannot be transferred unchanged to ten-second footage. The quota resets 24 hours after first use, not into an accumulating monthly bank. No overage, renewal or second month is assumed. [HF pricing](https://huggingface.co/pricing), [ZeroGPU quota/billing](https://huggingface.co/docs/hub/spaces-zerogpu), [official Space source](https://huggingface.co/spaces/Lightricks/LTX-2.5/blob/main/app.py).

Earlier 6 November plan research also considered Pika ($10/month, 600 credits; 60 five-second H3 Flex attempts), PixVerse ($10/month, 1,200 cycle + 60 daily credits), Luma (commercial Plus $29.99; $9.99 Lite is noncommercial/watermarked), Hailuo and Wan APIs. None supplied a verified, capability-matched 600–660-attempt allowance at this budget and acceptance standard. Pika's quoted monthly allocation is one tenth of the base attempt count; PixVerse needs exact model/duration quotes and daily scheduling before capacity can be inferred. The cheap fal Wan2.2 Turbo endpoint advertised removal on 4 January 2027, so it is not our repeatable foundation. Runpod's checked main-page 4090 price was $0.89/h plus storage and a $10 initial deposit; at that rate it provides less compute per euro than the required Vast envelope. These are dated comparisons, not new account quotes. [Pika](https://pika.art/pricing) · [PixVerse](https://app.pixverse.ai/subscribe) · [Luma licensing/plans](https://lumalabs.ai/learning-hub/payments-subscriptions) · [Wan endpoint](https://fal.ai/models/fal-ai/wan/v2.2-a14b/image-to-video/turbo) · [Runpod pricing](https://www.runpod.io/pricing).

## Sustainable completion, with the same quality requirement

There is no extra watermark-removal purchase in the owned pipeline. Retain the exact checkpoint and backend terms in the [license/provenance record](../tools/kaggle-a2v/NOTICE.md); code, community-converted LTX weights and Gemma have distinct licenses. The current WanGP license allows private production/output use and requires credit for direct output sales; it is not permission to resell a hosted generation service. Do not assume another checkpoint inherits these terms.

The repeatable route is renewable free compute plus an optional **bounded** paid burst, retained source/editing code and checked footage. Its output must still be ten complete songs with the selected motion deliveries and credible editing, not ten long encodes of failed/frozen characters. The cash ceiling can be enforced; **production yield and the full finished-film result are not yet proven**. No paid-only alternative has passed both the cost and performance gate for this exact plan. Continue the current free tests and whole-film integration; activate the single conditional rental recommendation only if it earns its cost within the same €20 envelope.
