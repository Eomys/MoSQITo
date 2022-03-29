# -*- coding: utf-8 -*-

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package."
    )

import numpy as np
from scipy.fft import fft

# Local application imports
from mosqito.sq_metrics import roughness_dw, roughness_dw_freq
from tests.sq_metrics.roughness.signals_test_generation import signal_test


@pytest.mark.roughness_dw  # to skip or run only Daniel and Weber roughness tests
def test_roughness_dw():
    """Test function for the roughness calculation of a audio signal

    Test function for the script "comp_roughness" method with signal array
    as input. The input signals are chosen according to the article "Psychoacoustical
    roughness: implementation of an optimized model" by Daniel and Weber in 1997.
    The figure 3 is used to compare amplitude-modulated signals created according to
    their carrier frequency and modulation frequency to the article results.
    One .png compliance plot is generated.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """

    # Stimulus generation
    stimulus = signal_test(fc=1000, fmod=70, mdepth=1, fs=44100, d=0.2, dB=70)

    # Roughness calculation
    roughness, time, _, _ = roughness_dw(stimulus, fs=44100, overlap=0)
    R = {
        "name": "Roughness",
        "values": roughness,
        "time": time,
    }

    # Check compliance
    tst = check_compliance(R)

    assert tst


@pytest.mark.roughness_dw  # to skip or run only Daniel and Weber roughness tests
def test_roughness_dw_freq():
    """Test function for the roughness calculation of a audio signal

    Test function for the script "comp_roughness" method with spectrum array
    as input. The input signals are chosen according to the article "Psychoacoustical
    roughness: implementation of an optimized model" by Daniel and Weber in 1997.
    The figure 3 is used to compare amplitude-modulated signals created according to
    their carrier frequency and modulation frequency to the article results.
    One .png compliance plot is generated.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """

    # Stimulus generation
    stimulus = signal_test(fc=1000, fmod=70, mdepth=1, fs=44100, d=0.2, dB=60)

    # conversion into frequency domain
    n = len(stimulus)
    window = np.blackman(n)
    window = window / sum(window)

    # Creation of the spectrum by FFT using the Blackman window
    spec = fft(stimulus * window)[0:n//2] * 1.42
    # Highest frequency
    nMax = round(n / 2)
    # Frequency axis in Hertz
    freqs = np.arange(1, nMax + 1, 1) * (44100 / n)

    # Roughness calculation
    roughness, _, _ = roughness_dw_freq(spec, freqs)
    R = {
        "name": "Roughness",
        "values": roughness,
    }

    # Check compliance
    tst = check_compliance(R)

    assert tst


def check_compliance(R):
    """Check the compliance of roughness calc. to Daniel and Weber article
    "Psychoacoustical roughness: implementation of an optimized model", 1997.

    Check the compliance of the input data R to figure 3 of the article
    using the reference data described in the dictionary article_ref.

    Parameter
    ---------
    R: numpy.array
        Calculated roughnesses [asper]

    Output
    ------
    tst : bool
        Compliance to the reference data
    """

    # Reference value of 1 asper given by Zwicker and Fastl
    ref = 1

    # Test for comformance (17% tolerance)
    tst = (R["values"] >= ref * 0.83).all() and (R["values"] <= ref * 1.17).all()

    return tst


# test de la fonction
if __name__ == "__main__":
    test_roughness_dw()
    test_roughness_dw_freq()
