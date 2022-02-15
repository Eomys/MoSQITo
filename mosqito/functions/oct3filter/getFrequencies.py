import numpy as np


def getFrequencies(fstart, fend, b, G=10, fr=1000):
    """
    Calculate octave filter specifications
    :param fstart: start frequency
    :param fend: end frequency
    :param b: number of bands pr octave
    :param G: base
    :param fr: reference frequency
    :return: filter specification dict
    """

    # frequency matrix
    freqs = np.empty((0, 3))

    if G == 10:
        G = 10 ** (3 / 10)  # Base ten
    elif G == 2:
        G = 2
    else:
        print("The base system is not permitted. G must be 10 or 2")
        # raise

    x = -1000
    f2 = 0
    while f2 <= fend:
        # Exact midband frequencies
        if b % 2 == 0:  # even
            fm = (G ** ((2 * x - 59) / (2 * b))) * (fr)
        else:  # odd
            fm = (G ** ((x - 30) / b)) * (fr)
        # Bandedge frequencies
        f1 = (G ** (-1 / (2 * b))) * (fm)
        f2 = (G ** (1 / (2 * b))) * (fm)
        if f2 >= fstart:
            freqs = np.append(freqs, np.array([[f1, fm, f2]]), axis=0)
        x += 1
    return {"f": freqs, "b": b, "G": G}