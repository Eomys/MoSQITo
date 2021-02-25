# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 13:41:37 2020

@author: wantysal
"""

# Standard imports
import pytest

# Local application imports
from mosqito.functions.roughness_danielweber.comp_roughness import comp_roughness
from mosqito.tests.roughness.signals_test_generation import signal_test


@pytest.mark.roughness_dw  # to skip or run only Daniel and Weber roughness tests
def test_roughness():
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
    stimulus = signal_test(fc=1000, fmod=70, mdepth=1, fs=44100, d=0.2, dB=60)

    # Roughness calculation
    R = comp_roughness(stimulus, fs=44100, overlap=0)

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
    test_roughness()
