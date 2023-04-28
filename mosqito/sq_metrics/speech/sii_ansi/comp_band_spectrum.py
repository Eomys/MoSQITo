from numpy import zeros, where, log10


def comp_band_spectrum(x, y, lower_frequencies, upper_frequencies):
    nbands = len(lower_frequencies)
    band_spectrum = zeros((nbands))
    # convert spectrum on the selected frequency bands
    for i in range(nbands):
        # index of the frequencies within the band
        idx = where((x >= lower_frequencies[i]) & (x < upper_frequencies[i]))[0]
        band_spectrum[i] = 10 * log10(sum(10 ** (y[idx] / 10)))
    return band_spectrum
