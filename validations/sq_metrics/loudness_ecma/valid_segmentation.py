# -*- coding: utf-8 -*-

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
    )

# Local application imports
from mosqito.utils.sine_wave_generator import (
    sine_wave_generator,
)
from mosqito.utils import time_segmentation


signal, _ = sine_wave_generator(
    fs=48000,
    t=1,
    spl_value=60,
    freq=40,
)
blocks = time_segmentation(signal, 8192, 2048, is_ecma=True)

plt.subplot(211)
plt.plot(signal)
plt.subplot(212)
plt.plot(blocks[0], label="block 1")
plt.plot(blocks[1], label="block 2")
plt.plot(blocks[2], label="block 3")
plt.plot(blocks[5], label="block 6")
plt.legend()
plt.show()