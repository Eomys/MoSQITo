from numpy import(
    abs,
    power,
    zeros,
    empty,
    sum,
    array,
    clip,
    exp,
    mean,
    median,
    where,
    diff,
    sign
)
from numpy.fft import fft
from scipy.signal import (hilbert, resample)
from scipy.signal.windows import hann

# Project Imports
from mosqito.sq_metrics.loudness.loudness_ecma._rectified_band_pass_signals import _rectified_band_pass_signals
from mosqito.sq_metrics.loudness.loudness_ecma._nonlinearity import _nonlinearity

# Data import
# Threshold in quiet
from mosqito.sq_metrics import loudness_ecma
from mosqito.utils import load




def comp_specific_roughness_ecma(signal):
    """Calculation of the specific roughness according to ECMA-418-2 section 7

    Parameters
    ----------
    signal: numpy.array
        time signal values in 'Pa'. The sampling frequency of the signal must be 48000 Hz.

    Returns
    -------
    n_specific: list of numpy.array
        Specific Loudness [sone_HMS per Bark]. Each of the 53 element of the list corresponds to the time-dependant
        specific loudness for a given bark band. Can be a ragged array if a different sb/sh are used for each band.
    bark_axis: numpy.array
        Bark axis
    """