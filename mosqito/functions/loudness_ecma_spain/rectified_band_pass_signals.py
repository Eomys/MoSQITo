# -*- coding: utf-8 -*-

import numpy as np
import scipy.signal as sp_signal

from mosqito.functions.loudness_ecma_spain.ear_filter_design import ear_filter_design
from mosqito.functions.loudness_ecma_spain.gen_auditory_filters_centre_freq import (
    gen_auditory_filters_centre_freq,
)
from mosqito.functions.loudness_ecma_spain.gammatone import gammatone
from mosqito.functions.loudness_ecma_spain.segmentation_blocks import (
    segmentation_blocks,
)


def rectified_band_pass_signals(sig, sb=2048, sh=1024):
    """Compute the rectified band-pass signals as per Clause 5.1.5 of ECMA-418-2:2020

    Calculation of the rectified band-pass signals along the 53 critical band rates
    scale. Each band pass signal is segmented into time blocks according to sb and sh


    Parameters
    ----------
    signal: numpy.array
        'Pa', time signal values. It can be, stereo (2 dimensions) or mono (1 dimension).The sampling frequency of the
        signal must be 48000 Hz.
    sb: int or list of int
        block size.
    sh: int or list of int
        Hop size.
    Returns
    -------
    block_array_rect: list of numpy.array
        rectified band-pass signals
    """

    if isinstance(sb, int):
        sb = sb * np.ones(53, dtype=int)
    elif len(sb) != 53:
        raise ValueError("ERROR: len(sb) shall be either 1 or 53")
    if isinstance(sh, int):
        sh = sh * np.ones(53, dtype=int)
    elif len(sh) != 53:
        raise ValueError("ERROR: len(sh) shall be either 1 or 53")

    """ OUTER AND MIDDLE EAR FILTERING (5.1.2)

    It is important to use the "filtfilt" version of the filter in order to reduce the lag in the results.
    The Auditory Filtering Bank must be done by filtering with a non zero-phase filter in order to avoid filtering the
    signal much more than it is intended to.
    """
    sos_ear = ear_filter_design()
    signal_filtered = sp_signal.sosfilt(sos_ear, sig, axis=0)
    # b, a = sp_signal.sos2tf(sos_ear)
    # signal_filtered = sp_signal.lfilter(a, b, sig, axis=0)

    """ AUDITORY FILTERING BANK (5.1.3)

    In the following section, the signal is filtered by a series of 53 asymmetric and overlapping filters. They are 
    supposed to replicate the activation process of the auditory hair cells, and their shape matches the one from the 
    gammatone filters. First, we have to calculate the parameters (central frequency, bandwidth, delay, and "d" 
    coefficient) that are going to define our filter and that are used in the recursive formula number 10. Second, 
    we have to link the critical band rate scale "z", with a certain hop size "sh_array" and its band dependent block 
    size "sb_array" (Table G.1). After that, it comes the coefficient calculation (Formula 11 and 12), in which we 
    compute the values for the filter coefficients (*), and we store them in a list. Finally, the end of this section 
    comes with the filtering of the signal.

    (*) An error in the standard has been found in expressions 13 and 14. The prior paragraph says that in order to 
    obtain the approximation of the band-pass filter, the low-pass filter coefficients shall be modified by adding a 
    negative exponential with the transformation parameters "complex_exponential". If we try to develop the filter with 
    these guidelines, we find that the resulting filter is a low-pass filter, not a band-pass. The actual way of 
    obtaining a band-pass filter by transforming a low-pass filter is to multiply the low pass filter coefficients in 
    time with a positive exponential. After the multiplication we will have complex filter coefficients, we have 2 
    options in order to fix this. Either we make 2 transformations, one to the right and another one to the left, and 
    we adapt the transformation parameter, or we take for granted the last transformation by discarding the complex part 
    of the filter and multiplying by "2" (two transformations) and by a cosine with the original transformation 
    parameter. We decided to implement the second option as they did on ECMA-418-2.
    """
    # Order of the Outer and Middle ear filter
    filter_order_k = 5
    # Sampling frequency
    fs = 48000.00
    # Auditory filters centre frequencies
    centre_freq = gen_auditory_filters_centre_freq()

    block_array_rect = []
    for band_number in range(53):
        # bm_mod, am_mod = gammatone(
        #     centre_freq[band_number], order=filter_order_k, fs=fs
        # )
        bm_mod, am_mod = sp_signal.gammatone(centre_freq[band_number], "fir", fs=fs)

        """ 
        "scipy.signal.lfilter" instead of "scipy.signal.filtfilt" in order to maintain consistency. That process 
        makes possible to obtain a signal "band_pass_signal" that does not line up in time with the original signal 
        because of the non zero-phase filtering of "lfilter", but it has a more appropriate slope than filtfilt. 
        By using filtfilt the slope is that high that filters too much the signal. 
        """
        band_pass_signal = (
            2.0
            * (
                sp_signal.lfilter(
                    bm_mod,
                    am_mod,
                    signal_filtered,
                    axis=0,
                )
            ).real
        )

        """SEGMENTATION OF THE SIGNAL INTO BLOCKS (5.1.4)

        The segmentation of the signal is done in order to obtain results for intervals of time, not for the whole
        duration of the signal. The reason behind this decision resides in the fact that processing the signal in its
        full length at one time could end up in imprecise results. By using a "for loop", we are able to decompose the
        signal array "band_pass_signal_hr" into blocks. "sb_array" is the block size which changes depending on the
        "band_number" in which we are processing the signal. "sh_array" is the step size, the time shift to the next
        block.
        """
        block_array = segmentation_blocks(
            band_pass_signal, sb[band_number], sh[band_number], dim=1
        )

        """RECTIFICATION (5.1.5)

        This part acts as the activation of the auditory nerves when the basilar membrane vibrates in a certain
        direction. In order to rectify the signal we are using "np.clip" which establish a minimum and a maximum value
        for the signal. "a_min" is set to 0 float, while "a_max" is set to "None" in order to consider the positive
        value of the signal.
        """
        block_array_rect.append(np.clip(block_array, a_min=0.00, a_max=None))

    return block_array_rect