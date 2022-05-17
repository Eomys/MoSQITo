# -*- coding: utf-8 -*-


# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package."
    )


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
    # Test signal as input for prominence ratio calculation
    # signals generated using audacity : white noise + tones at 200 and 2000 Hz

    signal =  {
            "tones freq": [200, 2000],
            "data_file": "tests/input/white_noise_442_1768_Hz_stationary.wav"
        }

    # Load signal
    audio, fs = load(signal["data_file"])
    # Compute tone-to-noise ratio
    t_tnr, tnr, prom, tones_freqs = tnr_ecma_st(audio, fs, prominence=True)
        
if __name__ == "__main__":
    test_tnr_ecma_st()


