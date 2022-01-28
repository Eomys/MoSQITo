# -*- coding: utf-8 -*-

# Third party imports
import pytest
import numpy as np

# Local application imports
from mosqito.functions.shared.sine_wave_generator import (
    sine_wave_generator,
)
from mosqito.functions.loudness_ecma.comp_loudness_alt import comp_loudness


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
    n_specific = np.array(comp_loudness(signal))
    n_tot = np.sum(n_specific, axis=0)
    n_tot_mean_1kHz = np.mean(n_tot[5:])

    # Generate a 5kHz / 78.7 dB test tone and compute loudness
    signal, _ = sine_wave_generator(
        fs=48000,
        t=0.25,
        spl_value=78.73977248964925,
        freq=5000,
    )
    n_specific = np.array(comp_loudness(signal))
    n_tot = np.sum(n_specific, axis=0)
    n_tot_mean_5kHz = np.mean(n_tot[5:])

    # Compare loudness
    np.testing.assert_almost_equal(n_tot_mean_1kHz, n_tot_mean_5kHz)


# test de la fonction
if __name__ == "__main__":
    test_loudness_ecma()
