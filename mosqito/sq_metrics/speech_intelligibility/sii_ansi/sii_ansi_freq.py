# -*- coding: utf-8 -*-

from mosqito.sq_metrics.speech_intelligibility.sii_ansi._band_procedure_data import _get_critical_band_data, _get_equal_critical_band_data, _get_octave_band_data, _get_third_octave_band_data
from mosqito.sq_metrics.speech_intelligibility.sii_ansi._speech_data import _get_critical_band_speech_data, _get_equal_critical_band_speech_data, _get_octave_band_speech_data, _get_third_octave_band_speech_data
from mosqito.sq_metrics.speech_intelligibility.sii_ansi._main_sii import _main_sii

from mosqito.sound_level_meter.freq_band_synthesis import freq_band_synthesis

def sii_ansi_freq(spectrum, freqs, method, speech_level, threshold=None):
    """Calculate speech intelligibility index

    This function computes SII values for a noise spectrum in dB according to ANSI S3.5 standard.

    Parameters
    ----------
    spectrum : array_like
        Noise spectrum [dB ref. 2e-5 Pa].
    freqs: array_like
        Frequency axis [Hz] of the spectrum.
    method: {"critical", "equally_critical", "third_octave", "octave"}
        Type of frequency band to be used for the calculation. See § 3.4 of the standard.
    speech_level : {'normal', 'raised', 'loud', 'shout'}
        Speech level to assess, the corresponding speech spectrum defined in the standard is used for calculation.
    threshold : array_like or 'zwicker'
        Threshold of hearing [dB ref. 2e-5 Pa] with same size as the chosen method frequency axis, or 'zwicker' to use the standard threshold.
        Default to None sets the threshold to zeros on each frequency band.
        
    Returns
    -------
    sii: numpy.ndarray
        Overall SII value.
    specific_sii: numpy.ndarray
        Specific SII values along the frequency axis.
    freq_axis: numpy.ndarray
        Frequency axis corresponding to the chosen method.
        
    See also
    --------
    sii_ansi : Speech intelligibility with a time signal as background noise
    sii_ansi_level : Speech intelligibility with an overall SPL level as background noise
    
    References
    ----------
    :cite:empty:'SII-ANSI.S3.5:2017'
    
    .. bibliography::
        :keyprefix: SII-

    Examples
    --------
    .. plot::
       :include-source:

        >>> from mosqito.sq_metrics import sii_ansi_freq
        >>> from mosqito.sound_level_meter.comp_spectrum import comp_spectrum
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> fs=48000
        >>> d=0.2
        >>> dB=60
        >>> time = np.arange(0, d, 1/fs)
        >>> f = 50
        >>> stimulus = np.sin(2 * np.pi * f * time) * np.sin(np.pi * f * time) + np.sin(10 * np.pi * f * time) + np.sin(100 * np.pi * f * time)
        >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
        >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
        >>> stimulus = stimulus * ampl
        >>> spec, freqs = comp_spectrum(stimulus, fs, db=True)
        >>> SII, SII_spec, freq_axis = sii_ansi_freq(spec, freqs, method='critical', speech_level='normal')
        >>> plt.plot(freq_axis, SII_spec)
        >>> plt.xlabel("Frequency [Hz]")
        >>> plt.ylabel("Specific value ")
        >>> plt.title("Speech Intelligibility Index = " + f"{SII:.2f}")   
    
    """
    
    if (method!='critical') & (method!='equally_critical') & (method!='third_octave') & (method!='octave'):
        raise ValueError('Method should be within {"critical", "equally_critical", "third_octave", "octave"}.')
        
    if (speech_level!='normal') & (speech_level!='raised') & (speech_level!='loud') & (speech_level!='shout'):
        raise ValueError('Speech level should be within {"normal", "raised", "loud", "shout"} to use the corresponding standard data.')
    
    # Get standard speech spectrum
    if method == 'critical':
        speech_spectrum, speech_level = _get_critical_band_speech_data(speech_level)
        CENTER_FREQUENCIES, LOWER_FREQUENCIES, UPPER_FREQUENCIES, _, _, _ = _get_critical_band_data()
    elif method == 'equally_critical':
        speech_spectrum, speech_level = _get_equal_critical_band_speech_data(speech_level)
        CENTER_FREQUENCIES, LOWER_FREQUENCIES, UPPER_FREQUENCIES, _, _, _ = _get_equal_critical_band_data()
    elif method == 'third_octave':
        speech_spectrum, speech_level = _get_third_octave_band_speech_data(speech_level)
        CENTER_FREQUENCIES, LOWER_FREQUENCIES, UPPER_FREQUENCIES, _, _, _, _ = _get_third_octave_band_data()
    elif method == 'octave':
        speech_spectrum, speech_level = _get_octave_band_speech_data(speech_level)
        CENTER_FREQUENCIES, LOWER_FREQUENCIES, UPPER_FREQUENCIES, _, _, _, _, = _get_octave_band_data()
    nbands = len(speech_spectrum)
    
    if (len(spectrum) != nbands) or (freqs != CENTER_FREQUENCIES).any():
        noise_spectrum,_ = freq_band_synthesis(spectrum, freqs, LOWER_FREQUENCIES, UPPER_FREQUENCIES)
    else:
        noise_spectrum = spectrum
        
    SII, SII_specific, freq_axis = _main_sii(method, speech_spectrum, noise_spectrum, threshold)    
    
    return SII, SII_specific, freq_axis
