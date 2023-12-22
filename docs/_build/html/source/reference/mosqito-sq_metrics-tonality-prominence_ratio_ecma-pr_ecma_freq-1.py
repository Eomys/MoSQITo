import numpy as np
import matplotlib.pyplot as plt
from mosqito.sound_level_meter.comp_spectrum import comp_spectrum
fs = 48000
d = 2
f = 1000
dB = 60
time = np.arange(0, d, 1/fs)
stimulus = np.sin(2 * np.pi * f * time) + 0.5 * np.sin(2 * np.pi * 3 * f * time)+ np.random.normal(0,0.5, len(time))
rms = np.sqrt(np.mean(np.power(stimulus, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = stimulus * ampl
spectrum_db, freq_axis = comp_spectrum(stimulus, fs, db=True)
plt.plot(freq_axis, spectrum_db)
plt.ylim(0,60)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Acoustic pressure [dB]")
