# -*- coding: utf-8 -*-

from numpy import array, empty, log10


def equal_loudness_contours(phones):
    """ "This function will return a 29-point equal loudness contour for your desired phon level. The frequencies
    evaluated in this function only span from 20Hz - 12.5kHz, and only 29 selective frequencies are covered. This is
    the limitation of the ISO standard".

    Function based on the MATLAB project from Jeff Tackett, 'ISO 226 Equal-Loudness-Level Contour Signal'
    (es.mathworks.com/matlabcentral/fileexchange/7028-iso-226-equal-loudness-level-contour-signal).

    Parameters
    ----------
    phones: int
        Logarithmic unit for the evaluation curve of the perceived sound (1phon = 1dB @ 1kHz).

    Returns
    -------
    spl_array: numpy.array
        Sound pressure level ('SPL') values.

    frequencies_array: numpy.array
        Frequencies in which the function computes the resulting 'SPL' values.
    """
    n_frequencies = 29
    freq_array = array([20.0, 25.0, 31.5, 40.0, 50.0, 63.0, 80.0, 100.0, 125.0, 160.0, 200.0, 250.0, 315.0, 400.0,
                           500.0, 630.0, 800.0, 1000.0, 1250.0, 1600.0, 2000.0, 2500.0, 3150.0, 4000.0, 5000.0, 6300.0,
                           8000.0, 10000.0, 12500.0])

    af = array(
        [
            0.532,
            0.506,
            0.480,
            0.455,
            0.432,
            0.409,
            0.387,
            0.367,
            0.349,
            0.330,
            0.315,
            0.301,
            0.288,
            0.276,
            0.267,
            0.259,
            0.253,
            0.250,
            0.246,
            0.244,
            0.243,
            0.243,
            0.243,
            0.242,
            0.242,
            0.245,
            0.254,
            0.271,
            0.301,
        ]
    )

    Lu = array(
        [
            -31.6,
            -27.2,
            -23.0,
            -19.1,
            -15.9,
            -13.0,
            -10.3,
            -8.1,
            -6.2,
            -4.5,
            -3.1,
            -2.0,
            -1.1,
            -0.4,
            0.0,
            0.3,
            0.5,
            0.0,
            -2.7,
            -4.1,
            -1.0,
            1.7,
            2.5,
            1.2,
            -2.1,
            -7.1,
            -11.2,
            -10.7,
            -3.1,
        ]
    )

    Tf = array(
        [
            78.5,
            68.7,
            59.5,
            51.1,
            44.0,
            37.5,
            31.5,
            26.5,
            22.1,
            17.9,
            14.4,
            11.4,
            8.6,
            6.2,
            4.4,
            3.0,
            2.2,
            2.4,
            3.5,
            1.7,
            -1.3,
            -4.2,
            -6.0,
            -5.4,
            -1.5,
            6.0,
            12.6,
            13.9,
            12.3,
        ]
    )

    # Ln = phones
    # Lp = SPL
    spl_array = empty(n_frequencies, dtype=float)

    # Deriving sound pressure level from loudness level (iso226 sect 4.1). Ln = phones
    Af = (4.47 * (10 ** (-3))) * ((10 ** (0.025 * phones)) - 1.15) + (
        (0.4 * (10 ** (((Tf + Lu) / 10) - 9))) ** af
    )

    spl_array = ((10. / af) * log10(Af)) - Lu + 94

    return spl_array, freq_array
