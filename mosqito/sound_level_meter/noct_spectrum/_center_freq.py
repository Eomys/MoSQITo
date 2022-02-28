import numpy as np

from mosqito.sound_level_meter.noct_spectrum._nominal_frequency import (
    NOMINAL_OCTAVE_CENTER_FREQUENCIES,
    NOMINAL_THIRD_OCTAVE_CENTER_FREQUENCIES,
)


def _center_freq(fmin, fmax, n=3, G=10, fr=1000):
    """
    Compute nth octave filter frequencies

    References:
        ANSI S1.1-1986 (ASA 65-1986): Specifications for
        Octave-Band and Fractional-Octave-Band Analog and
        Digital Filters.

    Parameters
    ----------
    fmin : float
        Min frequency band [Hz]
    fmax : float
        Max frequency band [Hz]
    n : int, optional
        number of bands pr octave. Default to 3
    G : int, optional
        System for specifying the exact geometric mean frequencies.
        Can be base 2 or base 10. Default to base 10
    fr : int, optional
        Reference frequency. Shall be set to 1 kHz for audible frequency
        range, to 1 Hz for infrasonic range (f < 20 Hz) and to 1 MHz for
        ultrasonic range (f > 31.5 kHz). Default to 1000 Hz

    Outputs
    -------
    f_exact : ndarray
        Exact center frequencies
    """

    # determine band numbers
    b = 1 / n
    if G == 2:
        U = 2 ** b  # ANSI eq2
    elif G == 10:
        U = 10 ** (3 * b / 10)  # ANSI eq4
    else:
        raise ValueError(
            """ERROR: Only base 2 and base 10 are allowed for nth
            octave center frequency definition"""
        )
    [kmin, kmax] = np.round(
        np.log10(np.array([fmin, fmax]) / fr) / np.log10(U), 0)

    # Band numbers such that f_exact = fr for k=0
    k = np.arange(kmin, kmax + 1).astype(int)

    # compute ANSI eq1
    f_exact = fr * U ** k

    ####
    # get normalized frequencies
    ####

    f_nom = f_exact.copy()

    if n == 1:
        freq = NOMINAL_OCTAVE_CENTER_FREQUENCIES
    elif n == 3:
        freq = NOMINAL_THIRD_OCTAVE_CENTER_FREQUENCIES
    if n == 1 or n == 3:
        i_ref = np.where(freq == fr)[0][0]
        ind = np.where(k >= -i_ref) and np.where(k < len(freq) - i_ref)
        f_nom[ind] = freq[k[ind] + i_ref]

    # TODO
    # Manage other values of n
    # Manage band outside the known bands

    return f_exact, f_nom


if __name__ == "__main__":
    f_exact, f_nom = _center_freq(25, 50000, n=3, G=10, fr=1000)
    pass
