# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""

import numpy as np


def time_segmentation(sig, sb, sh, is_ecma=False):
    """Function used for the segmentation of a time signal into
    smaller parts of audio (blocks).

    If is_ecma = True, the implementation is as described in
    Formula 16 (section 5.1.4) of ECMA-418-2.

    Parameters
    ----------
    sig: numpy.array
        time signal, shape (N,)
    sb: int
        block size
    sh: int
        Hop size.

    Returns
    -------
    block_array: List
        Array list of blocks in which the signal has been segmented.
    """

    if is_ecma:
        # pad with zeroes at the begining
        sig = np.hstack((np.zeros(sb), sig))

    l = 0
    block_array = []
    while l * sh <= len(sig):
        block_array.append(sig[l * sh : sb + l * sh])
        l += 1

    return block_array
