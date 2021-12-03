import numpy as np

NOMINAL_OCTAVE_CENTER_FREQUENCIES = np.array(
    [31.5, 63.0, 125.0, 250.0, 500.0, 1000.0, 2000.0, 4000.0, 8000.0, 16000.0]
)
"""Nominal octave center frequencies.
"""

NOMINAL_THIRD_OCTAVE_CENTER_FREQUENCIES = np.array(
    [
        25.0,
        31.5,
        40.0,
        50.0,
        63.0,
        80.0,
        100.0,
        125.0,
        160.0,
        200.0,
        250.0,
        315.0,
        400.0,
        500.0,
        630.0,
        800.0,
        1000.0,
        1250.0,
        1600.0,
        2000.0,
        2500.0,
        3150.0,
        4000.0,
        5000.0,
        6300.0,
        8000.0,
        10000.0,
        12500.0,
        16000.0,
        20000.0,
    ]
)


def index_of_frequency(frequency, fraction=1, ref=1000, G=10):
    """Determine the band index `x` from a given frequency.
    :param frequency: Frequencies :math:`f`.
    :param fraction: Bandwidth designator :math:`b`.
    :param ref: Reference frequency.
    :param G: Octave frequency ratio :math:`G`.
    The index of the center frequency is given by
    .. math:: x = round{b \\frac{\log{f/f_{ref} }}{\log{G} }}
    .. note:: This equation is not part of the standard. However, it follows from :func:`exact_center_frequency`.
    """
    fraction = np.asarray(fraction)
    uneven = (fraction % 2).astype("bool")
    return (
        np.round((2.0 * fraction * np.log(frequency / ref) / np.log(G) - 1.0))
        / 2.0
        * np.logical_not(uneven)
        + uneven
        * np.round(fraction * np.log(frequency / ref) / np.log(G)).astype("int16")
    ).astype("int16")


def exact_center_frequency(x, fraction=1, ref=1000, G=10):
    """
    Center frequencies :math:`f_m` for band indices :math:`x`. See equation 2 and 3.
    :param x: Band index :math:`x`.
    :param ref: Reference center frequency :math:`f_r`.
    :param fraction: Bandwidth designator :math`b`. For example, for 1/3-octave filter b=3.
    :param G: Octave frequency ratio :math:`G`.
    The center frequencies are given by
    .. math:: f_m = f_r G^{x/b}
    In case the bandwidth designator :math:`b` is an even number, the center frequencies are given by
    .. math:: f_m = f_r G^{(2x+1)/2b}
    See equation 2 and 3 of the standard.
    """
    fraction = np.asarray(fraction)
    uneven = (fraction % 2).astype("bool")
    return ref * G ** ((2.0 * x + 1.0) / (2.0 * fraction)) * np.logical_not(
        uneven
    ) + uneven * ref * G ** (x / fraction)


def nominal_center_freq(center, fraction):
    """Nominal frequency according to standard.
    :param center: Exact mid-frequency to be rounded.
    :param fraction: Bandwidth designator or fraction.
    """

    def _roundn(x, n):
        return round(x, -int(np.floor(np.sign(x) * np.log10(abs(x)))) + n)

    b = fraction
    x = center

    # Section E.1: 1/1-octaves
    if b == 1:
        n = index_of_frequency(x, b)
        if -6 <= n < 5:  # Correspond to indices when n=0 corresponds to 1000 Hz
            return NOMINAL_OCTAVE_CENTER_FREQUENCIES[n + 6]
        elif n >= 5:
            return 2.0 * nominal_center_freq(
                exact_center_frequency(n - 1, b), b
            )  # WARNING: Unclear in standard!
        else:
            return (
                1.0 / 2.0 * nominal_center_freq(exact_center_frequency(n + 1, b), b)
            )  # WARNING: Unclear in standard!

    # Section E.2: 1/2-octaves
    elif b == 2:
        return _roundn(x, 2)

    # Section E.1: 1/3-octaves
    elif b == 3:
        n = index_of_frequency(x, b)

        if -20 <= n < 14:  # Correspond to indices when n=0 corresponds to 1000 Hz
            return NOMINAL_THIRD_OCTAVE_CENTER_FREQUENCIES[n + 20]
        elif n >= 14:
            return 10.0 * nominal_center_freq(
                exact_center_frequency(n - 10, b), b
            )  # WARNING: Unclear in standard!
        else:
            return (
                1.0 / 10.0 * nominal_center_freq(exact_center_frequency(n + 10, b), b)
            )  # WARNING: Unclear in standard!

    # Section E3.3: 1/4 to 1/24-octaves, inclusive
    elif 4 <= b <= 24:
        msd = x // 10.0 ** np.floor(np.log10(x))
        if msd < 5:
            return _roundn(x, 2)  # E3.2
        else:
            return _roundn(x, 1)  # E3.3

    # Section E3.5: > 1/24-octaves
    elif b > 24:
        raise NotImplementedError("b > 24 is not implemented")
    else:
        raise ValueError("Wrong value for b")