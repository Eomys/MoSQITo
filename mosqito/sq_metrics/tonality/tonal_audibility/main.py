import _spectra
import _formula
import _uncertainty
import _freq_range
import numpy as np
import math
import matplotlib.pyplot as plt
from numpy.fft import fft
from mosqito.utils.load import load
from mosqito.utils import time_segmentation
from mosqito.utils import conversion
from mosqito.sound_level_meter.spectrum import spectrum
import pandas as pd

archivo='white_noise_442_1768_Hz_stationary.wav'
signal, fs=load(archivo, wav_calib=0.01)  #fs=48kHz
print(fs)
t_st=np.linspace(0,(len(signal)-1)/fs,len(signal))
plt.figure(1)
plt.plot(t_st,signal)
plt.xlabel('Time')
plt.ylabel('Pressure [Pa]')
plt.title('Stationary signal- White noise')
plt.show()

#Show spectrum of the input signal
signal_spectrum,freqs=spectrum(signal,fs)
plt.figure(2)
plt.plot(freqs, signal_spectrum)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude [dB re. 2e-5Pa]")
plt.xlim(50,3000)
plt.ylim(-100,50)
plt.title('Sepctrum - Stationary signal- White noise')
plt.show()

No, delta_f=_formula._delta_f(fs)
N,delta_f=_formula._nextpow2(No,fs)
array1=np.array([]) #signal 2-d segmented signal
array2=np.array([]) #time axis
array1,array2=time_segmentation.time_segmentation(signal, fs,N, 0)

#number of audio clips is the size of the array1 divided by the number of samples(N)
#Duration of the clips is N divided by fs (array2 shows when each of the clips stop)
#Each of the colums of the array1 is a clip, and each of the lines is the value of a sample for each of the clips
num_blocks=array1.size//N
print("Number of clips:",num_blocks)
clips={}
spectra={}
spectra_dBA={}
#change dims
array1=np.transpose(array1)
print("\nSHAPE OF THE MATRIX (CLIPS)",array1.shape)

for i in range(num_blocks):
	name="clip{0}".format(i+1)
	clips[name]=array1[i]
	Lp,freq_axis=spectrum(array1[i],fs)
	name_sp="spectra{0}".format(i+1)
	spectra[name_sp]=np.round(Lp,2)
	Lp_dBA=conversion.spectrum2dBA(Lp, fs)
	name_sp_dBA="spectra{0}_dBA".format(i+1)
	spectra_dBA[name_sp_dBA]=Lp_dBA

#Narrow down the the frequency range to 50Hz - 3kHz
freq_axis, spectra, spectra_dBA=_freq_range._freq_range(freq_axis, delta_f,spectra, spectra_dBA)

#EXPORT SPECTRA TO EXCEL FOR VALIDATION
#writer = pd.ExcelWriter('sample_spectrum_dBA.xlsx')
#i=0
#for k in spectra_dBA:
#	data = pd.DataFrame({"f":freq_axis,"Li":spectra_dBA.get(k)})
#	sheet_name="sheet{0}".format(i+1)
#	data.to_excel(writer, sheet_name, index=False)
#	writer.save()
#	i=i+1
#writer.close()

dec_auds=[]
list_dec_sigmas=[]
list_f=freq_axis.tolist()

for key in spectra_dBA:
	list_spectra_i=spectra_dBA.get(key).tolist()
	print("\n>>>>>>>>>>>>>>>>>>>>>", key)
	decisive_aud, dec_sigma=_spectra._spectra_i_tonal_audibility(list_f, list_spectra_i, delta_f)
	dec_auds.append(decisive_aud)
	list_dec_sigmas.append(dec_sigma)

print("\nLIST OF DECISIVE AUDS: ", dec_auds)
print("\nLIST of its sigmas", list_dec_sigmas)
mean_audibility=_formula._mean_aud(dec_auds)
mean_unc=_uncertainty._mean_aud_uncertainty(dec_auds, list_dec_sigmas)
print("\nThe MEAN AUDIBILITY of the whole spectrum is:", round(mean_audibility,2), "dB and its uncertainty", round(mean_unc,2), "dB")