from mosqito.utils import am_sine_generator
import matplotlib.pyplot as plt
import numpy as np
fs = 48000      # [Hz]
duration = 1
t = np.linspace(0, duration, int(fs*duration))
dB = 60         # [dB SPL]
fc = 100        # [Hz]
fm = 4          # [Hz]
xmod = np.sin(2*np.pi*t*fm)
y_am, m = am_sine_generator(xmod, fs, fc, dB, True)
plt.plot(t, y_am)
plt.xlabel("Time axis [s]")
plt.ylabel("Amplitude signal [Pa]")
plt.title(f'Modulation index = {m:.1f}')
