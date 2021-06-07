# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""
import numpy as np
import math
import scipy as sp
from scipy.special import comb


def afb_ppal_parameters(fs, band_number, filter_order_k):
    """ Principal parameters for the Auditory Filtering Bank coefficients and other calculations in later sections:
    central frequency, bandwidth, delay, d coefficient, block size and hop size.
    This has been implemented as described in section 5.1.3 of ECMA-418-2.

    Parameters
    ----------
    fs: float
        'Hz', sampling frequency.

    band_number: int
        Band number in which the filter is going to be applied over the signal.

    filter_order_k: int
        Order of the auditory filtering bank.

    Returns
    -------
    centre_freq: float
        'Hz', central frequency of the filter.

    f_bandwidth: float
        Filter bandwidth.

    t_delay: float
        's'.

    d_coefficients: float
        "d coefficient", related with sampling rate and delay.

    sb: int
        Block size.

    sh: int
        Hop size.
    """
    z_step_size = 0.50
    af_f0 = 81.9289  # ECMA-418-2
    c = 0.1618  # ECMA-418-2

    # Exponent of the delay
    exponent_1 = (2.0 * filter_order_k) - 1.0
    # Binomial coefficient
    n_binomial = (2.0 * filter_order_k) - 2.0
    k_binomial = filter_order_k - 1.0
    binomial_coef_1 = float(sp.special.comb(int(n_binomial), int(k_binomial), exact=True))

    # Critical band rate scale
    z = (band_number + 1) * z_step_size
    var = c * z

    # Central frequency
    centre_freq = (af_f0 / c) * math.sinh(var)

    # Bandwidth
    f_bandwidth = math.sqrt((af_f0 ** 2) + ((c * centre_freq) ** 2))

    # Time constant, delay
    t_delay = (1.0 / (2.0 ** exponent_1)) * binomial_coef_1 * (1.0 / f_bandwidth)

    # "d" coefficient
    d_coefficients = float(np.exp((-1.0) / (fs * t_delay)))

    # Block length and hop size, for further calculations (Root-Mean-Square Values, section 5.1.6)
    if z >= 13:
        sb = 1024
        sh = 256
    elif 8.5 <= z < 13:
        sb = 2048
        sh = 512
    elif 2 <= z < 8.5:
        sb = 4096
        sh = 1024
    else:
        sb = 8192
        sh = 2048

    return centre_freq, f_bandwidth, t_delay, d_coefficients, sb, sh
