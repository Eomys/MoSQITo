# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""

import numpy as np


def phone2spl(phones, tf, af, lu):
    """ Conversion from phones to Sound Pressure Level (dB SPL), based on the standard ISO/FDIS 226:2003.

    Parameters
    ----------
    phones: float
        Logarithmic unit of loudness ('phon' = Ln).

    tf: float
        Threshold of hearing.

    af: float
        Exponent used for loudness perception.

    lu: float
        Factor of the linear transfer function normalized at 1 kHz.

    Returns
    -------
    spl: float
        Sound pressure level ('dB SPL').

    """
    # "Af" is argument of the dB SPL conversion formula
    Af = (4.47 * (10 ** (-3))) * ((10 ** (0.025 * phones)) - 1.15) + ((0.4 * (10 ** (((tf + lu) / 10) - 9))) ** af)

    # Result of the phone value converted to dB SPL value
    spl = ((10. / af) * np.log10(Af)) - lu + 94

    return spl
