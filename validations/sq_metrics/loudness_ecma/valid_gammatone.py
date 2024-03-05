# -*- coding: utf-8 -*-
try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
    )


from scipy.signal import gammatone as scipy_gamma, freqz
import numpy as np

from mosqito.sq_metrics.loudness.loudness_ecma._gammatone import (
    _gammatone as mosqito_gamma,
)
from mosqito.sq_metrics.loudness.loudness_ecma._auditory_filters_centre_freq import (
    _auditory_filters_centre_freq,
)

# Sampling frequency
fs = 48000

# Auditory filters centre frequencies
centre_freq = _auditory_filters_centre_freq()
freq = centre_freq[17]

# Compute auditory filter coefficients
b, a = mosqito_gamma(freq)

m = np.arange(6)
exponential = np.exp(+1j * 2 * np.pi * freq * m / fs)

am = a / exponential
bm = b / exponential[:-1]


w, h = freqz(bm, am, worN=round(fs / 2), fs=fs)
h_db = 20.0 * np.log10(np.abs(h))
plt.semilogx(w, h_db, label="am, bm from eq. 14 and 15")

w, h = freqz(b, a, worN=round(fs / 2), fs=fs)
h_db = 20.0 * np.log10(np.abs(h))
plt.semilogx(w, h_db, label="am', bm' from eq. 16 and 17")

plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude [dB]")
plt.grid(which="both", axis="both")
plt.legend()

plt.title(
    "Auditory filter for critical band 18 (centre freq = " + str(int(freq)) + " Hz)"
)
plt.savefig(
    "./validations/sq_metrics/loudness_ecma/output/" + "validation_auditory_filter.png",
    format="png",
)
plt.close()

# Compare MOSQITO filter with Scipy one
w, h = freqz(b, a, worN=round(fs / 2), fs=fs)
h_db = 20.0 * np.log10(np.abs(h))
plt.semilogx(w, h_db, label="mosqito")

b, a = scipy_gamma(freq, "iir", fs=fs)
w, h = freqz(b, a, worN=round(fs / 2), fs=fs)
h_db = 20.0 * np.log10(np.abs(h))
plt.semilogx(w, h_db, label="scipy")

plt.title("Gammatone filter frequency response")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude [dB]")
plt.grid(which="both", axis="both")
plt.legend()
plt.savefig(
    "./validations/sq_metrics/loudness_ecma/output/" + "comparison_auditory_filter.png",
    format="png",
)
