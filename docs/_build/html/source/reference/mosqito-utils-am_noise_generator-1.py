from mosqito.utils import am_noise_generator
import matplotlib.pyplot as plt
import numpy as np
fs = 48000
duration = 1
t = np.linspace(0, duration, int(duration*fs))
dB = 60
fm = 4
xmod = np.sin(2*np.pi*t*fm)
y_am, MI = am_noise_generator(xmod, dB, True)
plt.plot(t, y_am)
plt.xlabel("Time axis [s]")
plt.ylabel("Amplitude signal [Pa]")
plt.title(f'Modulation index = {MI:.1f}')
