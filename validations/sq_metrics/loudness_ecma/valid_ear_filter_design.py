# -*- coding: utf-8 -*-
try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
        )


import scipy.signal as sp_signal
from numpy import (
    log10,
    abs as np_abs,
    maximum as np_maximum,
    sqrt,
    mean,
)

from mosqito.sq_metrics.loudness.loudness_ecma._ear_filter_design import (
    _ear_filter_design,
)
from mosqito.utils.sine_wave_generator import (
    sine_wave_generator,
)

# Data import
# Threshold in quiet
from validations.sq_metrics.loudness_ecma.input.ear_filter_ecma import (
    freq as freq_ecma,
    level as level_ecma,
)

# generate outer and middle/inner ear filter coeeficient
sos_ear = _ear_filter_design()

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
    "./validations/sq_metrics/loudness_ecma/output/"
    + "validation_ear_filter_design.png",
    format="png",
)
plt.clf()