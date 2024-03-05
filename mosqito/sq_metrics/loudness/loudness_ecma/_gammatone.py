
from scipy.special import comb
import numpy as np


def _gammatone(freq, k=5, fs=48000):
    """ECMA-418-2:2022 Gammatone filter design

    This function computes the coefficients of a gammatone digital filter
    according to ECMA-418-2, 2nd Ed (2022), section 5.1.4.

    Parameters
    ----------
    freq: float
        Center frequency of the filter ['Hz'].

    k: int, optional
        The order of the filter. Default is "5" according to ECMA-418.2.

    fs: float, optional
        The sampling frequency of the signal. Default is 48000 Hz.

    Returns
    -------
    bm_prim, am_prim: ndarray, ndarray
        Numerator (b) and denominator (a) polynomials of the filter.

    """

    # ECMA-418-2 constants
    af_f0 = 81.9289
    c = 0.1618

    # Bandwidth (ECMA 418-2:2022 equation 10)
    delta_f = np.sqrt((af_f0**2) + ((c * freq) ** 2))

    # Time constant, delay (ECMA 418-2:2022 equation 8)
    binom = comb(2 * k - 2, k - 1, exact=True)
    tau = (1 / (2 ** (2 * k - 1))) * binom * (1.0 / delta_f)

    # "d" coefficient
    d = np.exp(-1 / (fs * tau))

    # coeff am (ECMA 418-2:2022 equation 14 - index 'm_' goes from 1 to k)
    m_ = np.arange(5) + 1
    am = np.power((-d), m_) * comb(5, m_)
    am = np.insert(am, 0, 1)

    # coeff bm (ECMA 418-2 equation 15 - index 'm' goes from 0 to k-1)
    em = np.array([0, 1, 11, 11, 1])
    i = np.arange(4) + 1
    denom = np.sum(em[i] * d**i)
    m = np.arange(5)
    bm = ((1 - d) ** k) / denom * (d**m) * em[m]

    # band pass filter coefficients (ECMA 418-2:2022 equation 16 & 17)
    # [by modifying the filter cofficients with a positive exponential,
    # the filter is a low-pass filter instead of the expected bandpass
    # filter]
    m = np.arange(6)
    exponential = np.exp(+1j * 2 * np.pi * freq * m / fs)
    am_prim_ecma = am * exponential
    bm_prim_ecma = bm * exponential[:-1]

    return bm_prim_ecma, am_prim_ecma
