# -*- coding: utf-8 -*-

# Third party imports
import numpy as np

# Local application imports
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import (
    noct_spectrum,
)
from mosqito.sq_metrics.loudness.loudness_zwst._main_loudness import (
    _main_loudness,
)
from mosqito.sq_metrics.loudness.loudness_zwst._calc_slopes import (
    _calc_slopes,
)


def loudness_zwst(signal, fs, field_type="free"):
    """Zwicker-loudness calculation for stationary signals

    Calculates the acoustic loudness according to Zwicker method for
    stationary signals.
    Normatice reference:
        ISO 532:1975 (method B)
        DIN 45631:1991
        ISO 532-1:2017 (method 1)
    The code is based on BASIC program published in "Program for
    calculating loudness according to DIN 45631 (ISO 532B)", E.Zwicker
    and H.Fastl, J.A.S.J (E) 12, 1 (1991).
    Note that due to normative continuity, as defined in the
    preceeding standards, the method is in accordance with
    ISO 226:1987 equal loudness contours (instead of ISO 226:2003)

    Parameters
    ----------
    signal : numpy.array
        time signal values [Pa]
    fs : integer
        sampling frequency
    field_type : str
        Type of soundfield corresponding to spec_third ("free" by
        default or "diffuse")

    Outputs
    -------
    N : float
        Calculated loudness [sones]
    N_specific : numpy.ndarray
        Specific loudness [sones/bark]
    """

    #
    # Compute third octave band spectrum
    spec_third, _ = noct_spectrum(signal, fs, fmin=24, fmax=12600)
    spec_third = 20 * np.log10(spec_third / 2e-5)
    #
    # Compute main loudness
    Nm = _main_loudness(spec_third, field_type)
    #
    # Computation of specific loudness pattern and integration of overall
    # loudness by attaching slopes towards higher frequencies
    N, N_specific = _calc_slopes(Nm)
    #
    # Define Bark axis
    bark_axis = np.linspace(0.1, 24, int(24 / 0.1))

    return N, N_specific, bark_axis
