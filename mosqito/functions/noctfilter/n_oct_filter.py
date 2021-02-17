from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

"""
Script shared by https://www.encida.dk
ISO61260
"""


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
        # Excact midband frequencies
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


def designFilters(freqDict, fs=48000, plot=False):
    """
    Design octave band filters
    :param freqDict: filter specification dict
    :param fs: sample rate
    :param plot: bool if filters should be plotted
    :return: filter coefficients
    """

    freqs = freqDict["f"]
    b = freqDict["b"]
    G = freqDict["G"]

    order = 4
    filters = np.empty((0, 6))
    for index in range(np.size(freqs, axis=0)):
        lowCutoff = 2 * freqs[index, 0] / fs
        highCutoff = 2 * freqs[index, 2] / fs
        sos = signal.butter(
            order, [lowCutoff, highCutoff], btype="bandpass", output="sos"
        )
        filters = np.append(filters, sos, axis=0)

    if plot is True:
        # Requirements
        maskLevelmax = -np.array([0.15, 0.2, 0.4, 1.1, 4.5, 4.5, 200, 200, 200, 200])
        maskLevelmin = -np.array(
            [-0.15, -0.15, -0.15, -0.15, -0.15, 2.3, 18, 42.5, 62, 75]
        )
        breakpoints = np.array([0, 1 / 8, 1 / 4, 3 / 8, 1 / 2, 1 / 2, 1, 2, 3, 4])

        freqH = 1 + ((G ** (1 / (2 * b)) - 1) / (G ** (1 / 2) - 1)) * (
            G ** (breakpoints) - 1
        )
        freqL = 1 / freqH

        plt.figure(
            "Filter responses with {} bands from {} Hz to {} Hz".format(
                np.size(freqs, 0), np.int(freqs[0, 0]), np.int(freqs[-1, 2])
            )
        )
        for index in range(np.size(freqs, axis=0)):
            # Plot
            w, h = signal.sosfreqz(
                filters[(order * index) : (order * index + order), :], worN=fs
            )
            plt.semilogx(freqH * freqs[index, 1], maskLevelmax, "k--")
            plt.semilogx(freqH * freqs[index, 1], maskLevelmin, "k--")
            plt.semilogx(freqL * freqs[index, 1], maskLevelmax, "k--")
            plt.semilogx(freqL * freqs[index, 1], maskLevelmin, "k--")
            plt.semilogx((fs * 0.5 / np.pi) * w, 20 * np.log10(abs(h)))
            plt.ylim([-100, 1])
        plt.show()
    return filters


def filterData(filters, data):
    """
    Filter data using octave filters
    :param filters: octave filter coefficients
    :param data: data that should be filtered
    :return: filtered data
    """

    order = 4
    # Construct signal
    if data.ndim == 1:
        filteredSignal = np.zeros(
            [np.size(data, axis=0), int(np.size(filters, 0) / order)]
        )
        for index in range(int(np.size(filters, axis=0) / order)):
            filteredSignal[:, index] = signal.sosfilt(
                filters[(order * index) : (order * index + order), :], data
            )
    elif data.ndim == 2:
        filteredSignal = np.zeros(
            [
                np.size(data, axis=0),
                int(np.size(filters, 0) / order),
                np.size(data, axis=1),
            ]
        )
        for dataIndex in range(np.size(data, axis=1)):
            for bandIndex in range(int(np.size(filters, axis=0) / order)):
                filteredSignal[:, bandIndex, dataIndex] = signal.sosfilt(
                    filters[(order * bandIndex) : (order * bandIndex + order), :],
                    data[:, dataIndex],
                )
    return filteredSignal


def analyseData(filters, data, freqDict=None, plot=False):
    """
    Octave band analyse
    :param filters: octave filter coefficients
    :param data: data to be analysed
    :param freqDict: filter specification dict
    :param plot: bool if analysis should be plotted
    :return:
    """

    filteredSignal = filterData(filters, data)
    meanSignal = np.sqrt(np.mean(filteredSignal ** 2, axis=0))
    if plot == 1:
        minMean = np.min(np.min(20 * np.log10(meanSignal), axis=0) - 5, axis=0)
        freqs = freqDict["f"]
        fig, ax = plt.subplots()
        if meanSignal.ndim == 1:
            ax.bar(
                freqs[:, 0],
                20 * np.log10(meanSignal) - minMean,
                align="edge",
                bottom=minMean,
                width=(freqs[:, 2] - freqs[:, 0]),
            )
        elif meanSignal.ndim == 2:
            for i in range(np.size(meanSignal, axis=1)):
                ax.bar(
                    freqs[:, 0],
                    20 * np.log10(meanSignal[:, i]) - minMean,
                    align="edge",
                    bottom=minMean,
                    width=(freqs[:, 2] - freqs[:, 0]),
                )
        ax.set_xscale("log")
        plt.show()
    return meanSignal


# if __name__ == "__main__":
#     fs = 48000

#     freqs = getFrequencies(60, 20000, 1)
#     filters = designFilters(freqs, fs, plot=False)
#     # data
#     t = np.arange(0, 1, 1 / fs)
#     s = np.sin(2 * np.pi * 1000 * t)
#     # filter
#     filteredSignal = filterData(filters, s)

#     # analyse
#     rmsData = analyseData(filters, s, freqs, plot=False)

#     #plot
#     plt.figure('Results')
#     plt.subplot(1, 2, 1)
#     plt.title('Filtered signal')
#     plt.plot(filteredSignal)
#     plt.subplot(1, 2, 2)
#     plt.title('RMS signal')
#     plt.step(freqs['f'][:,1],rmsData)
#     plt.xscale('log')
#     plt.show()
