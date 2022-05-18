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
from mosqito.utils import load
from mosqito.sq_metrics import tnr_ecma_st


@pytest.mark.tnr_st  # to skip or run PR test
def test_tnr_ecma_st():
    """Test function for the prominence ratio calculation of an audio signal

    Validation function for the "tnr_ecma_st" function with stationary signal array
    as input. The input signal was generated using audacity.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """
    # Test signal as input for tone to noise ratio calculation
    # signals generated using audacity : white noise + tones at 442 and 1768 Hz

    signal =  {
            "tones freq": [442, 1768],
            "data_file": "tests/input/white_noise_442_1768_Hz_stationary.wav"
        }

    # Load signal
    audio, fs = load(signal["data_file"], wav_calib=0.01)
    # Compute tone-to-noise ratio
    t_tnr, tnr, prom, freq = tnr_ecma_st(audio, fs, prominence=True)
    np.testing.assert_almost_equal(t_tnr, 32.7142766)
    np.testing.assert_almost_equal(freq.astype(np.int32), [442, 1768])
    assert np.count_nonzero(prom == True) == 2
        
if __name__ == "__main__":
    test_tnr_ecma_st()


