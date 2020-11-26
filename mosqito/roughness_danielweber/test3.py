# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:43:45 2020

@author: pc
"""

import sys
sys.path.append('../../..')

#Standard imports
import numpy as np
import matplotlib.pyplot as plt
import pytest

# Local application imports
from mosqito.roughness_danielweber.comp_roughness import comp_roughness
from mosqito.tests.roughness.test_signals_generation import test_signal
from mosqito.tests.roughness.ref import ref_roughness





# Parameters definition for signals generation 
fs = 48000
carrier  = np.array([125, 250, 500, 1000, 2000, 4000, 8000])
fmod     = np.array([10, 20, 30, 40, 50, 60, 70, 80, 100, 150, 200, 400])
mdepth = 1   
duration = 2
dB = 60
    
# Overlapping definition for roughness calculation
overlap = 0

R_ref = np.zeros((len(carrier),len(fmod)))
R = np.zeros((len(carrier),len(fmod)))
           
# Each carrier frequency is considered separately
for ind_fc in range(carrier.size):
    # Roughness reference values
    R_ref[ind_fc,:] = ref_roughness(carrier[ind_fc], fmod)
    # Roughness calculation for each modulation frequency
    for ind_fmod in range(fmod.size):     
        signal = test_signal(carrier[ind_fc], fmod[ind_fmod], mdepth, fs, duration, dB)
        Rc,_ = comp_roughness(signal, fs, overlap)
        R[ind_fc,ind_fmod] = Rc[2]
        


fig, axs = plt.subplots(4, 2)

axs[0, 0].plot(fmod, R[0,:],color='blue')
axs[0, 0].plot(fmod, R_ref[0,:],'b--')
axs[0, 0].set(xlim=(10, 400), ylim=(0, 1))
axs[0, 0].set_title('125 Hz', fontsize=10)


axs[0, 1].plot(fmod, R[1,:],color='blue')
axs[0, 1].plot(fmod, R_ref[1,:],'b--')
axs[0, 1].set(xlim=(10, 400), ylim=(0, 1))
axs[0, 1].set_title('250 Hz', fontsize=10)

axs[1, 0].plot(fmod, R[2,:],color='blue')
axs[1, 0].plot(fmod, R_ref[2,:],'b--')
axs[1, 0].set(xlim=(10, 400), ylim=(0, 1))
axs[1, 0].set_title('500 Hz', fontsize=10)

axs[1, 1].plot(fmod, R[3,:],color='blue')
axs[1, 1].plot(fmod, R_ref[3,:],'b--')
axs[1, 1].set(xlim=(10, 400), ylim=(0, 1))
axs[1, 1].set_title('1000 Hz', fontsize=10)

axs[2, 0].plot(fmod, R[4,:],color='blue')
axs[2, 0].plot(fmod, R_ref[4,:],'b--')
axs[2, 0].set(xlim=(10, 400), ylim=(0, 1))
axs[2, 0].set_title('2000 Hz', fontsize=10)

axs[2, 1].plot(fmod, R[5,:],color='blue')
axs[2, 1].plot(fmod, R_ref[5,:],'b--')
axs[2, 1].set(xlim=(10, 400), ylim=(0, 1))
axs[2, 1].set_title('4000 Hz', fontsize=10)

axs[3, 0].plot(fmod, R[6,:],color='blue')
axs[3, 0].plot(fmod, R_ref[6,:],'b--')
axs[3, 0].set(xlim=(10, 400), ylim=(0, 1))
axs[3, 0].set_title('4000 Hz', fontsize=10)


plt.figure()
plt.plot(fmod[0:11],R_ref[1,0:11] ,linestyle='dotted',color='black')
plt.plot(fmod[0:11],R[1,0:11],marker='s',color='black')
plt.plot(x250,y250,marker='o',color='black')

plt.plot(fmod[0:11],R_ref[5,0:11],linestyle='dotted',color='blue')
plt.plot(fmod[0:11],R[5,0:11],marker='s',color='blue')
plt.plot(x1000,y1000,marker='o',color='blue')

plt.plot(fmod[0:11],R_ref[3,0:11],linestyle='dotted',color='green')
plt.plot(fmod[0:11],R[3,0:11],marker='s',color='green')
plt.plot(x4000,y4000,marker='o',color='green')


