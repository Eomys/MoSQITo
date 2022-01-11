# -*- coding: utf-8 -*-
"""
    Author: Cristina Taboada (TinaTabo)
    Start date: 17/11/2021
"""

# Local imports
from mosqito.functions.oct3filter.comp_third_spectrum import comp_third_spec
from mosqito.functions.shared.load import load


def comp_tonality(signal, fs):
    """
    <Function to obtain the prominent tones of a given signal 
    according to the procedure described in ISO 1996-2 Annex K.>

    Parameters
    ----------
    signal : numpy.array
        time signal values
    fs : integer
        sampling frequency

    Outputs
    -------
    prominent_tones: dictionary
        dictionary with {fc:Lp} pairs where prominent tones are detected.
    """

    #-- we obtain the data of the Lp in thirds of octave of the signal of which 
    #-- we want to know the prominent tones
    third_spec = comp_third_spec(is_stationary=True, signal=signal, fs=fs)

    # -- Obtain the lists of the central frequencies and the average Lp
    freqs = third_spec["freqs"]
    values = third_spec["values"]

    #-- list of center frequencies
    fc = freqs.tolist()

    #-- list of the average Lp corresponding to each third octave band
    Lp_mean = values.tolist()

    #-- Lp_mean is a list of lists, we create 
    #-- a single list with the data of each list.
    Lp = []
    for i in range (0, len(Lp_mean)):
        level = Lp_mean[i][0]
        Lp.append(level)
    

    """-------BORRAR AL FINAL-------"""
    #print(fc)
    #print(Lp)
    """-----------------------------"""

    # -- List where the indexes corresponding to the positions where there is 
    # -- a prominent tone will be stored.
    index_tone_list = []

    #-- length of the lists
    idx = len(fc) - 1

    #-- level differences depending on the frequency range to determine if there 
    #-- is a prominent pitch.
    diff_low_freqs = 15.0
    diff_medium_freqs = 8.0
    diff_high_freqs = 5.0

    for x in range(0, idx):
        # -- Variables to compare
        if x == 0:
            Lp_prev = 0
            Lp_central = abs(Lp[x])
            Lp_post = abs(Lp[x + 1])
        else:
            Lp_prev = abs(Lp[x - 1])
            Lp_central = abs(Lp[x])
            Lp_post = abs(Lp[x + 1])

        #-- calculate the difference
        Lp_diff_prev = Lp_central - Lp_prev
        Lp_diff_post = Lp_central - Lp_post

        """----------BORRAR AL FINAL-----------"""
       # print("++++++++++++++++++")
       # print(Lp_diff_prev)
       # print(Lp_diff_post)
       # print("++++++++++++++++++")
        """------------------------------------"""


        #-- if the value of the difference is constant with respect to the bands below and above 
        #-- the one studied, we obtain the value of the difference and proceed to check if we have 
        #-- found a prominent tone.

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
        elif x > fc.index(400.0) and x < fc.index(12500.0):
            # -- "HIGH FREQUENCY --> 5 dB difference".
            if Lp_diff_prev >= diff_high_freqs and Lp_diff_post >= diff_high_freqs:
                # -- there is a tone in x, we store its value.
                index_tone_list.append(x)

    # -- Dictionary in which the data corresponding to the prominent tones 
    # -- will be stored, i.e. {fc : Lp_mean}
    prominent_tones = {}

    for i in range(0, len(index_tone_list)):
        index = index_tone_list[i]
        key = fc[index]
        value = Lp[index]
        prominent_tones[key] = value

    # -- Return of the function.
    return prominent_tones


#-- Main call to the function for its execution.
if __name__ == "__main__":

    #-- CORRECTO --
    """----PRUEBA--TONO--100-Hz----"""
    sig, fs = load(True, "tests\input\TONE100HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")

    #-- CORRECTO --
    """----PRUEBA--TONO--200-Hz----"""
    sig, fs = load(True, "tests\input\TONE200HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")

    #-- CORRECTO --
    """----PRUEBA--TONO--1-KHz----"""
    sig, fs = load(True, "tests/input/1KHZ60DB.WAV", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")

    #-- CORRECTO --
    """----PRUEBA--TONO--2-KHz----"""
    sig, fs = load(True, "tests\input\TONE2000HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")

    #-- CORRECTO --
    """----PRUEBA--TONO--4-KHz----"""
    sig, fs = load(True, "tests\input\TONE4000HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")

    #-- CORRECTO --
    """----PRUEBA--TONO--5000-Hz----"""
    sig, fs = load(True, "tests\input\TONE5000HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")

    pass