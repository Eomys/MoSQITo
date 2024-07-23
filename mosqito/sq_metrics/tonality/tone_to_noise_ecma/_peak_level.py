# -*- coding: utf-8 -*-

# Standard library import
from numpy import abs, log10


def _peak_level(freqs, spec, peak_index):
    """
        Correct the level of the peak present at peak_index

        This kind of error in peak levels is due to spectrum resolution
        The algorithm sums up the levels which are strictly decreasing
        from the peak with a level difference under 10 dB.

    Parameters
    ----------
    freqs : numpy.array
        frequency axis
    spec : numpy.array
        SPL spectrum in dB
    peak_index : integer
        index where to find the peak in the spectrum

    Returns
    -------
    Lt : float
        corrected SPL at peak_index

    """

    # initial level
    Li = spec[peak_index]
    # modified level
    L = spec[peak_index]

    # Screen the right points of the peak
    temp = peak_index + 1

    if temp != len(spec):
        Ltemp = Li
        # As long as the level decreases,
        while Ltemp - abs(spec[temp]) > 0:
            # if the level of the point is close enough of the peak point,
            if Li - spec[temp] < 10:
                Ltemp = spec[temp]
                # its level is summed up with the peak's one
                L = 10 * log10(10 ** (L / 10) + 10 ** (spec[temp] / 10))

                temp += 1
                if temp == len(spec):
                    temp -= 1
                    Ltemp = -1
            else:
                Ltemp = -1

    # Screen the left points of the peak
    temp = peak_index - 1

    if temp != -1:
        Ltemp = Li
        # As long as the level decreases,
        while Ltemp - abs(spec[temp]) > 0:
            # if the level of the point is close enough of the peak point,
            if Li - spec[temp] < 10:
                Ltemp = spec[temp]
                # its level is summed up with the peak's one
                L = 10 * log10(10 ** (L / 10) + 10 ** (spec[temp] / 10))

                temp -= 1
                if temp < 0:
                    temp += 1
                    Ltemp = -1
            else:
                Ltemp = -1

    return L
