from mosqito.sound_level_meter import noct_synthesis
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
n = len(stimulus)
spec = np.abs(2/np.sqrt(2)/n*np.fft.fft(stimulus)[:n//2])
freqs = np.linspace(0, fs//2,n//2)
spec_3, freq_axis = noct_synthesis(spec, freqs, fmin=90, fmax=14000)
spec_3db = amp2db(spec_3, ref=2e-5)
plt.step(freq_axis, spec_3db)
plt.ylim(0,60)
plt.xlabel("Center frequency [Hz]")
plt.ylabel("Amplitude [dB]")
