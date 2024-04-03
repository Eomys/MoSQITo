# -*- coding: utf-8 -*-

from numpy import ones, ceil, linspace, arange, mean, int32


def _ecma_time_segmentation(signal_block, sb, sh, n_new):
    """Function used for the segmentation of a time signal into
    smaller parts of audio (blocks) following Formulas 18 to 20 (section 5.1.5)
    of ECMA-418-2:2022.

    Parameters
    ----------
    signal_block: list
        List of Numpy arrays containing bandpassed signals per critical band

    sb: int or list of int
        Block size, or list of block sizes per band

    sh: int or list of int
        Hop size, or list of hop sizes per band

    n_new : int
        Number of samples in signal after zero padding (Eq. 3)

    Returns
    -------
    block_array: list
        List of 53 two-dimensional arrays of size (nperseg, nseg)
        containing the segmented signal per critical band.

    time: list
        List of  Numpy arrays of size (nseg,) containing the time axis
        corresponding to each segmented signal. For each block, the time
        value chosen is the mean of the segmented time axis.
    """

    # Sampling frequency must be 48 kHz for ECMA-418-2 (2022)
    fs = 48000

    if isinstance(sb, int):
        sb = sb * ones(53, dtype=int)
    elif len(sb) != 53:
        raise ValueError("ERROR: len(sb) shall be either 1 or 53")

    if isinstance(sh, int):
        sh = sh * ones(53, dtype=int)
    elif len(sh) != 53:
        raise ValueError("ERROR: len(sh) shall be either 1 or 53")

    # Eq. (19)
    i_start = sb[0] - sb
    # Eq. (20) - number of blocks for each critical band
    L_last = (ceil((n_new + sh) / sh) - 1).astype("int")

    block_array = []
    time_array = []

    for z in range(53):

        signal = signal_block[z]

        # build time vector for signal
        time = linspace(0, (signal.shape[0] - 1) / fs, signal.shape[0])

        # Eq. (18)
        L = arange(L_last[z])
        idx = (
            linspace(L * sh[z] + i_start[z], L * sh[z] + i_start[z] + sb[z], sb[z])
            .astype(int32)
            .T
        )

        block_array.append(signal[idx])
        time_array.append(mean(time[idx], axis=1))

    return block_array, time_array
