# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:38:13 2020

@author: pc
"""
# Standard library import
import numpy as np
import math


def H_function(n, fs):
    """Weighting functions Hi definition for each 1-bark-wide interval i

    The code is based on the article "Psychoacoustical roughness:
    implementation of an optimized model" by Daniel and Weber in 1997.
    H2, H16 and H42 are given (figure 2), the others are derived from them
    in the following way:
        for i = 1,2, ... ,4 (Zi = 0.5,1, ... ,2 Bark)
            H1 = H2 = H3 = H4
        for i = 6,8, ... , 16 (Zi = 3,4, ... ,8 Bark) :
            Hi-1 = Hi and
            Hi is linearly interpolated between H4 and H16
        for i = 17,18,19,20 (Zi = 7.5,8, ... ,lOBark):
            Hi = H16
        for i = 22,24, ... ,42 (Zi = 11,12, ... ,21 Bark):
            Hi-1 = Hi and
            Hi is linearly interpolated between H20 and H42
        for i = 43,44, ... ,47 (Zi = 21.5,22, ... ,23.5 Bark):
            Hi = H42.

    Parameters
    ------------
    N : integer
        size of the full symetrical spectrum
    fs: integer
        sampling frequency
    Outputs
    -------
    H : numpy.array
        47 weighting functions Hi

    """
    cut = 2
    # freq_axis = np.concatenate((np.arange(0,int(n/2),1)*fs/n,np.zeros((int(n/2)))))
    H = np.zeros((47, n))

    # H2, H16 and H42 are given

    H2_x = np.array([0, 17, 23, 25, 32, 37, 48, 67, 90, 114, 171, 206, 247, 294, 358])
    H2_y = np.array(
        [0, 0.8, 0.95, 0.975, 1, 0.975, 0.9, 0.8, 0.7, 0.6, 0.4, 0.3, 0.2, 0.1, 0]
    )
    last = math.floor((358 / fs) * n)
    j = np.arange(cut, last)
    freq = j * fs / n
    H[1, j] = np.interp(freq[j - cut], H2_x, H2_y)

    H5_x = np.array([0, 32, 43, 56, 69, 92, 120, 142, 165, 231, 277, 331, 397, 502])
    H5_y = np.array([0, 0.8, 0.95, 1, 0.975, 0.9, 0.8, 0.7, 0.6, 0.4, 0.3, 0.2, 0.1, 0])
    last = math.floor((502 / fs) * n)
    j = np.arange(cut, last)
    freq = j * fs / n
    H[4, j] = np.interp(freq[j - cut], H5_x, H5_y)

    H16_x = np.array(
        [
            0,
            23.5,
            34,
            47,
            56,
            63,
            79,
            100,
            115,
            135,
            159,
            172,
            194,
            215,
            244,
            290,
            348,
            415,
            500,
            645,
        ]
    )
    H16_y = np.array(
        [
            0,
            0.4,
            0.6,
            0.8,
            0.9,
            0.95,
            1,
            0.975,
            0.95,
            0.9,
            0.85,
            0.8,
            0.7,
            0.6,
            0.5,
            0.4,
            0.3,
            0.2,
            0.1,
            0,
        ]
    )
    last = math.floor((502 / fs) * n)
    j = np.arange(cut, last)
    freq = j * fs / n

    H[15, j] = np.interp(freq[j - cut], H16_x, H16_y)

    H21_x = np.array(
        [
            0,
            19,
            44,
            52.5,
            58,
            75,
            101.5,
            114.5,
            132.5,
            143.5,
            165.5,
            197.5,
            241,
            290,
            348,
            415,
            500,
            645,
        ]
    )
    H21_y = np.array(
        [
            0,
            0.4,
            0.8,
            0.9,
            0.95,
            1,
            0.95,
            0.9,
            0.85,
            0.8,
            0.7,
            0.6,
            0.5,
            0.4,
            0.3,
            0.2,
            0.1,
            0,
        ]
    )
    H[20, j] = np.interp(freq[j - cut], H21_x, H21_y)

    H42_x = np.array(
        [
            0,
            15,
            41,
            49,
            53,
            64,
            71,
            88,
            94,
            106,
            115,
            137,
            180,
            238,
            290,
            348,
            415,
            500,
            645,
        ]
    )
    H42_y = np.array(
        [
            0,
            0.4,
            0.8,
            0.9,
            0.965,
            0.99,
            1,
            0.95,
            0.9,
            0.85,
            0.8,
            0.7,
            0.6,
            0.5,
            0.4,
            0.3,
            0.2,
            0.1,
            0,
        ]
    )
    H[41, j] = np.interp(freq[j - cut], H42_x, H42_y)

    # According to the article we have :

    H[0, :] = H[2, :] = H[3, :] = H[1, :]
    for i in range(5, 15):
        H[i, :] = H[4, :]
    for i in range(16, 20):
        H[i, :] = H[15, :]
    for i in range(21, 41):
        H[i, :] = H[20, :]
    for i in range(42, 47):
        H[i, :] = H[41, :]

    return H
