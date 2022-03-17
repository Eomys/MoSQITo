# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError("In order to perform the tests you need the 'pytest' package.")

import numpy as np
from mosqito.utils import sine_wave_generator
from mosqito.utils import time_segmentation


@pytest.mark.utils  # to skip or run only tests on utils module
def test_time_segmentation():

    signal, _ = sine_wave_generator(
        fs=48000,
        t=1,
        spl_value=60,
        freq=40,
    )

    blocks = time_segmentation(signal, 8192, 2048, is_ecma=True)
    np.testing.assert_array_equal(blocks.shape[1], 24)

    blocks = time_segmentation(signal, 8192, 2048, is_ecma=False)
    np.testing.assert_array_equal(blocks.shape[1], 20)


# test de la fonction
if __name__ == "__main__":
    test_time_segmentation()