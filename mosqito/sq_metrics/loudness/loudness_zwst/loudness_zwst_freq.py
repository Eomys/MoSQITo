# -*- coding: utf-8 -*-

# Third party imports
from numpy import linspace, arange, tile, diff
from scipy.interpolate import interp1d

# Local application imports
from mosqito.sound_level_meter.noct_spectrum.noct_synthesis import noct_synthesis
from mosqito.sq_metrics.loudness.loudness_zwst._main_loudness import _main_loudness
from mosqito.sq_metrics.loudness.loudness_zwst._calc_slopes import _calc_slopes
from mosqito.utils import amp2db


def loudness_zwst_freq(spectrum, freqs, field_type="free"):
    """
    Compute the loudness value from a fine band spectrum

    This function computes the acoustic loudness according to Zwicker method for
    stationary signals (ISO.532-1:2017).

    Parameters
    ----------
    spectrum : array_like
        A RMS spectrum.
    freqs : array_like
        Frequency axis.
    field_type : {'free', 'diffuse'}
        Type of soundfield.
        Default is 'free'

    Returns
    -------
    N : float or array_like
        Overall loudness array in [sones], size (Ntime,).
    N_specific : array_like
        Specific loudness array [sones/bark], size (Nbark, Ntime).
    bark_axis: array_like
        Bark axis array, size (Nbark,).

    Warning
    -------
    The sampling frequency of the signal must be >= 48 kHz to fulfill requirements.
    If the provided signal doesn't meet the requirements, it will be resampled.

    See Also
    --------
    .loudness_zwst : Loudness computation for a stationary time signal
    .loudness_zwst_perseg : Loudness computation by time-segment
    .loudness_zwtv : Loudness computation for a non-stationary time signal

    Notes
    -----
    The total loudness :math:`N` is computed as the integral of the specific loudness :math:`N'` measured in sone/bark, over the Bark scale.
    The values of specific loudness are evaluated from third octave band levels as function of critical band rate :math:`z` in Bark.

    .. math::
        N=\\int_{0}^{24Bark}N'(z)\\textup{dz}

    Due to normative continuity, the method is in accordance with ISO 226:1987 equal loudness contours
    instead of ISO 226:2003, as defined in the following standards:
        * ISO 532:1975 (method B)
        * DIN 45631:1991
        * ISO 532-1:2017 (method 1)

    References
    ----------
    :cite:empty:`L_zw-ZF91`
    :cite:empty:`L_zw-ISO.532-1:2017`

    .. bibliography::
        :keyprefix: L_zw-

    Examples
    --------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import loudness_zwst_freq
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
       >>> N, N_spec, bark_axis = loudness_zwst_freq(spec, freqs)
       >>> plt.plot(bark_axis, N_spec)
       >>> plt.xlabel("Frequency band [Bark]")
       >>> plt.ylabel("Specific loudness [Sone/Bark]")
       >>> plt.title("Loudness = " + f"{N:.2f}" + " [Sone]")
    """

    # Check the inputs
    if len(spectrum) != len(freqs):
        raise ValueError("Input spectrum and frequency axis must have the same shape")

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

    # Compute third octave band spectrum
    spec_third, _ = noct_synthesis(spectrum, freqs, fmin=24, fmax=12600)

    # Compute dB values
    spec_third = amp2db(spec_third, ref=2e-5)

    # Compute main loudness
    Nm = _main_loudness(spec_third, field_type)
    #
    # Computation of specific loudness pattern and integration of overall
    # loudness by attaching slopes towards higher frequencies
    N, N_specific = _calc_slopes(Nm)

    # Define Bark axis
    bark_axis = linspace(0.1, 24, int(24 / 0.1))

    return N, N_specific, bark_axis
