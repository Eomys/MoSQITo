# -*- coding: utf-8 -*-

# Standard imports
from numpy import empty, arange, mean, tile

# Local imports
from mosqito.sq_metrics.roughness.roughness_dw._roughness_dw_main_calc import (
    _roughness_dw_main_calc,
)
from mosqito.sq_metrics.roughness.roughness_dw._gzi_weighting import _gzi_weighting
from mosqito.sq_metrics.roughness.roughness_dw._H_weighting import _H_weighting


def roughness_dw_freq(spectrum, freqs):
    """
    Computes the roughness according to Daniel and Weber method from
    a fine band spectrum

    This function computes the global and specific roughness values
    of a signal sampled at 48 kHz.

    Parameters
    ----------
    spectrum : array_like
        Input amplitude or complex frequency spectrum, dim (nperseg x nseg)
    freqs : array
        Input frequency axis , dim (nperseg) if identical for all the blocks,
        else (nperseg x nseg).

    Returns
    -------
    R : numpy.array
        Roughness value in [asper], dim (nseg).
    R_spec : numpy.array
        Specific roughness over bark axis, dim (47 bark x nseg).
    bark_axis : numpy.array
        Frequency axis in [bark], dim (nseg).

    Warning
    -------
    The input spectrum must be an amplitude spectrum (use abs() on complex spectrum).

    See Also
    --------
    .roughness_dw : roughness computation from a time signal

    Notes
    -----
    The model consists of a parallel processing structure made up
    of successive stages to calculate intermediate specific roughnesses :math:`R'`,
    which are summed up to determine the total roughness :math:`R`:

    .. math::
        R=0.25\\sum_{i=1}^{47}R'_{i}

    References
    ----------
    :cite:empty:`R-roughnessDW`

    .. bibliography::
        :keyprefix: R-

    Examples
    --------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import roughness_dw_freq
       >>> from mosqito.sound_level_meter import comp_spectrum
       >>> import matplotlib.pyplot as plt
       >>> import numpy as np
       >>> fc=1000
       >>> fmod=70
       >>> fs=44100
       >>> d=0.2
       >>> dB=60
       >>> time = np.arange(0, d, 1/fs)
       >>> stimulus = (
       >>> 0.5
       >>> * (1 + np.sin(2 * np.pi * fmod * time))
       >>> * np.sin(2 * np.pi * fc * time))
       >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
       >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
       >>> stimulus = stimulus * ampl
       >>> n = len(stimulus)
       >>> spec, freqs = comp_spectrum(stimulus, fs, db=False)
       >>> R, R_specific, bark = roughness_dw_freq(spec, freqs)
       >>> plt.plot(bark, R_specific)
       >>> plt.xlabel("Bark axis [Bark]")
       >>> plt.ylabel("Specific roughness, [Asper/Bark]")
       >>> plt.title("Roughness = " + f"{R:.2f}" + " [Asper]")
    """

    # Check input size coherence
    if len(spectrum) != len(freqs):
        raise ValueError("Input spectrum and frequency axis must have the same size !")

    if spectrum.any() < 0:
        raise ValueError(
            "Input must be an amplitude spectrum (use abs() on complex spectrum)."
        )

    # 1D spectrum
    if len(spectrum.shape) == 1:
        nperseg = len(spectrum)
        nseg = 1
        fs = int(2 * nperseg * mean(freqs[1:] - freqs[:-1]))

    # 2D spectrum
    elif len(spectrum.shape) > 1:
        nperseg = spectrum.shape[0]
        nseg = spectrum.shape[1]
        # one frequency axis per block
        if len(freqs.shape) > 1:
            fs = int(2 * nperseg * mean(freqs[0, 1:] - freqs[0, :-1]))
        # one frequency axis for all the blocks
        elif len(freqs.shape) == 1:
            fs = int(2 * nperseg * mean(freqs[1:] - freqs[:-1]))
            freqs = tile(freqs, (nseg, 1)).T

    # Initialization of the weighting functions H and g
    hWeight = _H_weighting(2 * nperseg, fs)
    # Aures modulation depth weighting function
    gzi = _gzi_weighting(arange(1, 48, 1) / 2)

    if len(spectrum.shape) > 1:
        R = empty((nseg))
        R_spec = empty((47, nseg))
        for i in range(nseg):
            R[i], R_spec[:, i], bark_axis = _roughness_dw_main_calc(
                spectrum[:, i], freqs[:, i], fs, gzi, hWeight
            )
    else:
        R, R_spec, bark_axis = _roughness_dw_main_calc(
            spectrum, freqs, fs, gzi, hWeight
        )

    return R, R_spec, bark_axis


if __name__ == "__main__":
    from mosqito.sq_metrics import roughness_dw_freq
    from mosqito.sound_level_meter import comp_spectrum
    import matplotlib.pyplot as plt
    import numpy as np

    fc = 1000
    fmod = 70
    fs = 44100
    d = 0.2
    dB = 60
    time = np.arange(0, d, 1 / fs)
    stimulus = (
        0.5 * (1 + np.sin(2 * np.pi * fmod * time)) * np.sin(2 * np.pi * fc * time)
    )
    rms = np.sqrt(np.mean(np.power(stimulus, 2)))
    ampl = 0.00002 * np.power(10, dB / 20) / rms
    stimulus = stimulus * ampl
    n = len(stimulus)
    spec, freqs = comp_spectrum(stimulus, fs, db=False)
    R, R_specific, bark = roughness_dw_freq(spec, freqs)
    plt.plot(bark, R_specific)
    plt.xlabel("Bark axis [Bark]")
    plt.ylabel("Specific roughness, [Asper/Bark]")
    plt.title("Roughness = " + f"{R:.2f}" + " [Asper]")
    plt.show(block=True)
