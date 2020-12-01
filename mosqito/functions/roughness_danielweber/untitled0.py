# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 10:59:28 2020

@author: pc
"""
import numpy as np
import math
from mosqito.conversion import freq2bark, amp2db, bark2freq
from mosqito.roughness_danielweber.LTQ import LTQ

freqs = np.arange(0,4800,1)/0.2
barks = freq2bark(freqs)
minexcit = LTQ(barks)


z = np.arange(1,48,1)/2             # center freq
zb = bark2freq(z)*0.2              # position des center freq sur l'axe des frequences en Hz
minex = np.interp(zb,np.arange(0,4800,1),minexcit)

bins = 2
last = math.floor((358/fs)*N)      # position de la dernière freq pondérée sur l'axe des freqs en Hz
j = np.arange(bins+1,last+1)        # index des freqs pondérées
f = (j-1)*fs/N























