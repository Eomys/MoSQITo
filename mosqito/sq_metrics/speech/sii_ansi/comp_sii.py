from numpy import log10, zeros, array, maximum as np_maximum, where, sum, ndarray
from .get_band_procedure import get_band_procedure
from .get_standard_speech_level import get_standard_speech_level
from .comp_band_spectrum import comp_band_spectrum

from mosqito.utils.LTQ import LTQ
from mosqito.utils.conversion import freq2bark


def comp_sii(
    method,
    noise,
    speech_type,
    speech_distance=1,
    speech_level=0,
    threshold=None,
):
    """
    Computation of the Speech Intelligibility Index based on ANSI S3.5-1997.
    Parameters
    ----------
      method: str
        Frequency bands choice, either 'critical_bands', 'equal_critical_bands', 'third_octave_bands' or 'octave_bands'.
    noise : ndarray
        Background noise spectrum in dB. ! axis should be the same as the one specified in method.
        In case of a single value, it will be set on each frequency band.
        If None, it is set to -50 dB.
    speech_type: str / array
        Str to used as speech data either 'normal', 'raised', 'loud', 'shouted'. Could also be a array to use directly
      speech_distance: float
        Distance from the lips of the talker to the center of the head of the listener in meters.
        Default is 1m.
      speech_level: float
        If the speech was measured, the standard speech spectra can be adjusted to the measured overall level.
        By default the standard level corresponds to the input method.
      threshold: str
        Either an array to use directly, 'zwicker' to use ANSI standard threshold or None (0 on all bands).
    """

    if (
        (method != "critical_bands")
        and (method != "equal_critical_bands")
        and (method != "third_octave_bands")
        and (method != "octave_bands")
    ):
        raise ValueError(
            'Method should be "critical_bands", "equal_critical_bands", "third_octave_bands" or "octave_bands".'
        )

    if (
        (not type(speech_type) != array)
        and (speech_type != "normal")
        and (speech_type != "raised")
        and (speech_type != "loud")
        and (speech_type != "shout")
    ):
        raise ValueError(
            'Speech should be either an array or "normal", "raised", "loud" or "shout" to use standard data.'
        )

    if (not type(speech_type) != array) and (method != "zwicker") and (method != None):
        raise ValueError('Threshold should be "zwicker", an array or "None".')

    # Step 1 : Loading the computation parameters corresponding to the chosen method
    (
        CENTER_FREQUENCIES,
        LOWER_FREQUENCIES,
        UPPER_FREQUENCIES,
        IMPORTANCE,
        REFERENCE_INTERNAL_NOISE_SPECTRUM,
        STANDARD_SPEECH_SPECTRUM_NORMAL,
    ) = get_band_procedure(method=method)

    nbands = len(CENTER_FREQUENCIES)

    # Step 2 : Creating a vector for the background noise
    nbands = len(CENTER_FREQUENCIES)

    if noise is None:
        N = zeros((len(E)))
        N.fill(-50)
    else:
        N = array(noise)
        if N.size == 1:
            N = zeros((len(E)))
            N.fill(noise)

    # noise_data = np_empty((nbands))
    # noise_data.fill(10 * log10(10 ** (noise / 10) / nbands))
    # noise_axis = CENTER_FREQUENCIES

    # # Convert the data to match the frequency bands
    # if array(noise_axis != CENTER_FREQUENCIES).any():
    #     N = comp_band_spectrum(
    #         noise_axis, noise_data, LOWER_FREQUENCIES, UPPER_FREQUENCIES
    #     )
    # else:
    #     N = noise_data

    # Step 3: Recovering the speech according to the input given (method and speech type)
    E, reference_level = get_standard_speech_level(
        method=method, speech_type=speech_type
    )

    ######### Not sure if correcting level is necessary
    # correct the level according to the distance between talker's lips and listener's head center
    if speech_distance != 1:
        E -= 20 * log10(speech_distance)

    # set dB level by comparison with standard data
    if speech_level != 0:
        E += speech_level - reference_level

    # Defining threshold if necessary
    if threshold == None:
        T = zeros((nbands))
    elif threshold == "zwicker":
        T = LTQ(freq2bark(CENTER_FREQUENCIES))
    else:
        T = array(threshold)

    # Step 4: Computation
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

    return sii, spec_sii
