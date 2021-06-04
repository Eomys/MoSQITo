# -*- coding: utf-8 -*-

from scipy import signal
from numpy import log10, abs as np_abs, maximum as np_maximum
import matplotlib.pyplot as plt

from mosqito.functions.hearing_model.ear_filter_design import ear_filter_design

# generate outer and middle/inner ear filter coeeficient
sos_ear = ear_filter_design()
# Compute the frequency response of the filter
w, h = signal.sosfreqz(sos_ear, worN=1500, fs=48000)
db = 20 * log10(np_maximum(np_abs(h), 1e-5))

# Generate figure to be compared to figure F.3 from ECMA-74:2019
plt.semilogx(w, db)
plt.grid(which="both")
plt.xlim((20, 20000))
plt.ylim((-25, 11))
plt.xlabel("Frequency [Hz]")
plt.ylabel("Level [dB]")
plt.show()
