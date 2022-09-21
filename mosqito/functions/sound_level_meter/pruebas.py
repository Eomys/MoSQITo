# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 11:02:48 2020

@author: wantysal
"""

# Third party imports
from sqlite3 import dbapi2
from this import d
import numpy as np

# Local imports
from Leq_3oct import Leq_3oct
from mosqito.utils.conversion import spectrum2dBA
from  mosqito.utils.load import load
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
from mosqito.utils.conversion import amp2db

# -----------------------------------dB <-> dBA---------------------------------


def spectrum2dBA(spectrum, fs):
    """A_weighting dB ponderation of a spectrum according to CEI 61672:2014

    Third-octave spectrum are directly calculated, other are calculated
    using linear interpolation.

    Parameters
    ----------
    spectrum: numpy.array
              input spectrum
    fs: integer
        sampling frequency

    """

    # Ponderation coefficients from the standard
    A_standard = np.array(
        [
            -70.4,
            -63.4,
            -56.7,
            -50.5,
            -44.7,
            -39.4,
            -34.6,
            -30.2,
            -26.2,
            -22.5,
            -19.1,
            -16.1,
            -13.4,
            -10.9,
            -8.6,
            -6.6,
            -4.8,
            -3.2,
            -1.9,
            -0.8,
            0,
            0.6,
            1,
            1.2,
            1.3,
            1.2,
            1,
            0.5,
            -0.1,
            -1.1,
            -2.5,
            -4.3,
            -6.6,
            -9.3,
        ]
    )

    freq_standard = np.array(
        [
            10,
            12.5,
            16,
            20,
            25,
            31.5,
            40,
            50,
            63,
            80,
            100,
            125,
            160,
            200,
            250,
            315,
            400,
            500,
            630,
            800,
            1000,
            1250,
            1600,
            2000,
            2500,
            3150,
            4000,
            5000,
            6300,
            8000,
            10000,
            12500,
            16000,
            20000,
        ]
    )

    print("ENTRA ESTO")
    print(spectrum)

    # Linear interpolation on the spectrum axis
    spectrum_freq_axis = np.linspace(0, int(fs / 2), spectrum.size)
    print("spectrum.size")
    print(spectrum.size)
    print("spectrum_freq_axis")
    print(spectrum_freq_axis)
    A_pond = np.interp(spectrum_freq_axis, freq_standard, A_standard)
    print("A_pond")
    print(A_pond)
    # Ponderation of the given spectrum
    spectrum_dBA = np.zeros(spectrum.shape)
    for i in range(spectrum.shape[0]):
        spectrum_dBA[i] = spectrum[i] + A_pond[i]

    print(spectrum_dBA)
    #return spectrum_dBA

if __name__ == "__main__":
    
    sig, fs = load(r"tests\input\Test signal 5 (pinknoise 60 dB).wav")

    f_min = 25
    f_max = 20000

    spectrum_signal_1 = noct_spectrum(sig,fs,f_min,f_max)[0]
    spectrum_signal_2 = noct_spectrum(sig,fs,f_min,f_max)[0]
    spectrum_signal_3 = noct_spectrum(sig,fs,f_min,f_max)[0]
    spectrum_all_signals = np.stack((spectrum_signal_1,spectrum_signal_2,spectrum_signal_3), axis=1)
    spectrum_all_signals_dB = np.zeros(spectrum_all_signals.shape)

    freq = np.array(noct_spectrum(sig,fs,f_min,f_max)[1])

    prueba = np.array([70.0])


    for i in range(spectrum_all_signals.shape[1]):
        # For each value in the column (signal) a conversion to dB is performed.
        for j in range(freq.shape[0]): 
            # Conversion Pa to dB
            dB = amp2db(spectrum_all_signals[j][i])
            # Save the values in dB in another array
            spectrum_all_signals_dB[j][i] = dB
        # Conversion Pa to dB

        #dBA = spectrum2dBA(sig, fs)
        #dBA = spectrum2dBA(spectrum_all_signals_dB[:,i])
        dBA = spectrum2dBA(prueba, 200)
        print(dBA)
    pass