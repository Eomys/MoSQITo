# -*- coding: utf-8 -*-

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
    )

from pathlib import Path

from mosqito.sq_metrics.tonality.tonality_aures.tonality_aures_validation import (
    summarize_validation,
)
from mosqito import COLORS as clr


def validation_tonality_aures():
    """Run the Aures tonality validation and generate a summary plot."""

    summary = summarize_validation()
    reference = summary["reference"]
    dataset = summary["dataset"]

    prominence = [item["prominence_db"] for item in dataset["results"]]
    tonality = [item["computed_tu"] for item in dataset["results"]]

    plt.figure()
    plt.plot(prominence, tonality, marker="o", color=clr[0])
    plt.axhline(reference["expected_tu"], linestyle="--", color=clr[5], linewidth=1)
    plt.xlabel("Tone prominence [dB]")
    plt.ylabel("Tonality [t.u.]")
    plt.title("Aures tonality validation")

    if summary["success"]:
        color = clr[5]
        text = (
            f"Reference: {reference['computed_tu']:.3f} t.u. "
            f"(target {reference['expected_tu']:.1f})\n"
            "SQAT trend: pass"
        )
    else:
        color = clr[1]
        text = (
            f"Reference: {reference['computed_tu']:.3f} t.u. "
            f"(target {reference['expected_tu']:.1f})\n"
            "SQAT trend: fail"
        )

    props = dict(boxstyle="round", facecolor=color, alpha=0.3)
    plt.text(
        0.5,
        0.05,
        text,
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=plt.gca().transAxes,
        bbox=props,
    )

    out_dir = Path(__file__).resolve().parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_dir / "validation_tonality_aures.png", format="png")
    plt.close()

    return summary


if __name__ == "__main__":
    validation_tonality_aures()
