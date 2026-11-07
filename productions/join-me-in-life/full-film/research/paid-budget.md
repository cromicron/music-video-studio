# Paid version: ten complete films within €20

**Latest measured result, 7 November:** the supplied-song LTX2.3 test now completes on free dual T4s: 4.041667 seconds of picture took 255.161 seconds of generation and 774.901 seconds including cold setup. The original audio is preserved; independent motion review is pending. The earlier memory failure is fixed. The 13B hospital test produced only a 2.033-second visually usable aftermath interval, and its full action and the summer test were rejected. These observations still do not establish a reliable production acceptance yield. No new cash or purchased credits spent. [Actual A2V result](../assets/motion/ltx23-a2v-bridge-pilot/render.json).

**7 November execution update:** The owned Kaggle 13B route now ran on actual dual T4s: a 4.033-second take required 146.681 seconds of generation and 815.988 seconds including cold setup/download/loading; displayed quota moved 30.00→29.76 h. The take was rejected after detailed visual review, so accepted-seconds-per-hour is still zero. This proves runtime access, not a sustainable quality yield or ten-film budget. [Provenance](../assets/motion/ltx13b-bridge-pilot/render.json) · [review](../review/ltx13b-bridge-pilot-review.md). The dated research below retains its original assumptions.

Research checked 6 November 2026. This is a recommendation and a reproducible budget, not a paid render or an assertion that generation quality has passed. No purchase, subscription, account change, or paid generation was made by this research task. Numeric assumptions and the read-only GPU marketplace snapshot are in [budget.json](budget.json).

**Latest access research:** before purchasing anything, benchmark the **private Kaggle T4×2 route** documented in [free-gpu.md](free-gpu.md), and inspect any Colab compute already included in the user's paid Google AI plan. Kaggle publishes 30 renewable GPU session hours per week. A reviewed 13B creator workflow reports 4–6 minutes per 10-second source clip; at three takes and eight retained seconds per keeper, ten films would need approximately 70–105 session hours before setup and extra rejections. Account access and runtime are now verified above; reliable movement quality and production acceptance yield remain unproven. This is a stronger sustained free-production candidate than buying a small daily quota solely because an existing connector is available.

**Paid hosted candidate after the live free-capability and quota tests:** benchmark the already working **LTX-2.5 Hugging Face Space**, then consider **one $9 month of Hugging Face PRO** for a hybrid with substantial generated footage if the free GPU route is unsuitable. A first free generation completed in 16.93 seconds, but its acting failed the intended direction. The next attempt was refused because it required 150 quota seconds and only 72 remained. This defeats the earlier projection from walltime alone. At an illustrative 48-second debit per attempt, one month supports about **1,410 attempts**, short of the **2,100** allowed by the three-take full-coverage budget. Ten finished generative films within €20 remain a target to prove, not an achieved result.

**Predictable paid fallback:** retain the complete locally animated film and buy selected action shots with **Hedra / Seedance 1.5 Pro, 480p, audio off**. Reserve at most **$13 before tax for the entire ten-film batch**, with an absolute checkout-and-usage cap of **€20 including taxes and fees**. The latest read-only estimate prices the planned batch at **$12.85767**, approximately **€15.76 under the conservative calculation below**. The estimate has no source-image upload yet; the complete image-to-video payload must be estimated again before spending. It provides **24 seconds of newly generated action per complete 4:38 film**, assuming the planned acceptance rate. The remaining **253.776 seconds per film are local animation**. It must be described as a hybrid, not as 4:38 of new AI-generated character animation. This fallback and HF PRO are alternatives; buying both at their full allocations exceeds the budget.

Our own LTX workflow on rented GPUs is a second full-coverage candidate, conditional on a measured speed and quality test. None of the verified per-output commercial APIs can provide ten fully generated 4:38 films within €20 at their ordinary rates, even at one take per shot. Shared GPU subscription quotas are a different economic model and must be measured separately. Repeatedly looping or slowing a few clips does not solve the quality requirement.

## Hugging Face PRO: a tested access route, an unproven production yield

The capability investigation successfully generated a **5.04-second, 896×512, 24fps LTX-2.5 clip** from this project's waiting-room art without a paid account. The saved sample is `free-test/LTX25_waitingroom_free_5s.mp4`. Submission-to-completion file times span **16.929 seconds**. The endpoint and client are retained in `free-test/`. That proves access and a real output. It does not prove correct performance: the requested withdrawn gaze was not maintained.

[HF PRO costs $9/month](https://huggingface.co/pricing). [Official ZeroGPU documentation](https://huggingface.co/docs/hub/spaces-zerogpu) lists 40 minutes of daily PRO quota; the Space uses `xlarge`, which consumes quota at 2×. Quota resets 24 hours after first usage. Overage consumes prepaid credits at $1/10 quota minutes. Avoid overage; do not count included inference-credit dollars twice. The [official Space source](https://huggingface.co/spaces/Lightricks/LTX-2.5/blob/main/app.py) reserves an estimated 75 GPU seconds for the tested settings, giving a **150-second weighted admission requirement**.

The next five-second request returned: **“150s requested vs. 72s left”**, with reset in **23:55:36**. Its raw response is saved in [her_window_take1/events.txt](../assets/motion/her_window_take1/events.txt). The initial quota was not measured. If the documented anonymous starting allowance of 120 seconds applied and no other debit occurred, the first attempt consumed **48 weighted seconds**; that is an inference, not an observed before/after charge. Admission of the first 150-second reservation despite the documented 120-second allowance is unresolved. The 16.929-second walltime must not be substituted for quota consumption.

Even the smallest supported request has a 60-second GPU reservation floor, weighted to **120 quota seconds** on `xlarge`. Therefore the observed 72-second remainder cannot admit another job. No attempt was made to bypass that quota. Future account access must use the provider's ordinary authenticated allowance.

For a daily allowance `Q`, admission reservation `R` and measured constant debit `d`, maximum admitted jobs are `floor((Q - R) / d) + 1` when `Q >= R`. With PRO, `Q = 2,400` and this shot's `R = 150`. A 30-day planning cycle then gives:

| Weighted debit per attempt | Jobs per daily cycle | Jobs in 30 cycles | Retained seconds per film at 3 takes and 4s per keeper |
| --- | ---: | ---: | ---: |
| 48s — inference from the documented anonymous allowance | 47 | 1,410 | 188 |
| 75s — sensitivity case, not a measurement | 31 | 930 | 124 |
| 100s — sensitivity case, not a measurement | 23 | 690 | 92 |

The 48-second case leaves **144 quota seconds unusable for another 150-second reservation each day**. It covers only about 68% of each film at the assumed acceptance rate; the rest needs local animation. To fit all **2,100 attempts in 30 cycles** requires 70 jobs daily, which means at most **32.61 weighted quota seconds per attempt** after allowing for admission. This supersedes the earlier 17.14-GPU-second calculation that omitted the admission buffer.

At a **two-take** rather than three-take yield, 1,410 attempts could supply 705 four-second keepers, just above the 700 rounded keepers needed for ten films. That would leave only ten attempts beyond the 1,400 base allocation. The first acting test failed, so neither that yield nor an appropriate mix of two- and three-take shots has been demonstrated. With the 48-second scenario and three-take yield, the batch needs approximately **45 daily cycles**. Two subscription months could supply the quota, but the cash cap still governs their actual invoices.

The cost at dollar/euro parity, 19% assumed VAT and 3% conversion allowance is **€11.03 for one month**. The [ECB reference for 6 November is $1.1165 per euro](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.ff.html); at that reference the same estimate is €9.88. Two $9 months would be approximately **€19.76**, leaving only **€0.24** under the cap and no meaningful protection against the second month's exchange rate or fee changes. At parity they would cost €22.06. Do not promise or authorize two months from the current estimate. Consider one month after the pilot, with any renewal contingent on actual cumulative invoices remaining below **€20 all-in**. HF states that fees exclude applicable taxes. [Billing](https://huggingface.co/docs/hub/billing), [terms](https://huggingface.co/terms-of-service).

A credible pilot should record actual account quota before/after, generation seconds, retries and retained seconds across several representative actions. An independent visual pass must reject unwanted movement even when the model outputs a valid file. Preserve the [LTX-2.5 model license](https://huggingface.co/Lightricks/LTX-2.5) and use our own saved client/editor; a hosted demo can change or disappear. PRO is a renewable subscription, not guaranteed dedicated compute or unlimited generation. A failed or unavailable public Space requires our retained local workflow or the priced hybrid fallback.

## What the budget actually buys

Ten films of 277.776 seconds require **2,777.76 final seconds (46.296 minutes)**. The ceiling is €2 per finished film, or approximately **€0.00720 per final second**, inclusive of everything newly purchased. Existing ChatGPT/Claude subscriptions, existing artwork, local CPU rendering and existing source footage are treated as sunk costs, as Dario requested. Future paid API usage is not free merely because a wallet already holds purchased credits.

The supplied Runway connection reported **1,897 purchased credits and zero plan credits**. That is finite prepaid inventory, not renewable free capacity. This research does not authorize spending it or count it as a sustainable zero-cost allowance.

The proposed paid hybrid is deliberately specific:

| Item | Ten-film allocation |
| --- | ---: |
| Accepted new action shots | 60: six per film |
| Accepted length per shot | 4 seconds |
| Generated length per attempt | 5 seconds, leaving 1 second for handles/trimming |
| Attempts allocated per accepted shot | 3 |
| Additional shared retry reserve | 30 attempts |
| Maximum attempts / generated seconds | 210 / 1,050 seconds |
| Published rounded Seedance 1.5 Pro 480p silent rate | $0.0122 per generated second |
| Read-only account quote for one 5s attempt | **$0.061227** |
| Estimated 210-attempt model cost at that quote | **$12.85767** |
| New generative action in each finished film | 24 seconds, 8.64% of its running time |

Hedra's current catalog identifies the low price with **Seedance 1.5 Pro at 480p with sound disabled**. It accepts a start frame and an optional end frame. Its newer Seedance models, higher resolutions, and native sound have different prices. The song supplies the final soundtrack, so no generated audio is needed. Price the exact payload with the provider's estimate operation before submission. [Hedra catalog](https://www.hedra.com/models/video), [configuration-specific pricing and input comparison](https://www.hedra.com/blog/video-model-api-cost-comparison).

The [saved read-only estimate](hedra-seedance-15-estimate.json) was obtained from the actual account catalog with `seedance-15-pro`, 5 seconds, 480p, 16:9 and `generate_audio: false`. It returns **$0.061227 per attempt**, slightly above the rounded public rate. It omitted the source image; no image upload or generation was performed, so re-estimate the complete payload before any purchase or generation.

The conversion is a **budget stress assumption, not an exchange-rate quote**: $12.85767 × €1 per dollar × 1.19 assumed VAT × 1.03 card/conversion allowance = **€15.7596**. This leaves **€4.2404** below the hard ceiling. If the actual billing country, exchange rate, tax, minimum deposit or price differs, the real checkout total and remaining usage allowance govern. Do not commit more than €20. A nominal €20 net allowance is insufficient because tax can be added afterward.

At three attempts per keeper, generation quality is still uncertain. Test representative actions first: a head turn, a restrained seated reaction and an outdoor memory action. Reject face changes, sliding feet, impossible hands, unwanted body sway and extra gestures. Count rejected takes in the budget. If no satisfactory shot survives the reserved attempts, keep the local scene and report the failed upgrade; do not silently spend more or call a bad clip approved.

This method is renewable at the current public price, has no trial-credit dependency, and retains editing and composition in our own source. API wallet funds are separate from Hedra Studio credits. The published API pricing describes prepaid billing without a subscription or minimum; account access and the actual commercial-use terms still need to be confirmed for the chosen route. [Hedra API pricing](https://www.hedra.com/pricing), [developer onboarding and wallet distinction](https://www.hedra.com/develop).

## Market comparison

Rates are USD unless stated otherwise. These are distinct products; website subscriptions and API wallets must not be mixed. “All generated” costs below are deliberately optimistic lower bounds: no tax, retries, editing handles, image costs or minimum clip rounding.

| Tool / route | Verified current terms | Budget conclusion |
| --- | --- | --- |
| **Hedra / Seedance 1.5 Pro** | $0.0122/s published at 480p silent; actual 5s estimate $0.061227. Full 10-film running time alone extrapolates to **$34.01** before clip rounding. | Best verified managed option for selected action shots. Full generative coverage fails before retries. [Catalog](https://www.hedra.com/models/video). |
| **LTX API** | LTX-2.3 Fast image-to-video at 720p is **$0.03/s**; 1080p $0.06/s. Current LTX-2.5 Fast 720p is $0.09/s. | 2.3 Fast costs **$83.33** for the complete running time before retries. Useful alternative for a few 720p shots, not ten fully generated films. [Official pricing](https://docs.ltx.io/pricing). |
| **Runway API** | Gen-4 Turbo **5 credits/s = $0.05/s**. | **$138.89** for full running time before retries. Existing 1,897 credits are purchased inventory. [API pricing](https://dev.runwayml.com/pricing). |
| **Runway website** | Standard $15 monthly / $12 monthly equivalent billed annually; 625 monthly credits. Free allocation is **125 one-time credits**. | Annual sticker price hides a commitment beyond €20; one monthly allocation is far too small. Pricing page contains inconsistent Turbo duration examples, so use the exact generation quote. [Plans](https://runway.com/pricing), [Gen-4 Turbo cost](https://help.runwayml.com/hc/en-us/articles/37327109429011-Creating-with-Gen-4-Video). |
| **Pika** | Starter **$10 monthly**, **600 credits**, commercial license, no watermark. H3 Flex 768p/5s is **10 credits**. Free now has **zero monthly credits**, credit packs only. Minimum advertised pack $25. | One month buys 300 raw seconds. With three takes and trimming 5s to 4s, this is **80 accepted seconds across ten films**, or 8s each. Credible hybrid alternative. The H3 app page still says 900 Starter credits; use the lower 600 from the actual pricing table. [Plans and model costs](https://pika.art/pricing), [H3 Flex settings](https://creation.pika.art/apps/pika-h3-flex). |
| **PixVerse website** | Standard **$10 monthly**, 1,200 cycle credits plus **60 daily credits**, up to 720p, no watermark; annual option is $96 upfront. Basic lists 30 daily credits, up to 540p. | Worth testing renewable daily credit access. A 30-day Standard cycle can offer up to 3,000 credits only if daily allowances are used when available. Model-specific quotes, commercial-use terms and scheduling determine useful output; no promise of ten films. [Live subscription page](https://app.pixverse.ai/subscribe), [official dated summary](https://pixverse.ai/en/ai-info-page). |
| **Kling via fal** | Kling 2.5 Turbo Pro is **$0.35/5s**, then $0.07/additional second; commercial-use label. Direct Kling web pricing could not be reliably retrieved due robots restrictions. | Verified API route costs **$194.44** for full running time before retries. Do not extrapolate third-party daily-credit claims into a current allowance. [Endpoint pricing](https://fal.ai/models/fal-ai/kling-video/v2.5-turbo/pro/image-to-video). |
| **Luma Dream Machine** | Lite $9.99 monthly, watermarks, noncommercial use; Plus $29.99 monthly with commercial use and no watermark. API is separate. | Lite cannot supply a band release on its stated license; Plus exceeds the total cap before generation. [Official plan guide](https://lumalabs.ai/learning-hub/payments-subscriptions), [licensing](https://lumalabs.ai/learning-hub/licensing). |
| **MiniMax Hailuo / H3** | Hailuo advertises Standard $9.99; some trials are launch promotions. Hedra catalog lists Hailuo 2.3 from $0.19/6s, H3 Max Turbo from $0.025/s. | Even the latter is **$69.44** for the full running time before retries. Promotions are useful for this film if actually available, not a recurring ten-film cost model. [Hailuo plan overview](https://hailuoai.video/pages/blog/paid-vs-free-ai-video-generators), [launch-trial limits](https://hailuoai.video/pages/blog/introducing-hailuo-2-3-ai-video-generator), [current Hedra catalog](https://www.hedra.com/models/video). |
| **Wan 2.2 Turbo via fal** | **$0.05/480p clip**, $0.075/580p, $0.10/720p. Page explicitly announces removal **4 January 2027**. | Cheap for a short-term experiment, unsuitable as the sustainable foundation. Do not confuse flat per-clip billing here with per-second billing elsewhere. [Live endpoint](https://fal.ai/models/fal-ai/wan/v2.2-a14b/image-to-video/turbo). |
| **LTX Video 0.9.7 via fal** | Live image-to-video page says **$0.04/s at 24fps**, doubled with the detail pass. A separate multiconditioning page/search result says $0.04 per video. | Those endpoints/claims are not interchangeable. Budget against the specific endpoint's current quote; do not promise 25 finished clips per dollar for I2V. [I2V pricing](https://fal.ai/models/fal-ai/ltx-video-13b-distilled/image-to-video). |
| **Haiper** | Old official FAQ still discusses unlimited membership. Current homepage returned no readable app or pricing; pricing route failed. | No currently verified purchasable offering. Reject old “free/unlimited” advice. [Current homepage](https://haiper.ai/), [old FAQ](https://book.haiper.ai/haiper-video-generator/faq). |

Fal's current documentation says the minimum top-up is $1, credits expire after 365 days, and quoted prices exclude taxes. The service bills successful outputs: a technically successful but unusable hand movement still consumes money. [Minimum and billing](https://fal.ai/learn/tools/how-to-generate-ai-videos-with-an-api), [terms](https://fal.ai/legal/terms-of-service), [billing units](https://fal.ai/docs/documentation/model-apis/pricing).

## The route that could support fully generated films

**Own ComfyUI/LTX pipeline plus a rented GPU**, with local editing and encoding. This is closer to Dario's goal of a reusable studio than paying each time for an opaque app. The weights and workflows can be pinned and retained. However, cheaper open models are not automatically better performers for this anime style, and the actual yield matters more than headline seconds per generation.

The official LTX repository provides distilled 2B and 13B workflows, including low-memory variants. Its low-memory speed claim describes 720×480×121-frame generation in under a minute on an RTX 4060, not a measured result on this production. Model weights have their own license; do not assume the repository code's Apache license covers every checkpoint. [Official LTX repository](https://github.com/Lightricks/LTX-Video), [model card and checkpoint variants](https://huggingface.co/Lightricks/LTX-Video), [LTX-2.3 model/license](https://huggingface.co/Lightricks/LTX-2.3).

I tested the **read-only** Vast search-offers API successfully. The first query found RTX 4090 offers around $0.376–0.388/hour with approximately 99.7–99.9% reported reliability, plus separately priced storage and transfer. A later filtered query changed the available offers; its exact response is in `budget.json`. These are transient offers, not reserved capacity. Some cheaper offers had poor reliability or high bandwidth/storage charges. No instance was started. [Official pricing and supported search API](https://docs.vast.ai/guides/instances/pricing).

An explicit full-coverage feasibility test is:

| Assumption / pass requirement | Value |
| --- | ---: |
| Source clip / retained keeper | 5 seconds / 4 seconds |
| Keeper clips per film | ceil(277.776 / 4) = 70 |
| Attempts per keeper | 3 |
| Attempts across ten films | 2,100 |
| Maximum compute quote | $0.40/hour |
| Storage allowance | $0.02/hour |
| Setup/download allowance | 1.5 GPU hours |
| Bandwidth / other contingency | $1 / $1 |
| Total net envelope | $15 |
| Resulting maximum mean time per attempted generation | **50.49 seconds** |
| Gross stress estimate | $15 × 1.19 × 1.03 = **€18.3855** at parity |

The outside judge is the ledger plus accepted footage: a representative pilot must demonstrate both this average run time and at least one usable four-second shot per three attempts, including failure cases. Ten handpicked easy camera pushes cannot validate character acting. Use seated acting, hands, a head turn, summer movement and the bridge performer. If the test misses either threshold, **full generative coverage is not established within budget**. Keep a hybrid or revise the method; do not present extrapolated quality as a measured success.

The present workspace has five CPU cores and no detected NVIDIA GPU, so this runtime/yield benchmark was not possible without renting hardware. GPU rental needs authorization and a real quote. Vast requires prepayment, charges stopped-instance storage, and may charge a saved card for negative balances; a prepaid balance is not itself a hard spending cap. A runner must download verified outputs, destroy its instance/volumes at the stop threshold, and verify no resources remain billable. [Billing details](https://docs.vast.ai/guides/reference/billing).

Runpod is an alternative if a deployment quote fits: its main pricing page, updated 4 November, displayed RTX 4090 at **$0.89/hour** while the older product page still advertised a **$0.34 starting rate**. Those cannot be treated as a guaranteed available rate. It describes a $10 entry deposit, per-second billing, additional storage and no data-transfer fees. At $0.89/hour the budget allows far less rendering time. [Current pricing](https://www.runpod.io/pricing), [billing and minimum deposit](https://docs.runpod.io/accounts-billing/billing), [storage](https://docs.runpod.io/pods/pricing).

## What is established and what remains

- Established: primary-source pricing comparison, current credit-class distinction, arithmetic with retries/handles/tax allowance, a working read-only GPU offer query, and an actual quota rejection after the first free LTX clip.
- Recommended first paid candidate: one $9 month of HF PRO for the working LTX-2.5 route, after a representative quota/yield pilot. The 48-second debit scenario supports about 188 generated seconds per film with three takes, not complete coverage. Full coverage would require better measured yield, more quota cycles, or our own GPU workflow within the same hard cash cap.
- Priced alternative: the €20-capped **hybrid** using six short Seedance action shots per film, subject to an exact price estimate and a quality pilot. These are alternatives, not a combined purchase recommendation.
- Alternative for a long-term fully generated studio: our own LTX workflow on rented GPU, only after the measured pilot meets the cost/yield gate.
- Not established: acceptable motion on this project's actual images, 1080p source detail from 480p generations, usable free-credit balances outside the observed connection, a paid render, a completed second generated version, or full coverage under €20.

No annual subscription, promotion that expires, watermark removal, new-account cycling, indefinite daily-credit accumulation, or duplicated/slow-motion footage is counted as proof that ten complete generative videos fit the budget.
