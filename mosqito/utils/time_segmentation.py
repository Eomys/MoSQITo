# -*- coding: utf-8 -*-

import numpy as np


def time_segmentation(sig, fs, nperseg=2048, noverlap=None, is_ecma=False):
    """Function used for the segmentation of a time signal into
    smaller parts of audio (blocks).

    Parameters
    ----------
    sig: numpy.array
        A 1-dimensional time signal array.
    fs : float
        The time signal sampling frequency.
    nperseg: int, optional
        Length of each segment. Defaults to 2048.
    noverlap: int, optional
        Number of points to overlap between segments.
        If None, noverlap = nperseg / 2. Defaults to None.
    is_ecma: bool, optional
        If is_ecma = True, the implementation is as described
        in Formula 16 (section 5.1.4) of ECMA-418-2. Defaults
        to False.

    Returns
    -------
    block_array: numpy.array
        A 2-dimensional array of size (nperseg, nseg)
        containing the segmented signal.
    time: numpy.array
        The time axis corresponding to the segmented
        signal, size (nseg,)
    """

    if noverlap is None:
        noverlap = int(nperseg / 2)
        
    if noverlap == 0:
        noverlap = nperseg

    if is_ecma:
        # pad with zeros at the begining
        sig = np.hstack((np.zeros(nperseg), sig))

    # build time axis for sig
    time = np.linspace(0, (len(sig) - 1) / fs, num=len(sig))

    l = 0
    block_array = []
    time_array = []
    while l * noverlap <= len(sig) - nperseg:
        block_array.append(sig[l * noverlap : nperseg + l * noverlap])
        time_array.append(np.mean(time[l * noverlap : nperseg + l * noverlap]))
        l += 1

    return np.array(block_array).T, np.array(time_array)
