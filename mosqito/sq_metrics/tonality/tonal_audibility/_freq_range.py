import numpy as np
#Function to define the frequency range under study
#Param: 
#	Inputs: freq_axis - frequency axis of the spectrum
#			delta_f - spectral resolution or line spacing
#			spectra - dictionary with the audio clips's spectra
#			spectra_dBA - dictionary with the audio clips's A weightened spectra
#	Output: freq_axis - new frequency axis limited with the range defined
#			spectra - dictionary with the audio clips's delimited spectra
#			spectra_dBA - dictionary with the audio clips's A weightened delimited spectra
def _freq_range(freq_axis, delta_f,spectra, spectra_dBA):
	#Constants to narrow down the study.
	max_f=3000
	min_f=50
	for x in range(len(freq_axis)):
		if freq_axis[x]<=max_f and freq_axis[x]>=(max_f-delta_f):
			upper_range_index=x
	for x in range(len(freq_axis)):
		if freq_axis[x]>=min_f and freq_axis[x]<=(min_f+delta_f):
			lower_range_index=x

	print("Range of frequencies to be studied [Hz]:",round(freq_axis[lower_range_index],2),"-", round(freq_axis[upper_range_index],2))

	#Delete frequencies above 3kHz and under 50Hz
	for z in range(len(freq_axis)-1,upper_range_index,-1):
		freq_axis=np.delete(freq_axis, np.s_[z])
	for z1 in range(lower_range_index-1,-1,-1): #?-1 instead of 0 in the middle to earse also f=0. Not erased otherwise
		freq_axis=np.delete(freq_axis, np.s_[z1])

	#Delete Li values respectively (f>3kHz and f<50Hz)
	for keys in spectra:
		for j in range(len(spectra.get(keys))-1, upper_range_index,-1):
			spectra[keys]=np.delete(spectra.get(keys), np.s_[j])
		for j in range(lower_range_index-1,-1,-1): 
			spectra[keys]=np.delete(spectra.get(keys), np.s_[j])

	for keys2 in spectra_dBA:
		for r in range(len(spectra_dBA.get(keys2))-1, upper_range_index,-1):
			spectra_dBA[keys2]=np.delete(spectra_dBA.get(keys2), np.s_[r])
		for r in range(lower_range_index-1,-1,-1):
			spectra_dBA[keys2]=np.delete(spectra_dBA.get(keys2), np.s_[r])
	return freq_axis, spectra, spectra_dBA 