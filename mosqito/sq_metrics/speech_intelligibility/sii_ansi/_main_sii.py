# -*- coding: utf-8 -*-


from numpy import array, zeros, log10, maximum, where, sum

from mosqito.sq_metrics.speech_intelligibility.sii_ansi._band_procedure_data import (
    _get_critical_band_data,
    _get_equal_critical_band_data,
    _get_octave_band_data,
    _get_third_octave_band_data,
)
from mosqito.sq_metrics.speech_intelligibility.sii_ansi._speech_data import (
    _get_critical_band_speech_data,
    _get_equal_critical_band_speech_data,
    _get_octave_band_speech_data,
    _get_third_octave_band_speech_data,
)
from mosqito.utils.LTQ import LTQ
from mosqito.utils.conversion import freq2bark


def _main_sii(method, speech_spectrum, noise_spectrum, threshold):
    """Calculate core speech intelligibility index

    This function computes SII values based on ANSI S3.5 standard.

    Parameters
    ----------
    method: {"critical", "equally_critical", "third_octave", "octave"}
        Type of frequency band to be used for the calculation.
    speech_spectrum : array_like
        Speech spectrum [dB ref. 2e-5 Pa] with same size as the chosen method frequency axis.
    noise_spectrum : array_like
        Noise spectrum [dB ref. 2e-5 Pa] with same size as the chosen method frequency axis.
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
    """

    if (
        (method != "critical")
        & (method != "equally_critical")
        & (method != "third_octave")
        & (method != "octave")
    ):
        raise ValueError(
            'Method should be within {"critical", "equally_critical", "third_octave", "octave"}.'
        )

    # Get band data according to the chosen method
    if method == "critical":
        (
            CENTER_FREQUENCIES,
            LOWER_FREQUENCIES,
            UPPER_FREQUENCIES,
            IMPORTANCE,
            REFERENCE_INTERNAL_NOISE_SPECTRUM,
            STANDARD_SPEECH_SPECTRUM_NORMAL,
        ) = _get_critical_band_data()
    elif method == "equally_critical":
        (
            CENTER_FREQUENCIES,
            LOWER_FREQUENCIES,
            UPPER_FREQUENCIES,
            IMPORTANCE,
            REFERENCE_INTERNAL_NOISE_SPECTRUM,
            STANDARD_SPEECH_SPECTRUM_NORMAL,
        ) = _get_equal_critical_band_data()
    elif method == "third_octave":
        (
            CENTER_FREQUENCIES,
            _,
            _,
            _,
            IMPORTANCE,
            REFERENCE_INTERNAL_NOISE_SPECTRUM,
            STANDARD_SPEECH_SPECTRUM_NORMAL,
        ) = _get_third_octave_band_data()
    elif method == "octave":
        (
            CENTER_FREQUENCIES,
            _,
            _,
            _,
            IMPORTANCE,
            REFERENCE_INTERNAL_NOISE_SPECTRUM,
            STANDARD_SPEECH_SPECTRUM_NORMAL,
        ) = _get_octave_band_data()
    nbands = len(CENTER_FREQUENCIES)

    if threshold is None:
        T = zeros((nbands))
    elif threshold == "zwicker":
        T = LTQ(freq2bark(CENTER_FREQUENCIES))
    else:
        T = array(threshold)

    # dB bandwidth adjustement
    if (method == "critical_bands") or (method == "equal_critical_bands"):
        noise_spectrum -= 10 * log10(UPPER_FREQUENCIES - LOWER_FREQUENCIES)

    # STEP 3
    if method == "octave":
        Z = noise_spectrum
    else:
        V = speech_spectrum - 24
        B = maximum(noise_spectrum, V)
        if method == "third_octave":
            C = -80 + 0.6 * (B + 10 * log10(CENTER_FREQUENCIES) - 6.353)
            Z = zeros((nbands))
            for i in range(nbands):
                s = 0
                for k in range(i):
                    s += 10 ** (
                        0.1
                        * (
                            B[k]
                            + 3.32
                            * C[k]
                            * log10(
                                0.89 * CENTER_FREQUENCIES[i] / CENTER_FREQUENCIES[k]
                            )
                        )
                    )
                Z[i] = 10 * log10(10 ** (0.1 * noise_spectrum[i]) + s)
        else:
            C = -80 + 0.6 * (B + 10 * log10(UPPER_FREQUENCIES - LOWER_FREQUENCIES))
            Z = zeros((nbands))
            for i in range(nbands):
                s = 0
                for k in range(i - 1):
                    s += 10 ** (
                        0.1
                        * (
                            B[k]
                            + 3.32
                            * C[k]
                            * log10(CENTER_FREQUENCIES[i] / CENTER_FREQUENCIES[k])
                        )
                    )
                Z[i] = 10 * log10(10 ** (0.1 * noise_spectrum[i]) + s)
        # 4.3.2.4
        Z[0] = B[0]

    # STEP 4
    X = REFERENCE_INTERNAL_NOISE_SPECTRUM + T

    # STEP 5
    D = maximum(Z, X)

    # STEP 6
    L = 1 - (speech_spectrum - STANDARD_SPEECH_SPECTRUM_NORMAL - 10) / 160
    L[where(L > 1)] = 1

    # STEP 7
    K = (speech_spectrum - D + 15) / 30
    K[where(K > 1)] = 1
    K[where(K < 0)] = 0
    A = L * K

    # STEP 8
    SII = sum(IMPORTANCE * A)
    SII_specific = IMPORTANCE * A

    return SII, SII_specific, CENTER_FREQUENCIES
