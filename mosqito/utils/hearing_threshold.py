from numpy import interp, nan

from mosqito.utils.conversion import freq2bark, bark2freq
from mosqito.utils._hearing_threshold_data import f_iso226, ht_iso226, bark_dw, ht_dw


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
    DW_1997 :
        Hearing threshold defined in [DW]

    References
    ----------
    .. [ISO226] ISO 226:2003 Normal equal-loudness-level contours
    .. [DW] "Psychoacoustical roughness: implementation of an optimized model" by Daniel and Weber in 1997


    Examples
    --------

    """

    if method == "ISO_226:2003":
        if axis_type == "bark":
            axis = bark2freq(axis)
        ht = interp(axis, f_iso226, ht_iso226, left=nan, right=nan)

    elif method == "DW_1997":
        if axis_type == "freq":
            axis = freq2bark(axis)
        ht = interp(axis, bark_dw, ht_dw)

    return ht
