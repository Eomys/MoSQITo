# -*- coding: utf-8 -*-
"""
    Author: Cristina Taboada (TinaTabo)
    Start date: 17/11/2021 
"""
# Standard library imports
import math

# Local imports
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum


def comp_tonality(sig, fs):
    """
    <Function to obtain the prominent tones of a given signal
    according to the procedure described in ISO 1996-2 Annex K.>

    Parameters
    ----------
    sig : numpy.array
        time signal values
    fs : integer
        sampling frequency

    Outputs
    -------
    prominent_tones: dictionary
        dictionary with {fc:Lp_dB} pairs where prominent tones are detected.
    """


    #-- As the tonality is studied for the audible frequency range, 
    #-- we set the minimum and maximum frequencies at 25 Hz and 20 kHz.
    fmin = 25
    fmax = 10000

    # -- we obtain the data of the Lp in Pa in thirds of octave of the signal of which
    # -- we want to know the prominent tones
    third_spec = noct_spectrum(sig=sig, fs=fs, fmin=fmin, fmax=fmax)

    #-- Returns a tuple with two arrays, one with the Lp_Pa of each third octave band 
    #-- and the other with the center frequencies, fc, of each band.
    #-- Convert tuple to list for further processing
    third_spec = list(third_spec)

    # -- Obtain the lists of the central frequencies and the average Lp
    fc = third_spec[1].tolist()
    Lp_Pa = third_spec[0].tolist()

    #-- Create a list with the Lp conversion in dB.
    Lp_dB = []
    P_ref = 2e-05
    for i in range(0, len(Lp_Pa)):
        P = Lp_Pa[i][0]
        level = 20*math.log10(P/P_ref)
        Lp_dB.append(level)

    # -- List where the indexes corresponding to the positions where there is
    # -- a prominent tone will be stored.
    index_tone_list = []

    # -- length of the lists
    idx = len(fc) - 1

    # -- level differences depending on the frequency range to determine if there
    # -- is a prominent pitch.
    diff_low_freqs = 15.0
    diff_medium_freqs = 8.0
    diff_high_freqs = 5.0

    for x in range(0, idx):
        # -- Variables to compare
        if x == 0:
            Lp_prev = 0
            Lp_central = abs(Lp_dB[x])
            Lp_post = abs(Lp_dB[x + 1])
        else:
            Lp_prev = abs(Lp_dB[x - 1])
            Lp_central = abs(Lp_dB[x])
            Lp_post = abs(Lp_dB[x + 1])

        # -- calculate the difference
        Lp_diff_prev = Lp_central - Lp_prev
        Lp_diff_post = Lp_central - Lp_post

        # -- if the value of the difference is constant with respect to the bands below and above
        # -- the one studied, we obtain the value of the difference and proceed to check if we have
        # -- found a prominent tone.

        if x > fc.index(25.0) and x < fc.index(160.0):
            # -- "LOW FREQUENCY --> difference 15 dB".
            if Lp_diff_prev >= diff_low_freqs and Lp_diff_post >= diff_low_freqs:
                # -- there is a tone in x, we store its value.
                index_tone_list.append(x)

        elif x > fc.index(125.0) and x < fc.index(500.0):
            # -- "HALF FREQUENCY --> difference 8 dB"
            if Lp_diff_prev >= diff_medium_freqs and Lp_diff_post >= diff_medium_freqs:
                # -- there is a tone in x, we store its value.
                index_tone_list.append(x)
        elif x > fc.index(400.0) and x < fc.index(10000.0):
            # -- "HIGH FREQUENCY --> 5 dB difference".
            if Lp_diff_prev >= diff_high_freqs and Lp_diff_post >= diff_high_freqs:
                # -- there is a tone in x, we store its value.
                index_tone_list.append(x)

    # -- Dictionary in which the data corresponding to the prominent tones
    # -- will be stored, i.e. {fc : Lp_dB}
    prominent_tones = {}

    for i in range(0, len(index_tone_list)):
        index = index_tone_list[i]
        key = fc[index]
        value = Lp_dB[index]
        prominent_tones[key] = value

    # -- Return of the function.
    return prominent_tones
    