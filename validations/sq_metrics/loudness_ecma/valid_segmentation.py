# -*- coding: utf-8 -*-

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
    )

import numpy as np
# Local application imports
from mosqito.utils import sine_wave_generator
from mosqito.sq_metrics.loudness.loudness_ecma._ecma_time_segmentation import (
    _ecma_time_segmentation,
)
from mosqito.sq_metrics.loudness.loudness_ecma._band_pass_signals import (
    _band_pass_signals,
)

signal, _ = sine_wave_generator(
    fs=48000,
    t=1,
    spl_value=60,
    freq=40,
)

sb = 8192
sh = 2048

block_signals = _band_pass_signals(signal)
blocks, _ = _ecma_time_segmentation(block_signals, sb, sh, 12288)


plt.subplot(211)
plt.plot(signal)
plt.subplot(212)
plt.plot(np.arange(0, sb), blocks[0][0, :], label="block 1")
plt.plot(np.arange(sh, sh+sb), blocks[0][1, :], label="block 2")
plt.plot(np.arange(2*sh, 2*sh+sb), blocks[0][2, :], label="block 3")
plt.plot(np.arange(5*sh, 5*sh+sb), blocks[0][5, :], label="block 6")
plt.legend()
plt.show(block=True)
