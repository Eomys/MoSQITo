# -*- coding: utf-8 -*-

# Standard library import
from numpy import asarray, delete, array, where

# Local application imports
from mosqito.sound_level_meter.noct_spectrum._center_freq import _center_freq
from mosqito.sound_level_meter.noct_spectrum._filter_bandwidth import _filter_bandwidth
from mosqito.sound_level_meter.noct_spectrum._n_oct_freq_filter import _n_oct_freq_filter

def noct_synthesis(spectrum, freqs, fmin, fmax, n=3, G=10, fr=1000):
    """Adapt input spectrum to nth-octave band spectrum
                
    This function the input spectrum to n-th octave band levels.
                       
    Parameters
    ----------
    spectrum : array_like
        RMS amplitude one-sided spectrum, size (nperseg, nseg).
    freqs : list
        List of input frequency , size (nperseg) or (nperseg, nseg).
    fmin : float
        Minimum frequency band [Hz].
    fmax : float
        Maximum frequency band [Hz].
    n : int
        Number of bands per octave.
    G : int
        System for specifying the exact geometric mean frequencies.
        Can be base 2 or base 10.
    fr : int
        Reference frequency. Shall be set to 1 kHz for audible frequency
        range, to 1 Hz for infrasonic range (f < 20 Hz) and to 1 MHz for
        ultrasonic range (f > 31.5 kHz).

    Returns
    -------
    spec : numpy.ndarray
        nth-octave octave band spectrum of signal sig [dB re.2e-5 Pa], size (nbands, nseg).
    fpref : numpy.ndarray
        Corresponding preferred nth-octave octave band center frequencies, size (nbands).

    See Also
    --------
    .comp_spectrum : Spectrum computation from a time signal
    .noct_spectrum : N-th octave band spectrum computation from a time signal

    Examples
    --------
    .. plot::
       :include-source:

        >>> from mosqito.sound_level_meter import comp_spectrum, noct_synthesis
        >>> from mosqito.utils import amp2db
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> f=1000
        >>> fs=48000
        >>> d=0.2
        >>> dB=60
        >>> time = np.arange(0, d, 1/fs)
        >>> stimulus = np.sin(2 * np.pi * f * time) + 0.5 * np.sin(6 * np.pi * f * time)
        >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
        >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
        >>> stimulus = stimulus * ampl
        >>> spec, freqs = comp_spectrum(stimulus, fs, db=False)
        >>> spec_3, freq_axis = noct_synthesis(spec, freqs, fmin=90, fmax=14000)
        >>> spec_3db = amp2db(spec_3, ref=2e-5)
        >>> plt.step(freq_axis, spec_3db)
        >>> plt.xlabel("Center frequency [Hz]")
        >>> plt.ylabel("Amplitude [dB]")

    """

    # Deduce sampling frequency
    fs = freqs.max() * 2

    # Sampling frequency shall be equal to 48 kHz (as per ISO 532)
    if round(fs) != 48000:
        raise ValueError("""ERROR: Sampling frequency shall be equal to 48 kHz""")

    # Get filters center frequencies
    fc_vec, fpref = _center_freq(fmin=fmin, fmax=fmax, n=n, G=G, fr=fr)

    # Compute the filters bandwidth
    alpha_vec, f_low, f_high = _filter_bandwidth(fc_vec, n=n)

    # Delete ends frequencies to prevent aliasing
    idx = asarray(where(f_high > fs / 2))
    if any(idx[0]):
        fc_vec = delete(fc_vec, idx)
        f_low = delete(f_low, idx)
        f_high = delete(f_high, idx)

    # Calculation of the rms level of the signal in each band
    spec = []
    for fc, alpha in zip(fc_vec, alpha_vec):
        spec.append(_n_oct_freq_filter(spectrum, fs, fc, alpha))

    return array(spec), fpref
