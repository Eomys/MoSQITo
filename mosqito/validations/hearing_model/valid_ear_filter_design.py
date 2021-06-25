# -*- coding: utf-8 -*-

from scipy import signal
from numpy import log10, abs as np_abs, maximum as np_maximum, sqrt, arange
from numpy.random import normal as random
import matplotlib.pyplot as plt

from mosqito.functions.hearing_model.ear_filter_design import ear_filter_design

# generate outer and middle/inner ear filter coeeficient
sos_ear = ear_filter_design()

# Compute the frequency response of the filter
w, h = signal.sosfreqz(sos_ear, worN=1500, fs=48000)
db = 20 * log10(np_maximum(np_abs(h), 1e-5))

# Generate figure to be compared to figure F.3 from ECMA-74:2019
# plt.semilogx(w, db)
# plt.grid(which="both")
# plt.xlim((20, 20000))
# plt.ylim((-25, 11))
# plt.xlabel("Frequency [Hz]")
# plt.ylabel("Level [dB]")
# plt.show()

# Generate white noise
fs = 48000
N = 1e5
amp = 2 * sqrt(2)
noise_power = 0.001 * fs / 2
time = arange(N) / fs
# filter noise
x = random(scale=sqrt(noise_power), size=time.shape)
xfilt = signal.sosfiltfilt(sos_ear, x, axis=0)
# plot
f, Pxx_den = signal.welch(x, fs, nperseg=1024)
plt.loglog(f, Pxx_den, label="Raw signal")
f, Pxx_den_filt = signal.welch(xfilt, fs, nperseg=1024)
plt.loglog(f, Pxx_den_filt, label="Filtered signal")
plt.ylim([0.5e-3, 1])
plt.xlabel("frequency [Hz]")
plt.ylabel("PSD [V**2/Hz]")
plt.show()