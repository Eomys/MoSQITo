# -*- coding: utf-8 -*-

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package."
        )
import numpy as np

# Local application imports
from mosqito.utils.sine_wave_generator import (
    sine_wave_generator,
)
from mosqito.sq_metrics import loudness_ecma


@pytest.mark.loudness_ecma  # to skip or run only loudness ecma tests
def test_loudness_ecma():
    """Test function for the Loudness_ecma calculation"""

    # Generate a 1kHz / 80 dB test tone and compute loudness
    signal, _ = sine_wave_generator(
        fs=48000,
        t=0.25,
        spl_value=80,
        freq=1000,
    )
    n_specific, _ = loudness_ecma(signal)
    n_specific = np.array(n_specific)
    n_tot = np.sum(n_specific, axis=0)
    n_tot_mean_1kHz = np.mean(n_tot[5:])

    # Generate a 5kHz / 78.7 dB test tone and compute loudness
    signal, _ = sine_wave_generator(
        fs=48000,
        t=0.25,
        spl_value=78.73977248964925,
        freq=5000,
    )
    n_specific, _ = loudness_ecma(signal)
    n_specific = np.array(n_specific)
    n_tot = np.sum(n_specific, axis=0)
    n_tot_mean_5kHz = np.mean(n_tot[5:])

    # Compare loudness
    np.testing.assert_almost_equal(n_tot_mean_1kHz, n_tot_mean_5kHz)


# test de la fonction
if __name__ == "__main__":
    test_loudness_ecma()
