from scipy.special import comb
from numpy import arange, exp, power as np_power, sqrt, insert as np_insert


def gammatone(freq, order=5, fs=48000):
    """
    ECMA-418-2 Gammatone filter design

    This function computes the coefficients of a gammatone digital filter according to ECMA-418-2 section 5.1.3.

    Parameters
    ----------
    freq: float
        Center frequency of the filter ['Hz'].

    order: int, optional
        The order of the filter. Default is "5" according to ECMA-418.2.

    fs: float, optional
        The sampling frequency of the signal. Default is 48000 Hz.

    Returns
    -------
    b, a: ndarray, ndarray
        Numerator (b) and denominator (a) polynomials of the filter.

    """

    # ECMA-418-2 constants
    af_f0 = 81.9289
    c = 0.1618

    # Bandwidth
    f_bandwidth = sqrt((af_f0 ** 2) + ((c * freq) ** 2))

    # Exponent of the delay
    exponent_1 = (2.0 * order) - 1.0

    # Binomial coefficient
    n_binomial = (2.0 * order) - 2.0
    k_binomial = order - 1.0
    binomial_coef_1 = float(comb(int(n_binomial), int(k_binomial), exact=True))

    # Time constant, delay
    t_delay = (1.0 / (2.0 ** exponent_1)) * binomial_coef_1 * (1.0 / f_bandwidth)

    # "d" coefficient
    d_coefficients = float(exp((-1.0) / (fs * t_delay)))

    # coeff am
    m = arange(5) + 1
    am = np_power((-d_coefficients), m) * comb(5, m)
    am = np_insert(am, 0, 1)
