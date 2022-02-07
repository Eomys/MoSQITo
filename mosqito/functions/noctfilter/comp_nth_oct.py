from numpy import log10

from mosqito.functions.noctfilter.n_oct_filter import (
    getFrequencies,
    designFilters,
    analyseData,
)
from mosqito.functions.noctfilter.nominal_center_freq import nominal_center_freq
from mosqito.functions.shared.load import load


def comp_nth_oct(signal, fs, fmin=25, fmax=12500, n=3):
    """nth-octave band spectrum calculation

    Parameters
    ----------
    signal : ndarray
        time signal values [Pa]
    fs : int
        sampling frequency
    fmin : float
        min frequency of the output spectrum
    fmax : float
        max frequency of the output spectrum
    n : int
        number of bands pr octave


    Outputs
    --------
    spectrum : ndarray
        nth octave band spectrum of signal sig [Pa]
    freq : ndarray
        Corresponding nth octave bands center frequencies
    """

    f_dict = getFrequencies(fmin, fmax, n)
    filters = designFilters(f_dict, fs, plot=False)
    spectrum = analyseData(filters, signal, f_dict, plot=False)

    spec_dB = 20 * log10((spectrum) / (2e-5))

    freq = [nominal_center_freq(f, n) for f in f_dict["f"][:, 1]]

    return spec_dB, freq


if __name__ == "__main__":
    signal, fs = load(
        "./validations/loudness_zwicker/data/ISO_532-1/Test signal 5 (pinknoise 60 dB).wav",
        calib=2 * 2 ** 0.5,
    )
    spectrum, freq = comp_nth_oct(signal, fs)