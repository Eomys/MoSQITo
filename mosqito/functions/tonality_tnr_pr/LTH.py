# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:54:02 2020

@author: wantysal
"""
import numpy as np


def LTH(freqs):
    """Definition of the lower threshold of hearing according to
    ECMA-74 annex D.7.1"""

    LTH = np.zeros((len(freqs)))
    for i in range(len(freqs)):
        f = freqs[i]

        if f >= 20 and f < 305:
            fmean = 167.5
            fstd = 87.3212
            a1 = 1.415532
            a2 = -2.451068
            a3 = 1.498869
            a4 = -6.983224
            a5 = 8.621226

        elif f >= 305 and f < 2230:
            fmean = 1157.5
            fstd = 488.582
            a1 = 0.397994
            a2 = -0.891839
            a3 = -0.815138
            a4 = -1.221319
            a5 = -7.600754

        elif f >= 2230 and f < 14000:
            fmean = 7250
            fstd = 3033.25
            a1 = 1.584978
            a2 = -2.766599
            a3 = -6.9061912
            a4 = 10.138553
            a5 = -3.149339

        elif f >= 14000 and f < 22050:
            fmean = 16990.0
            fstd = 4049.0
            a1 = -5.775593
            a2 = -9.200034
            a3 = 26.59115
            a4 = 52.16712
            a5 = 15.61552048

        ff = (f - fmean) / fstd
        LTH[i] = a1 * ff ** 4 + a2 * ff ** 3 + a3 * ff ** 2 + a4 * ff + a5

    return LTH
