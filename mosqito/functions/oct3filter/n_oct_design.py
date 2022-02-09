# -*- coding: utf-8 -*-

# Standard library imports
import numpy as np
from scipy import signal

# local import
from mosqito.functions.oct3filter.center_freq import center_freq


def n_oct_design(fs, fmin, fmax, n=3, G=10, fr=1000, N=3):
    """Design of a nth octave filter set

    Designs a digital 1/3-octave filter with center frequency fc for
    sampling frequency fs. The filter is designed according to the
    Order-N specification of the ANSI S1.1-1986 standard. Default
    value for N is 3.

    References:
        ANSI S1.1-1986 (ASA 65-1986): Specifications for
        Octave-Band and Fractional-Octave-Band Analog and
        Digital Filters.

    Parameters
    ----------
    fs : float
        Sampling frequency [Hz]
    fmin : float
        Min frequency band [Hz]
    fmax : float
        Max frequency band [Hz]
    n : int
        number of bands pr octave
    G : int
        System for specifying the exact geometric mean frequencies.
        Can be base 2 or base 10
    fr : int
        Reference frequency. Shall be set to 1 kHz for audible frequency
        range, to 1 Hz for infrasonic range (f < 20 Hz) and to 1 MHz for
        ultrasonic range (f > 31.5 kHz)
    N : int
        Filter order

    Outputs
    -------
    A : numpy.ndarray
        Denominator coefficient of the filter rational transfer function
    B : numpy.ndarray
        Numerator coefficient of the filter rational transfer function
    """

    """
    Initial implementation as oct3dsgn.m by Christophe Couvreur, 
    Faculte Polytechnique de Mons (Belgium) couvreur@thor.fpms.ac.be
    (version: Aug. 25, 1997, 2:00pm)

    TODO: Check compliancy with the following standards
        - IEC 61260 – 1 (2014), 1/1-octave Bands and 1/3-octave Bands, Class 1
        - IEC 61260 (1995 – 07) plus Amendment 1 (2001 – 09), 1/1-octave Bands and 1/3-octave Bands, Class 0
        - ANSI S1.11 – 1986, 1/1-octave Bands and 1/3-octave Bands, Order 3, Type 0 – C
        - ANSI S1.11 – 2004, 1/1-octave Bands and 1/3-octave Bands, Class 0
        - ANSI/ASA S1.11 – 2014 Part 1, 1/1-octave Bands and 1/3-octave Bands, Class 1
    """

    # Filters center frequency
    fc, k = center_freq(fmin=fmin, fmax=fmax, n=n, G=G, fr=fr)

    # Check for high fc/fs causing filter design issue [ref needed]
    if fc < fs / 200:
        raise ValueError(
            """ERROR: Design not possible. Filter center frequency shall
            verify: fc > fs / 200"""
        )

    # Check for Nyquist-Shannon criteria
    if max(fc) > 0.88 * (fs / 2):
        raise ValueError(
            """ERROR: Design not possible. Filter center frequency shall
            verify: fc <= 0.88 * (fs / 2)."""
        )

    # Design Butterworth 2Nth-order one-third-octave filter
    # Note: BUTTER is based on a bilinear transformation, as suggested in
    # ANSI S1.1-1986.
    b = 1 / n
    f1 = fc / (2 ** (b / 2))  # ANSI eq5
    f2 = fc * (2 ** (b / 2))  # ANSI eq6
    qr = fc / (f2 - f1)  # ANSI eq7 & 8
    qd = (np.pi / 2 / N) / (np.sin(np.pi / 2 / N)) * qr  # ANSI eq9
    alpha = (1 + np.sqrt(1 + 4 * qd ** 2)) / 2 / qd
    w1 = fc / (fs / 2) / alpha
    w2 = fc / (fs / 2) * alpha
    b, a = signal.butter(n, [w1, w2], "bandpass", analog=False)
    return b, a


if __name__ == "__main__":
    n_oct_design(fs=48000, fmin=25, fmax=12500)
    pass