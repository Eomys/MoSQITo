# -*- coding: utf-8 -*-


# Local imports
from mosqito.sq_metrics import loudness_zwst_freq
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import (
    sharpness_din_from_loudness,
)

from numpy import arange, linspace, tile, diff
from scipy.interpolate import interp1d


def sharpness_din_freq(spectrum, freqs, weighting="din", field_type="free"):
    """Acoustic sharpness calculation according to different methods
      (Aures, Von Bismarck, DIN 45692, Fastl) from a complex spectrum.

    Parameters:
    ----------
    signal: numpy.array
        A RMS spectrum.
    freqs: integer
        Frequency axis.
    method : string
        To specify the Loudness computation method
    weighting : string
        To specify the weighting function used for the
        sharpness computation.'din' by default,'aures', 'bismarck','fastl'
    field_type : str
        Type of soundfield corresponding to spec_third ("free" by
        default or "diffuse").

    Outputs
    ------
    S : float
        sharpness value
    time_axis: numpy.array
        The time axis array, size (Ntime,) or None

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
