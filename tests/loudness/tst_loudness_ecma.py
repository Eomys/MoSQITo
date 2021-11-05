# -*- coding: utf-8 -*-

# Third party imports
import pytest
import numpy as np

# Local application imports
from mosqito.functions.hearing_model.sine_wave_generator import sine_wave_generator
from mosqito.functions.hearing_model.comp_loudness_alt import comp_loudness
from mosqito.functions.hearing_model.sone2phone import sone2phone


# @pytest.mark.loudness_ecma  # to skip or run only loudness ecma tests
def tst_loudness_ecma():
    """Test function for the Loudness_ecma calculation

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """

    signal, _ = sine_wave_generator(
        fs=48000,
        t=1,
        spl_value=60,
        freq=1000,
    )
    n_array = comp_loudness(signal)
    specific_loudness = np.array(n_array)
    tot_loudness = np.sum(specific_loudness, axis=0)
    mean_tot_loudness = np.mean(tot_loudness)
    phon_loudness_value = sone2phone(mean_tot_loudness)
    assert phon_loudness_value < 60.1 and phon_loudness_value > 59.9

    pass


# test de la fonction
if __name__ == "__main__":
    tst_loudness_ecma()
