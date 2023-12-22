import numpy as np

# Project Imports
from mosqito.sq_metrics.loudness.loudness_ecma._rectified_band_pass_signals import (
    _rectified_band_pass_signals,
)
from mosqito.sq_metrics.loudness.loudness_ecma._nonlinearity import _nonlinearity

# Data import
# Threshold in quiet
from mosqito.sq_metrics.loudness.loudness_ecma._loudness_ecma_data import ltq_z


def tonality_ecma(signal, sb=2048, sh=1024):
    """Calculation of the tonality according to ECMA-418-2 section 6

    Parameters
    ----------
    signal: numpy.array
        time signal values in 'Pa'. The sampling frequency of the signal must be 48000 Hz.
    sb: int or list of int
        block size.
    sh: int or list of int
        Hop size.
    Returns
    -------
    n_specific: list of numpy.array
        Specific Loudness [sone_HMS per Bark]. Each of the 53 element of the list corresponds to the time-dependant
        specific loudness for a given bark band. Can be a ragged array if a different sb/sh are used for each band.
    bark_axis: numpy.array
        Bark axis
    """
    
    
    # Sampling frequency
    fs = 48000

    # delta_f dans _gammatone pour déterminer les sb et sh en fonction de la largeur de chaque bande

    # sb and sh for Tonality
    z = np.linspace(0.5, 26.5, num=53, endpoint=True)
    sb = np.ones(53, dtype="int")
    sh = np.ones(53, dtype="int")
    sb[z <= 1.5] = 8192
    sh[z <= 1.5] = 2048
    sb[np.all([z >= 2, z <= 8], axis=0)] = 4096
    sh[np.all([z >= 2, z <= 8], axis=0)] = 1024
    sb[np.all([z >= 8.5, z <= 12.5], axis=0)] = 2048
    sh[np.all([z >= 8.5, z <= 12.5], axis=0)] = 512
    sb[z >= 13] = 1024
    sh[z >= 13] = 256

    # AUTOCORRELATION FUNCTION (6.2.2)



    # AVERAGING OF THE SCALED ACF (6.2.3)

    # In neighboring bands
    # NB for the averaging of ACF

    # In neighboring blocks
    # Only for sb = 8192 and sb = 4096

    # APPLICATION OF ACF WINDOW (6.2.4)

    # Lag times limits
    tau_min = 2 #millisecond
    tau_start = np.max(0.5/delta_f, tau_min)
    tau_end = np.max(4/delta_f, tau_start+1)  # !! +1 millisecond

    # Indices for the calcultaed lag times
    m_start = np.ceil(tau_start * fs) - 1
    m_end = np.florr(tau_end * fs) - 1

    # The window is applied to all elements of index m_start<m<m_end, 0 elsewhere
    
    # Number of samples in the window
    M = m_end - m_start + 1


    # ESTIMATION OF TONAL LOUDNESS (6.2.5)

    # RESAMPLING TO COMMON TIME BASIS (6.2.6)

    # NOISE REDUCTION (6.2.7)

    # CALCULATION OF TIME DEPENDENT SPECIFIC TONALITY (6.2.8)

    # CALCULATION OF AVERAGED SPECIFIC TONALITY (6.2.9)

    # CALCULATION OF TIME DEPENDENT TONALITY (6.2.10)
