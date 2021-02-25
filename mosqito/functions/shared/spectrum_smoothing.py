# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 16:44:36 2020

@author: wantysal
"""
# Standard library import
import numpy as np

# Local import
from mosqito.functions.noctfilter.n_oct_filter import getFrequencies


def spectrum_smoothing(freqs_in, spec, noct, low_freq, high_freq, freqs_out):
    """
        Compute smoothed spectrum according to the n-th octave band chosen

    Parameters
    ----------
    freqs : numpy.array
        frequency axis
    spec : numpy.array
        spectrum in dB
    noct : integer
        n-th octave-band according to which smooth the spectrum
    low_freq : float
        lowest frequency of the n-th octave bands
    high_freq : float
        highest frequency of the n-th octave bands
    freqs_out : numpy.array
        frequency axis along which the smoothed spectrum is given

    Returns
    -------
    smoothed-spectrum : numpy.array
        smoothed spectrum along the given frequency axis

    """

    # n-th octave bands filter
    filter_freqs = getFrequencies(low_freq, high_freq, noct, G=10, fr=1000)["f"]
    filter_freqs[len(filter_freqs) - 1, 2] = high_freq
    filter_freqs[0, 0] = low_freq

    # Smoothed spectrum creation
    nb_bands = filter_freqs.shape[0]
    smoothed_spectrum = np.zeros((nb_bands))
    i = 0
    # Each band is considered individually until all of them have been treated
    while nb_bands > 0:
        # Find the index of the spectral components within the frequency bin
        bin_index = np.where(
            (freqs_in >= filter_freqs[i, 0]) & (freqs_in <= filter_freqs[i, 2])
        )[0]
        # If the frequency bin is empty, it is deleted from the list
        if len(bin_index) == 0:
            smoothed_spectrum = np.delete(smoothed_spectrum, i, axis=0)
            filter_freqs = np.delete(filter_freqs, i, axis=0)
            nb_bands -= 1

        else:
            # The spectral components within the frequency bin are averaged on an energy basis
            spec_sum = 0
            for j in bin_index:
                spec_sum += 10 ** (spec[j] / 10)
            smoothed_spectrum[i] = 10 * np.log10(spec_sum / len(bin_index))
        nb_bands -= 1
        i += 1

    # Pose of the smoothed spectrum on the frequency-axis
    cor = []
    low = []
    high = []
    # Index of the lower, center and higher limit of each frequency bin into the original spectrum
    for i in range(len(filter_freqs)):
        cor.append(np.argmin(np.abs(freqs_out - filter_freqs[i, 1])))
        low.append(np.argmin(np.abs(freqs_out - filter_freqs[i, 0])))
        high.append(np.argmin(np.abs(freqs_out - filter_freqs[i, 2])))

    smooth_spec = np.zeros((spec.shape))
    for i in range(filter_freqs.shape[0]):
        smooth_spec[low[i] : high[i]] = smoothed_spectrum[i]

    return smooth_spec
