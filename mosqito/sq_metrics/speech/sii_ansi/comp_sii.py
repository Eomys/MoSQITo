from numpy import (
    empty as np_empty,
    log10,
    zeros,
    array,
    maximum as np_maximum,
    where,
    sum,
)
from get_band_procedure import get_band_procedure
from get_standard_speech_level import get_standard_speech_level


def compute_band_spectrum(x, y, lower_frequencies, upper_frequencies):
    nbands = len(lower_frequencies)
    band_spectrum = zeros((nbands))
    # convert spectrum on the selected frequency bands
    for i in range(nbands):
        # index of the frequencies within the band
        idx = where((x >= lower_frequencies[i]) & (x < upper_frequencies[i]))[0]
        band_spectrum[i] = 10 * log10(sum(10 ** (y[idx] / 10)))
    return band_spectrum


### Speech Intelligibility Index ANSI S3.5 ###
def comp_sii(
    method, noise, speech, speech_distance=1, speech_level="default", threshold=None
):
    """
    Computation of the Speech Intelligibility Index based on ANSI S3.5-1997.
    Parameters
    ----------
      method: str
        Frequency bands choice, either 'critical_bands', 'equal_critical_bands', 'third_octave_bands' or 'octave_bands'.
      noise: int / float
        Value of the noise that will be used as background noise data or overall dB level.
      speech: str
        Str to used as speech data either 'normal', 'raised', 'loud', 'shouted'.
      speech_distance: float
        Distance from the lips of the talker to the center of the head of the listener in meters.
        Default is 1m.
      speech_level: str
        If the speech was measured, the standard speech spectra can be adjusted to the measured overall level.
        'default' is the standard level corresponding to the input method.
      threshold: str
        Either 'standard' to use ANSI standard threshold, or None (0 on all bands).
    """

    # sanity checks

    # load the calculation parameters corresponding to the chosen method
    (
        CENTER_FREQUENCIES,
        LOWER_FREQUENCIES,
        UPPER_FREQUENCIES,
        IMPORTANCE,
        REFERENCE_INTERNAL_NOISE_SPECTRUM,
        STANDARD_SPEECH_SPECTRUM_NORMAL,
    ) = get_band_procedure(method=method)

    nbands = len(CENTER_FREQUENCIES)

    # if noise is an overall dB level
    if (type(noise) == float) or (type(noise) == int):
        nbands = len(CENTER_FREQUENCIES)
        noise_data = np_empty((nbands))
        noise_data.fill(10 * log10(10 ** (noise / 10) / nbands))
        noise_axis = CENTER_FREQUENCIES

    # convert the data to match the frequency bands
    if array(noise_axis != CENTER_FREQUENCIES).any():
        N = compute_band_spectrum(
            noise_axis, noise_data, LOWER_FREQUENCIES, UPPER_FREQUENCIES
        )
    else:
        N = noise_data

    # if speech is an import from the standard
    if type(speech) == str:
        E, reference_level = get_standard_speech_level(method=method, speech=speech)

        if speech_distance != 1:
            # correct the level according to the distance between talker's lips and listener's head center
            E -= 20 * log10(speech_distance)
        if speech_level != "default":
            # set dB level by comparison with standard data
            E += speech_level - reference_level

    if threshold == None:
        T = zeros((nbands))
    elif threshold == "standard":
        from mosqito.utils.LTQ import LTQ
        from mosqito.utils.conversion import freq2bark

        T = LTQ(freq2bark(CENTER_FREQUENCIES))

    # Computation
    if method == "octave_bands":
        Z = N
    else:
        V = array(E) - 24
        B = np_maximum(N, V)

        if method == "third_octave_bands":
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

                Z[i] = 10 * log10(10 ** (0.1 * N[i]) + s)
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
                            * log10(CENTER_FREQUENCIES[i] / UPPER_FREQUENCIES[k])
                        )
                    )

                    Z[i] = 10 * log10(10 ** (0.1 * N[i]) + s)
        # 4.3.2.4
        Z[0] = B[0]

    # STEP 4
    X = REFERENCE_INTERNAL_NOISE_SPECTRUM + T

    # STEP 5
    D = np_maximum(Z, X)

    # STEP 6
    L = 1 - (E - STANDARD_SPEECH_SPECTRUM_NORMAL - 10) / 160
    L[where(L > 1)] = 1

    # STEP 7
    K = (E - D + 15) / 30
    K[where(K > 1)] = 1
    K[where(K < 0)] = 0
    A = L * K

    # STEP 8
    spec_sii = IMPORTANCE * A
    sii = sum(spec_sii)

    return sii, spec_sii, CENTER_FREQUENCIES
