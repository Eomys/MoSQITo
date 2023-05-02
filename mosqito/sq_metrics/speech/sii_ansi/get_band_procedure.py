def get_band_procedure(method):
    """
    # Import and return the calculation parameters corresponding to the method given according to ANSI S3.5-1997
    Parameters
    ----------
    method: str
        Frequency bands choice, either 'critical_bands', 'equal_critical_bands', 'third_octave_bands' or 'octave_bands'.
    Returns
    -------
    CENTER_FREQUENCIES: array
        Array of the values corresponding to the center frequency of each critical band
    LOWER_FREQUENCIES: array
        Array of the values corresponding to the lower frequency of each critical band
    UPPER_FREQUENCIES: array
        Array of the values corresponding to the higher frequency of each critical band
    IMPORTANCE: array
        Array of values corresponding to the importance of each critical band
    REFERENCE_INTERNAL_NOISE_SPECTRUM: array
        Array of reference internal noise spectrum level (in dB)
    """

    if method == "critical_bands":
        from .SII_critical_band_procedure import (
            CENTER_FREQUENCIES,
            LOWER_FREQUENCIES,
            UPPER_FREQUENCIES,
            IMPORTANCE,
            REFERENCE_INTERNAL_NOISE_SPECTRUM,
            STANDARD_SPEECH_SPECTRUM_NORMAL,
        )

    elif method == "equal_critical_bands":
        from .SII_equal_critical_band_procedure import (
            CENTER_FREQUENCIES,
            LOWER_FREQUENCIES,
            UPPER_FREQUENCIES,
            IMPORTANCE,
            REFERENCE_INTERNAL_NOISE_SPECTRUM,
            STANDARD_SPEECH_SPECTRUM_NORMAL,
        )
    elif method == "third_octave_bands":
        from .SII_third_octave_band_procedure import (
            CENTER_FREQUENCIES,
            LOWER_FREQUENCIES,
            UPPER_FREQUENCIES,
            IMPORTANCE,
            REFERENCE_INTERNAL_NOISE_SPECTRUM,
            STANDARD_SPEECH_SPECTRUM_NORMAL,
        )
    elif method == "octave_bands":
        from .SII_octave_band_procedure import (
            CENTER_FREQUENCIES,
            LOWER_FREQUENCIES,
            UPPER_FREQUENCIES,
            IMPORTANCE,
            REFERENCE_INTERNAL_NOISE_SPECTRUM,
            STANDARD_SPEECH_SPECTRUM_NORMAL,
        )

    return (
        CENTER_FREQUENCIES,
        LOWER_FREQUENCIES,
        UPPER_FREQUENCIES,
        IMPORTANCE,
        REFERENCE_INTERNAL_NOISE_SPECTRUM,
        STANDARD_SPEECH_SPECTRUM_NORMAL,
    )
