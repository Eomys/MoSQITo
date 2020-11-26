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
dataa=[]
data = np.zeros((len(carrier),len(am)))
diff = np.zeros((len(carrier),len(am)))

subjectivedata =np.array([[0.23456556, 0.3274993 , 0.21416558, 0.14741029, 0.080655],
                         [0.24667008, 0.48513448, 0.39511221, 0.30115538, 0.24304293],
                         [0.25038396, 0.57844726, 0.66962706, 0.51623566, 0.45832908],
                         [0.2725881 , 0.65835877, 0.96381663, 0.94625531, 0.79233478],
                         [0.21526468, 0.54674524, 0.81576486, 0.80799296, 0.64492723],
                         [0.16549911, 0.42709552, 0.63131927, 0.62242067, 0.48489772]])

subjectivedataa =np.array([0.23456556, 0.3274993 , 0.21416558, 0.14741029, 0.080655,
                         0.24667008, 0.48513448, 0.39511221, 0.30115538, 0.24304293,
                         0.25038396, 0.57844726, 0.66962706, 0.51623566, 0.45832908,
                         0.2725881 , 0.65835877, 0.96381663, 0.94625531, 0.79233478,
                         0.21526468, 0.54674524, 0.81576486, 0.80799296, 0.64492723,
                         0.16549911, 0.42709552, 0.63131927, 0.62242067, 0.48489772])

for i in range(len(carrier)):
    for j in range (len(am)):
        signal = test_signal(carrier[i], am[j], m, 48000, 2, 60)       
        R,R_spec = comp_roughness(signal, 48000, 0)   
        data[i,j] = R[3]
        diff[i,j] = (data[i,j] - subjectivedata[i,j])/subjectivedata[i,j] * 100
 
        dataa.append(R[3])

difff = np.zeros((30))
for i in range(30):
    difff[i] = (dataa[i] - subjectivedataa[i])/subjectivedataa[i] * 100
 
    
plt.figure() 
plt.plot(difff)

plt.figure()
plt.plot(dataa)
plt.plot(subjectivedataa)
    



fig, axs = plt.subplots(3, 2)

axs[0, 0].plot(am, data[0,:],color='blue')
axs[0, 0].plot(am, subjectivedata[0,:],'b--')
axs[0, 0].set(xlim=(20, 100), ylim=(0, 1))
axs[0, 0].set_title('125 Hz', fontsize=10)


axs[0, 1].plot(am, data[1,:],color='blue')
axs[0, 1].plot(am, subjectivedata[1,:],'b--')
axs[0, 1].set(xlim=(20, 100), ylim=(0, 1))
axs[0, 1].set_title('250 Hz', fontsize=10)

axs[1, 0].plot(am, data[2,:],color='blue')
axs[1, 0].plot(am, subjectivedata[2,:],'b--')
axs[1, 0].set(xlim=(20, 100), ylim=(0, 1))
axs[1, 0].set_title('500 Hz', fontsize=10)

axs[1, 1].plot(am, data[3,:],color='blue')
axs[1, 1].plot(am, subjectivedata[3,:],'b--')
axs[1, 1].set(xlim=(20, 100), ylim=(0, 1))
axs[1, 1].set_title('1000 Hz', fontsize=10)

axs[2, 0].plot(am, data[4,:],color='blue')
axs[2, 0].plot(am, subjectivedata[4,:],'b--')
axs[2, 0].set(xlim=(20, 100), ylim=(0, 1))
axs[2, 0].set_title('2000 Hz', fontsize=10)

axs[2, 1].plot(am, data[5,:],color='blue')
axs[2, 1].plot(am, subjectivedata[5,:],'b--')
axs[2, 1].set(xlim=(20, 100), ylim=(0, 1))
axs[2, 1].set_title('4000 Hz', fontsize=10)





