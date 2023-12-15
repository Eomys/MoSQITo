# -*- coding: utf-8 -*-

import numpy as np
from scipy.fft import fft, fftfreq

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package.")
try:
    from SciDataTool import DataLinspace, DataTime
except ImportError:
    raise RuntimeError(
        "In order to handle Data objects you need the 'SciDataTool' package."
    )

# Local application imports
from mosqito.utils import load
from mosqito.sq_metrics import sii, sii_freq, sii_level


@pytest.fixture
def test_signal():
    # Input signal from DIN 45692_2009E
    sig, fs = load("tests/input/broadband_570.wav", wav_calib=1)
    sig_dict = {
        "signal": sig,
        "fs": fs,
        "S_din": 2.85,
    }
    return sig_dict


@pytest.mark.sii  # to skip or run sharpness test
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
    SII, _, _ = sii(sig, fs, method, 'normal')
    SII, _, _ = sii(sig, fs, method, 'raised')
    SII, _, _ = sii(sig, fs, method, 'loud')
    SII, _, _ = sii(sig, fs, method, 'shout')
    



@pytest.mark.sii # to skip or run sharpness test
def test_sii_freq():
    """Test function for the sharpness calculation of an time-varying audio signal.

    Parameters
    ----------
    None
    Outputs
    -------
    None
    """

    # Input signal
    sig = test_spectrum
    
    # Compute sharpness
    SII, _, _ = sii(spec, freqs, method, 'normal')
    SII, _, _ = sii(spec, freqs, method, 'raised')
    SII, _, _ = sii(spec, freqs, method, 'loud')
    SII, _, _ = sii(spec, freqs, method, 'shout')

    # Check that the value is within the desired values +/- 1%
    np.testing.assert_allclose(SII, test_signal["SII"], rtol=0.05)



@pytest.mark.sii
def test_sii_level(test_signal):
    
    # Compute sharpness
    SII, _, _ = sii(60, method, 'normal')
    SII, _, _ = sii(60, method, 'raised')
    SII, _, _ = sii(60, method, 'loud')
    SII, _, _ = sii(60, method, 'shout')

def check_compliance(S, signal):
    """Check the comppiance of loudness calc. to ISO 532-1

    The compliance is assessed according to chapter 6 of the
    standard DIN 45692_2009E.

    Parameters
    ----------
    S : float
        computed sharpness value
    signal : dict
        {"data file" : <path to the standard file >
         "S" : <sharpness reference value>
         }

    Outputs
    -------
    tst : bool
        Compliance to the reference data
    """

    # Load reference value
    ref = signal["S"]

    # Test for DIN 45692_2009E comformance (chapter 6)
    tst = (S >= np.amax([ref * 0.95, ref - 0.05], axis=0)).all() and (
        S <= np.amin([ref * 1.05, ref + 0.05], axis=0)
    ).all()

    return tst


# test de la fonction
if __name__ == "__main__":
    # Reproduce the code from the fixture
    # Input signal from ANSI S3.5
    sig, fs = load("tests/input/broadband_570.wav", wav_calib=1)
    test_signal = {
        "signal": sig,
        "fs": fs,
        "S_din": 2.85,
    }
    test_spectrum = []
    
    test_sii(test_signal)
    test_sii_freq(test_spectrum)
    test_sii_level()
