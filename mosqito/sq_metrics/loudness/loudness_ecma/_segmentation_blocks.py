# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""

import numpy as np


def _segmentation_blocks(band_pass_signal_hr, sb, sh):
    """Function used for the segmentation of the signal into smaller parts of audio (blocks).
    This has been implemented as described in Formula 16 (section 5.1.4) of ECMA-418-2.

    Parameters
    ----------
    band_pass_signal_hr: numpy.array
        time signal values of the input signal
    sb: int
        block size
    sh: int
        Hop size.

    Returns
    -------
    block_array: List
        Array list of blocks in which the signal has been segmented.
    """

    # TODO: check first blocks

    l = 0
    block_array = []
    while l * sh <= len(band_pass_signal_hr):
        i_begin = l * sh - sb
        i_end = l * sh
        if i_begin < 0 and i_end <= 0:
            block_array.append(np.zeros(sb))
        elif i_begin < 0:
            block_array.append(
                np.concatenate((np.zeros(-i_begin), band_pass_signal_hr[0:i_end]))
            )
        else:
            block_array.append(band_pass_signal_hr[i_begin:i_end])
        l += 1

    return block_array
