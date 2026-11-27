# -*- coding: utf-8 -*-

import sys
import types
import warnings

try:
    import pyuff  # noqa: F401
except ImportError:
    sys.modules.setdefault("pyuff", types.ModuleType("pyuff"))

import numpy as np
import pytest

from mosqito.sq_metrics import tnr_ecma_freq
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._tnr_main_calc import _tnr_main_calc


@pytest.mark.tnr_freq
def test_tnr_ecma_freq_close_tones_lt_exceeds_ltot():
    """Verify two close tones in one critical band do not raise RuntimeWarning."""
    freqs = np.arange(0.0, 24000.0, 2.0)
    spec_db = np.full_like(freqs, 20.0)
    spec_db[499:504] = [40.0, 80.0, 70.1, 79.5, 40.0]
    spectrum = 2e-5 * 10 ** (spec_db / 20.0)

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        t_tnr, tnr, prom, tones_freqs = tnr_ecma_freq(spectrum, freqs, prominence=True)

    assert np.all(np.isfinite(t_tnr))
    assert np.all(np.isfinite(tnr))
    assert len(tones_freqs) == 1
    assert np.isclose(tones_freqs[0], 1000.0)
    assert bool(prom[0]) is True


@pytest.mark.tnr_freq
def test_tnr_ecma_freq_single_peak_lt_equals_ltot():
    """Verify a single peak whose corrected level equals band total falls back cleanly."""
    freqs = np.arange(0.0, 24000.0, 10.0)
    spec_db = np.full_like(freqs, 20.0)
    # Minimal non-peak energy inside the 1000 Hz critical band so _peak_level matches Ltot.
    spec_db[90:110] = -200.0
    spec_db[99:102] = [70.2, 80.0, -200.0]
    spectrum = 2e-5 * 10 ** (spec_db / 20.0)

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        t_tnr, tnr, prom, tones_freqs = tnr_ecma_freq(spectrum, freqs, prominence=True)

    assert np.all(np.isfinite(t_tnr))
    assert np.all(np.isfinite(tnr))
    assert len(tones_freqs) == 1
    assert np.isclose(tones_freqs[0], 1000.0)
    assert bool(prom[0]) is True


@pytest.mark.tnr_tv
def test_tnr_main_calc_multi_segment_lt_exceeds_ltot():
    """Verify segmented spectra where Lt exceeds Ltot do not raise RuntimeWarning."""
    freqs = np.arange(0.0, 24000.0, 2.0)
    seg_close = np.full_like(freqs, 20.0)
    seg_close[499:504] = [40.0, 80.0, 70.1, 79.5, 40.0]
    spectrum_db = np.column_stack((seg_close, seg_close))

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        tones_freqs, tnr, prom, t_tnr = _tnr_main_calc(spectrum_db, freqs)

    assert len(t_tnr) == 2
    assert np.all(np.isfinite(np.asarray(t_tnr, dtype=float)))
    assert len(tones_freqs[0]) == 1
    assert len(tones_freqs[1]) == 1
    assert np.all(np.isfinite(np.asarray(tnr[0], dtype=float)))
    assert np.all(np.isfinite(np.asarray(tnr[1], dtype=float)))


@pytest.mark.tnr_freq
def test_tnr_main_calc_zero_noise_band_no_warning():
    """Verify a critical band with negligible noise energy does not raise RuntimeWarning."""
    freqs = np.arange(0.0, 24000.0, 10.0)
    spec_db = np.full_like(freqs, -200.0)
    spec_db[100] = 80.0

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        tones_freqs, tnr, prom, t_tnr = _tnr_main_calc(spec_db, freqs)

    assert np.all(np.isfinite(np.atleast_1d(np.asarray(t_tnr, dtype=float))))
