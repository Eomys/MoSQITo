# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""

import numpy as np
import math


def nonlinear_common(p_0, alpha, m_exponents, v_i_array, threshold_db_array):
    """ Array lists that are necessary for the calculation of the non-linearity and are general to each band. This has
    been implemented as described in formula F.18 (section F.3.6) of Annex F (ECMA-74).

    Parameters
    ----------
    p_0: numpy.array
        '20 uPa'.

    alpha: float
        Constant for the exponent.

    m_exponents: int
        Max index of the multiplication sequence in Formula 18.

    v_i_array: numpy.array
        Exponents for the multiplication sequence in Formula 18.

    threshold_db_array: numpy.array
        Thresholds for their corresponding "vi" exponent.

    Returns
    -------
    a_exponent_array: numpy.array

    pt_threshold_array: numpy.array
        'dB'
    """
    pt_threshold_array = np.zeros(m_exponents, dtype=float)

    # Numpy array for the exponent in the non-linearity function
    a_exponent_array = np.array(np.diff(v_i_array) / alpha)

    # COMMON CALCULATIONS
    for i_position in range(m_exponents):
        # "pt_threshold" changes to the value of each pt threshold (Table F.2)
        th_exponent = threshold_db_array[i_position] / 20
        pt_threshold = p_0 * math.pow(10, th_exponent)
        # Numpy array for the threshold in the non-linearity function
        pt_threshold_array[i_position] = pt_threshold

    return a_exponent_array, pt_threshold_array
