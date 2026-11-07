# Music timing for the new storyboard

Prepared 7 November 2026 from the actual original recording, its existing two ASR passes, and the earlier reviewed Short cues. [Machine-readable cue map](../story/music-cues.json). This is an editorial timing analysis, **not subjective listening, phoneme alignment or a completed audiovisual review**.

## What is reliable enough to plan

The unmodified [take 49](../../../full-song/track-49.mp3) is 277.776 seconds; fresh mono decoding at22,050Hz gives6,124,961samples /277.776009 seconds (sample rounding). Its SHA-256 remains `0fe0f566e985a0b028e12543679d3b142ee7b1b62425fcb595799b35ba116cbb`. The complete picture needs6,667frames at24fps /277.791667seconds. No audio was cut, transformed for delivery or replaced.

The14 existing Short lyric cues at100.373–159.173seconds remain the strongest reviewed phrase anchors. They were transferred through a waveform-derived offset; this pass does not replace them. Most other positions come from related `base.en` and `small.en` ASR passes: their agreement is useful for planning but is not an independent listening verdict. The [final lyric sheet](../../../full-song/lyrics.txt), not misrecognized ASR text, controls words.

| Passage | Usable timing / confidence | Consequence for the new picture |
| --- | --- | --- |
| Opening hook | First-word ASR disagreement12.70–15.36s; low confidence | Do not time a frozen mouth or a subtitle from these numbers. Develop a visible event through the phrase. |
| Opening musical expansion | Measured texture/accent region22.9–24.1s; a strong event at23.021s | Candidate point for the consequence of the initiating event or an active scene transition. It does not identify a specific instrument or word. |
| Verse1 / pre-chorus1 / chorus1 | Plan33.12 /50.50 /66.52s; medium, not exact bar lines | Actions can anticipate the lyrics and cross a section boundary. Chorus1 must change the situation. |
| Verse2 → chorus2 | Reviewed anchors100.373 /126.753 /142.653s; high relative to other cues | Use the exact original song to pace the memory, changed support and consequential second chorus. |
| Post-chorus2 / instrumental | Planning159.173 /171.36s; medium; last hook endpoint differs169.16–171.36s | Singing can overlap the cut. A gap in detected words is not a measured synth entrance. Reserve instrumental time for a story turn. |
| Bridge verse |191.10–191.60s ASR start; medium | The lyric-sheet label “near silence” is a direction, not measured literal silence. Keep reaction time before the pleas. |
| Four pleas | Planning207.86 /211.24 /215.94 /219.36s | All four are screamed from the first. Generate exact original-audio excerpts with handles, then choose the cut from actual action. Do not repeat one raised arm four times. |
| Final chorus / hook |223.24–223.50s /239.44–239.66s; medium | The final refrain has changed wording and should show an altered situation. Hook sustain ends244.36–245.64s in ASR, so do not freeze at one guessed endpoint. |
| Outro | First phrase around247.1s; lexical/end/repetition uncertainty remains | Its dynamics have three stages. The whole final30.6seconds needs purposeful action and consequence, not a long dawn image. |

The JSON also contains each scream's onset range, nearest24fps frame, suggested conditioning window and the cue confidence. Those windows include handles and may overlap in the original audio; retained generated picture intervals must still be chosen explicitly and not duplicated. Audio-conditioning itself does not establish perfect mouth synchronization.

## New raw-audio evidence: the ending has another turn

I freshly decoded the source with FFmpeg, measured50ms RMS and positive log spectral flux, and inspected the resulting intro, four-plea and outro plots. The samples are from the **mixed soundtrack**; percussion, voices and other instruments are not separated. Peaks are therefore musical texture/accent candidates, not authenticated vocal consonants.

The ending does not simply fade for30seconds. Per-second RMS remains around−13 to−14dBFS at247–251s, retreats through252–261s (−29.43dBFS at261s), then returns to−21.16dBFS at262s and continues with renewed activity into the270s. A strong spectral event occurs at**261.9579s**, nearest picture frame**6,287**. Final decay becomes clear around275s and reaches−46.09dBFS in the last partial second. A chosen action at the renewed event can earn the ending; this is a staging opportunity, not an instruction to make every cut follow an amplitude peak.

The opening has a clear texture expansion near23s, after the opening vocal region. The first plea's uncertain onset precedes a pronounced mixed-audio transition around208.27–209s. These measured events can help place anticipation and consequence; they do not resolve the first syllable or authorize changing the lyric.

## Reproduction and limits

Scratch outputs are `build/v2music/analyze.py`, `waveform-evidence.json`, `intro.png`, `solo_bridge.png`, `four_pleas.png`, and `outro.png`. They are diagnostic working files; the durable JSON retains source hash, method, measured peaks, final31 per-second RMS values and all editorial cues. The measurement uses:

- FFmpeg mono float32 decoding at22,050Hz, preserving the source file.
- SciPy STFT with1,024sample window and110sample hop, no boundary padding.
- Positive differences of `log1p(abs(STFT) * 1000)`, averaged across frequency bins.
- Local maxima separated by at least0.15seconds, prominence at least half the full-track flux standard deviation; top three inside each explicitly named region.
- RMS from consecutive50ms sample blocks and separately from full one-second blocks. The last partial block is counted; zero padding of the50ms plot is not evidence of earlier silence.

The original tempo autocorrelation has117.44 and78.32BPM candidates. Neither is a verified beat/bar grid. **Do not quantize the entire film to either number.** Preserve the original14 high-confidence lyric cues, use the other intervals as flexible editorial ranges, and check the actual song-paced animatic before final animation. No fresh transcription was run: another same-family ASR pass would not, on its own, convert these unresolved sung onsets into evidence of precise synchronization.
