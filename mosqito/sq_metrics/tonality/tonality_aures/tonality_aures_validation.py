# -*- coding: utf-8 -*-

"""Validation helpers for the Aures tonality implementation.

This module focuses on the validation material used by SQAT v1.0:

* The Aures reference signal from Table 1 of Greco et al. (2023):
  a 1 kHz pure tone at 60 dB SPL, which should yield 1 t.u.
* The ``Tonality_Aures1985`` validation dataset from Zenodo record 7933206:
  1 kHz tones at 85 dB SPL embedded in one-critical-band noise with
  prominence levels from 0 to 80 dB.

The helpers below do not modify the tonality algorithm. They provide a
reproducible way to assess whether the current implementation behaves like the
reference description and whether it follows the basic dataset trend.
"""

from pathlib import Path
import re

import numpy as np

from mosqito.sq_metrics.tonality.tonality_aures.tonality_aures import tonality_aures
from mosqito.utils import load


REFERENCE_SIGNAL_FREQ_HZ = 1000.0
REFERENCE_SIGNAL_SPL_DB = 60.0
REFERENCE_SIGNAL_DURATION_S = 1.0
REFERENCE_TONALITY_TU = 1.0
REFERENCE_TOLERANCE_TU = 0.1

SQAT_DATASET_DIR = Path(__file__).resolve().parent / "validation_SQAT_v1_0" / "Tonality_Aures1985"


def generate_reference_signal(
    fs=48000,
    duration=REFERENCE_SIGNAL_DURATION_S,
    frequency=REFERENCE_SIGNAL_FREQ_HZ,
    spl_db=REFERENCE_SIGNAL_SPL_DB,
):
    """Generate the SQAT Aures reference signal in Pascal."""

    time = np.arange(0, duration, 1 / fs)
    signal = np.sin(2 * np.pi * frequency * time)

    rms = np.sqrt(np.mean(signal**2))
    ref_rms = 2e-5 * 10 ** (spl_db / 20)
    signal *= ref_rms / rms

    return signal, fs


def validate_reference_signal():
    """Compute tonality for the 1 kHz, 60 dB SPL Aures reference signal."""

    signal, fs = generate_reference_signal()
    tonality = tonality_aures(signal, fs)

    return {
        "frequency_hz": REFERENCE_SIGNAL_FREQ_HZ,
        "level_db_spl": REFERENCE_SIGNAL_SPL_DB,
        "expected_tu": REFERENCE_TONALITY_TU,
        "tolerance_tu": REFERENCE_TOLERANCE_TU,
        "computed_tu": float(tonality),
        "error_tu": float(tonality - REFERENCE_TONALITY_TU),
        "passes": bool(
            np.isfinite(tonality)
            and abs(tonality - REFERENCE_TONALITY_TU) <= REFERENCE_TOLERANCE_TU
        ),
    }


def iter_sqat_dataset_results(dataset_dir=SQAT_DATASET_DIR):
    """Yield tonality values for the local SQAT v1.0 validation sounds."""

    if not dataset_dir.exists():
        raise FileNotFoundError(f"SQAT validation dataset not found: {dataset_dir}")

    for wav_path in sorted(dataset_dir.glob("*.wav")):
        match = re.search(r"prominence_(\d+)dB", wav_path.name)
        prominence_db = int(match.group(1)) if match else None

        signal, fs = load(str(wav_path), wav_calib=1)
        tonality = tonality_aures(signal, fs)

        yield {
            "file": wav_path.name,
            "path": wav_path,
            "prominence_db": prominence_db,
            "computed_tu": float(tonality),
        }


def validate_sqat_dataset(dataset_dir=SQAT_DATASET_DIR):
    """Return SQAT dataset results and simple trend checks."""

    results = sorted(
        iter_sqat_dataset_results(dataset_dir),
        key=lambda item: (
            item["prominence_db"] is None,
            item["prominence_db"] if item["prominence_db"] is not None else item["file"],
        ),
    )

    values = np.array([item["computed_tu"] for item in results], dtype=float)
    increments = np.diff(values)

    return {
        "dataset_dir": dataset_dir,
        "results": results,
        "is_monotonic_non_decreasing": bool(np.all(increments >= -1e-12)),
        "has_strict_increase": bool(np.any(increments > 0)),
        "min_tu": float(values.min()) if len(values) else np.nan,
        "max_tu": float(values.max()) if len(values) else np.nan,
    }


def summarize_validation(reference_tol=REFERENCE_TOLERANCE_TU):
    """Collect the key validation outcomes in one dictionary."""

    reference = validate_reference_signal()
    dataset = validate_sqat_dataset()

    success = (
        abs(reference["computed_tu"] - REFERENCE_TONALITY_TU) <= reference_tol
        and dataset["is_monotonic_non_decreasing"]
        and dataset["has_strict_increase"]
    )

    return {
        "reference": reference,
        "dataset": dataset,
        "success": bool(success),
    }


def _format_dataset_rows(results):
    lines = ["Prominence (dB) | Tonality (t.u.)", "--- | ---"]
    for item in results:
        lines.append(f"{item['prominence_db']:>3} | {item['computed_tu']:.6f}")
    return "\n".join(lines)


def print_validation_report():
    """Print a concise validation report for manual checks."""

    summary = summarize_validation()
    reference = summary["reference"]
    dataset = summary["dataset"]

    print("Aures reference signal")
    print(
        "expected={:.3f} t.u., computed={:.6f} t.u., error={:+.6f} t.u., passes={}".format(
            reference["expected_tu"],
            reference["computed_tu"],
            reference["error_tu"],
            reference["passes"],
        )
    )
    print()
    print("SQAT v1.0 dataset trend")
    print(_format_dataset_rows(dataset["results"]))
    print()
    print(
        "monotonic_non_decreasing={}, has_strict_increase={}, overall_success={}".format(
            dataset["is_monotonic_non_decreasing"],
            dataset["has_strict_increase"],
            summary["success"],
        )
    )

    return summary


if __name__ == "__main__":
    print_validation_report()
