# -*- coding: utf-8 -*-

# Standard library import
import numpy as np

# Local application imports
from mosqito.sound_level_meter.noct_spectrum._center_freq import _center_freq
from mosqito.sound_level_meter.noct_spectrum._filter_bandwidth import _filter_bandwidth
from mosqito.sound_level_meter.noct_spectrum._n_oct_freq_filter import _n_oct_freq_filter


def noct_synthesis(spectrum, freqs, fmin, fmax, n=3, G=10, fr=1000):
    """Adapt input spectrum to nth-octave band spectrum
    
    Convert the input spectrum to third-octave band spectrum
    between "fc_min" and "fc_max".
    Parameters
    ----------
    spectrum : numpy.ndarray
        amplitude rms of the one-sided spectrum of the signal, size (nperseg, nseg).
    freqs : list
        List of input frequency , size (nperseg) or (nperseg, nseg).
    fmin : float
        Min frequency band [Hz].
    fmax : float
        Max frequency band [Hz].
    n : int
        Number of bands pr octave.
    G : int
        System for specifying the exact geometric mean frequencies.
        Can be base 2 or base 10.
    fr : int
        Reference frequency. Shall be set to 1 kHz for audible frequency
        range, to 1 Hz for infrasonic range (f < 20 Hz) and to 1 MHz for
        ultrasonic range (f > 31.5 kHz).
    Outputs
    -------
    spec : numpy.ndarray
        Third octave band spectrum of signal sig [dB re.2e-5 Pa], size (nbands, nseg).
    fpref : numpy.ndarray
        Corresponding preferred third octave band center frequencies, size (nbands).
    """
    
    # Deduce sampling frequency
    fs = np.mean(freqs[1:] - freqs[:-1]) * 2 * (len(spectrum)-1)
    
    # Sampling frequency shall be equal to 48 kHz (as per ISO 532)
    if fs != 48000:
        raise ValueError("""ERROR: Sampling frequency shall be equal to 48 kHz""")

    # Get filters center frequencies
    fc_vec, fpref = _center_freq(fmin=fmin, fmax=fmax, n=n, G=G, fr=fr)
    
    # Compute the filters bandwidth
    alpha_vec, f_low, f_high = _filter_bandwidth(fc_vec, n=n)
    
    # Delete ends frequencies to prevent aliasing
    idx = np.asarray(np.where(f_high > fs / 2))
    if any(idx[0]):
        fc_vec = np.delete(fc_vec, idx)
        f_low = np.delete(f_low, idx)
        f_high = np.delete(f_high, idx)

    # Number of nth bands
    nband = len(fc_vec)
    
    # Results array initialization
    if len(spectrum.shape) > 1:
        nseg = spectrum.shape[1]
        spec = np.zeros((nband, nseg))
        # If only one axis is given, it is used for all the spectra
        if len(freqs.shape) == 1:
            freqs = np.tile(freqs, (nseg, 1)).T
    else:
        nseg = 1
        spec = np.zeros((nband))

    # Calculation of the rms level of the signal in each band
    spec = []
    for fc, alpha in zip(fc_vec, alpha_vec):
        spec.append(_n_oct_freq_filter(spectrum, fs, fc, alpha))

    return np.array(spec), fpref
