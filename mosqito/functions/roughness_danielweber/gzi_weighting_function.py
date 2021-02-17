# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 10:29:02 2020

@author: wantysal
"""

import numpy as np


def gzi_definition(center_freq):
    """ Weighting function for the specific roughness given by Aures """

    gr_x = np.arange(0, 25, 1)
    gr_y = np.array(
        [
            0.15,
            0.26,
            0.38,
            0.47,
            0.54,
            0.65,
            0.76,
            0.83,
            0.90,
            0.98,
            0.98,
            0.90,
            0.80,
            0.70,
            0.62,
            0.54,
            0.49,
            0.43,
            0.39,
            0.35,
            0.30,
            0.30,
            0.30,
            0.30,
            0.30,
        ]
    )

    gzi = np.interp(center_freq, gr_x, gr_y)

    return gzi
