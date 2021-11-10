# -*- coding: utf-8 -*-

import scipy.signal as sp_signal
from numpy import (
    log10,
    abs as np_abs,
    maximum as np_maximum,
    sqrt,
    arange,
    all as np_all,
)
from numpy.random import normal as random
import matplotlib.pyplot as plt

from mosqito.functions.loudness_ecma_spain.ear_filter_design import ear_filter_design
from mosqito.functions.loudness_ecma_spain.sine_wave_generator import (
    sine_wave_generator,
)

# generate outer and middle/inner ear filter coeeficient
sos_ear = ear_filter_design()

b, a = sp_signal.sos2tf(sos_ear)

# Compute the frequency response of the filter
w, h = sp_signal.sosfreqz(sos_ear, worN=1500, fs=48000)
db = 20 * log10(np_maximum(np_abs(h), 1e-5))

# Generate figure to be compared to figure F.3 from ECMA-74:2019
plt.semilogx(w, db)
plt.grid(which="both")
plt.xlim((20, 20000))
plt.ylim((-25, 11))
plt.xlabel("Frequency [Hz]")
plt.ylabel("Level [dB]")
plt.show()

# Generate test signal
signal, _ = sine_wave_generator(
    fs=48000,
    t=1,
    spl_value=60,
    freq=1000,
)
signal_filtered = sp_signal.sosfilt(sos_ear, signal, axis=0)
# 20*np.log10(np.sqrt(np.mean(signal ** 2))/(2e-5))
pass

# # Generate white noise
# fs = 48000
# N = 1e5
# # amp = 1 * sqrt(2)
# noise_power = fs / 2
# time = arange(N) / fs
# # filter noise
# x = random(scale=sqrt(noise_power), size=time.shape)
# # xfilt = signal.sosfiltfilt(sos_ear, x, axis=0)
# xfilt = signal.lfilter(a, b, x, axis=0)

# # plot
# f, pxx_den = signal.welch(x, fs, nperseg=1024, scaling="spectrum")
# df = f[1] - f[0]
# Pxx_den = 10 * log10(
#     pxx_den / pxx_den[np_all([f > (1000 - df / 2), f < (1000 + df / 2)], axis=0)]
# )
# plt.semilogx(f, Pxx_den, label="Raw signal")

# f, pxx_den_filt = signal.welch(xfilt, fs, nperseg=1024, scaling="spectrum")
# Pxx_den_filt = 10 * log10(
#     pxx_den_filt
#     / pxx_den_filt[np_all([f > (1000 - df / 2), f < (1000 + df / 2)], axis=0)]
# )
# plt.semilogx(f, Pxx_den_filt, label="Filtered signal")
# plt.xlim((20, 20000))
# plt.ylim((-25, 11))
# plt.xlabel("frequency [Hz]")
# plt.ylabel("PSD [V**2]")
# plt.legend()
# plt.show()