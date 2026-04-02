# -*- coding: utf-8 -*-

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError("In order to perform the tests you need the 'pytest' package.")

from mosqito.sq_metrics.tonality.tonality_aures.tonality_aures_validation import (
    summarize_validation,
    validate_reference_signal,
    validate_sqat_dataset,
)


@pytest.mark.aures_tonality
def test_tonality_aures_reference_signal_runs():
    """The Aures reference signal should match the 1 t.u. definition."""

    result = validate_reference_signal()

    assert result["passes"]


@pytest.mark.aures_tonality
def test_tonality_aures_sqat_dataset_trend_is_monotonic():
    """SQAT validation files should yield a monotonic tonality trend."""

    dataset = validate_sqat_dataset()

    assert len(dataset["results"]) == 9
    assert dataset["is_monotonic_non_decreasing"]
    assert dataset["has_strict_increase"]


@pytest.mark.aures_tonality
def test_tonality_aures_validation_summary_succeeds():
    """The reference signal and SQAT trend checks should both pass."""

    summary = summarize_validation()

    assert summary["success"]


if __name__ == "__main__":
    test_tonality_aures_reference_signal_runs()
    test_tonality_aures_sqat_dataset_trend_is_monotonic()
    test_tonality_aures_validation_summary_succeeds()
