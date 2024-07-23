from mosqito.sq_metrics import loudness_zwtv, sharpness_din_from_loudness
import matplotlib.pyplot as plt
import numpy as np
f=1000
fs=48000
d=0.2
dB=60
time = np.arange(0, d, 1/fs)
f = np.linspace(1000,5000, len(time))
stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
rms = np.sqrt(np.mean(np.power(stimulus, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = stimulus * ampl
N, N_spec, bark_axis, time_axis = loudness_zwtv(stimulus, fs=fs)
S = sharpness_din_from_loudness(N, N_spec)
plt.plot(time_axis, S)
plt.xlabel("Time [s]")
plt.ylabel("Sharpness [Acum]")
