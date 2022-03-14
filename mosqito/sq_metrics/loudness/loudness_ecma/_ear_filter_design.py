# -*- coding: utf-8 -*-
from numpy import column_stack


def _ear_filter_design():
    """Return second-order filter coefficients of outer and middle/inner ear filter according to
    ECMA-418-2:2020 section 5.1.2.

    Parameters
    ----------

    Returns
    -------
    sos : array_like
        Array of second-order filter coefficients. Each row corresponds to a
        second-order section, with the first three columns providing the numerator
        coefficients and the last three providing the denominator coefficients.

    """

    # Filer coefficients (ECMA-418-2:2020, Table 1)
    filter_a = [
        [1.0, -1.9253, 0.9380],
        [1.0, -1.8061, 0.8354],
        [1.0, -1.7636, 0.7832],
        [1.0, -1.4347, 0.7276],
        [1.0, -0.3661, -0.2841],
        [1.0, -1.7960, 0.8058],
        [1.0, -1.9124, 0.9142],
        [1.0, 0.1623, 0.2842],
    ]
    filter_b = [
        [1.0159, -1.9253, 0.9221],
        [0.9589, -1.8061, 0.8764],
        [0.9614, -1.7636, 0.8218],
        [2.2258, -1.4347, -0.4982],
        [0.4717, -0.3661, 0.2441],
        [0.1153, 0.0000, -0.1153],
        [0.9880, -1.9124, 0.9261],
        [1.9522, 0.1623, -0.6680],
    ]
    sos_ear = column_stack((filter_b, filter_a))

    return sos_ear
