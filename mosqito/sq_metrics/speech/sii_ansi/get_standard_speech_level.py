def get_standard_speech_level(method, speech_type):
    """
    # Import and return the standard speech spectrum and overall level according to the method and speech type given according to ANSI S3.5-1997
    Parameters
    ----------
    method: str
        Frequency bands choice, either 'critical_bands', 'equal_critical_bands', 'third_octave_bands' or 'octave_bands'.
    speech: str
        Str to used as speech data either 'normal', 'raised', 'loud', 'shouted'.
    Returns
    -------
    STANDARD_SPEECH_SPECTRUM: array
        Array of value corresponding to the spectrum of speech for the method and speech given
    OVERALL_SPEECH_LEVEL: Float
        Value of the overall of the speech for the method and speech given
    """

    if method == "critical_bands":
        from SII_critical_band_procedure import (
            STANDARD_SPEECH_SPECTRUM_NORMAL,
            OVERALL_SPEECH_LEVEL_NORMAL,
            STANDARD_SPEECH_SPECTRUM_RAISED,
            OVERALL_SPEECH_LEVEL_RAISED,
            STANDARD_SPEECH_SPECTRUM_LOUD,
            OVERALL_SPEECH_LEVEL_LOUD,
            STANDARD_SPEECH_SPECTRUM_SHOUT,
            OVERALL_SPEECH_LEVEL_SHOUT,
        )

    elif method == "equal_critical_bands":
        from SII_equal_critical_band_procedure import (
            STANDARD_SPEECH_SPECTRUM_NORMAL,
            OVERALL_SPEECH_LEVEL_NORMAL,
            STANDARD_SPEECH_SPECTRUM_RAISED,
            OVERALL_SPEECH_LEVEL_RAISED,
            STANDARD_SPEECH_SPECTRUM_LOUD,
            OVERALL_SPEECH_LEVEL_LOUD,
            STANDARD_SPEECH_SPECTRUM_SHOUT,
            OVERALL_SPEECH_LEVEL_SHOUT,
        )
    elif method == "third_octave_bands":
        from SII_third_octave_band_procedure import (
            STANDARD_SPEECH_SPECTRUM_NORMAL,
            OVERALL_SPEECH_LEVEL_NORMAL,
            STANDARD_SPEECH_SPECTRUM_RAISED,
            OVERALL_SPEECH_LEVEL_RAISED,
            STANDARD_SPEECH_SPECTRUM_LOUD,
            OVERALL_SPEECH_LEVEL_LOUD,
            STANDARD_SPEECH_SPECTRUM_SHOUT,
            OVERALL_SPEECH_LEVEL_SHOUT,
        )
    elif method == "octave_bands":
        from SII_octave_band_procedure import (
            STANDARD_SPEECH_SPECTRUM_NORMAL,
            OVERALL_SPEECH_LEVEL_NORMAL,
            STANDARD_SPEECH_SPECTRUM_RAISED,
            OVERALL_SPEECH_LEVEL_RAISED,
            STANDARD_SPEECH_SPECTRUM_LOUD,
            OVERALL_SPEECH_LEVEL_LOUD,
            STANDARD_SPEECH_SPECTRUM_SHOUT,
            OVERALL_SPEECH_LEVEL_SHOUT,
        )

    if speech_type == "normal":
        return STANDARD_SPEECH_SPECTRUM_NORMAL, OVERALL_SPEECH_LEVEL_NORMAL
    elif speech_type == "raised":
        return STANDARD_SPEECH_SPECTRUM_RAISED, OVERALL_SPEECH_LEVEL_RAISED
    elif speech_type == "loud":
        return STANDARD_SPEECH_SPECTRUM_LOUD, OVERALL_SPEECH_LEVEL_LOUD
    elif speech_type == "shout":
        return STANDARD_SPEECH_SPECTRUM_SHOUT, OVERALL_SPEECH_LEVEL_SHOUT
