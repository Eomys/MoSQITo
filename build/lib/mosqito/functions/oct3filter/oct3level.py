# -*- coding: utf-8 -*-
"""
@date Created on Fri Mar 13 2020
@author martin_g for Eomys
"""


# Standard library imports
import numpy as np
from scipy import signal

# Local application imports
from mosqito.functions.oct3filter.oct3dsgn import oct3dsgn


def oct3level(sig, fs, fc, sig_type="stationary", dec_factor=24):
    """Calculate rms level of a signal in the third octave band fc

    Calculate the rms level of the signal "sig" in the third-octave
    band centered on frequency "fc". If "fc" is such that fc < fs/200,
    the signal is downsampled for better third-octave filter design.

    Parameters
    ----------
    sig : numpy.ndarray
        time signal [any unit]
    fs : float
        Sampling frequency [Hz]
    fc : float
        Filter exact center frequency [Hz]
    sig_type : str
        Type of signal ('stationary' or 'time-varying')
    dec_factor : int
        Time signal to RMS vs. time decimation factor

    Outputs
    -------
    level : numpy.ndarray
        Rms level of sig in the third octave band centered on fc
    """

    """
    For meaningful design results, center frequency used should 
    preferably be higher than fs/200 (source ???). The signal is
    then downsampled if fc < fs/200. The procedure is inspired by 
    script GenerateFilters.m by Aaron Hastings, Herrick Labs, 
    Purdue University (version: 31 Oct 00)

    TODO: generalize to dec_factor that is not divisor of fs
            (using resample instead of decimate)
    """

    # Check for Nyquist-Shannon criteria
    if fc > 0.88 * (fs / 2):
        raise ValueError(
            """ERROR: Design not possible. Filter center frequency shall
            verify: fc <= 0.88 * (fs / 2)"""
        )
    # Check if dec_factor is a divisor of fs
    fs_divisor = [n for n in range(1, (fs + 1)) if fs % n == 0]
    if (sig_type != "stationary") and (not dec_factor in fs_divisor):
        raise ValueError(
            """ERROR: Design not possible. Time decimation factor shall
            be a divisor of fs"""
        )

    # Downsampling to a multiple of fs to respect "fc > fs/200"
    # (in case of time varying signal, the decimation factor shall be
    # a multiple of dec_factor)
    if sig_type == "stationary":
        dec_factors = fs_divisor
    else:
        dec_factors = [n for n in fs_divisor if dec_factor % n == 0]
    for i in dec_factors:
        fs_sub = fs / i
        if fs_sub / fc < 200:
            break
    dec_factor = int(dec_factor / i)
    if i == dec_factors[-1] and fs_sub / fc >= 200:
        raise ValueError(
            """ERROR: Design not possible. No time decimation factor that 
            satisfies fs_sub / (fc) > 200 have been found"""
        )
    # Generate the 1/3 oct. digital filter
    b, a = oct3dsgn(fc, fs_sub, n=3)
    # Downsample the signal
    if fs != fs_sub:
        sig = signal.decimate(sig, int(fs / fs_sub))
    # Filter the signal
    sig_filt = signal.lfilter(b, a, sig)
    if sig_type == "stationary":
        # Calculate overall rms level
        level = np.sqrt(sum(sig_filt ** 2) / len(sig_filt))
    else:
        # Calculate rms level versus time
        n_level = int(np.floor(sig_filt.shape[0] / dec_factor))
        sig_reshaped = sig_filt[: dec_factor * n_level].reshape((n_level, dec_factor))
        level = np.sqrt(np.mean(sig_reshaped ** 2, 1))
        if sig_filt.shape[0] % dec_factor != 0:
            level = np.append(
                level, np.sqrt(np.mean(sig_filt[dec_factor * n_level :] ** 2))
            )
    return level
