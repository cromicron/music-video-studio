# Audio conditioning: tested fallback, not vocal isolation

**Keep the current C29 source/prompt repair first.** If it still needs a separately controlled audio-conditioning trial, the selected fallback hypothesis is a mild FFmpeg band emphasis: existing mono mean, 140Hz high-pass and 6.5kHz low-pass. No GPU trial was run. These CPU measurements do **not** establish clearer vocals, phoneme accuracy or improved generated performance; they cannot solve C30’s invented-person continuity defect by themselves.

## Original stem and access search

No exact take49 vocal stem was found in the current production files, reachable Git audio-object history, handoffs, access records or directly inventoried band Drive folder. Its Suno-uploads subfolder has two other-song guides; no take49 vocal export. The handbook discusses generic historical stem capability/failures, not an existing exact stem. [Discovery record](source-discovery.json) bounds this search; missing private chats/accounts remain unknown.

The retained original **Suno/Ace Data audio ID is `9e161437-55d3-49c5-b99f-646f6d351352`**, corroborated by the [full-song record](../../../../full-song/README.md) and current band handbook. The known recording is the [original Drive master](https://drive.google.com/file/d/1qpYn0sshheJ6KKjLbJUkvrsoDx1M0vfZ/view). No verified original Suno play URL or existing stem URL was supplied by those records. No Suno/Ace Data connector is active; metadata from three saved browser profiles showed no signed-in Suno/Ace Data site. This does not prove no other session exists. No account login, subscription or separation request was made. An already-existing exact original vocal stem would take precedence if real access later provides it.

## What the existing input and tests establish

The actual retrieved wrapper already uses `samples.mean(axis=1)` before LTX encoding. FFmpeg `pan=mono|c0=0.5*c0+0.5*c1` produces **exactly the same float samples** for both test excerpts; plain center-pan is not a new conditioning treatment.

Two transparent FFmpeg recipes were tested, with 1s real master context on each side, original sample ranges retained, no stretch or padding, and final RMS matched to the baseline mono mix:

```text
band_emphasis:
  pan=mono|c0=0.5*c0+0.5*c1,highpass=f=140:p=2,lowpass=f=6500:p=2
spectral_center_band:
  dialoguenhance=original=1:enhance=0,pan=mono|c0=FC,
  highpass=f=140:p=2,lowpass=f=6500:p=2
```

| Exact conditioning excerpt | Samples / 48kHz | Original energy below 140Hz | Band emphasis | Spectral-center +band |
|---|---:|---:|---:|---:|
| C29, master 207.625000–211.666667s | 194000 | 28.15% | 6.51% | 6.88% |
| C30, master 211.000000–216.375000s | 258000 | 33.98% | 8.86% | 11.18% |

These are **frequency-band energy fractions, not vocal-to-instrument ratios**. Bass reduction is technically established. Guitars, drums, backing voices and reverb overlapping the retained band remain; vocal body can also be reduced. L/R correlation is 0.645/0.626, so stereo information exists, but it is not a labelled vocal source. Spectral-center processing is not selected: it adds an alignment hazard and a more complex change without evidence of better perceptual intelligibility here.

A synthetic identical-channel impulse measured **1,536 samples / 32ms delay** from `dialoguenhance` at 48kHz. The tested spectral candidate compensates it by selecting output samples beginning one context second plus 1,536 samples later; post-context supplies the real tail. No inserted silence or stretch is used. After compensation, both recipes’ peak waveform-correlation lag is 1 sample/20.8µs against the mono original; frequency-dependent IIR phase still differs. Correlation does not certify vocal clarity or lip sync. The selected band-only recipe has no 32ms spectral delay.

All four diagnostic WAVs decode, contain exactly 194,000/258,000 stereo PCM16 samples at 48kHz, have identical L/R conditioning channels and no clipped samples. RMS matching is within 0.000003dB; measured peaks remain below −2.5dBFS. Each filename ends `FILTERED-MIX-NOT-VOCALS.wav`. [Measurements](measurements.json) records complete filter expressions, exact gain, timing compensation, hashes, spectrum fractions and source PCM checks; [decode checks](decode-checks.json) separately verify output transport. No subjective hearing or model-quality pass is claimed.

## Reproduce and preserve the original song

Run from repository root:

```sh
python3 productions/join-me-in-life/full-film/unfinished-morning/research/audio-conditioning/reproduce.py
```

The [script](reproduce.py) uses existing FFmpeg for filtering/gain/encoding and NumPy for PCM checks, range selection and measurements. It writes only to this research directory and ignored `build/c-audio-conditioning/`; it adds no neural separator or fourth creative service. Two band-emphasis candidates and two deliberately unselected spectral comparisons are retained there, with exact paths/hashes in the measurements. The untouched master SHA256 remains `0fe0f566e985a0b028e12543679d3b142ee7b1b62425fcb595799b35ba116cbb` before and after.

**A later trial must separate conditioning audio from review/final audio.** Current wrapper lines 146–158 load and remux the same `manifest['audio']`; dropping a filtered file into that field would also replace what its review falsely calls original stereo PCM. Do not overwrite the existing conditioning input or relabel that result. A future bounded integration needs separate filtered-conditioning and original-review inputs, with independent hashes and a check that final/review PCM is still the original take49 excerpt. This task makes no such integration or model run. Current B remains unchanged. [Primary sources and wrapper evidence](sources.json) retain the vendor’s vocal-isolation/closed-mouth guidance and the exact FFmpeg implementation used.
