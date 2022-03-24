# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 11:02:48 2020

@author: wantysal
"""

# Standard import
import numpy as np


# ----------------------------------Pa <-> dB-----------------------------------
def db2amp(dB, ref=1):
    """Linearisation of a SPL level in dB

    Parameters
    ----------
    dB : numpy.array
        dB values to be converted
    ref: float
        reference value
    """
    if ref == 0:
        raise ValueError("Reference must be different from 0")

    return np.power(10, 0.05 * dB) * ref


def amp2db(amp, ref=1):
    """Conversion of an amplitude value into dB

    Parameters:
    -----------
    amp: np.array
        amplitude values to be converted
    ref: float
        reference value

    """
    if ref == 0:
        raise ValueError("Reference must be different from 0")
    elif ref != 0:
        db = 20 * np.log10(amp / ref)

    return db


# ------------------------------Hertz <-> Bark----------------------------------


def bark2freq(bark_axis):
    """Frequency conversion from Bark to Hertz

     See E. Zwicker, H. Fastl: Psychoacoustics. Springer,Berlin, Heidelberg, 1990.
     The coefficients are linearly interpolated from the values given in table 6.1.

     Parameter
     ---------
     bark_axis : numpy.array
                 Bark frequencies to be converted

     Output
     ------
    freq_axis : numpy.array
                frequencies converted in Hertz

    """

    xp = np.arange(0, 25, 0.5)

    yp = np.array(
        [
            0,
            50,
            100,
            150,
            200,
            250,
            300,
            350,
            400,
            450,
            510,
            570,
            630,
            700,
            770,
            840,
            920,
            1000,
            1080,
            1170,
            1270,
            1370,
            1480,
            1600,
            1720,
            1850,
            2000,
            2150,
            2320,
            2500,
            2700,
            2900,
            3150,
            3400,
            3700,
            4000,
            4400,
            4800,
            5300,
            5800,
            6400,
            7000,
            7700,
            8500,
            9500,
            10500,
            12000,
            13500,
            15500,
            20000,
        ]
    )

    return np.interp(bark_axis, xp, yp)


def freq2bark(freq_axis):
    """Frequency conversion from Hertz to Bark

     See E. Zwicker, H. Fastl: Psychoacoustics. Springer,Berlin, Heidelberg, 1990.
     The coefficients are linearly interpolated from the values given in table 6.1.

     Parameter
     ---------
     freq_axis : numpy.array
                 Hertz frequencies to be converted

     Output
     ------
    bark_axis : numpy.array
               frequencies converted in Bark

    """

    xp = np.array(
        [
            0,
            50,
            100,
            150,
            200,
            250,
            300,
            350,
            400,
            450,
            510,
            570,
            630,
            700,
            770,
            840,
            920,
            1000,
            1080,
            1170,
            1270,
            1370,
            1480,
            1600,
            1720,
            1850,
            2000,
            2150,
            2320,
            2500,
            2700,
            2900,
            3150,
            3400,
            3700,
            4000,
            4400,
            4800,
            5300,
            5800,
            6400,
            7000,
            7700,
            8500,
            9500,
            10500,
            12000,
            13500,
            15500,
            20000,
        ]
    )

    yp = np.arange(0, 25, 0.5)

    return np.interp(freq_axis, xp, yp)


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

    # Linear interpolation on the spectrum axis
    spectrum_freq_axis = np.linspace(0, int(fs / 2), spectrum.size)
    A_pond = np.interp(spectrum_freq_axis, freq_standard, A_standard)

    # Ponderation of the given spectrum
    spectrum_dBA = np.zeros(spectrum.shape)
    for i in range(spectrum.shape[0]):
        spectrum_dBA[i] = spectrum[i] + A_pond[i]

    return spectrum_dBA
