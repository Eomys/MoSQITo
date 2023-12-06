from mosqito.sq_metrics import loudness_zwst_freq
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
n = len(stimulus)
spec = np.abs(2/np.sqrt(2)/n*np.fft.fft(stimulus)[:n//2])
freqs = np.linspace(0, fs//2,n//2)
N, N_spec, bark_axis = loudness_zwst_freq(spec, freqs)
plt.plot(bark_axis, N_spec)
plt.xlabel("Frequency band [Bark]")
plt.ylabel("Specific loudness [Sone/Bark]")
plt.title("Loudness = " + f"{N:.2f}" + " [Sone]")
