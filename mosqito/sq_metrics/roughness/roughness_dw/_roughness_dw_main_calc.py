# -*- coding: utf-8 -*-

# Standard imports
from numpy import concatenate, zeros, arange, where, interp, mean, real, corrcoef, power, sqrt
from numpy.fft import fft, ifft
import math

# Local imports
from mosqito.utils.LTQ import LTQ
from mosqito.sq_metrics.roughness.roughness_dw._ear_filter_coeff import (
    _ear_filter_coeff,
)
from mosqito.utils import freq2bark, db2amp, amp2db, bark2freq

def _roughness_dw_main_calc(spec, freq_axis, fs, gzi, hWeight):
    """
    Daniel and Weber roughness main calculation

    Parameters
    ----------
    spec : array
        An amplitude or complex spectrum.
    freq_axis : array
        Frequency axis in [Hz].
    fs : integer
        Sampling frequency.
    gzi : array
        gzi weighting function.
    hWeight : array
        H weighting function.

    Returns
    -------
    R : float
        Roughness computed for the given spectrum.

    """
    if len(spec) != len(freq_axis):
        raise ValueError(
            "spectrum and frequency axis should have the same number of points !"
        )

    # convert spectrum to 2-sided
    spec = concatenate((spec, spec[len(spec)::-1]))

    n = len(spec)
    # Frequency axis in Bark
    bark_axis = freq2bark(freq_axis)
    # Highest frequency
    nZ = arange(1, n//2 + 1, 1)

    # Calculate Zwicker a0 factor (transfer characteristic of the outer and inner ear)
    a0 = zeros((n))
    a0[nZ - 1] = db2amp(_ear_filter_coeff(bark_axis), ref=1)
    spec = a0 * spec

    # Conversion of the spec into dB
    module = abs(spec[0:n//2])
    spec_dB = amp2db(module, ref=2e-5)
    
    # Find the audible components within the spec
    threshold = LTQ(bark_axis, reference="roughness")
    audible_index = where(spec_dB > threshold)[0]
    # Number of audible frequencies
    n_aud = len(audible_index)

    # --------------------------------- stage 1 ------------------------------------
    # ----------------Creation of the specific excitations functions----------------

    # Terhardt's slopes definition
    # lower slope [dB/Bark]
    s1 = -27
    s2 = zeros((n_aud))
    # upper slope [dB/Bark]
    for k in arange(0, n_aud, 1):
        s2[k] = min(
            -24 - (230 / freq_axis[audible_index[k]]) + (0.2 * spec_dB[audible_index[k]]),
            0,
        )

    # The excitation pattern are calculated for 47 overlapping 1-bark-wide channels
    n_channel = 47
    # Channels number
    zi = arange(1, n_channel + 1) / 2
    # Center frequencies for each channel
    zb = bark2freq(zi) * n / fs
    # Minimum excitation level
    minExcitDB = interp(zb, nZ, threshold)
    
    ch_low = zeros((n_aud))
    ch_high = zeros((n_aud))
    for i in arange(0, n_aud):
        # Lower limit of the channel corresponding to each component
        ch_low[i] = math.floor(2 * bark_axis[audible_index[i]]) - 1
        # Higher limit
        ch_high[i] = math.ceil(2 * bark_axis[audible_index[i]]) - 1

    # Creation of the excitation pattern
    slopes = zeros((n_aud, n_channel))
    for k in arange(0, n_aud):
        levDB = spec_dB[audible_index[k]]
        b = bark_axis[audible_index[k]]
        for j in arange(0, int(ch_low[k] + 1)):
            sl = (s1 * (b - ((j + 1) * 0.5))) + levDB
            if sl > minExcitDB[j]:
                slopes[k, j] = db2amp(sl, ref=0.00002)
        for j in arange(int(ch_high[k]), n_channel):
            sl = (s2[k] * (((j + 1) * 0.5) - b)) + levDB
            if sl > minExcitDB[j]:
                slopes[k, j] = db2amp(sl, ref=0.00002)

    # Initialization
    hBP = zeros((n_channel, n))
    mod_depth = zeros((n_channel))

    # Definition of the excitation amplitude
    for i in arange(0, n_channel, 1):
        exc = zeros((n), dtype=complex)
        for j in arange(0, n_aud, 1):
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

            # reconstruction of the spec
            exc[ind] = ampl * spec[ind]

        # The temporal specific excitation functions are obtained by IFFT
        temporal_excitation = abs(n * real(ifft(exc)))
        # ------------------------------- stage 2 --------------------------------------
        # ---------------------modulation depth calculation-----------------------------

        # The fluctuations of the envelope are contained in the low frequency part
        # of the spec of specific excitations in absolute value
        h0 = mean(temporal_excitation)
        envelope_spec = fft(temporal_excitation - h0)

        # This spec is weighted to model the low-frequency  bandpass
        # characteristic of the roughness on modulation frequency
        envelope_spec = envelope_spec * hWeight[i, :]
        # The time functions of the bandpass filtered envelopes hBPi(t)
        # are calculated via inverse Fourier transform :
        hBP[i, :] = 2 * real(ifft(envelope_spec))

        # Modulation depth estimation is given by envelope RMS values
        # and excitation functions time average :
        hBPrms = sqrt(mean(power(hBP[i, :], 2)))
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
    ki = zeros((47))

    for i in range(0, 45):
        if hBP[i].all() != 0 and hBP[i + 2].all() != 0:
            ki[i] = corrcoef(hBP[i, :], hBP[i + 2, :])[0, 1]

    # Specific roughness calculation with gzi the modulation depth weighting
    # function given by Aures
    R_spec = zeros((47))

    R_spec[0] = gzi[0] * pow(mod_depth[0] * ki[0], 2)
    R_spec[1] = gzi[1] * pow(mod_depth[1] * ki[1], 2)
    for i in arange(2, 45):
        R_spec[i] = gzi[i] * pow(mod_depth[i] * ki[i] * ki[i - 2], 2)
    R_spec[45] = gzi[45] * pow(mod_depth[45] * ki[43], 2)
    R_spec[46] = gzi[46] * pow(mod_depth[46] * ki[44], 2)

    # Total roughness calculation with calibration factor of 0.25 given in the article
    # to produce a roughness of 1 asper for a 1-kHz, 60dB tone with carrier frequency
    # of 70 Hz and a modulation depth of 1

    R = 0.25 * sum(R_spec)

    return R, R_spec, zi



