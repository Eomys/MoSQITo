# -*- coding: utf-8 -*-

# Standard library import
from numpy import arange, zeros, where, delete, argmin, mean, log10, squeeze, abs

# Local import
from mosqito.sound_level_meter.noct_spectrum._getFrequencies import _getFrequencies


def _spectrum_smoothing(freqs_in, spec, noct, low_freq, high_freq, freqs_out):
    """
        Compute smoothed spectrum according to the n-th octave band chosen

    Parameters
    ----------
    freqs : numpy.array
        frequency axis dim (nperseg)
    spec : numpy.array
        spectrum in dB (nperseg, nseg)
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
    nperseg = spec.shape[0]
    if len(spec.shape) > 1:
        nseg = spec.shape[1]
    else:
        nseg = 1
    spec = spec.ravel()
    stop = arange(1, nseg + 1) * nperseg
    freqs_in = freqs_in.ravel()

    # n-th octave bands filter
    filter_freqs = _getFrequencies(low_freq, high_freq, noct, G=10, fr=1000)["f"]
    filter_freqs[len(filter_freqs) - 1, 2] = high_freq
    filter_freqs[0, 0] = low_freq

    # Smoothed spectrum creation
    nb_bands = filter_freqs.shape[0]
    smoothed_spectrum = zeros((nb_bands, nseg))
    i = 0
    # Each band is considered individually until all of them have been treated
    while nb_bands > 0:
        # Find the index of the spectral components within the frequency bin
        bin_index = where((freqs_in >= filter_freqs[i, 0]) & (freqs_in <= filter_freqs[i, 2]))[0]

        # If the frequency bin is empty, it is deleted from the list
        if len(bin_index) == 0:
            smoothed_spectrum = delete(smoothed_spectrum, i, axis=0)
            filter_freqs = delete(filter_freqs, i, axis=0)
            nb_bands -= 1

        else:
            # The spectral components within the frequency bin are averaged on an energy basis
            spec_sum = zeros((nseg))
            for j in range(nseg):
                if len(bin_index[(bin_index < stop[j]) & (bin_index > (stop[j] - nperseg))])!= 0:
                    spec_sum[j] = mean(10** (spec[bin_index[(bin_index < stop[j]) & (bin_index > (stop[j] - nperseg))]]/ 10))
                else:
                    spec_sum[j] = 1e-12
            smoothed_spectrum[i, :] = 10 * log10(spec_sum)# / len(bin_index[(bin_index < stop[j]) & (bin_index > (stop[j] - m))]))
        nb_bands -= 1
        i += 1
    # Pose of the smoothed spectrum on the frequency-axis
    low = zeros((filter_freqs.shape[0], nseg))
    high = zeros((filter_freqs.shape[0], nseg))

    # Index of the lower and higher limit of each frequency bin into the original spectrum
    for i in range(len(filter_freqs)):
        low[i,:] = argmin(abs(freqs_out - filter_freqs[i, 0]))
        high[i,:] = argmin(abs(freqs_out - filter_freqs[i, 2]))
    low = low.astype(int)
    high = high.astype(int)

    smooth_spec = zeros((nperseg, nseg))
    for i in range(nseg):
        for j in range(filter_freqs.shape[0]):
            smooth_spec[low[j,i] : high[j,i], i] = smoothed_spectrum[j,i]
    
    if smooth_spec.shape[1] == 1:
        smooth_spec = squeeze(smooth_spec)

    return smooth_spec
