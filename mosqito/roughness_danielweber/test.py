# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 13:42:08 2020

@author: pc
"""



import numpy as np
import matplotlib.pyplot as plt
from mosqito.tests.roughness.test_signals_generation import test_signal


signal = test_signal(1000, 70, 1, 48000, 2, 60)       
fs = 48000
overlap = 0
i_time = 6


# Spectrum
plt.figure(figsize=(12,4))
plt.plot(audible_freq_axis,LdB,'b')
plt.xlabel('Fréquence (Hz)')
plt.title('Audio signal spectrum')
plt.ylabel('Amplitude')
plt.axis([0,fs/2,0,LdB.max()])
plt.grid()

# Specific excitation spectrum
for i in range(47):
    plt.vlines(freq_axis,[0],spec_excitation_spectrum[i,0:4800])
    plt.title('Specific excitation spectrum')
    plt.ylim([0,100])

# Specific excitation function
plt.figure()
time = np.arange(0,0.2,1/fs)
for i in range(47):        
    plt.plot(time,ei[i]) 
    plt.title('Specific excitation function')

# Envelope spectrum
plt.figure()
for i in range(15):             
    plt.vlines(np.arange(0,48000,5),[0],Fei[i,0:9600])
    plt.title('Envelope spectrum')  

# Weighted envelope spectrum
plt.figure()
for i in range(47):             
    plt.vlines(np.linspace(0,48000,9600),[0],weighted_envelope[i,:])
    plt.title('Envelope spectrum')  
              

# Envelope function 
plt.figure()
time = np.arange(0,0.2,1/fs)
for i in range(47):        
    plt.plot(time,hBPi[i])
    plt.title('Envelope function')
    
    
for i in range(25):
# Excitation + envelope   
    plt.figure()
    time = np.arange(0,0.2,1/fs)  
    plt.plot(time,ei[i])     
    plt.plot(time,hBPi[i])
    
        
# RMS(i)
plt.figure()
x = np.arange(0,47,1)
plt.step(x,RMSh)
plt.title('Envelope rms')


# time average h0(i)
plt.figure()
x = np.arange(0,47,1)
plt.step(x,h0)
plt.title('Time average(envelope)')

# m(i)        
plt.figure()
x = np.arange(0,47,1)
plt.step(x,mdept)
plt.title('Modulation depth')        
        


# Hi
plt.figure()
for i in range(47):
    plt.plot(H[i,:], color='blue')
    plt.xlabel('Modulation frequency')
    plt.ylabel('Hi(fmod)')
    plt.title('H weighting functions')


#A0    
plt.figure(figsize=(12,4))
plt.plot(bark_axis,A0,color='blue')
plt.xlabel('Frequency')
plt.ylabel('a0 coefficient')
plt.title('Zwicker coefficient representing the transmission between free field and hearing system')
plt.xticks([0,4,8,12,16,20,24])

#Gi
plt.step(center_freq,G,color='blue')
plt.xlabel('Bark frequency zi')
plt.ylabel('G(zi)')
plt.title('Aures weighting function')
plt.xticks([0,4,8,12,16,20,24])
plt.ylim([0,1.2])
    
    
    
    
    