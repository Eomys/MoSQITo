# -*- coding: utf-8 -*-
from numpy import column_stack


def _ear_filter_design():
    """Return second-order filter coefficients of outer and middle/inner ear
    filter according to ECMA-418-2, 2nd Ed. (2022), Section 5.1.3.

    Parameters
    ----------

    Returns
    -------
    sos : array_like
        Array of second-order filter coefficients. Each row corresponds to a
        second-order section, with the first three columns providing the numerator
        coefficients and the last three providing the denominator coefficients.

    """


    # Filer coefficients (ECMA-418-2, 2nd Ed (2022) Table 1)
    filter_a = [
        [1.0, -1.925299, 0.938014],
        [1.0, -1.806088, 0.835382],
        [1.0, -1.763632, 0.783160],
        [1.0, -1.434650, 0.727599],
        [1.0, -0.366092, -0.284120],
        [1.0, -1.796003, 0.805838],
        [1.0, -1.912434, 0.914161],
        [1.0, 0.162320, 0.284244],
    ]
    
    filter_b = [
        [1.015896, -1.925299, 0.922118],
        [0.958943, -1.806088, 0.876439],
        [0.961372, -1.763632, 0.821788],
        [2.225804, -1.434650, -0.498204],
        [0.471735, -0.366092, 0.244145],
        [0.115267, 0.000000, -0.115267],
        [0.988029, -1.912434, 0.926132],
        [1.952238, 0.162320, -0.667994],
    ]
    
    sos_ear = column_stack((filter_b, filter_a))

    return sos_ear
