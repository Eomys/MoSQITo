# -*- coding: utf-8 -*-
"""
@date Created on Tue Mar 03 2020
@author martin_g for Eomys
"""
# Standard library imports
import math
from scipy import signal


def oct3dsgn(fc, fs, n=3):
    """Design of a one-third-octave filter

    Designs a digital 1/3-octave filter with center frequency fc for
    sampling frequency fs. The filter is designed according to the
    Order-N specification of the ANSI S1.1-1986 standard. Default
    value for N is 3.

    References:
        ANSI S1.1-1986 (ASA 65-1986): Specifications for
        Octave-Band and Fractional-Octave-Band Analog and
        Digital Filters, 1993.

    Parameters
    ----------
    fc : float
        Filter center frequency [Hz]
    fs : float
        Sampling frequency [Hz]
    N : str
        Filter order according to ANSI S1.1-1986

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

    # Check for high fc/fs causing filter design issue [ref needed]
    if fc < fs / 200:
        raise ValueError(
            """ERROR: Design not possible. Filter center frequency shall
            verify: fc > fs / 200"""
        )

    # Check for Nyquist-Shannon criteria
    if fc > 0.88 * (fs / 2):
        raise ValueError(
            """ERROR: Design not possible. Filter center frequency shall
            verify: fc <= 0.88 * (fs / 2)"""
        )

    # Design Butterworth 2Nth-order one-third-octave filter
    # Note: BUTTER is based on a bilinear transformation, as suggested in
    # ANSI S1.1-1986.
    f1 = fc / (2 ** (1 / 6))
    f2 = fc * (2 ** (1 / 6))
    qr = fc / (f2 - f1)
    qd = (math.pi / 2 / n) / (math.sin(math.pi / 2 / n)) * qr
    alpha = (1 + math.sqrt(1 + 4 * qd ** 2)) / 2 / qd
    w1 = fc / (fs / 2) / alpha
    w2 = fc / (fs / 2) * alpha
    b, a = signal.butter(n, [w1, w2], "bandpass", analog=False)
    return b, a
