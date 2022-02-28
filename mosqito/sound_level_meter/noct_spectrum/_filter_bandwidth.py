# -*- coding: utf-8 -*-

# Standard library imports
import numpy as np

# local import
from mosqito.sound_level_meter.noct_spectrum._center_freq import _center_freq


def _filter_bandwidth(fc, n=3, N=3):
    """Define nth octave filter bandwidth

    The filter bandwidth is designed according to the Order-N
    specification of the ANSI S1.1-1986 standard. Default
    value for N is 3.

    References:
        ANSI S1.1-1986 (ASA 65-1986): Specifications for
        Octave-Band and Fractional-Octave-Band Analog and
        Digital Filters.

    Parameters
    ----------
    fc : ndarray
        Filters exact center frequencies
    n : int, optional
        Number of bands pr octave. Default to 3
    N : int, optional
        Filter order. Default to 3

    Outputs
    -------
    alpha : numpy.ndarray
        Ratio of the upper and lower band-edge frequencies to the mid-band
        frequency
    """

    """
    TODO: Check compliancy with the following standards
        - IEC 61260 – 1 (2014), 1/1-octave Bands and 1/3-octave Bands, Class 1
        - IEC 61260 (1995 – 07) plus Amendment 1 (2001 – 09), 1/1-octave Bands and 1/3-octave Bands, Class 0
        - ANSI S1.11 – 1986, 1/1-octave Bands and 1/3-octave Bands, Order 3, Type 0 – C
        - ANSI S1.11 – 2004, 1/1-octave Bands and 1/3-octave Bands, Class 0
        - ANSI/ASA S1.11 – 2014 Part 1, 1/1-octave Bands and 1/3-octave Bands, Class 1
    """

    # Design for Butterworth 2Nth-order nth-octave filter
    # Note: BUTTER is based on a bilinear transformation, as suggested in
    # ANSI S1.1-1986.
    b = 1 / n
    f1 = fc / (2 ** (b / 2))  # ANSI eq5
    f2 = fc * (2 ** (b / 2))  # ANSI eq6
    # Reference bandwidth quotient
    qr = fc / (f2 - f1)  # ANSI eq7 & 8
    # Design bandwidth quotient
    qd = (np.pi / 2 / N) / (np.sin(np.pi / 2 / N)) * qr  # ANSI eq9
    # Ratio of the upper and lower band-edge frequencies to the mid-band frequency
    alpha = (1 + np.sqrt(1 + 4 * qd ** 2)) / 2 / qd

    return alpha


if __name__ == "__main__":
    pass
