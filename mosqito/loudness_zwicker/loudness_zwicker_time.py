# -*- coding: utf-8 -*-
"""
@date Created on Thu Mar 26 2020
@author martin_g for Eomys
"""

# Temporary for testing purpose
import sys
sys.path.append('../../..')
from pandas import ExcelFile, read_excel

# Standard library imports
import numpy as np

# Local applications imports
from mosqito.loudness_zwicker.loudness_zwicker_shared import calc_main_loudness
from mosqito.loudness_zwicker.loudness_zwicker_nonlinear_decay import calc_nl_loudness
from mosqito.loudness_zwicker.loudness_zwicker_shared import calc_slopes
from mosqito.loudness_zwicker.loudness_zwicker_temporal_weighting import loudness_zwicker_temporal_weighting

def loudness_zwicker_time(third_octave_levels, field_type):
    """Calculate Zwicker-loudness for time-varying signals

    Calculate the acoustic loudness according to Zwicker method for
    time-varying signals.
    Normatice reference:
        DIN 45631/A1:2010
        ISO 532-1:2017 (method 2)
    The code is based on C program source code published alongside
    with ISO 532-1 standard. 
    Note that for reasons of normative continuity, as defined in the
    preceeding standards, the method is in accordance with 
    ISO 226:1987 equal loudness contours (instead of ISO 226:2003)

    Parameters
    ----------
    third_octave_levels : numpy.ndarray
        rms acoustic pressure [Pa] per third octave versus time 
        (temporal resolution = 0.5ms)
    field_type : str
        Type of soundfield corresponding to signal ("free" by 
        default or "diffuse")

    Outputs
    -------
    N : float
        Calculated loudness [sones]
    N_specific : numpy.ndarray
        Specific loudness [sones/bark]
    bark_axis : numpy.ndarray
        Corresponding bark axis
    """
    
    # Calculate core loudness
    num_sample_level = np.shape(third_octave_levels)[1]
    core_loudness = np.zeros((21, num_sample_level))
    for i in np.arange(num_sample_level-1):
        core_loudness[:,i] = calc_main_loudness(third_octave_levels[:,i], field_type)
    #
    # Nonlinearity
    core_loudness = calc_nl_loudness(core_loudness)
    #
    # Calculation of specific loudness
    loudness = np.zeros(np.shape(core_loudness)[1])
    spec_loudness = np.zeros((240,np.shape(core_loudness)[1]))
    for i_time in np.arange(np.shape(core_loudness)[1]):
        loudness[i_time], spec_loudness[:,i_time] = calc_slopes(core_loudness[:,i_time])
    #
    # temporal weigthing
    filt_loudness = loudness_zwicker_temporal_weighting(loudness)
    #
    # Decimation from temporal resolution 0.5 ms to 2ms and return
    dec_factor = 4
    N = filt_loudness[::dec_factor]
    N_spec = spec_loudness[:,::dec_factor]
    return N, N_spec

# test de la fonction
if __name__ == "__main__":
    signal = {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 16 (hairdryer).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 16",
            "N_specif_bark": -1,
            "field": "free",
        }

    xls_file = ExcelFile(signal["xls"])

    third_octave_levels, freq = wav_to_oct3(signal["data_file"], calib = 2 * 2**0.5, out_type='time_iso')
    # third_octave_levels = 20 * np.log10((third_octave_levels + 1e-12) / (2*10**-5))
    N, N_specific, bark_axis = loudness_zwicker_time(third_octave_levels, 'free')
    bark = signal["N_specif_bark"]
    i_bark = np.nonzero((np.abs(bark_axis - bark)) == np.amin(np.abs(bark_axis - bark)))[0][0]

    N_iso = np.transpose(read_excel(xls_file, sheet_name=signal["tab"], header=None, skiprows=10, usecols = 'B', squeeze=True).to_numpy())
    N_specif_iso = np.transpose(read_excel(xls_file, sheet_name=signal["tab"], header=None, skiprows=10, usecols = 'L', squeeze=True).to_numpy())
    check_compliance(N, N_specific, bark_axis, signal)
    pass
