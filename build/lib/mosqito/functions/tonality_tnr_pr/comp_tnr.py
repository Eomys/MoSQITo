# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:51:19 2020

@author: wantysal
"""


# Standard library imports
import numpy as np
import math

# Local functions imports
from mosqito.functions.tonality_tnr_pr.tnr_main_calc import tnr_main_calc


def comp_tnr(is_stationary, signal, fs, prominence=True):
    """Computation of tone-to-noise ration according to ECMA-74, annex D.9
        The T-TNR value is calculated according to ECMA-TR/108

    Parameters
    ----------
    is_stationary : boolean
        True if the signal is stationary
    signal :numpy.array
        time signal values
    fs : integer
        sampling frequency
    prominence : boolean
        if True, the algorithm only returns the prominent tones, if False it returns all tones detected

    Output
    ------
    output = dict
    {    "name" : "tone-to-noise ratio",
         "time" : np.linspace(0, len(signal)/fs, num=nb_frame),
         "freqs" : <frequency of the tones>
         "values" : <TNR calculated value for each tone>
         "prominence" : <True or False according to ECMA criteria>
         "global value" : <sum of the specific TNR values>
            }


    """
    # Prominence criteria
    freqs = np.arange(90, 11200, 100)
    limit = np.zeros((len(freqs)))
    for i in range(len(freqs)):
        if freqs[i] >= 89.1 and freqs[i] < 1000:
            limit[i] = 8 + 8.33 * np.log10(1000 / freqs[i])
        if freqs[i] >= 1000 and freqs[i] < 11200:
            limit[i] = 8

    if is_stationary == True:
        tones_freqs, tnr, prom, t_tnr = tnr_main_calc(signal, fs)

        tones_freqs = tones_freqs.astype(int)

        if prominence == True:
            output = {
                "name": "tone-to-noise ratio",
                "freqs": tones_freqs[prom],
                "values": tnr[prom],
                "prominence": True,
                "global value": t_tnr,
            }

        else:
            output = {
                "name": "tone-to-noise ratio",
                "freqs": tones_freqs,
                "values": tnr,
                "prominence": prom,
                "global value": t_tnr,
            }

    if is_stationary == False:
        # Signal cut in frames of 200 ms along the time axis
        n = 0.5 * fs
        nb_frame = math.floor(signal.size / n)
        time = np.linspace(0, len(signal) / fs, num=nb_frame)
        time = np.around(time, 1)

        # Initialization of the result arrays
        tones_freqs = np.zeros((nb_frame), dtype=list)
        tnr = np.zeros((nb_frame), dtype=list)
        prom = np.zeros((nb_frame), dtype=list)
        t_tnr = np.zeros((nb_frame))

        # Calculate TNR values along time
        for i_frame in range(nb_frame):
            segment = signal[int(i_frame * n) : int(i_frame * n + n)]
            (
                tones_freqs[i_frame],
                tnr[i_frame],
                prom[i_frame],
                t_tnr[i_frame],
            ) = tnr_main_calc(segment, fs)

        # Store the results in a time vs frequency array
        freqs = np.logspace(np.log10(90), np.log10(11200), num=1000)
        results = np.zeros((len(freqs), nb_frame))
        promi = np.zeros((len(freqs), nb_frame), dtype=bool)

        if prominence == True:

            for t in range(nb_frame):
                for f in range(len(tones_freqs[t])):
                    if prom[t][f] == True:
                        ind = np.argmin(np.abs(freqs - tones_freqs[t][f]))
                        results[ind, t] = tnr[t][f]
                        promi[ind, t] = True
        else:
            for t in range(nb_frame):
                for f in range(len(tones_freqs[t])):
                    ind = np.argmin(np.abs(freqs - tones_freqs[t][f]))
                    results[ind, t] = tnr[t][f]
                    promi[ind, t] = prom[t][f]

        output = {
            "name": "tone-to-noise ratio",
            "time": time,
            "freqs": freqs,
            "values": results,
            "prominence": promi,
            "global value": t_tnr,
        }

    return output
