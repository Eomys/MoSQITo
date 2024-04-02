# -*- coding: utf-8 -*-

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError("In order to perform the tests you need the 'pytest' package.")

import numpy as np
from scipy.fft import fft

# Local application imports
from mosqito.sq_metrics import roughness_ecma, roughness_ecma
from mosqito.utils.am_sine_wave_generator import am_sine_wave_generator


@pytest.mark.roughness_ecma  # to skip or run only ECMA 418-2 roughness tests
def test_roughness_ecma():
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
    stimulus = am_sine_wave_generator(d=1, fs=48000, fc=1000, fmod=70, mdepth=1 , dB_level=60)

    # Roughness calculation
    R, _, _, _, _ = roughness_ecma(stimulus, fs=48000)

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

    # Test for comformance (0.1 asper tolerance)
    tst = (R >= ref - 0.1).all() and (R <= ref + 0.1).all()

    return tst


# test de la fonction
if __name__ == "__main__":
    test_roughness_ecma()
