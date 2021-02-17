# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 09:04:04 2020

@author: pc
"""
import numpy as np


def critical_band(f0):
    """Analytical definition of the critical band centered on f0
    according to ECMA-74 annex D.8"""

    delta_fc = 25 + 75 * np.power(1 + 1.4 * np.power(f0 / 1000, 2), 0.69)

    if f0 < 500:
        f1 = f0 - delta_fc / 2
        f2 = f0 + delta_fc / 2

    elif f0 >= 500:
        f1 = -1 * delta_fc / 2 + np.sqrt(delta_fc ** 2 + 4 * f0 ** 2) / 2
        f2 = f1 + delta_fc

    return f1, f2


def lower_critical_band(f0):
    """Analytical definition of the critical band immediately below and contiguous
    with the critical band centered on f0 according to ECMA-74 annex D.10
    """

    f2, _ = critical_band(f0)

    if f0 < 171.4:
        c0 = 20
        c1 = 0
        c2 = 0
    elif f0 >= 171.4 and f0 <= 1600:
        c0 = -149.5
        c1 = 1.001
        c2 = -6.9e-05
    elif f0 > 1600:
        c0 = 6.8
        c1 = 0.806
        c2 = -8.2e-06

    f1 = c0 + c1 * f0 + c2 * f0 ** 2

    return f1, f2


def upper_critical_band(f0):
    """Analytical definition of the critical band immediately above and contiguous
    with the critical band centered on f0 according to ECMA-74 annex D.10
    """

    _, f1 = critical_band(f0)

    if f0 <= 1600:
        c0 = 149.5
        c1 = 1.035
        c2 = 7.7e-05
    elif f0 > 1600:
        c0 = 3.3
        c1 = 1.215
        c2 = 2.16e-05

    f2 = c0 + c1 * f0 + c2 * f0 ** 2

    return f1, f2
