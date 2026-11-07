"""CPU-only FFmpeg conditioning probes; never edits master, manifests or jobs.

Outputs are filtered mixes, NOT isolated vocals. All audio is scratch material
under root build/c-audio-conditioning. NumPy inspects/aligns PCM sample ranges
and computes measurements; FFmpeg applies filters, gain and final encoding.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import wave
import numpy as np

ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent
BUILD = ROOT / "build/c-audio-conditioning"
MASTER = ROOT / "productions/join-me-in-life/full-song/track-49.mp3"
MASTER_SHA = "0fe0f566e985a0b028e12543679d3b142ee7b1b62425fcb595799b35ba116cbb"
SR = 48000
EXCERPTS = {
    "C29": (9966000, 10160000, "4e5bb99f8afebb215b9af5a4a990d4dc7831ef4a86bf05b2b812e8f17c694a15"),
    "C30": (10128000, 10386000, "8e29c9bcbbc8bf91d86413a6c150be243760d799b7ebf48df223d98ba2c2af73"),
}
FILTERS = {
    "mono_baseline": "pan=mono|c0=0.5*c0+0.5*c1",
    "band_emphasis": "pan=mono|c0=0.5*c0+0.5*c1,highpass=f=140:p=2,lowpass=f=6500:p=2",
    "spectral_center_band": "dialoguenhance=original=1:enhance=0,pan=mono|c0=FC,highpass=f=140:p=2,lowpass=f=6500:p=2",
}


def ffmpeg(args, data=None):
    return subprocess.run(["ffmpeg", "-v", "error", "-y", *args], input=data,
                          stdout=subprocess.PIPE, check=True).stdout


def filter_float(stereo, expression):
    raw = ffmpeg(["-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "pipe:0",
                  "-af", expression, "-f", "f32le", "-c:a", "pcm_f32le", "pipe:1"],
                 stereo.astype("<f4").tobytes())
    return np.frombuffer(raw, dtype="<f4").copy()


def rms(x):
    return float(np.sqrt(np.mean(np.square(x.astype(np.float64)))))


def db(x):
    return float(20 * np.log10(max(float(x), 1e-15)))


def band_powers(x):
    spectrum = np.abs(np.fft.rfft(x.astype(np.float64))) ** 2
    freqs = np.fft.rfftfreq(len(x), 1 / SR)
    total = spectrum.sum()
    bands = [(0, 140), (140, 700), (700, 5000), (5000, 6500), (6500, 24001)]
    return {f"{lo}_{hi}_Hz": float(spectrum[(freqs >= lo) & (freqs < hi)].sum() / total)
            for lo, hi in bands}


def correlation_and_lag(a, b):
    a, b = a.astype(np.float64), b.astype(np.float64)
    a -= a.mean(); b -= b.mean()
    length = 1 << (2 * len(a) - 1).bit_length()
    corr = np.fft.irfft(np.fft.rfft(b, length) * np.conj(np.fft.rfft(a, length)), length)
    lag = np.arange(-4800, 4801)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    values = corr[lag % length] / norm
    best = int(np.argmax(values))
    return {"peak_correlation": float(values[best]), "lag_samples": int(lag[best]),
            "lag_seconds": float(lag[best] / SR), "zero_lag_correlation": float(corr[0] / norm)}


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    assert hashlib.sha256(MASTER.read_bytes()).hexdigest() == MASTER_SHA
    impulse = np.zeros((SR, 2), np.float32); impulse[SR // 2] = 0.5
    impulse_out = filter_float(impulse, "dialoguenhance=original=1:enhance=0,pan=mono|c0=FC")
    delay = int(np.argmax(np.abs(impulse_out))) - SR // 2
    assert delay == 1536, "Re-evaluate latency for this FFmpeg version before deriving clips"
    report = {
        "scope": "Conditioning-only CPU tests. Filtered mix, not isolated vocals; no perceptual or LTX-quality pass.",
        "master_sha256": MASTER_SHA,
        "ffmpeg_version": subprocess.check_output(["ffmpeg", "-version"], text=True).splitlines()[0],
        "spectral_center_impulse_delay_samples": delay,
        "spectral_center_impulse_delay_seconds": delay / SR,
        "filter_expressions": FILTERS,
        "amplitude_policy": "Match each candidate to baseline mono RMS where peak <=0.95; otherwise cap at0.95. Report actual difference.",
        "processing_context_samples_each_side": SR,
        "outputs_are_two_identical_channels": True,
        "shots": {},
    }
    for shot, (start, end, expected_pcm_hash) in EXCERPTS.items():
        raw = ffmpeg(["-i", str(MASTER), "-af", f"atrim=start_sample={start-SR}:end_sample={end+SR},asetpts=PTS-STARTPTS",
                      "-ac", "2", "-ar", str(SR), "-f", "s16le", "-c:a", "pcm_s16le", "pipe:1"])
        stereo_i16 = np.frombuffer(raw, dtype="<i2").reshape(-1, 2)
        n = end - start
        original_i16 = stereo_i16[SR:SR+n]
        assert hashlib.sha256(original_i16.tobytes()).hexdigest() == expected_pcm_hash
        stereo = stereo_i16.astype(np.float32) / 32768
        original = stereo[SR:SR+n]
        mono = original.mean(axis=1)
        side = (original[:, 0] - original[:, 1]) / 2
        entry = {"start_sample": start, "end_sample_exclusive": end, "start_seconds": start/SR,
                 "samples": n, "duration_seconds": n/SR, "original_pcm_sha256": expected_pcm_hash,
                 "stereo_lr_correlation": float(np.corrcoef(original.T)[0, 1]),
                 "mid_rms_dbfs": db(rms(mono)), "side_rms_dbfs": db(rms(side)),
                 "side_to_mid_db": db(rms(side) / rms(mono)),
                 "baseline_band_power_fraction": band_powers(mono), "variants": {}}
        for variant, expression in FILTERS.items():
            result = filter_float(stereo, expression)
            compensation = delay if variant == "spectral_center_band" else 0
            result = result[SR+compensation:SR+compensation+n]
            assert len(result) == n and np.isfinite(result).all()
            if variant == "mono_baseline":
                assert np.array_equal(result, mono)
                entry["plain_pan_equals_existing_model_mono_exactly"] = True
                continue
            wanted_gain = rms(mono) / rms(result)
            gain = min(wanted_gain, 0.95 / float(np.max(np.abs(result))))
            path = BUILD / f"{shot}-{variant}-FILTERED-MIX-NOT-VOCALS.wav"
            # FFmpeg alone writes the audio derivative; duplicated channels fit
            # the current input shape without creating artificial stereo width.
            ffmpeg(["-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "pipe:0",
                    "-af", f"volume={gain:.17g},pan=stereo|c0=c0|c1=c0", "-c:a", "pcm_s16le", str(path)],
                   result.astype("<f4").tobytes())
            with wave.open(str(path)) as wav:
                encoded = np.frombuffer(wav.readframes(wav.getnframes()), "<i2").reshape(-1, 2)
                assert wav.getnframes() == n and wav.getframerate() == SR and wav.getnchannels() == 2
            assert np.array_equal(encoded[:, 0], encoded[:, 1])
            sample = encoded[:, 0].astype(np.float32) / 32768
            entry["variants"][variant] = {
                "path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "samples": n, "sample_rate": SR, "channels": 2, "sample_width_bytes": 2,
                "delay_compensation_samples": compensation, "gain_db": db(gain), "gain_linear": gain,
                "final_ffmpeg_filter": f"volume={gain:.17g},pan=stereo|c0=c0|c1=c0",
                "rms_dbfs": db(rms(sample)), "rms_difference_from_baseline_db": db(rms(sample)/rms(mono)),
                "peak_dbfs": db(np.max(np.abs(sample))), "clipped_samples": int(np.sum(np.abs(encoded[:, 0].astype(np.int32)) >= 32767)),
                "timing_correlation": correlation_and_lag(mono.copy(), sample.copy()),
                "band_power_fraction": band_powers(sample),
                "warning": "Filtered mix only: centered instruments, backing vocals and reverb can remain; singing intelligibility and generation improvement unverified.",
            }
        report["shots"][shot] = entry
    assert hashlib.sha256(MASTER.read_bytes()).hexdigest() == MASTER_SHA
    report["original_master_unchanged"] = True
    (HERE / "measurements.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
