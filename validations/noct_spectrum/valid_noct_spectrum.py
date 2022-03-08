try:
    import pyuff
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'pyuff' package."
        )
try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
        )

import numpy as np

from mosqito.functions.noct_spectrum.comp_noct_spectrum import comp_noct_spectrum


def valid_nthoctave(is_gen_txt=False):

    # Load signal
    uff_file = pyuff.UFF(
        "./input/electric_motor_vibration_signal.uff"
    )
    dataset = uff_file.read_sets()
    sig = dataset["data"]
    # save as txt file
    if is_gen_txt:
        np.savetxt(
            "./input/electric_motor_vibration_signal.txt",
            sig,
            delimiter=";",
        )
    # compute nth oct spectrum
    oct3, freq3 = comp_noct_spectrum(sig, fs=52000, fmin=25, fmax=20000, n=3)
    oct1, freq1 = comp_noct_spectrum(sig, fs=52000, fmin=25, fmax=20000, n=1)

    # Load DEWESOFT post-processing
    uff_file = pyuff.UFF(
        "./input/electric_motor_vibration_noct_dewe.uff"
    )
    datasets = uff_file.read_sets()
    oct3_dewe = datasets[0]["data"]
    oct1_dewe = datasets[1]["data"]

    # Load OROS post-processing
    oct3_oros = np.loadtxt(
        "./input/electric_motor_vibration_3oct_oros.txt",
        delimiter="\t",
        skiprows=2,
        usecols=1,
    )
    oct1_oros = np.loadtxt(
        "./input/electric_motor_vibration_1oct_oros.txt",
        delimiter="\t",
        skiprows=2,
        usecols=1,
    )

    # plot
    plt.semilogx(freq3, 10 * np.log10(oct3 / 1e-6), label="Mosqito")
    plt.semilogx(freq3, 10 * np.log10(oct3_dewe / 1e-6), label="DEWESOFT")
    plt.semilogx(freq3, 10 * np.log10(oct3_oros / 1e-6), label="OROS")
    plt.legend()
    plt.xlabel("Frequency")
    plt.ylabel("Vibration acceleration [dB]")
    plt.savefig(
        "./output/" + "validation_3oct_spectrum.png",
        format="png",
    )
    plt.clf()

    plt.semilogx(freq1, 10 * np.log10(oct1 / 1e-6), label="Mosqito")
    plt.semilogx(freq1, 10 * np.log10(oct1_dewe / 1e-6), label="DEWESOFT")
    plt.semilogx(freq1, 10 * np.log10(oct1_oros / 1e-6), label="OROS")
    plt.legend()
    plt.xlabel("Frequency")
    plt.ylabel("Vibration acceleration [dB]")
    plt.savefig(
        "./output/" + "validation_1oct_spectrum.png",
        format="png",
    )
    plt.clf()


if __name__ == "__main__":
    valid_nthoctave()