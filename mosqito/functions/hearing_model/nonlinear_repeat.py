# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""

import numpy as np


def nonlinear_repeat(specific_loudness_array, band_number):
    """ It repeats certain blocks depending on the band that you are in, in order pseudo-link bands on time, because
    lower bands have larger blocks than the higher ones.

    Parameters
    ----------
    specific_loudness_array: numpy.array
        'sones hms' array of specific loudness values.

    band_number: int
        Band number in which the filter is going to be applied over the signal.

    Parameters
    ----------

    Returns
    -------
    sl_array_rep: numpy.array
        'sones hms'.
    """
    # Critical band rate scale
    z = (band_number + 1) * 0.50

    # It makes possible to create arrays of repeated values based on their critical band rate scale, and consequently
    # on their block size
    if z >= 13:
        sl_array_rep = specific_loudness_array

    elif 8.5 <= z < 13:
        sl_array_rep = np.repeat(specific_loudness_array, repeats=2, axis=0)

    elif 2 <= z < 8.5:
        sl_array_rep = np.repeat(specific_loudness_array, repeats=4, axis=0)

    else:
        sl_array_rep = np.repeat(specific_loudness_array, repeats=8, axis=0)

    return sl_array_rep
