# -*- coding: utf-8 -*-

"""Validation helpers for the Aures tonality implementation.

Every check uses synthetic signals generated here, so that the validation
needs no external data:

* reference tone (Aures 1985, p. 137): 1 kHz, 60 dB SPL gives 1 t.u.
* Fig. 5: tonality of pure tones against frequency follows Gl. (9)
* Fig. 6: tonality of narrowband noise against bandwidth follows Gl. (7)
* Fig. 7: tonality of a 1 kHz tone is independent of its level
* a tone between two FFT bins reads the same as a tone on a bin
* a 1 kHz tone in one-critical-band noise: tonality rises with the level
  of the tone over the noise
* white noise has no tonality

``compare_with_sqat`` runs the same deterministic signals as
``input/sqat_aures_results.csv``, which holds the values obtained with the
SQAT toolbox (MATLAB, GPL-3.0, Tonality_Aures1985.m at the commit named in
the file), an implementation of a different lineage.
"""

import csv
from pathlib import Path

import numpy as np

from mosqito.sq_metrics import tonality_aures
from mosqito.sq_metrics.tonality.tonality_aures.tonality_aures import _bark

HERE = Path(__file__).resolve().parent
SQAT_CSV = HERE / "input" / "sqat_aures_results.csv"

FS = 48000
DURATION = 2  # s


# ---------------------------------------------------------------- signals
def pure_tone(freq, spl, fs=FS, duration=DURATION):
    """Zero-phase sinusoid in [Pa] at the given level in [dB SPL]."""
    t = np.arange(int(round(fs * duration))) / fs
    return np.sqrt(2) * 2e-5 * 10 ** (spl / 20) * np.sin(2 * np.pi * freq * t)


def band_noise(f_low, f_high, spl, seed=0, fs=FS, duration=DURATION):
    """Gaussian noise limited to [f_low, f_high] Hz in [Pa] at the given level."""
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(int(round(fs * duration)))
    spectrum = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(x.size, 1 / fs)
    spectrum[(freqs < f_low) | (freqs > f_high)] = 0
    y = np.fft.irfft(spectrum, n=x.size)
    return y * 2e-5 * 10 ** (spl / 20) / np.sqrt(np.mean(y**2))


def multisine_lcg(f_low, f_high, spl, seed=12345, fs=FS, duration=DURATION):
    """Equal-amplitude lines at 1 Hz spacing with pseudo-random phases in [Pa].

    The phases come from the Park-Miller generator (exact in double precision),
    so the MATLAB driver of the SQAT comparison builds the same samples. Phases
    linear in the line index (a golden-ratio sequence, for instance) would make
    a pulse train, which a frame-wise analysis reads very differently from the
    long-term spectrum; the generator phases keep the signal stationary at the
    frame scale (crest factor about 10 dB).
    """
    t = np.arange(int(round(fs * duration))) / fs
    n_lines = f_high - f_low + 1
    amp = np.sqrt(2 / n_lines) * 2e-5 * 10 ** (spl / 20)
    state = seed
    x = np.zeros(t.size)
    for k in range(n_lines):
        state = (16807 * state) % 2147483647
        x += amp * np.sin(2 * np.pi * (f_low + k) * t + 2 * np.pi * state / 2147483647)
    return x


def bark2freq(z):
    """Inverse of the Bark scale of Zwicker and Terhardt (1980) used by the model."""
    lo, hi = 1.0, 24000.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if _bark(mid) < z else (lo, mid)
    return 0.5 * (lo + hi)


def w1(dz):
    """Gl. (7): bandwidth weighting."""
    return 0.13 / (dz + 0.13)


def w2(freq):
    """Gl. (9): frequency weighting."""
    return (1 / np.sqrt(1 + 0.2 * (freq / 700 + 700 / freq) ** 2)) ** 0.29


# ---------------------------------------------------------------- checks
def _row(signal, source, target, obtained, tolerance):
    deviation = obtained - target
    return {
        "signal": signal,
        "source": source,
        "target": target,
        "obtained": obtained,
        "deviation": deviation,
        "tolerance": tolerance,
        "passes": bool(abs(deviation) <= tolerance),
    }


def check_reference():
    """1 kHz, 60 dB SPL defines 1 t.u. (Aures 1985, p. 137)."""
    k = tonality_aures(pure_tone(1000, 60), FS)
    return [_row("1 kHz, 60 dB SPL", "Aures 1985 p. 137", 1.0, k, 0.001)]


def check_bin_alignment():
    """A tone between two bins (spacing 12.5 Hz) reads as a tone on a bin."""
    rows = []
    for freq in np.arange(990, 1011, 2.5):
        k = tonality_aures(pure_tone(freq, 60), FS)
        rows.append(_row(f"{freq:g} Hz, 60 dB SPL", "same as 1 kHz", 1.0, k, 0.01))
    return rows


def check_frequency():
    """Fig. 5: pure tones at 60 dB SPL follow Gl. (9), normalised at 1 kHz."""
    rows = []
    for freq in (250, 500, 1000, 2000, 4000, 8000):
        k = tonality_aures(pure_tone(freq, 60), FS)
        rows.append(_row(f"{freq} Hz, 60 dB SPL", "Gl. (9) / Fig. 5", w2(freq) / w2(1000), k, 0.05))
    return rows


def check_bandwidth():
    """Fig. 6: 1 kHz band noise at 60 dB SPL follows Gl. (7)."""
    rows = []
    z0 = float(_bark(1000))
    for dz in (0.2, 0.3, 0.5, 0.7, 1.0, 1.4):
        f_low, f_high = bark2freq(z0 - dz / 2), bark2freq(z0 + dz / 2)
        k = tonality_aures(band_noise(f_low, f_high, 60), FS)
        rows.append(_row(f"1 kHz band noise, dz = {dz} Bark ({f_high - f_low:.0f} Hz), 60 dB SPL",
                         "Gl. (7) / Fig. 6", w1(dz), k, 0.15 * w1(dz)))
    return rows


def check_level():
    """Fig. 7: the tonality of a 1 kHz tone does not depend on its level (2 to 28 sone)."""
    rows = []
    for spl in (40, 50, 60, 70, 80):
        k = tonality_aures(pure_tone(1000, spl), FS)
        rows.append(_row(f"1 kHz, {spl} dB SPL", "Fig. 7", 1.0, k, 0.03))
    return rows


def check_tone_in_noise():
    """1 kHz, 82 dB SPL tone in noise one critical band wide (912-1088 Hz)."""
    rows = []
    previous = -1.0
    for prominence, noise_spl in zip(range(0, 90, 10), (106, 96, 86, 76, 66, 56, 46, 36, 26)):
        k = tonality_aures(pure_tone(1000, 82) + band_noise(912, 1088, noise_spl, seed=1), FS)
        rows.append({"prominence_db": prominence, "noise_spl": noise_spl, "computed_tu": k,
                     "passes": bool(k >= previous - 1e-9)})
        previous = k
    return rows


def check_white_noise():
    """White noise has no tonal component."""
    k = tonality_aures(band_noise(20, 20000, 60), FS)
    return [_row("white noise 20 Hz - 20 kHz, 60 dB SPL", "Aures section 2.3.2", 0.0, k, 0.02)]


def compare_with_sqat(csv_path=SQAT_CSV):
    """Our values against SQAT's for the deterministic signals of the CSV."""
    if not csv_path.exists():
        return {"commit": "", "rows": []}
    with csv_path.open(encoding="utf-8") as fh:
        first = fh.readline()
        reader = csv.DictReader(fh)
        sqat = list(reader)
    commit = first.strip("# \n")
    signals = {
        "ref": pure_tone(1000, 60),
        "bin_1000": pure_tone(1000, 60),
        "bin_1003": pure_tone(1003, 60),
        "bin_1006.25": pure_tone(1006.25, 60),
        "bin_1009": pure_tone(1009, 60),
        "two_A": pure_tone(1000, 60) + pure_tone(1500, 30),
        "two_B": pure_tone(1000, 60) + pure_tone(1200, 40),
        "three": pure_tone(500, 50) + pure_tone(1000, 50) + pure_tone(2000, 50),
        "lcg_band": multisine_lcg(961, 1040, 60),
        "lcg_tone_26dB": pure_tone(1000, 82) + multisine_lcg(912, 1088, 56),
        "lcg_tone_6dB": pure_tone(1000, 82) + multisine_lcg(912, 1088, 76),
    }
    for spl in (40, 50, 60, 70, 80):
        signals[f"level_{spl}"] = pure_tone(1000, spl)
    for freq in (250, 500, 2000, 4000):
        signals[f"freq_{freq}"] = pure_tone(freq, 60)
    rows = []
    for entry in sqat:
        name = entry["case"]
        if name not in signals:
            continue
        ours = tonality_aures(signals[name], FS)
        theirs = float(entry["K_mean"])
        rows.append({"case": name, "description": entry["description"], "sqat": theirs,
                     "mosqito": ours, "difference": ours - theirs})
    return {"commit": commit, "rows": rows}


RECORDINGS_CSV = HERE / "input" / "sqat_aures_recordings.csv"
RECORDINGS_DIRS = {
    "Test signal 1": "validations/sq_metrics/loudness_zwtv/input/ISO_532-1/Annex B.5",
    "Test signal 2": "validations/sq_metrics/loudness_zwtv/input/ISO_532-1/Annex B.5",
    "Test signal 7": "validations/sq_metrics/loudness_zwtv/input/ISO_532-1/Annex B.4",
    "Test signal 3": "validations/sq_metrics/loudness_zwst/input/ISO_532_1",
    "Test signal 5": "validations/sq_metrics/loudness_zwst/input/ISO_532_1",
    "trafic": "validations/sq_metrics/loudness_zwst/input/ISO_532_1",
    "white_noise": "tests/input",
}


def compare_with_sqat_recordings(csv_path=RECORDINGS_CSV):
    """Our values against SQAT's on the recordings shipped with MoSQITo.

    The files are loaded with the calibration MoSQITo uses for them (column
    ``calib`` of the CSV, the ``wav_calib`` argument of ``mosqito.utils.load``).
    SQAT gives the mean over 250 ms frames; we give one value for the whole
    file, so the two agree only for stationary sounds.
    """
    from mosqito.utils import load

    if not csv_path.exists():
        return {"commit": "", "rows": []}
    root = HERE.parents[2]
    with csv_path.open(encoding="utf-8") as fh:
        commit = fh.readline().strip("# \n")
        sqat = list(csv.DictReader(fh))
    rows = []
    for entry in sqat:
        name = entry["file"]
        folder = next((d for key, d in RECORDINGS_DIRS.items() if name.startswith(key)), None)
        path = root / folder / name if folder else None
        if path is None or not path.exists():
            continue
        signal, fs = load(str(path), wav_calib=float(entry["calib"]))
        ours = tonality_aures(signal, fs)
        theirs = float(entry["K_mean"])
        rows.append({"file": name, "leq": float(entry["Leq_dB"]), "sqat_mean": theirs,
                     "sqat_max": float(entry["K_max"]), "mosqito": ours, "difference": ours - theirs})
    return {"commit": commit, "rows": rows}


def summarize_validation():
    """All checks in one dictionary, with an overall success flag."""
    summary = {
        "reference": check_reference(),
        "bin_alignment": check_bin_alignment(),
        "frequency": check_frequency(),
        "bandwidth": check_bandwidth(),
        "level": check_level(),
        "tone_in_noise": check_tone_in_noise(),
        "white_noise": check_white_noise(),
    }
    summary["success"] = all(row["passes"] for rows in summary.values() for row in rows)
    summary["sqat"] = compare_with_sqat()
    summary["sqat_recordings"] = compare_with_sqat_recordings()
    return summary


def format_table(rows):
    lines = ["| Signal | Source of the target | Target | Obtained | Deviation | Tolerance | Pass |",
             "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['signal']} | {r['source']} | {r['target']:.3f} | {r['obtained']:.3f} | "
                     f"{r['deviation']:+.3f} | {r['tolerance']:.3f} | {'yes' if r['passes'] else 'no'} |")
    return "\n".join(lines)


def print_validation_report():
    """Print every table in Markdown; returns the summary."""
    summary = summarize_validation()
    for name in ("reference", "bin_alignment", "frequency", "bandwidth", "level", "white_noise"):
        print(f"\n### {name}\n")
        print(format_table(summary[name]))
    print("\n### tone in noise (1 kHz, 82 dB SPL in 912-1088 Hz noise)\n")
    print("| Tone over noise band [dB] | Noise band [dB SPL] | Tonality [t.u.] |\n|---|---|---|")
    for r in summary["tone_in_noise"]:
        print(f"| {r['prominence_db']} | {r['noise_spl']} | {r['computed_tu']:.3f} |")
    if summary["sqat"]["rows"]:
        print(f"\n### comparison with SQAT ({summary['sqat']['commit']})\n")
        print("| Case | Signal | SQAT | MoSQITo | Difference |\n|---|---|---|---|---|")
        for r in summary["sqat"]["rows"]:
            print(f"| {r['case']} | {r['description']} | {r['sqat']:.3f} | {r['mosqito']:.3f} | {r['difference']:+.3f} |")
    if summary["sqat_recordings"]["rows"]:
        print(f"\n### recordings shipped with MoSQITo, SQAT ({summary['sqat_recordings']['commit']})\n")
        print("| File | Leq [dB] | SQAT mean | SQAT max | MoSQITo | Difference to the mean |\n|---|---|---|---|---|---|")
        for r in summary["sqat_recordings"]["rows"]:
            print(f"| {r['file']} | {r['leq']:.1f} | {r['sqat_mean']:.3f} | {r['sqat_max']:.3f} | {r['mosqito']:.3f} | {r['difference']:+.3f} |")
    print(f"\noverall success: {summary['success']}")
    return summary


if __name__ == "__main__":
    print_validation_report()
