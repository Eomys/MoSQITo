# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 10:34:04 2020

@author: wantysal
"""

# Standard imports
import numpy as np
from numpy.fft import fft, ifft
import math

# Local imports
from mosqito.functions.shared.LTQ import LTQ
from mosqito.functions.roughness_danielweber.gzi_weighting_function import (
    gzi_definition,
)
from mosqito.functions.roughness_danielweber.H_weighting_function import H_function
from mosqito.functions.roughness_danielweber.a0_zwicker import a0tab
from mosqito.functions.shared.conversion import freq2bark, db2amp, amp2db, bark2freq


def comp_roughness(signal, fs, overlap):
    """Roughness calculation of a signal sampled at 48kHz.

    The code is based on the algorithm described in "Psychoacoustical roughness:
    implementation of an optimized model" by Daniel and Weber in 1997.
    The roughness model consists of a parallel processing structure that is made up
    of successive stages and calculates intermediate specific roughnesses R_spec,
    which are summed up to determine the total roughness R.

    Parameters
    ----------
    signal : numpy.array
        signal amplitude values along time
    fs : integer
        sampling frequency
    overlap : float
        overlapping coefficient for the time windows of 200ms

    Outputs
    -------
    R : numpy.array
        roughness
    time : numpy.array
           time axis

    """
    print("Roughness is being calculated")

    # -----------------------------------Stage 0------------------------------------
    # -------Creation of overlapping frames of 200 ms from the input signal---------

    # Number of points within each frame according to the time resolution of 200ms
    n = int(0.2 * fs)

    # Number of frames according to the given overlap proportion
    nb_frame = math.floor(signal.size / ((1 - overlap) * n)) - 1

    if nb_frame == 0:
        nb_frame = 1

    # Creation of the corresponding time axis
    time = np.linspace(0, len(signal) / fs, num=nb_frame)

    # Initialization of the weighting functions H and g
    hWeight = H_function(n, fs)
    # Aures modulation depth weighting function
    gzi = gzi_definition(np.arange(1, 48, 1) / 2)

    R = np.zeros((nb_frame))
    for i_frame in range(nb_frame):
        segment = signal[
            i_frame * int(n * (1 - overlap)) : i_frame * int(n * (1 - overlap)) + n
        ]

        # Calculate Blackman analysis window
        window = np.blackman(n)
        window = window / sum(window)

        # Creation of the spectrum by FFT using the Blackman window
        spectrum = fft(segment * window) * 1.42
        # Highest frequency
        nMax = round(n / 2)
        nZ = np.arange(1, nMax + 1, 1)
        # Frequency axis in Hertz
        freqs = np.arange(1, nMax + 1, 1) * (fs / n)
        # Frequency axis in Bark
        barks = freq2bark(freqs)

        # Calculate Zwicker a0 factor (transfer characteristic of the outer and inner ear)
        a0 = np.zeros((n))
        a0[nZ - 1] = db2amp(a0tab(barks), ref=1)
        spectrum = a0 * spectrum

        # Conversion of the spectrum into dB
        module = abs(spectrum[0:nMax])
        spec_dB = amp2db(module, ref=0.00002)

        # Find the audible components within the spectrum
        threshold = LTQ(barks, reference="roughness")
        audible_index = np.where(spec_dB > threshold)[0]
        # Number of audible frequencies
        n_aud = len(audible_index)

        # --------------------------------- stage 1 ------------------------------------
        # ----------------Creation of the specific excitations functions----------------

        # Terhardt's slopes definition
        # lower slope [dB/Bark]
        s1 = -27
        s2 = np.zeros((n_aud))
        # upper slope [dB/Bark]
        for k in np.arange(0, n_aud, 1):
            s2[k] = min(
                -24
                - (230 / freqs[audible_index[k]])
                + (0.2 * spec_dB[audible_index[k]]),
                0,
            )

        # The excitation pattern are calculated for 47 overlapping 1-bark-wide channels
        n_channel = 47
        # Channels number
        zi = np.arange(1, n_channel + 1) / 2
        # Center frequencies for each channel
        zb = bark2freq(zi) * n / fs
        # Minimum excitation level
        minExcitDB = np.interp(zb, nZ, threshold)

        ch_low = np.zeros((n_aud))
        ch_high = np.zeros((n_aud))
        for i in np.arange(0, n_aud):
            # Lower limit of the channel corresponding to each component
            ch_low[i] = math.floor(2 * barks[audible_index[i]]) - 1
            # Higher limit
            ch_high[i] = math.ceil(2 * barks[audible_index[i]]) - 1

        # Creation of the excitation pattern
        slopes = np.zeros((n_aud, n_channel))
        for k in np.arange(0, n_aud):
            levDB = spec_dB[audible_index[k]]
            b = barks[audible_index[k]]
            for j in np.arange(0, int(ch_low[k] + 1)):
                sl = (s1 * (b - ((j + 1) * 0.5))) + levDB
                if sl > minExcitDB[j]:
                    slopes[k, j] = db2amp(sl, ref=0.00002)
            for j in np.arange(int(ch_high[k]), n_channel):
                sl = (s2[k] * (((j + 1) * 0.5) - b)) + levDB
                if sl > minExcitDB[j]:
                    slopes[k, j] = db2amp(sl, ref=0.00002)

        # Initialization
        hBP = np.zeros((n_channel, n))
        mod_depth = np.zeros((n_channel))

        # Definition of the excitation amplitude
        for i in np.arange(0, n_channel, 1):
            exc = np.zeros((n), dtype=complex)
            for j in np.arange(0, n_aud, 1):
                ind = audible_index[j]
                # the component belongs to the bark window
                if ch_low[j] == i:
                    ampl = 1
                elif ch_high[j] == i:
                    ampl = 1
                # the component is higher than the bark window
                elif ch_high[j] > i:
                    ampl = slopes[j, i + 1] / module[ind]
                # the component is lower than the considered window
                else:
                    ampl = slopes[j, i - 1] / module[ind]

                # reconstruction of the spectrum
                exc[ind] = ampl * spectrum[ind]

            # The temporal specific excitation functions are obtained by IFFT
            temporal_excitation = np.abs(n * np.real(ifft(exc)))

            # ------------------------------- stage 2 --------------------------------------
            # ---------------------modulation depth calculation-----------------------------

            # The fluctuations of the envelope are contained in the low frequency part
            # of the spectrum of specific excitations in absolute value
            h0 = np.mean(temporal_excitation)
            envelope_spec = fft(temporal_excitation - h0)

            # This spectrum is weighted to model the low-frequency  bandpass
            # characteristic of the roughness on modulation frequency
            envelope_spec = envelope_spec * hWeight[i, :]

            # The time functions of the bandpass filtered envelopes hBPi(t)
            # are calculated via inverse Fourier transform :
            hBP[i, :] = 2 * np.real(ifft(envelope_spec))

            # Modulation depth estimation is given by envelope RMS values
            # and excitation functions time average :
            hBPrms = np.sqrt(np.mean(np.power(hBP[i, :], 2)))
            if h0 > 0:
                mod_depth[i] = hBPrms / h0
                if mod_depth[i] > 1:
                    mod_depth[i] = 1
            else:
                mod_depth[i] = 0

        # ------------------------------- stage 3 --------------------------------------
        # ----------------roughness calculation with cross correlation------------------

        # Crosscorrelation coefficients between the envelopes of the channels
        # i and i+2 with dz= 1 bark
        ki = np.zeros((47))

        for i in range(0, 45):
            if hBP[i].all() != 0 and hBP[i + 2].all() != 0:
                ki[i] = np.corrcoef(hBP[i, :], hBP[i + 2, :])[0, 1]

        # Specific roughness calculation with gzi the modulation depth weighting
        # function given by Aures
        R_spec = np.zeros((47))

        R_spec[0] = gzi[0] * pow(mod_depth[0] * ki[0], 2)
        R_spec[1] = gzi[1] * pow(mod_depth[1] * ki[1], 2)
        for i in np.arange(2, 45):
            R_spec[i] = gzi[i] * pow(mod_depth[i] * ki[i] * ki[i - 2], 2)
        R_spec[45] = gzi[45] * pow(mod_depth[45] * ki[43], 2)
        R_spec[46] = gzi[46] * pow(mod_depth[46] * ki[44], 2)

        # Total roughness calculation with calibration factor of 0.25 given in the article
        # to produce a roughness of 1 asper for a 1-kHz, 60dB tone with carrier frequency
        # of 70 Hz and a modulation depth of 1

        R[i_frame] = 0.25 * sum(R_spec)

        output = {
            "name": "Roughness",
            "values": R,
            "time": time,
        }

    return output
