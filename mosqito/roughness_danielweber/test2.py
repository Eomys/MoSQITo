# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 16:28:09 2020

@author: pc
"""

import sys
sys.path.append('../..')

import numpy as np
import matplotlib.pyplot as plt

from mosqito.roughness_danielweber.comp_roughness import comp_roughness
from mosqito.tests.roughness.test_signals_generation import test_signal


carrier  = np.array([125, 250, 500, 1000, 2000, 4000])
am       = np.array([20, 40, 60, 80, 100])
m = 1
data = []


for i in  range(6):
    for j in range (5):
        signal = test_signal(carrier[i], am[j], m, 48000, 2, 60)       
        R,R_spec = comp_roughness(signal, 48000, 0)   
        data.append(R[3])

subjectivedata =np.array([0.23456556, 0.3274993 , 0.21416558, 0.14741029, 0.080655,
                         0.24667008, 0.48513448, 0.39511221, 0.30115538, 0.24304293,
                         0.25038396, 0.57844726, 0.66962706, 0.51623566, 0.45832908,
                         0.2725881 , 0.65835877, 0.96381663, 0.94625531, 0.79233478,
                         0.21526468, 0.54674524, 0.81576486, 0.80799296, 0.64492723,
                         0.16549911, 0.42709552, 0.63131927, 0.62242067, 0.48489772])

carriervec = np.array([125,125,125,125,125,250,250,250,250,250,500,500,500,500,500,1000,1000,1000,1000,1000,2000,2000,2000,2000,2000,4000,4000,4000,4000,4000])
amvec = np.array([20, 40, 60, 80, 100,20, 40, 60, 80, 100,20, 40, 60, 80, 100,20, 40, 60, 80, 100,20, 40, 60, 80, 100,20, 40, 60, 80, 100])

diff = np.zeros((30))
for i in range(30):
    diff[i] = (data[i] - subjectivedata[i])/subjectivedata[i] * 100
 
    
plt.figure(num='difference') 
plt.plot(diff)


plt.figure(num='comparaison')
plt.plot(data)
plt.plot(subjectivedata)

plt.figure()
amvec = np.array([20, 40, 60, 80, 100,20, 40, 60, 80, 100,20, 40, 60, 80, 100,
                  20, 40, 60, 80, 100,20, 40, 60, 80, 100,20, 40, 60, 80, 100])
carriervec = np.array([125,125,125,125,125,250,250,250,250,250,500,500,500,500,
                       500,1000,1000,1000,1000,1000,2000,2000,2000,2000,2000,4000,
                       4000,4000,4000,4000])
plt.scatter(amvec,carriervec,diff)