# -*- coding: utf-8 -*-


def ear_filter_design():
    """Return second-order filter coefficients of outer and middle/inner ear filter according to ECMA-418-2
    section 5.1.2.

    The first section psycho-acoustic hearing model of the Annex F corresponds to the signal filtering (*) done in the
    outer and middle ear.
    As it is described in the annex: "The filter is optimized  on the equal-loudness contours of ISO 226:2003 for
    frequencies higher than 1 kHz. For lower frequencies, the equal-loudness contours of ISO 226:1987 are chosen as
    target because there is a large uncertainty of the experimental data at low frequencies".
    We have to filter the signal with a high order filter (order = 8) (Formula 1), which is implemented as
    serially-cascaded second-order filters (digital biquad filter) with the recursive Formula 2. The coefficient for
    the filters are shown in Table 1. Each filter has its coefficients normalized to for having a0=1 on each one.
    Also, for the implementation of these filters, we decided to use "scipy.signal.sosfiltfilt", which takes the filter
    coefficients in "sos" format (**) and filters the signal twice times, once forward and once backwards. Consequently,
    the "sosfiltfilt" does not make possible to use this code in real-time situations, to change that use
    "scipy.signal.sosfilt" instead, which is a causal forward-in-time filter, with "sos" coefficients.

    (*) Filter coefficient values for the actual version of ECMA-74 (17th Edition/June 2019). Coefficients have changed
    from the previous version to the actual one.
    (**) sos format: b0, b1, b2, a0, a1, a2

    Parameters
    ----------

    Returns
    -------

    """

    # Filer coefficients
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
    sos_ear = []
    ear_filter_order = 8

    for ear_filter_number in range(ear_filter_order):
        sos_ear.append(
            [
                filter_b[ear_filter_number][0],
                filter_b[ear_filter_number][1],
                filter_b[ear_filter_number][2],
                filter_a[ear_filter_number][0],
                filter_a[ear_filter_number][1],
                filter_a[ear_filter_number][2],
            ]
        )

    return sos_ear
