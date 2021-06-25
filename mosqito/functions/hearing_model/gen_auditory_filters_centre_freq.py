from numpy import arange
from numpy import sinh


def gen_auditory_filters_centre_freq():
    """
    Auditory filter bank center frequencies generation

    This function generates the Auditory filter bank center frequencies according
    to ECMA-418-2 section 5.1.3.1 equation 6

    Parameters
    ----------

    Returns
    -------
    centre_freq: ndarray
        Vector of auditory filter bank center frequencies

    """

    band_number = arange(53)
    z_step_size = 0.50
    af_f0 = 81.9289  # ECMA-418-2
    c = 0.1618  # ECMA-418-2

    # Critical band rate scale
    z = (band_number + 1) * z_step_size
    var = c * z

    # Central frequency
    centre_freq = (af_f0 / c) * sinh(var)

    return centre_freq


if __name__ == "__main__":
    centre_freq = gen_auditory_filters_centre_freq()
