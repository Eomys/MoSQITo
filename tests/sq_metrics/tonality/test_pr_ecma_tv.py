# -*- coding: utf-8 -*-

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError("In order to perform the tests you need the 'pytest' package.")

import numpy as np

# Local application imports
from mosqito.utils import load
from mosqito.sq_metrics import pr_ecma_tv


@pytest.mark.pr_tv  # to skip or run PR test
def test_pr_ecma_tv():
    """Test function for the prominence ratio calculation of an audio signal

    Validation function for the Audio_signal class "tone_to_noise_ecma" method with signal array
    as input. The input signals are generated using audacity.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """
    # Test signal as input for prominence ratio calculation
    # signals generated using audacity : white noise + tones at 442 and 1768 Hz

    signal = {"data_file": "tests/input/white_noise_442_1768_Hz_varying.wav"}

    # Load signal
    audio, fs = load(signal["data_file"], wav_calib=0.01)

    # Compute tone-to-noise ratio
    t_pr, pr, prom, freq, time = pr_ecma_tv(audio, fs, prominence=True)
    np.testing.assert_almost_equal(max(t_pr), 34.02082433185258)
    assert pr[np.argmin(np.abs(freq - 442)), :].all() != np.nan
    assert pr[np.argmin(np.abs(freq - 1768)), 2:3].all() != np.nan
    assert np.count_nonzero(prom == True) == 8


if __name__ == "__main__":
    test_pr_ecma_tv()
