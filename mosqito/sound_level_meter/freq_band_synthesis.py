# -*- coding: utf-8 -*-

# Standard library import
from numpy import array, concatenate, zeros, log10, power, argmin, split, arange, interp, iscomplex

def freq_band_synthesis(spectrum, freqs, fmin, fmax):
    """Adapt input spectrum to frequency band levels
    
    Convert the input spectrum to frequency band spectrum
    between "fmin" and "fmax".
    
    Parameters
    ----------
    spectrum : numpy.ndarray
        One-sided spectrum of the signal in [dB], size (nperseg, nseg).
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
    if iscomplex(spectrum).any():
        raise ValueError('Input spectrum must be in dB, no complex value allowed.')
    
    if (fmin.min() < freqs.min()):
        print("[WARNING] Input spectrum minimum frequency if higher than fmin. Empty values will be filled with 0.")
        df = freqs[1] - freqs[0]
        spectrum = interp(arange(fmin.min(),fmax.max()+df, df), freqs, spectrum)
        freqs = arange(fmin.min(),fmax.max()+df, df)

    if (fmax.max() > freqs.max()):
        print("[WARNING] Input spectrum maximum frequency if lower than fmax. Empty values will be filled with 0.")
        df = freqs[1] - freqs[0]
        spectrum = interp(arange(fmin.min(),fmax.max()+df, df), freqs, spectrum)
        freqs = arange(fmin.min(),fmax.max()+df, df)
    
    # Find the lower and upper index of each band
    idx_low = argmin(abs(freqs[:,None] - fmin), axis=0)
    idx_up = argmin(abs(freqs[:,None] - fmax), axis=0)
    idx = concatenate((idx_low, [idx_up[-1]]))
    
    # Split the given spectrum in several bands
    bands = array(split(spectrum, idx), dtype=object)[1:-1]
    
    # Compute the bands level
    band_spectrum = zeros((len(bands)))
    i = 0
    for s in bands:
        band_spectrum[i] = 10*log10(sum(power(10,s/10)))      
        i += 1

    return band_spectrum, (fmin+fmax)/2


        



