# -*- coding: utf-8 -*-
# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError("In order to perform the tests you need the 'pytest' package.")

import numpy as np

# Local application imports
from mosqito.utils import load
from mosqito.sq_metrics import tnr_ecma_tv


@pytest.mark.tnr_tv  # to skip or run TNR test
def test_tnr_ecma_tv():
    """Test function for the prominence ratio calculation of an audio signal

    Validation function for the "tnr_ecma_tv" function with time-varying signal array
    as input. The input signal was generated using audacity.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """
    # Test signal as input for prominence ratio calculation
    # signals generated using audacity : white noise + tones at 200 and 2000 Hz

    signal = {"data_file": "tests/input/white_noise_442_1768_Hz_varying.wav"}

    # Load signal
    audio, fs = load(signal["data_file"])

    # Compute tone-to-noise ratio
    t_tnr, tnr, prom, freq, time = tnr_ecma_tv(audio, fs, prominence=True)
    np.testing.assert_almost_equal(max(t_tnr), 34.995108238375025)
    assert np.count_nonzero(prom == True) == 6


if __name__ == "__main__":
    test_tnr_ecma_tv()
