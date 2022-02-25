# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

# Local application imports
from mosqito.utils.sine_wave_generator import (
    sine_wave_generator,
)
from mosqito.sq_metrics.loudness.loudness_ecma._segmentation_blocks import (
    _segmentation_blocks,
)

signal, _ = sine_wave_generator(
    fs=48000,
    t=1,
    spl_value=60,
    freq=40,
)
blocks = _segmentation_blocks(signal, 8192, 2048)

plt.subplot(211)
plt.plot(signal)
plt.subplot(212)
plt.plot(blocks[0], label="block 1")
plt.plot(blocks[1], label="block 2")
plt.plot(blocks[2], label="block 3")
plt.plot(blocks[5], label="block 6")
plt.legend()
plt.show()