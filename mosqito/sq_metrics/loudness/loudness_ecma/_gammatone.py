try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
        )


from scipy.special import comb
from scipy.signal import freqz
from numpy import (
    abs as np_abs,
    arange,
    exp,
    pi,
    log10,
    power as np_power,
    sqrt,
    insert as np_insert,
    sum as np_sum,
    array as np_array,
)


def _gammatone(freq, k=5, fs=48000, is_plot=False):
    """ECMA-418-2 Gammatone filter design

    This function computes the coefficients of a gammatone digital filter according to ECMA-418-2 section 5.1.3.

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

    # Bandwidth (ECMA 418-2 equation 7)
    delta_f = sqrt((af_f0 ** 2) + ((c * freq) ** 2))

    # Time constant, delay (ECMA 418-2 equation 5)
    binom = comb(2 * k - 2, k - 1, exact=True)
    tau = (1 / (2 ** (2 * k - 1))) * binom * (1.0 / delta_f)

    # "d" coefficient
    d = exp(-1 / (fs * tau))

    # coeff am (ECMA 418-2 equation 11)
    m = arange(5) + 1
    am = np_power((-d), m) * comb(5, m)
    am = np_insert(am, 0, 1)

    # coeff bm (ECMA 418-2 equation 12)
    em = np_array([0, 1, 11, 11, 1])
    i = arange(4) + 1
    denom = np_sum(em[i] * d ** i)
    m = arange(5)
    bm = ((1 - d) ** k) / denom * (d ** m) * em[m]

    # band pass filter coefficients (ECMA 418-2 equation 13 & 14)
    # [by modifying the filter ceofficients with a negative exponential,
    # the filter is a low-pass filter instead of the expected bandpass
    # filter]
    m = arange(6)
    exponential = exp(-1j * 2 * pi * freq * m / fs)
    am_prim_ecma = am * exponential
    bm_prim_ecma = bm * exponential[:-1]

    # band pass filter coefficients (ECMA 418-2 from equation 13 & 14)
    # [corrected to get a bandpass filter, to be validated]
    m = arange(6)
    exponential = exp(1j * 2 * pi * freq * m / fs)
    am_prim = am * exponential
    bm_prim = bm * exponential[:-1]

    if is_plot:
        w, h = freqz(bm, am, worN=round(fs / 2), fs=fs)
        h_db = 20.0 * log10(np_abs(h))
        plt.semilogx(w, h_db, label="am, bm from eq. 11 and 12")

        w, h = freqz(bm_prim_ecma, am_prim_ecma, worN=round(fs / 2), fs=fs)
        h_db = 20.0 * log10(np_abs(h))
        plt.semilogx(w, h_db, label="am', bm' from eq. 13 and 14")

        w, h = freqz(bm_prim, am_prim, worN=round(fs / 2), fs=fs)
        h_db = 20.0 * log10(np_abs(h))
        plt.semilogx(w, h_db, label="am', bm' with positive exp")

        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Amplitude [dB]")
        plt.grid(which="both", axis="both")
        plt.legend()

    return bm_prim, am_prim