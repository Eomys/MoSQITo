# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.signal import welch

# Project Imports
from mosqito.functions.shared.load import load
from mosqito.functions.hearing_model.sine_wave_generator import sine_wave_generator
from mosqito.functions.hearing_model.ear_filter_design import ear_filter_design
from mosqito.functions.hearing_model.gen_auditory_filters_centre_freq import (
    gen_auditory_filters_centre_freq,
)
from mosqito.functions.hearing_model.gammatone import gammatone
from mosqito.functions.hearing_model.afb_ppal_parameters import afb_ppal_parameters
from mosqito.functions.hearing_model.segmentation_blocks import segmentation_blocks
from mosqito.functions.hearing_model.segmentation_blocks import (
    segmentation_blocks_test_a,
)
from mosqito.functions.hearing_model.segmentation_blocks import (
    segmentation_blocks_test_b,
)
from mosqito.functions.hearing_model.nonlinear_common import nonlinear_common
from mosqito.functions.hearing_model.nonlinear_repeat import nonlinear_repeat
from mosqito.functions.hearing_model.sone2phone import sone2phone
from mosqito.functions.hearing_model.sl_validation import annex_f_validation

import sys

sys.path.append("../../..")


def comp_loudness(signal, validation=False):
    """Calculation of specific loudness and total loudness of an input signal according to ECMA-418-2. It describes the
    loudness excitation in a critical band per Bark. The output of the signal consists in a pair of array lists, one
    for specific loudness and the other one for total loudness.

    Parameters
    ----------
    validation: boolean
        Default value is set to 'False'. It is used to mark whether complete validation is done or not.

    signal: numpy.array
        'Pa', time signal values. It can be, stereo (2 dimensions) or mono (1 dimension).The sampling frequency of the
        signal must be 48000 Hz.

    Returns
    -------
    n_array: numpy.array
        'Sone per Bark'. It is a numpy array that is arranged as a matrix. Each matrix row represents a certain block of
        audio (in chronological order) and each matrix column stores the value of the specific loudness for that block
        and that specific band (column number). If the input signal is stereo, another matrix dimension is added.

    t_array: numpy.array
        'Sone per Bark'. As well as "n_array", it is a numpy array that is arranged as a matrix. Each matrix row
        represents a certain block of audio (in chronological order). If the input signal is stereo, another matrix
        dimension is added.
    """
    """ CONSTANTS AND VARIABLES

    First, we are going to define some of the variables and constants that are needed in order to run our code, 
    section by section.
    """
    # Signal dimensions
    dim = signal.ndim

    """ CONSIDERATION OF THRESHOLD IN QUIET """
    # "The specific loudness in each band z is zero if it is at or below a critical-band-dependent specific loudness
    # threshold LTQ(z)"
    ltq_z = [
        0.3310,
        0.1625,
        0.1051,
        0.0757,
        0.0576,
        0.0453,
        0.0365,
        0.0298,
        0.0247,
        0.0207,
        0.0176,
        0.0151,
        0.0131,
        0.0115,
        0.0103,
        0.0093,
        0.0086,
        0.0081,
        0.0077,
        0.0074,
        0.0073,
        0.0072,
        0.0071,
        0.0072,
        0.0073,
        0.0074,
        0.0076,
        0.0079,
        0.0082,
        0.0086,
        0.0092,
        0.0100,
        0.0109,
        0.0122,
        0.0138,
        0.0157,
        0.0172,
        0.0180,
        0.0180,
        0.0177,
        0.0176,
        0.0177,
        0.0182,
        0.0190,
        0.0202,
        0.0217,
        0.0237,
        0.0263,
        0.0296,
        0.0339,
        0.0398,
        0.0485,
        0.0622,
    ]

    """ AUDITORY FILTERING BANK """
    # Order of the Outer and Middle ear filter
    filter_order_k = 5
    # Sampling frequency
    fs = 48000.00
    d_coefficients_array = []
    # Step size
    z_step_size = 0.50
    # Centre frequencies F(z), 26.5/0.5 = 53
    centre_freq_array = []
    # F Bandwidth Af(z)
    f_bandwidth_array = []
    # Retardation
    t_delay_array = []
    # Block length and hop size lists
    sb_array = []
    sh_array = []
    # Coefficients for the "Auditory Filtering Bank" part
    am_mod_coefficient_array = np.zeros((53, int(filter_order_k + 1)), dtype=complex)
    bm_mod_coefficient_array = np.zeros((53, int(filter_order_k + 1)), dtype=complex)
    band_pass_signal_array = []

    """ NON-LINEARITY. SOUND PRESSURE INTO SPECIFIC LOUDNESS """
    p_0 = 2e-5
    # c_N: In sones/bark
    c_N = 0.0217406
    alpha = 1.50
    threshold_db_array = np.array([15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0])
    v_i_array = np.array(
        [1.0, 0.6602, 0.0864, 0.6384, 0.0328, 0.4068, 0.2082, 0.3994, 0.6434]
    )
    M_exponents = len(threshold_db_array)
    a_exponent_array, pt_threshold_array = nonlinear_common(
        p_0, alpha, M_exponents, v_i_array, threshold_db_array
    )

    specific_loudness_all_bands_array = []

    """ TOTAL LOUDNESS """
    total_loudness_array = []

    """ OUTER AND MIDDLE EAR FILTERING (5.1.2)

    It is important to use the "filtfilt" version of the filter in order to reduce the lag in the results.
    The Auditory Filtering Bank must be done by filtering with a non zero-phase filter in order to avoid filtering the
    signal much more than it is intended to.
    """
    sos_ear = ear_filter_design()
    # signal_filtered is pom(n). We have to assign the input signal to the filtered signal in order to implement
    # the "sos" filtering
    signal_filtered = signal
    signal_filtered = sp.signal.sosfiltfilt(sos_ear, signal_filtered, axis=0)

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
    centre_freq = gen_auditory_filters_centre_freq()
    for band_number in range(53):
        (
            bm_mod_coefficient_array[band_number],
            am_mod_coefficient_array[band_number],
        ) = gammatone(centre_freq[band_number], order=5, fs=fs)

        """ 
        "scipy.signal.lfilter" instead of "scipy.signal.filtfilt" in order to maintain consistency. That process 
        makes possible to obtain a signal "band_pass_signal" that does not line up in time with the original signal 
        because of the non zero-phase filtering of "lfilter", but it has a more appropriate slope than filtfilt. 
        By using filtfilt the slope is that high that filters too much the signal. 
        """
        band_pass_signal = (
            2.0
            * (
                sp.signal.lfilter(
                    bm_mod_coefficient_array[band_number],
                    am_mod_coefficient_array[band_number],
                    signal_filtered,
                    axis=0,
                )
            ).real
        )

        """ RECTIFICATION (5.1.5)

        This part acts as the activation of the auditory nerves when the basilar membrane vibrates in a certain 
        direction. In order to rectify the signal we are using "np.clip" which establish a minimum and a maximum value
        for the signal. "a_min" is set to 0 float, while "a_max" is set to "None" in order to consider the positive 
        value of the signal. 
        """
        band_pass_signal_hr = np.clip(band_pass_signal, a_min=0.00, a_max=None)
        band_pass_signal_array.append(band_pass_signal_hr)

        """ SEGMENTATION OF THE SIGNAL INTO BLOCKS (5.1.4)

        The segmentation of the signal is done in order to obtain results for intervals of time, not for the whole 
        duration of the signal. The reason behind this decision resides in the fact that processing the signal in its 
        full length at one time could end up in imprecise results. By using a "for loop", we are able to decompose the 
        signal array "band_pass_signal_hr" into blocks. "sb_array" is the block size which changes depending on the 
        "band_number" in which we are processing the signal. "sh_array" is the step size, the time shift to the next 
        block.
        """
        _, _, _, _, sb, sh = afb_ppal_parameters(fs, band_number, filter_order_k)
        block_array = segmentation_blocks(band_pass_signal_hr, sb, sh, dim)

        """ ROOT-MEAN-SQUARE (5.1.6)

        After the segmentation of the signal into blocks, root-mean square values of each block are calculated in 
        Formula 17). Some of the necessary steps that are general to all of the blocks have been priorly calculated 
        in order to reach a better performance. 
        We have to initialize here "a_array" (array of A values) and "specific_loudness_array" (array of specific 
        loudness values), in order to treat each band-pass signal separately.
        """
        if signal.ndim == 2:
            empty_loudness_array = np.zeros((1, 2), dtype=float)

        else:
            empty_loudness_array = np.zeros((1, 1), dtype=float)

        # Auxiliary array list for loudness assignation before adding the first block
        specific_loudness_aux = []

        for l_number, l_block in enumerate(block_array):
            # The next line makes possible to save the value of the first block that it is not going to be repeated
            if l_number > 0:
                # We have to specify the type of the list in order to avoid some problems reported with this library,
                # where it results in having negative values as output
                rms_factor = np.mean(np.power(l_block.astype(float), 2), axis=0)

                # "rms_block_value" is the result in RMS-values of each block.
                rms_block_value = np.sqrt(2.00 * rms_factor)

                # NEXT PART REMAINS FOR TESTING PURPOSES - band number 17 is the one centered on 1 kHz (1027.0247 Hz)
                # It makes possible to print the RMS value of the block number 10 at 1 kHz, as well as to plot its
                # rectified signal.
                """
                if band_number == 17 and l_number == 10:
                    print('\nTEST - RMS block value at 1027.0247 Hz\n\tRMS block value: ' + str(rms_block_value)
                          + '\n\tCentral Frequency: ' + str(centre_freq)
                          + '\n\tz value: ' + str(z_step_size * band_number))

                    block_time = np.arange(len(l_block)) / fs
                    block_x_limit = len(l_block) / fs

                    plt.figure(figsize=(10, 5))
                    plt.plot(block_time, l_block)
                    plt.xlim(left=0, right=block_x_limit)
                    plt.ylim(bottom=0)
                    plt.xlabel('Time [s]')
                    plt.ylabel('Amplitude [Pa]')
                    plt.title('Rectified signal, block number 10, 1 kHz band')
                    plt.grid(which='both', linestyle='-', color='grey')
                    plt.show()
                    """

                """ NON-LINEARITY (5.1.7)

                This section covers the other part of the calculations needed to consider the non-linear transformation 
                of sound pressure to specific loudness that does the the auditory system. After this point, the 
                computation is done equally to every block in which we have divided our signal. The following loop makes 
                possible the product of the sequence shown in Formula 18. "M_exponents" equals "M", which is the number 
                of given exponents.
                """
                sequence_product = 1.0
                for i_position in range(M_exponents):
                    # "a_base" is used to store the value of the "i_position" element of the sequence
                    a_base = (
                        np.power(
                            (rms_block_value / pt_threshold_array[i_position]), alpha
                        )
                        + 1.00
                    )

                    # The first loop we do not have a previous element in the sequence ("sequence_product"). On each
                    # iteration the previous multiplication is multiplied by a new element
                    sequence_product *= np.power(a_base, a_exponent_array[i_position])

                # "a_value" is the variable used to store the resulting value after the appliance of the non-linearity.
                # It is the same value as the "specific loudness" without consideration of the threshold in quiet
                a_value = c_N * (rms_block_value / p_0) * sequence_product

                """ SPECIFIC LOUDNESS CONSIDERING THE THRESHOLD IN QUIET (5.1.8)

                The next calculation helps us obtain the result for the specific loudness - specific loudness with 
                consideration of the lower threshold of hearing. After all the calculations that have been done, 
                now its time to consider if the signal is stereo or mono. "signal.ndim" gives the number of dimensions 
                that has the array in order to difference mono and stereo calculations. Also, we are using  one-line 
                sentences in order to simplify the reading.

                ** ATTENTION ** This part gives problems later on, if we leave this part as it is it converts negative 
                results to zero. That conversion makes sense but it causes that the Figure 5 is not well represented,
                it will give the same result for values that are lower than the threshold.
                """
                if signal.ndim == 2:
                    left_value = (
                        0.00
                        if (a_value[0] < ltq_z[band_number])
                        else a_value[0] - ltq_z[band_number]
                    )
                    right_value = (
                        0.00
                        if (a_value[1] < ltq_z[band_number])
                        else a_value[1] - ltq_z[band_number]
                    )
                    specific_loudness_aux.append(np.array([left_value, right_value]))

                else:
                    mono_value = (
                        0.00
                        if (a_value < ltq_z[band_number])
                        else a_value - ltq_z[band_number]
                    )

                    specific_loudness_aux.append(np.array([mono_value]))

        # Next step line calls the function "nonlinear_repeat" that wil fill the necessary array slots in order to
        # then rearrange all the bands.
        # "np.insert" adds the empty array to the start of the blocks.
        band_blocks_array = np.insert(
            nonlinear_repeat(np.array(specific_loudness_aux), band_number),
            0,
            empty_loudness_array,
            axis=0,
        )
        # print('Band: ' + str(band_number) + ', length: ' + str(len(band_blocks_array)))

        specific_loudness_all_bands_array.append(band_blocks_array)

    """
    When we did the specific loudness calculation, we did it for all the blocks at a time, band per band. Therefore, 
    we obtained "specific_loudness_allbands_array", which is an array list of specific loudness per bands. In order to 
    obtain arrays in which the elements of every array are the results per band for that specific block of signal, 
    we have to use the "zip" function. "zip" creates new arrays with elements that have the same index.
    """
    n_array = np.array(
        [
            loudness_per_block
            for loudness_per_block in zip(*specific_loudness_all_bands_array)
        ]
    )

    """ TOTAL LOUDNESS (5.1.8)

    Inside the next "for loop", we are calculating the total loudness (Formula 21) for each block of audio in which 
    we divided our signal. After that, we append that value (stereo or mono) to an array list "total_loudness_array". 
    "n_block" is an array of all the N values of each band in that specific audio part (block). After the for loop and 
    the creation of the array list "total_loudness_array", we have to convert that list to a numpy array in order to 
    maintain stereo format when needed.
    """
    for n_block in n_array:
        total_loudness_value = np.sum(n_block, axis=0) * z_step_size
        total_loudness_array.append(total_loudness_value)

    t_array = np.array(total_loudness_array)

    """
    On the one hand, if "validation" is set to default value (False) it does not calculate the complete validation 
    steps. On the other hand, if "validation" is set to True, it runs the validation function.
    """
    if validation:
        annex_f_validation(
            fs,
            signal,
            signal_filtered,
            sos_ear,
            centre_freq_array,
            f_bandwidth_array,
            t_delay_array,
            d_coefficients_array,
            sb_array,
            sh_array,
            am_mod_coefficient_array,
            bm_mod_coefficient_array,
            band_pass_signal_array,
            n_array,
            t_array,
        )

    return n_array, t_array
