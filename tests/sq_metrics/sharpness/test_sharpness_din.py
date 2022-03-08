# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 09:20:41 2020

@author: wantysal
"""

import numpy as np
# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package."
        )


# Local application imports
from mosqito.utils import load
from mosqito.sq_metrics import sharpness_din


@pytest.mark.sharpness_din  # to skip or run sharpness test
def test_sharpness_din():
    """Test function for the sharpness calculation of an audio signal

    Test function for the function "comp_roughness" with 'din' method.
    The input signals come from DIN 45692_2009E. The compliance is assessed
    according to chapter 6 of the standard.
    One .png compliance plot is generated.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """

    # Input signal from DIN 45692_2009E
    signal = {"data_file": "tests/input/1KHZ60DB.wav", "S": 1}

    # Load signal
    sig, fs = load(signal["data_file"], wav_calib=1)

    # Compute sharpness
    sharpness = sharpness_din(True, sig, fs, method="din")

    assert check_compliance(sharpness, signal)


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
    test_sharpness_din()
