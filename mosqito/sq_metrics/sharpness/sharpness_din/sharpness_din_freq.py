# -*- coding: utf-8 -*-

# Standard library import
from numpy import interp, arange

# Local imports
from mosqito.sq_metrics import loudness_zwst_freq
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import (
    sharpness_din_from_loudness,
)

from numpy import arange, linspace, tile, diff
from scipy.interpolate import interp1d


def sharpness_din_freq(spectrum, freqs, weighting="din", field_type="free"):
    """
    Compute the sharpness value from a fine band spectrum

    This function computes the sharpness value along time according to different methods.

    Parameters
    -----------
    spectrum : array_like
        A RMS spectrum.
    freqs : array_like
        Frequency axis.
    weighting : {'din', 'aures', 'bismarck', 'fastl'}
        Weighting function used for the sharpness computation.
        Default is 'din'
    field_type : {'free', 'diffuse'}
        Type of soundfield.
        Default is 'free'

    Returns
    --------
    S : numpy.array
        Sharpness value in [acum]

    Warning
    -------
    The sampling frequency of the signal must be >= 48 kHz to fulfill requirements.
    If the provided signal doesn't meet the requirements, it will be resampled.

    See Also
    ---------
    .sharpness_din_from_loudness : Sharpness computation from loudness values
    .sharpness_din_st : Sharpness computation for a stationary time signal
    .sharpness_din_tv : Sharpness computation for a non-stationary time signal
    .sharpness_din_perseg : Sharpness computation by time-segment

    Notes
    ------
    The computation consists of a specific loudness weighting employing a weighting function :math:`g(z)`:

    .. math::
        S=0.11\\frac{\\int_{0}^{24Bark}N'(z)g(z)\\textup{dz}}{N}

    with :math:`N'` the specific loudness and :math:`N` the global loudness according to Zwicker method
    for stationary signals.

    The different methods available with the function account for the weighting function applied:
     * DIN 45692 : weighting defined in the standard
     * Aures
     * Bismarck
     * Fastl

    References
    -----------
    :cite:empty:`S-DIN.45692:2009`
    :cite:empty:`S-ZF:9`
    :cite:empty:`S-B74`

    .. bibliography::
        :keyprefix: S-

    Examples
    ---------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import sharpness_din_freq
       >>> from mosqito.sound_level_meter import comp_spectrum
       >>> import matplotlib.pyplot as plt
       >>> import numpy as np
       >>> fs=48000
       >>> d=0.2
       >>> dB=60
       >>> time = np.arange(0, d, 1/fs)
       >>> f = np.linspace(1000,5000, len(time))
       >>> stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
       >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
       >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
       >>> stimulus = stimulus * ampl
       >>> spec, freqs = comp_spectrum(stimulus, fs, db=False)
       >>> S = sharpness_din_freq(spec, freqs)
       >>> plt.plot(time, stimulus)
       >>> plt.xlim(0, 0.05)
       >>> plt.xlabel("Time [s]")
       >>> plt.ylabel("Amplitude [Pa]")
       >>> plt.title("Sharpness = " + f"{S:.2f}" + " [Acum]")
    """
    # 1D spectrum
    if len(spectrum.shape) == 1:
        if len(spectrum) != len(freqs):
            raise ValueError(
                "Input spectrum and frequency axis do not have the same length"
            )
        if (freqs.max() < 24000) or (freqs.min() > 24):
            print(
                "[WARNING] freqs argument is not wide enough to cover the full audio range. Missing frequency bands will be filled with 0. To fulfill the standard requirements, the frequency axis should go from 24Hz up to 24 kHz."
            )
            df = freqs[1] - freqs[0]
            spectrum = interp1d(
                freqs, spectrum, axis=0, bounds_error=False, fill_value=0
            )(linspace(0, 24000, int(24000 // df)))
            freqs = linspace(0, 24000, int(24000 // df))
    # 2D spectrum
    elif len(spectrum.shape) > 1:
        nseg = spectrum.shape[1]
        # one frequency axis per segment
        if len(freqs.shape) > 1:
            if spectrum.shape != freqs.shape:
                raise ValueError(
                    "Input spectrum and frequency axis do not have the same shape."
                )
            if (freqs.max() < 24000) or (freqs.min() > 24):
                print(
                    "[WARNING] freqs argument is not wide enough to cover the full audio range. Missing frequency bands will be filled with 0. To fulfill the standard requirements, the frequency axis should go from 24Hz up to 24 kHz."
                )
                df = diff(freqs, axis=0).min()
                nperseg = int(24000 // df)
                spectrum = (
                    interp1d(
                        freqs.ravel(),
                        spectrum.ravel(),
                        bounds_error=False,
                        fill_value=0,
                    )(tile(linspace(0, 24000, nperseg), nseg))
                    .reshape((nseg, nperseg))
                    .T
                )
                freqs = tile(linspace(0, 24000, nperseg), (nseg, 1)).T
        # one frequency axis for all the segments
        elif len(freqs.shape) == 1:
            if spectrum.shape[0] != len(freqs):
                raise ValueError(
                    'Input spectra and frequency axis do not have the same length. "freqs" must have dim(nperseg) and "spectra" must have dim(nperseg,nseg).'
                )
            if (freqs.max() < 24000) or (freqs.min() > 24):
                print(
                    "[WARNING] freqs argument is not wide enough to cover the full audio range. Missing frequency bands will be filled with 0. To fulfill the standard requirements, the frequency axis should go from 24Hz up to 24 kHz."
                )
                df = freqs[1] - freqs[0]
                nperseg = int(24000 // df)
                spectrum = interp1d(
                    freqs, spectrum, axis=0, bounds_error=False, fill_value=0
                )(linspace(0, 24000, nperseg))
                freqs = tile(linspace(0, 24000, nperseg), (nseg, 1)).T
   
    # Compute loudness
    N, N_specific, _ = loudness_zwst_freq(spectrum, freqs, field_type=field_type)

    if len(spectrum.shape) > 1:
        raise ValueError("With a 2D spectrum use 'sharpness_din_perseg' calculation.")

    # Compute sharpness from loudness
    S = sharpness_din_from_loudness(N, N_specific, weighting=weighting)

    return S
