# -*- coding: utf-8 -*-

from numpy import zeros, hstack, array, mean, linspace


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
        Length of each segment in samples. Defaults to 2048.
    noverlap: int, optional
        Hop size in samples between consecutive segment starts. The default
        (``None``) uses half the segment length rounded down, with a minimum
        of one sample. Set to ``0`` to use a hop of ``nperseg`` for
        non-overlapping segments.
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
        Segment center times in seconds, size (nseg,).
    """

    if noverlap is None:
        noverlap = int(nperseg / 2)

    if noverlap == 0:
        noverlap = nperseg

    if is_ecma:
        # pad with zeros at the begining
        sig = hstack((zeros(nperseg), sig))

    # build time axis for sig
    time = linspace(0, (len(sig) - 1) / fs, num=len(sig))

    l = 0
    block_array = []
    time_array = []
    while l * noverlap <= len(sig) - nperseg:
        block_array.append(sig[l * noverlap : nperseg + l * noverlap])
        time_array.append(mean(time[l * noverlap : nperseg + l * noverlap]))
        l += 1

    return array(block_array).T, array(time_array)
