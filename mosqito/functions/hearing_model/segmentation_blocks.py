# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""

import numpy as np


def segmentation_blocks(band_pass_signal_hr, sb, sh, dim):
    """ Function used for the segmentation of the signal into smaller parts of audio (blocks). This has been implemented
    as described in Formula 16 (section 5.1.4) of ECMA-418-2.

    Parameters
    ----------
    band_pass_signal_hr: numpy.array
        time signal values of the input signal

    sb: int
        block size

    sh: int
        Hop size.

    dim: int
        Signal dimensions.

    Returns
    -------
    block_array: List[None]
        Array list of blocks in which the signal has been segmented.
    """
    # Creation of the first empty block
    if dim == 2:
        first_block = np.zeros((sb, dim), dtype=float)
    else:
        first_block = np.zeros(sb, dtype=float)

    # Joins the first empty block with the rest of the signal
    band_pass_signal_hr_complete = np.concatenate((first_block, band_pass_signal_hr), axis=0)

    # For loop that helps to cut the signal into different blocks
    block_array = [band_pass_signal_hr_complete[block_s: block_s + sb]
                   for block_s in range(0, len(band_pass_signal_hr_complete), sh)]

    return block_array


def segmentation_blocks_test_a(band_pass_signal_hr, sb, sh, dim):
    """ THIS SECTION REMAINS FOR TESTING PURPOSES

    Function used for the segmentation of the signal into smaller parts of audio (blocks). This implementation
    has been modified in order to make a simpler version of the original one. After the tests, it has been proven that
    this algorithm is way faster than the original, it reduces some uncertainty and the number of blocks remains the
    same in most cases. Also, it treats the void that leaves the standard in blocks that have samples that ar out
    of bounds.

    Parameters
    ----------
    band_pass_signal_hr: numpy.array
        Time signal values of the input signal.

    sb: int
        Block size.

    sh: int
        Hop size.

    dim: int
        Signal dimensions.

    Returns
    -------
    block_array: List[List[float]]
        Array list of blocks in which the signal has been segmented.
    """
    # Creation of the Array list of blocks with a specific block size (sb) and hop size (sh)
    block_array = [band_pass_signal_hr[block_s: block_s + sb]
                   for block_s in range(0, len(band_pass_signal_hr), sh)]

    return block_array


def segmentation_blocks_test_b(band_pass_signal_hr, sb, sh, dim):
    """ THIS SECTION REMAINS FOR TESTING PURPOSES

    Function used for the segmentation of the signal into smaller parts of audio (blocks). This has been implemented
    as described in formula F.16 (section F.3.5) of Annex F (ECMA-74). It has some issues  when the input signal is
    stereo.

    Parameters
    ----------
    band_pass_signal_hr: numpy.array
        Time signal values of the input signal.

    sb: int
        Block size.

    sh: int
        Hop size.

    dim: int
        Signal dimensions.

    Returns
    -------
    block_array: List[List[float]]
        Array list of blocks in which the signal has been segmented.
    """
    # Array list of blocks
    block_array = []

    # Assignation of the empty  value for the block cell
    if band_pass_signal_hr.ndim == 2:
        empty_value = [0.00, 0.00]
    else:
        empty_value = 0.00

    """
    Total number of blocks. The sequence goes from "block_number = 0" to "block_number = total_blocks - 1". The result 
    of the number of blocks is rounded in order to prevent an error in the value assignment. Another option could be to 
    limit the call to higher positions in the array. The standard does not treat as it should the segmentation.
    """
    total_blocks = round((len(band_pass_signal_hr) + 1) / sh)

    for block_number in range(total_blocks):
        # Creation of the block
        block = np.zeros((sb, band_pass_signal_hr.ndim), dtype=float)

        # Here is stated the range for the assignment
        p_range = (sb - (block_number * sh))
        # Assignment position
        p_segmented = (block_number * sh) - sb

        for n_segmentation in range(sb):
            block[n_segmentation] = band_pass_signal_hr[p_segmented + n_segmentation] \
                if (n_segmentation >= p_range) else empty_value

        # Block assignment
        block_array.append(block)

    return block_array
