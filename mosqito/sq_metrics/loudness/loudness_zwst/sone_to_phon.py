# -*- coding: utf-8 -*-
"""
@date Created on Fri Feb 28 2020
@author martin_g for Eomys
"""

# Standard library imports
import math


def sone_to_phon(sone):
    """Calculate Loudness level [phons] from Loudness [sones]

    The code is based on BASIC program published in "Program for
    calculating loudness according to DIN 45631 (ISO 532B)", E.Zwicker
    and H.Fastl, J.A.S.J (E) 12, 1 (1991).

    Parameters
    ----------
    N : float
        Loudness [sones]

    Outputs
    -------
    LN : float
        Loudness level [phons]
    """

    if sone < 1:
        phon = 40 * sone ** 0.35
        if phon < 3:
            phon = 3
    else:
        phon = 10 * math.log2(sone) + 40
    return phon
