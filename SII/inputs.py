# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 12:13:52 2022

@author: salome.wanty
"""
import matplotlib.pyplot as plt
from numpy import array
import numpy

speech = array([32.41,
34.48,
34.75,
33.98,
34.59,
34.27,
32.06,
28.30,
25.01,
23.00,
20.15,
17.32,
13.18,
11.55,
9.33,
5.31,
2.59,
1.13])

x = array(
    [
    160,
    200,
    250,
    315,
    400,
    500,
    630,
    800,
    1000,
    1250,
    1600,
    2000,
    2500,
    3150,
    4000,
    5000,
    6300,
    8000
    ]
    )


noise = array([
0.00,
0.00,
10.00,
20.00,
30.00,
33.00,
40.00,
36.00,
22.00,
00.00,
00.00,
00.00,
00.00,
00.00,
00.00,
00.00,
00.00,
00.00   
    ])


plt.figure()
plt.plot(speech, label='Speech level',linestyle='--')
plt.plot(noise, label='Noise level')
plt.legend()
plt.xlabel('Frequency (third-octave band)')
plt.ylabel('Amplitude (dB')
plt.title('Input data')


plt.close()


y_speech = numpy.array([32.41,
        34.48,
        34.75,
        33.98,
        34.59,
        34.27,
        32.06,
        28.30,
        25.01,
        23.00,
        20.15,
        17.32,
        13.18,
        11.55,
        9.33,
        5.31,
        2.59,
        1.13])

y_speech = numpy.array([54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54])


x = numpy.array(
        [
        160,
        200,
        250,
        315,
        400,
        500,
        630,
        800,
        1000,
        1250,
        1600,
        2000,
        2500,
        3150,
        4000,
        5000,
        6300,
        8000
        ]
        )


y_noise = numpy.array([
        0.00,
        0.00,
        10.00,
        20.00,
        30.00,
        33.00,
        40.00,
        36.00,
        22.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00   
            ])

y_noise = numpy.array([
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
            ])


speech = SQMetrics(x, numpy.array(10**(y_speech/20)*2e-5,dtype=complex),domain='frequency',spectrum_type='spectrum')
noise = SQMetrics(x,numpy.array(10**(y_noise/20)*2e-5,dtype=complex),domain='frequency',spectrum_type='spectrum')

sii_from_speech = speech.sii('third_octave_bands', noise=noise, speech=speech, threshold='None')
sii_from_noise = noise.sii('third_octave_bands', noise=noise, speech='standard_normal_speech', threshold='standard')








