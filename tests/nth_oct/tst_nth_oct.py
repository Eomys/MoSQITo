import matplotlib.pyplot as plt
import numpy as np

from mosqito.functions.shared.load import load
from mosqito.functions.oct3filter.oct3spec import oct3spec
from mosqito.functions.oct3filter.comp_noct_spectrum import comp_noct_spectrum

signal, fs = load(
    "./validations/loudness_zwicker/data/ISO_532-1/Test signal 5 (pinknoise 60 dB).wav",
    calib=2 * 2 ** 0.5,
)
spec_third, third_axis = oct3spec(signal, fs)
plt.semilogx(third_axis, spec_third, label="oct3spec")

spec_1, freq = comp_noct_spectrum(signal, fs, 24, 12600, n=3)
spec_1_dB = 20 * np.log10((spec_1) / (2 * 10 ** -5))
plt.semilogx(freq, spec_1_dB, label="comp_noct_spectrum")

plt.legend()
plt.show()
pass