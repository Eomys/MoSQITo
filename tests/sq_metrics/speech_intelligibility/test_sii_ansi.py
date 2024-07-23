# -*- coding: utf-8 -*-

import numpy as np
from numpy import array, interp, linspace

from scipy.fft import ifft

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError("In order to perform the tests you need the 'pytest' package.")

# Local application imports
from mosqito import sii_ansi, sii_ansi_freq, sii_ansi_level
from mosqito.sq_metrics.speech_intelligibility.sii_ansi._main_sii import _main_sii


@pytest.fixture
def test_signal():

    spec = array([70, 65, 45, 25, 1, -15])
    freqs = array([250, 500, 1000, 2000, 4000, 8000])
    fs = 44100
    n = int(44100 * 0.2)
    f = linspace(0, fs // 2, 2 * n)
    sig = ifft(interp(f, freqs, spec, left=0, right=0)).real[4410:13230]
    test_signal = {
        "noise_spectrum": spec,
        "speech_spectrum": array([50, 40, 40, 30, 20, 0]),
        "freq_axis": freqs,
        "signal": sig,
        "fs": fs,
        "method": "octave",
        "SII": 0.504,
        "SII_spec": array([0, 0, 0.08, 0.17, 0.21, 0.04]),
    }

    return test_signal


@pytest.mark.sii_ansi  # to skip or run sharpness test
def test_sii(test_signal):
    """Test function for the sharpness calculation of an audio signal
    The input signals come from DIN 45692_2009E. The compliance is assessed
    according to chapter 6 of the standard.
    Parameters
    ----------
    None
    Outputs
    -------
    None
    """

    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    SII, _, _ = sii_ansi(sig, fs, "third_octave", "raised")
    SII, _, _ = sii_ansi(sig, fs, "critical", "loud")
    SII, _, _ = sii_ansi(sig, fs, "equally_critical", "shout")
    SII, _, _ = sii_ansi(sig, fs, "octave", "normal")


@pytest.mark.sii_ansi  # to skip or run sharpness test
def test_sii_freq(test_signal):
    """Test function for the sharpness calculation of an time-varying audio signal.

    Parameters
    ----------
    None
    Outputs
    -------
    None
    """

    # Input signal
    spec = test_signal["noise_spectrum"]
    freqs = test_signal["freq_axis"]
    # Compute sharpness
    SII, _, _ = sii_ansi_freq(spec, freqs, "critical", "loud")
    SII, _, _ = sii_ansi_freq(spec, freqs, "equally_critical", "raised")
    SII, _, _ = sii_ansi_freq(spec, freqs, "third_octave", "shout")
    SII, _, _ = sii_ansi_freq(spec, freqs, "octave", "normal")


@pytest.mark.sii_ansi
def test_sii_level():

    # Compute sharpness
    SII, _, _ = sii_ansi_level(60, "critical", "normal")
    SII, _, _ = sii_ansi_level(60, "equally_critical", "raised")
    SII, _, _ = sii_ansi_level(60, "octave", "loud")
    SII, _, _ = sii_ansi_level(60, "third_octave", "shout")


@pytest.mark.sii_ansi  # to skip or run sharpness test
def test_main_sii(test_signal):
    """Test function for the sharpness calculation of an time-varying audio signal."""

    SII, _, _ = _main_sii(
        test_signal["method"],
        test_signal["speech_spectrum"],
        test_signal["noise_spectrum"],
        threshold=None,
    )

    assert check_compliance(SII, test_signal["SII"])


def check_compliance(SII, reference):
    """Check the compliance of SII with ANSI S3.5

    The compliance is assessed according to ANSI S3.5 annex A

    Parameters
    ----------
    SII : float
        computed sharpness value
    reference : float
        reference value

    Outputs
    -------
    tst : bool
        Compliance to the reference data
    """

    # Test for DIN 45692_2009E comformance (chapter 6)
    tst = (SII >= np.amax([reference * 0.999, reference - 0.01], axis=0)).all() and (
        SII <= np.amin([reference * 1.01, reference + 0.01], axis=0)
    ).all()

    return tst


# test de la fonction
if __name__ == "__main__":

    spec = array([70, 65, 45, 25, 1, -15])
    freqs = array([250, 500, 1000, 2000, 4000, 8000])
    fs = 44100
    n = int(44100 * 0.2)
    f = linspace(0, fs // 2, 2 * n)
    sig = ifft(interp(f, freqs, spec, left=0, right=0)).real[4410:13230]
    sig = {
        "noise_spectrum": spec,
        "speech_spectrum": array([50, 40, 40, 30, 20, 0]),
        "freq_axis": freqs,
        "signal": sig,
        "fs": fs,
        "method": "octave",
        "SII": 0.504,
        "SII_spec": array([0, 0, 0.08, 0.17, 0.21, 0.04]),
    }

    test_sii(sig)
    test_sii_freq(sig)
    test_sii_level()
    test_main_sii(sig)
