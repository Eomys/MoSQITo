from mosqito.sq_metrics.speech_intelligibility import sii_ansi
import matplotlib.pyplot as plt
import numpy as np
fs=48000
d=0.2
dB=90
time = np.arange(0, d, 1/fs)
f = 50
stimulus = np.sin(2 * np.pi * f * time) * np.sin(np.pi * f * time) + np.sin(10 * np.pi * f * time) + np.sin(100 * np.pi * f * time)
rms = np.sqrt(np.mean(np.power(stimulus, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = stimulus * ampl
SII, SII_spec, freq_axis = sii_ansi(stimulus, fs, method='critical', speech_level='normal')
plt.plot(freq_axis, SII_spec)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Specific value ")
plt.title("Speech Intelligibility Index = " + f"{SII:.2f}")
