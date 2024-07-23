from mosqito.sound_level_meter import noct_spectrum
from mosqito.utils import amp2db
import matplotlib.pyplot as plt
import numpy as np
f=1000
fs=48000
d=0.2
dB=60
time = np.arange(0, d, 1/fs)
stimulus = np.sin(2 * np.pi * f * time) + 0.5 * np.sin(6 * np.pi * f * time)
rms = np.sqrt(np.mean(np.power(stimulus, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = stimulus * ampl
spec, freq_axis = noct_spectrum(stimulus, fs, fmin=90, fmax=14000)
spec_db = amp2db(spec, ref=2e-5)
plt.step(freq_axis, spec_db)
plt.xlabel("Center frequency [Hz]")
plt.ylabel("Amplitude [dB]")
