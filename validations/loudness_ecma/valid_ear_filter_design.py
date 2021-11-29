# -*- coding: utf-8 -*-

import scipy.signal as sp_signal
from numpy import (
    log10,
    abs as np_abs,
    maximum as np_maximum,
    sqrt,
    mean,
)
import matplotlib.pyplot as plt

from mosqito.functions.loudness_ecma_spain.ear_filter_design import ear_filter_design
from mosqito.functions.loudness_ecma_spain.sine_wave_generator import (
    sine_wave_generator,
)

# Data import
# Threshold in quiet
from validations.loudness_ecma.input.ear_filter_ecma import (
    freq as freq_ecma,
    level as level_ecma,
)

# generate outer and middle/inner ear filter coeeficient
sos_ear = ear_filter_design()

b, a = sp_signal.sos2tf(sos_ear)

# Compute the frequency response of the filter
w, h = sp_signal.sosfreqz(sos_ear, worN=1500, fs=48000)
db = 20 * log10(np_maximum(np_abs(h), 1e-5))

# Apply filter on sine wave for test
level = []
freq = []
f = 50
while f < 20000:
    # Generate test signal
    signal, _ = sine_wave_generator(
        fs=48000,
        t=1,
        spl_value=60,
        freq=f,
    )
    # Filter
    signal_filtered = sp_signal.sosfilt(sos_ear, signal, axis=0)
    level.append(
        20 * log10(sqrt(mean(signal_filtered ** 2)))
        - 20 * log10(sqrt(mean(signal ** 2)))
    )
    freq.append(f)
    f *= 2

# Generate figure to be compared to Figure 3 from ECMA 418-2:2020
plt.semilogx(w, db, label="MOSQITO filter response")
plt.semilogx(freq_ecma, level_ecma, label="ECMA Filter response")
plt.grid(which="both")
plt.xlim((20, 20000))
plt.ylim((-25, 11))
plt.xlabel("Frequency [Hz]")
plt.ylabel("Level [dB]")

plt.semilogx(freq, level, "o", label="Filtered sine signal")
plt.legend()
plt.savefig(
    "./validations/loudness_ecma/output/" + "validation_ear_filter_design.png",
    format="png",
)