# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""

import numpy as np


def time_segmentation(sig, nperseg=2048, noverlap=None, is_ecma=False):
    """Function used for the segmentation of a time signal into
    smaller parts of audio (blocks).

    If is_ecma = True, the implementation is as described in
    Formula 16 (section 5.1.4) of ECMA-418-2.

    Parameters
    ----------
    sig: numpy.array
        A 1-dimensional time signal array.
    nperseg: int, optional
        Length of each segment. Defaults to 2048.
    noverlap: int, optional
        Number of points to overlap between segments.
        If None, noverlap = nperseg / 2. Defaults to None.

    Returns
    -------
    block_array: numpy.array
        A 2-dimensional array of size (nperseg, nseg)
        containing the segmented signal.
    """

    if noverlap is None:
        noverlap = int(nperseg / 2)

    if is_ecma:
        # pad with zeroes at the begining
        sig = np.hstack((np.zeros(nperseg), sig))

    l = 0
    block_array = []
    while l * noverlap <= len(sig) - nperseg:
        block_array.append(sig[l * noverlap : nperseg + l * noverlap])
        l += 1

    return np.array(block_array).T
