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
    sig: numpy.array
        time signal in Pa. The sampling frequency of the signal must be 48000 Hz.
    sb: int or list of int
        block size.
    sh: int or list of int
        Hop size.
    Returns
    -------
    block_array_rect: numpy.array
        rectified band-pass signals (size: N_bark x N_block x sb)
    """

    if isinstance(sb, int):
        sb = sb * np.ones(53, dtype=int)
    elif len(sb) != 53:
        raise ValueError("ERROR: len(sb) shall be either 1 or 53")
    if isinstance(sh, int):
        sh = sh * np.ones(53, dtype=int)
    elif len(sh) != 53:
        raise ValueError("ERROR: len(sh) shall be either 1 or 53")

    # OUTER AND MIDDLE EAR FILTERING (ECMA 418-2 section 5.1.2)

    sos_ear = ear_filter_design()
    signal_filtered = sp_signal.sosfilt(sos_ear, sig, axis=0)

    # AUDITORY FILTERING BANK (ECMA 418-2 section 5.1.3)

    # Auditory filters centre frequencies
    centre_freq = gen_auditory_filters_centre_freq()

    block_array_rect = []
    for band_number in range(53):
        # Compute the filter coefficient for the current critical band
        bm_mod, am_mod = gammatone(centre_freq[band_number])
        # Filter the signal
        band_pass_signal = sp_signal.lfilter(
            bm_mod,
            am_mod,
            signal_filtered,
            axis=0,
        )
        band_pass_signal = 2.0 * band_pass_signal.real

        # SEGMENTATION OF THE SIGNAL INTO BLOCKS (ECMA 418-2 section 5.1.4)

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

    block_array_rect = np.array(block_array_rect)
    return block_array_rect