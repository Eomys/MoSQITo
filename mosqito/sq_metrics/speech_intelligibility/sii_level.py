# -*- coding: utf-8 -*-

from numpy import ones, log10, power

from mosqito.sq_metrics.speech_intelligibility._band_procedure_data import _get_critical_band_data, _get_equal_critical_band_data, _get_octave_band_data, _get_third_octave_band_data
from mosqito.sq_metrics.speech_intelligibility._speech_data import _get_critical_band_speech_data, _get_equal_critical_band_speech_data, _get_octave_band_speech_data, _get_third_octave_band_speech_data
from mosqito.sq_metrics.speech_intelligibility._main_sii import _main_sii
from mosqito.utils.LTQ import LTQ
from mosqito.utils.conversion import freq2bark


def sii_level(noise_level, method, speech_level, threshold=None):
    """Calculate speech intelligibility index

    This function computes SII values for an overall noise level in dB according to ANSI S3.5 standard.

    Parameters
    ----------
    noise_level : float
        Overall noise level in [dB ref. 2e-5 Pa]. This value is used to create a uniform noise spectrum. 
    method: {"critical", "equally_critical", "third_octave", "octave"}
        Type of frequency band to be used for the calculation.
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
        
    Examples
    --------
    .. plot::
       :include-source:
       
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> from mosqito.sq_metrics.speech_intelligibility import sii_level
        >>> fs=48000
        >>> d=0.2
        >>> dB=90
        >>> time = np.arange(0, d, 1/fs)
        >>> f = 50
        >>> stimulus = np.sin(2 * np.pi * f * time) * np.sin(np.pi * f * time) + np.sin(10 * np.pi * f * time) + np.sin(100 * np.pi * f * time)
        >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
        >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
        >>> stimulus = stimulus * ampl
        >>> speech_level = 'raised'
        >>> SII, SII_spec, freq_axis = sii_level(60, method='critical', speech_level=speech_level, threshold='zwicker')
        >>> plt.plot(freq_axis, SII_spec)
        >>> plt.xlabel("Frequency [Hz]")
        >>> plt.ylabel("Specific value ")
        >>> plt.title("Speech Intelligibility Index = " + f"{SII:.2f} \n Speech level: " + speech_level)   

    """
    
    if (method!='critical') & (method!='equally_critical') & (method!='third_octave') & (method!='octave'):
        raise ValueError('Method should be within {"critical", "equally_critical", "third_octave", "octave"}.')
        
    if (speech_level!='normal') & (speech_level!='raised') & (speech_level!='loud') & (speech_level!='shout'):
        raise ValueError('Speech level should be within {"normal", "raised", "loud", "shout"} to use the corresponding standard data.')
    
    # Get standard speech spectrum
    if method == 'critical':
        speech_spectrum, speech_level = _get_critical_band_speech_data(speech_level)
    elif method == 'equally_critical':
        speech_spectrum, speech_level = _get_equal_critical_band_speech_data(speech_level)
    elif method == 'third_octave':
        speech_spectrum, speech_level = _get_third_octave_band_speech_data(speech_level)
    elif method == 'octave':
        speech_spectrum, speech_level = _get_octave_band_speech_data(speech_level)
    nbands = len(speech_spectrum)
    
    # Create noise spectrum as uniform spectrum from overall level
    band_level = 10 * log10(power(10, noise_level/10)/nbands)
    noise_spectrum = ones((nbands)) * band_level
        
    # Compute SII
    SII, SII_specific, freq_axis = _main_sii(method, speech_spectrum, noise_spectrum, threshold)    
    
    return SII, SII_specific, freq_axis

