# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 20:23:01 2020

@author: Salomé
"""
# Standard library imports
import numpy as np

# Mosqito functions import
from mosqito.functions.tonality_tnr_pr.critical_band import critical_band


def find_highest_tone(freqs, spec_db, index, nb_tones, ind):
    """

    Method to find the two highest tones in a given spectrum from a given index
    according to their critical band

    Parameters
    ----------
    freqs : numpy.array
        frequency axis
    spec_db : numpy.array
        signal spectrum in dB
    index : numpy.array
        list of candidate tones index
    index : numpy.array
        list of candidate tones index
    nb_tones : integer
        number of candidate tones non examinated

    Returns
    -------
    ind_p : integer
        index of the highest tone in the critical band
    ind_p : integer
        index of the second highest tone in the critical band
    index : numpy.array
        list of candidate tones index updated
    nb_tones : integer
        number of candidate tones non examinated updated
    """

    f = freqs[ind]
    # critical band centered on f
    f1, f2 = critical_band(f)
    low_limit_idx = np.argmin(np.abs(freqs - f1))
    high_limit_idx = np.argmin(np.abs(freqs - f2))

    # Other tones in the critical band centered on f tones
    multiple_idx = index[index > low_limit_idx]
    multiple_idx = multiple_idx[multiple_idx < high_limit_idx]

    if len(multiple_idx) > 1:
        sort_spec = np.argsort(-1 * spec_db[multiple_idx])

        # highest tones in the critical band
        ind_p = multiple_idx[sort_spec[0]]
        ind_s = multiple_idx[sort_spec[1]]

        # suppression of the lower values
        for s in sort_spec[2:]:
            sup = np.where(index == multiple_idx[s])[0]
            index = np.delete(index, sup)
            nb_tones -= 1

        if ind_p != ind:
            # screening to find the highest value in the critical band centered on fp
            ind_p, ind_s, index, nb_tones = find_highest_tone(
                freqs, spec_db, index, nb_tones, ind_p
            )

    else:
        ind_p = ind
        ind_s = None

    return ind_p, ind_s, index, nb_tones
