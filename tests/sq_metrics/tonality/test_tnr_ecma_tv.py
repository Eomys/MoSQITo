# -*- coding: utf-8 -*-
# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError("In order to perform the tests you need the 'pytest' package.")

import numpy as np

# Local application imports
from mosqito.utils import load
from mosqito.sq_metrics import tnr_ecma_perseg


@pytest.mark.tnr_tv  # to skip or run TNR test
def test_tnr_ecma_perseg():
    """Test function for the prominence ratio calculation of an audio signal

    Validation function for the "tnr_ecma_perseg" function with time-varying signal array
    as input. The input signal was generated using audacity.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """
    # Test signal as input for prominence ratio calculation
    # signals generated using audacity : white noise + tones at 442 and 1768 Hz

    signal = {
        "freq": [442, 1768],
        "data_file": "tests/input/white_noise_442_1768_Hz_varying.wav",
    }

    # Load signal
    audio, fs = load(signal["data_file"], wav_calib=0.01)

    # Compute tone-to-noise ratio
    t_tnr, tnr, prom, freq, time = tnr_ecma_perseg(audio, fs, prominence=True)
    np.testing.assert_almost_equal(max(t_tnr), 34.710964273840155)
    assert tnr[np.argmin(np.abs(freq - 442)), :].all() != np.nan
    assert tnr[np.argmin(np.abs(freq - 1768)), 2:3].all() != np.nan
    assert np.count_nonzero(prom == True) == 8


if __name__ == "__main__":
    test_tnr_ecma_perseg()
