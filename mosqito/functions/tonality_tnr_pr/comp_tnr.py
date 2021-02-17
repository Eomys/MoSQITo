# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:51:19 2020

@author: wantysal
"""

import sys

sys.path.append("../../..")

# Standard library imports
import numpy as np
import math
import matplotlib.pyplot as plt

# Local functions imports
from mosqito.functions.tonality_tnr_pr.tnr_main_calc import tnr_main_calc


def comp_tnr(is_stationary, signal, fs, prominence=True, plot=False):
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
    plot : str
        True to plot the results, False to only return the dict

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

        if plot == True:
            plt.figure()
            plt.plot(
                freqs,
                limit,
                color="#e69f00",
                linewidth=2,
                dashes=[6, 2],
                label="Prominence criteria",
            )
            plt.bar(output["freqs"], output["values"], width=10, color="#69c3c5")
            plt.legend(fontsize=16)
            plt.grid(axis="y")
            plt.ylabel("TNR [dB]")

            # Title
            if prominence == True:
                plt.title(
                    "Prominent tones TNR values \n (Total TNR = "
                    + str(np.around(output["global value"], decimals=1))
                    + " dB)",
                    fontsize=16,
                )
            else:
                plt.title(
                    "Discrete tones TNR values \n  (Total TNR = "
                    + str(np.around(output["global value"], decimals=1))
                    + " dB)",
                    fontsize=16,
                )
            plt.legend()

            # Frequency axis
            plt.xlabel("Frequency [Hz]")
            plt.xscale("log")
            xticks_pos = [100, 1000, 10000] + list(output["freqs"])
            xticks_pos = np.sort(xticks_pos)
            xticks_label = [str(elem) for elem in xticks_pos]
            plt.xticks(xticks_pos, labels=xticks_label, rotation=30)

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
        freq_axis = np.logspace(np.log10(90), np.log10(11200), num=1000)
        results = np.zeros((len(freq_axis), nb_frame))
        promi = np.zeros((len(freq_axis), nb_frame), dtype=bool)

        if prominence == True:

            for t in range(nb_frame):
                for f in range(len(tones_freqs[t])):
                    if prom[t][f] == True:
                        ind = np.argmin(np.abs(freq_axis - tones_freqs[t][f]))
                        results[ind, t] = tnr[t][f]
                        promi[ind, t] = True
        else:
            for t in range(nb_frame):
                for f in range(len(tones_freqs[t])):
                    ind = np.argmin(np.abs(freq_axis - tones_freqs[t][f]))
                    results[ind, t] = tnr[t][f]
                    promi[ind, t] = prom[t][f]

        output = {
            "name": "tone-to-noise ratio",
            "time": time,
            "freqs": freq_axis,
            "values": results,
            "prominence": promi,
            "global value": t_tnr,
        }

        # Plot option
        if plot == True:
            plt.figure()
            plt.pcolormesh(results, vmin=0)
            plt.colorbar(label="TNR value in dB")
            if prominence == True:
                plt.title(
                    "Tone-to-noise ratio along time and frequency (prominent tones only)",
                    fontsize=14,
                )
            else:
                plt.title(
                    "Tone-to-noise ratio along time and frequency (all discrete tones)",
                    fontsize=14,
                )
            plt.xlabel("Time [s]")
            plt.ylabel("Frequency [Hz]")

            # Frequency axis
            freq_labels = [90, 200, 500, 1000, 2000, 5000, 10000]
            freq_ticks = []
            for i in range(len(freq_labels)):
                freq_ticks.append(np.argmin(np.abs(freq_axis - freq_labels[i])))
            plt.yticks(freq_ticks, labels=[str(elem) for elem in freq_labels])

            # Time axis
            plt.xticks(np.arange(nb_frame), labels=[str(elem) for elem in time])

    return output