# -*- coding: utf-8 -*-

# Standard library imports
import numpy as np
from scipy.signal import decimate, butter, lfilter


def n_oct_filter(sig, fs, fc, alpha, N=3):
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
    sig : numpy.ndarray
        Time signal [any unit]
    fs : float
        Sampling frequency [Hz]
    fc : float
        Filter exact center frequency [Hz]
    alpha : float
        Ratio of the upper and lower band-edge frequencies to the mid-band
        frequency
    N : int, optional
        Filter order. Default to 3

    Outputs
    -------
    level : float
        Rms level of sig in the third octave band centered on fc
    """

    # Check for Nyquist-Shannon criteria
    if fc > 0.88 * (fs / 2):
        raise ValueError(
            """ERROR: Design not possible. Filter center frequency shall
            verify: fc <= 0.88 * (fs / 2)"""
        )

    # Check for high fc/fs causing filter design issue
    # [ref needed] and downsample if needed
    if fc < fs / 200:
        q = 2
        while fc < fs / q / 200:
            q += 1
        sig = decimate(sig, q)
        fs = fs / q

    # Normalized cutoff frequencies
    w1 = fc / (fs / 2) / alpha
    w2 = fc / (fs / 2) * alpha

    # define filter coefficient
    b, a = butter(N, [w1, w2], "bandpass", analog=False)

    # filter signal
    sig_filt = lfilter(b, a, sig)

    # Compute overall rms level
    level = np.sqrt(np.mean(sig_filt ** 2))

    return level


if __name__ == "__main__":
    pass