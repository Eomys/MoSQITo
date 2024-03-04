# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:17:27 2020

@author: wantysal
"""
# Standard library import
import numpy as np
from scipy.io.wavfile import write


def signal_test_roughness(fc, fmod, mdepth, fs, d, dB):
    """Creation of stationary amplitude modulated signals for the roughness
    validation procedure (signal created according to equation 1 in
    "Psychoacoustical roughness:implementation of an optimized model"
    by Daniel and Weber in 1997.

    Parameters
    ----------
    fc: integer
        carrier frequency
    fmod: integer
        modulation frequency
    mdepth: float
        modulation depth
    fs: integer
        sampling frequency
    d: float
        signal duration [s]
    dB: integer
        SPL dB level of the carrier signal
    """

    # time axis definition
    dt = 1 / fs
    time = np.arange(0, d, dt)

    signal = (
        0.5
        * (1 + mdepth * (np.sin(2 * np.pi * fmod * time)))
        * np.sin(2 * np.pi * fc * time)
    )
    rms = np.sqrt(np.mean(np.power(signal, 2)))
    ampl = 0.00002 * np.power(10, dB / 20) / rms
    signal = signal * ampl

    return signal, time

def signal_test_tonality(f, L, fs, d, dB):
    """Creation of stationary amplitude modulated signals for the roughness
    validation procedure (signal created according to equation 1 in
    "Psychoacoustical roughness:implementation of an optimized model"
    by Daniel and Weber in 1997.

    Parameters
    ----------
    f: [integer]
        tones frequency
    L: [float]
        tones level
    fs: integer
        sampling frequency
    d: float
        signal duration [s]
    dB: integer
        SPL dB level of the carrier signal
    """

    # time axis definition
    dt = 1 / fs
    time = np.arange(0, d, dt)
    signal = np.zeros((len(time)))
    for i in range(len(f)):
        signal += L[i] * np.sin(2 * np.pi * f[i] * time)
    rms = np.sqrt(np.mean(np.power(signal, 2)))
    ampl = 0.00002 * np.power(10, dB / 20) / rms
    signal = signal * ampl

    return signal, time

def wav_test_roughness(fc, fmod, mdepth, fs, d, dB, folder):
    """Creation of .wav file of stationary amplitude modulated signals for the roughness
    validation procedure (signal created according to equation 1 in
    "Psychoacoustical roughness:implementation of an optimized model"
    by Daniel and Weber in 1997.

    Parameters
    ----------
    fc: integer
        carrier frequency
    fmod: integer or numpy.array
        modulation frequency
    mdepth: float
        modulation depth
    fs: integer
        sampling frequency
    d: float
        signal duration [s]
    dB: integer
        SPL dB level of the carrier signal
    folder: string
        path of the folder where to store the file
    """

    values, _ = signal_test_roughness(fc, fmod, mdepth, fs, d, dB)
    values = values * (2 ** 15 - 1)
    values = values.astype(np.int16)
    write(
        folder + "/Test_signal_fc" +
        str(fc) + "_fmod" + str(fmod) + ".wav", fs, values
    )
    
    
def wav_test_tonality(f, L, fs, d, dB, folder):
    """Creation of .wav file of stationary amplitude modulated signals for the roughness
    validation procedure (signal created according to equation 1 in
    "Psychoacoustical roughness:implementation of an optimized model"
    by Daniel and Weber in 1997.

    Parameters
    ----------
    fc: integer
        carrier frequency
    fmod: integer or numpy.array
        modulation frequency
    mdepth: float
        modulation depth
    fs: integer
        sampling frequency
    d: float
        signal duration [s]
    dB: integer
        SPL dB level of the carrier signal
    folder: string
        path of the folder where to store the file
    """

    values, _ = signal_test_tonality(f, L, fs, d, dB)
    if np.isnan(values).any():
        print("NAN !")
    # values = values / (2 * 2 ** 0.5)
    # values = values.astype(np.int16)
    write(
        folder + "/Test_signal_f" +
        str(f) + ".wav", fs, values*10
    )

if __name__ == "__main__":
    fc = [125,250,500,1000,2000,4000,8000]
    fmod = [20,30,40,50,60,70,80,90,100,120,140,160,200,300,400]
    for i in range(len(fc)):
        for j in range(len(fmod)):
            wav_test_roughness(fc[i], fmod[j], mdepth=1, fs=48000, d=2, dB=60, folder=r"C:\Users\SaloméWanty\Documents\Mosqito_roughness")
            
    # f = [[100,200,1000],[100,120,250,300,314,400,4000], [1000,1118],[442,4420,4620]]
    # L = [[0.5,0.2,0.1],[0.43,0.54,0.6,0.8,0.1,0.34,0.72], [0.3,0.7],[0.3,0.5,0.6]]
    # for i in range(4):
    #     wav_test_tonality(f[i], L[i], fs=48000, d=2, dB=60, folder=r"F:\tonality")
        
