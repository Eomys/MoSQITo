# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 12:28:15 2020

@author: josem
"""

# Add MoSQITo to the Python path
# import sys
# sys.path.append("..")

import scipy.signal as sig
from mosqito.functions.shared.load import load


# FIR filter definition
# Required input defintions are as follows;
# data:   The data to be filtered
# fs:     Sampling frecuency
# fc:   The centerline frequency to be filtered
# band:   The bandwidth around the centerline freqency that you wish to filter


def fir_notch_filter(data, fs, fc, band):
    order = 799

    # Se determinan las frecuencias de corte inferior y superior del filtro
    if fc <= band / 2:
        filtered_data = data
    else:
        low = fc - band / 2.0
        high = fc + band / 2.0

        # Se obtienen los coeficientes de un filtro elimina banda, utilizando ventana Hamming
        h = sig.firwin(
            order, [low, high], window="hamming", pass_zero="bandstop", fs=fs
        )

        filtered_data = sig.filtfilt(h, 1, data)

    return filtered_data


# IIR filter definition
# Required input defintions are as follows;
# data:   The data to be filtered
# fs:     Sampling frecuency
# fc:   The centerline frequency to be filtered
# band:   The bandwidth around the centerline frequency that you wish to filter


def iir_notch_filter(data, fs, fc, band):
    Q = fc / band

    b, a = sig.iirnotch(fc, Q, fs=fs)

    filtered_data = sig.filtfilt(b, a, data)

    return filtered_data


# Variant filter definition
# Required input defintions are as follows;
# signal:     Signal to be filtered
# track:   Signal to track de armonics
# ftype:   Type of filter. FIR = 0, IIR = 1
# armonic_order:   Order of the armonic to filter


def variant_filter(signal, track, ftype, armonic_order, band):
    # Load original and tracking data
    original_signal, fs = load(False, signal, calib=2 * 2 ** 0.5)
    signal_tracking, fs = load(False, track, calib=1)

    i = fs - 1
    j = 0
    filtered_signal = []

    while i <= len(signal_tracking):

        fc = (armonic_order * signal_tracking[i - 1]) / 6

        if ftype == 0:

            filtered_signal[j:i] = fir_notch_filter(original_signal[j:i], fs, fc, band)

        if ftype == 1:
            filtered_signal[j:i] = iir_notch_filter(original_signal[j:i], fs, fc, band)

        j = i
        i = i + fs

    return original_signal, filtered_signal, fs
