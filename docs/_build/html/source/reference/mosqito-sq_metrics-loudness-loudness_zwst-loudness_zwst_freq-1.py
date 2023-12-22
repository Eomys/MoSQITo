from mosqito.sq_metrics import loudness_zwst_freq
from mosqito.sound_level_meter import comp_spectrum
import matplotlib.pyplot as plt
import numpy as np
fs=48000
d=0.2
dB=60
time = np.arange(0, d, 1/fs)
f = np.linspace(1000,5000, len(time))
stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
rms = np.sqrt(np.mean(np.power(stimulus, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = stimulus * ampl
spec, freqs = comp_spectrum(stimulus, fs, db=False)
N, N_spec, bark_axis = loudness_zwst_freq(spec, freqs)
plt.plot(bark_axis, N_spec)
plt.xlabel("Frequency band [Bark]")
plt.ylabel("Specific loudness [Sone/Bark]")
plt.title("Loudness = " + f"{N:.2f}" + " [Sone]")
