# -*- coding: utf-8 -*-

from scipy.signal import gammatone as scipy_gamma, freqz
from numpy import log10, abs as np_abs
import matplotlib.pyplot as plt

from mosqito.functions.loudness_ecma_spain.gammatone import (
    gammatone as mosqito_gamma,
)
from mosqito.functions.loudness_ecma_spain.gen_auditory_filters_centre_freq import (
    gen_auditory_filters_centre_freq,
)

# Sampling frequency
fs = 48000

# Auditory filters centre frequencies
centre_freq = gen_auditory_filters_centre_freq()
freq = centre_freq[17]

# Compute auditory filter coefficients
b, a = mosqito_gamma(freq, is_plot=True)
plt.title(
    "Auditory filter for critical band 18 (centre freq = " + str(int(freq)) + " Hz)"
)
plt.savefig(
    "./validations/loudness_ecma/output/" + "validation_auditory_filter.png",
    format="png",
)
plt.close()

# Compare MOSQITO filter with Scipy one
w, h = freqz(b, a, worN=round(fs / 2), fs=fs)
h_db = 20.0 * log10(np_abs(h))
plt.semilogx(w, h_db, label="mosqito")

b, a = scipy_gamma(freq, "iir", fs=fs)
w, h = freqz(b, a, worN=round(fs / 2), fs=fs)
h_db = 20.0 * log10(np_abs(h))
plt.semilogx(w, h_db, label="scipy")

plt.title("Gammatone filter frequency response")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude [dB]")
plt.grid(which="both", axis="both")
plt.legend()
plt.savefig(
    "./validations/loudness_ecma/output/" + "comparison_auditory_filter.png",
    format="png",
)