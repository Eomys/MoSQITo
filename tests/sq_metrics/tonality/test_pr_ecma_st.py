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
from mosqito.sq_metrics import pr_ecma_st


@pytest.mark.pr_st  # to skip or run PR test
def test_pr_ecma_st():
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
    # signals generated using audacity : white noise + tones at 200 and 2000 Hz

    signal = {
            "data_file": "tests/input/white_noise_442_1768_Hz_stationary.wav"
        }

    # Load signal
    audio, fs = load(signal["data_file"])

    # Compute tone-to-noise ratio
    pr = pr_ecma_st( audio, fs, prominence=True)




if __name__ == "__main__":
    test_pr_ecma_st()

