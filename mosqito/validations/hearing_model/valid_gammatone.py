# -*- coding: utf-8 -*-

from scipy.signal import gammatone as scipy_gamma, freqz
from numpy import log10, abs as np_abs
import matplotlib.pyplot as plt

from mosqito.functions.hearing_model.gammatone import gammatone as mosqito_gamma

freq = 400
fs = 48000

b, a = mosqito_gamma(freq)
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
plt.show()
