# -*- coding: utf-8 -*-

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
    )

from pathlib import Path

import numpy as np

from tonality_aures_validation import print_validation_report, w1, w2
from mosqito import COLORS as clr


def validation_tonality_aures():
    """Run the Aures tonality validation, print the tables and save the figure."""

    summary = print_validation_report()

    fig, axes = plt.subplots(2, 3, figsize=(13, 7.5))
    fig.suptitle("Aures tonality: validation against Aures (1985)")

    # Fig. 5: frequency dependence of pure tones
    ax = axes[0, 0]
    rows = summary["frequency"]
    freqs = np.array([250, 500, 1000, 2000, 4000, 8000])
    f_axis = np.logspace(np.log10(200), np.log10(10000), 200)
    ax.semilogx(f_axis, w2(f_axis) / w2(1000), "--", color=clr[2], label="Gl. (9)")
    ax.semilogx(freqs, [r["obtained"] for r in rows], "o", color=clr[0], label="MoSQITo")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Tonality [t.u.]")
    ax.set_title("Pure tones, 60 dB SPL (Fig. 5)")
    ax.set_ylim(0, 1.2)
    ax.legend()

    # Fig. 6: bandwidth dependence of narrowband noise
    ax = axes[0, 1]
    rows = summary["bandwidth"]
    dz = np.array([0.2, 0.3, 0.5, 0.7, 1.0, 1.4])
    dz_axis = np.linspace(0.05, 1.6, 200)
    ax.plot(dz_axis, w1(dz_axis), "--", color=clr[2], label="Gl. (7)")
    ax.plot(dz, [r["obtained"] for r in rows], "o", color=clr[0], label="MoSQITo")
    ax.set_xlabel("Bandwidth [Bark]")
    ax.set_ylabel("Tonality [t.u.]")
    ax.set_title("1 kHz band noise, 60 dB SPL (Fig. 6)")
    ax.set_ylim(0, 1.0)
    ax.legend()

    # Fig. 7: level independence
    ax = axes[0, 2]
    rows = summary["level"]
    ax.plot([40, 50, 60, 70, 80], [r["obtained"] for r in rows], "o-", color=clr[0])
    ax.axhline(1.0, linestyle="--", color=clr[2])
    ax.set_xlabel("Level [dB SPL]")
    ax.set_ylabel("Tonality [t.u.]")
    ax.set_title("1 kHz tone, 40 - 80 dB SPL (Fig. 7)")
    ax.set_ylim(0.8, 1.2)

    # tone between two bins
    ax = axes[1, 0]
    rows = summary["bin_alignment"]
    ax.plot(np.arange(990, 1011, 2.5), [r["obtained"] for r in rows], "o-", color=clr[0])
    ax.axhline(1.0, linestyle="--", color=clr[2])
    ax.set_xlabel("Frequency [Hz]  (bins every 12.5 Hz)")
    ax.set_ylabel("Tonality [t.u.]")
    ax.set_title("Tone between FFT bins, 60 dB SPL")
    ax.set_ylim(0.8, 1.2)

    # tone in one-critical-band noise
    ax = axes[1, 1]
    rows = summary["tone_in_noise"]
    ax.plot([r["prominence_db"] for r in rows], [r["computed_tu"] for r in rows], "o-", color=clr[0])
    ax.set_xlabel("Tone level over noise band level [dB]")
    ax.set_ylabel("Tonality [t.u.]")
    ax.set_title("1 kHz, 82 dB SPL tone in 912 - 1088 Hz noise")
    ax.set_ylim(0, 1.2)

    # comparison with SQAT
    ax = axes[1, 2]
    rows = summary["sqat"]["rows"]
    if rows:
        ax.plot([0, 1.2], [0, 1.2], "--", color=clr[2])
        ax.plot([r["sqat"] for r in rows], [r["mosqito"] for r in rows], "o", color=clr[0])
        ax.set_xlabel("SQAT [t.u.]")
        ax.set_ylabel("MoSQITo [t.u.]")
        ax.set_title("Same signals, " + summary["sqat"]["commit"].split(" (")[0])
        ax.set_xlim(0.6, 1.2)
        ax.set_ylim(0.6, 1.2)

    color = clr[5] if summary["success"] else clr[1]
    fig.text(0.5, 0.01, "All checks passed" if summary["success"] else "Some checks failed",
             ha="center", bbox=dict(boxstyle="round", facecolor=color, alpha=0.3))
    fig.tight_layout(rect=(0, 0.03, 1, 0.96))

    out_dir = Path(__file__).resolve().parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_dir / "validation_tonality_aures.png", format="png", dpi=120)
    plt.close(fig)

    return summary


if __name__ == "__main__":
    validation_tonality_aures()
