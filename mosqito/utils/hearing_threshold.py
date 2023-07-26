from numpy import interp, nan

from mosqito.utils._hearing_threshold_data import f_iso226, ht_iso226


def hearing_threshold(axis, axis_type="freq", method="ISO_226:2003"):
    """Return the threshold of hearing

    This function computes the threshold of hearing according to various
    references

    Parameters
    ----------
    axis : ndarray
        Axis over which to compute the hearing threshold
    axis_type : {"freq", "bark"}, optional
        Type of axis. Default is "freq"
    method : str
        The method used to generate the threshold of hearing

    Returns
    -------
    ht : ndarray
        Threshold of hearing in dB

    Notes
    -----
    Method for the hearing threshold computation:
    ISO_226:2003 :
        Linear interpolation from the data provided in Table 1 of [ISO226]
    Zwicker :
        Linear interpolation from the data given in [ZF] (figure 2.1)
        SPL is given for a free-field condition relative to 2 × 10−5 Pa
        (Threshold for roughness is slightly different)

    References
    ----------
    .. [ISO226] ISO 226:2003 Normal equal-loudness-level contours
    .. [ZF] E. Zwicker, H. Fastl: Psychoacoustics. Springer, Berlin, Heidelberg, 1990.

    Examples
    --------

    """

    if method == "ISO_226:2003":
        ht = interp(axis, f_iso226, ht_iso226, left=nan, right=nan)

    return ht