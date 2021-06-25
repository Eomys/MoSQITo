# -*- coding: utf-8 -*-

# Third party imports
import pytest
from numpy import mean

# Local application imports
from mosqito.functions.hearing_model.sine_wave_generator import sine_wave_generator
from mosqito.functions.hearing_model.comp_loudness import comp_loudness
from mosqito.functions.hearing_model.sone2phone import sone2phone


@pytest.mark.loudness_ecma  # to skip or run only loudness ecma tests
def test_loudness_ecma():
    """Test function for the Loudness_ecma calculation

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """

    signal, samples = sine_wave_generator(
        fs=48000,
        t=1,
        spl_value=60,
        freq=1000,
    )
    t_array = comp_loudness(signal, validation=False)[1]
    mean_loudness_value = mean(t_array[:, 0])
    phon_loudness_value = sone2phone(mean_loudness_value)
    assert phon_loudness_value < 60.1 and phon_loudness_value > 59.9


# test de la fonction
if __name__ == "__main__":
    test_loudness_ecma()
