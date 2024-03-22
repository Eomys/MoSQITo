import numpy as np
import math

#Function to delimit the line spacing. It returns the N (number of points for the fft) neccesary to get that delta_f.
#The value of delta_f will be recalculated again afterwards when the number of points for the fft is rounded 
#to a power of 2
def _delta_f(fs):
	#>1.9Hz <4Hz
	delta_f=3 #duration(of each clip)=1/delta_f
	N=fs/delta_f;
	return N,delta_f


#Function that returns the smallest power of two that is greater than or equal to the absolute value of N.
#It also recalculates delta_f according to that new N (number of points for the fft)
#Param: N - numbre 
def _nextpow2(N,fs):
	n=np.log2(N)
	if(n%2!=0):
		n=math.ceil(n)
	else: n=n
	print(n)
	new_N=np.power(2,n)
	#recalculate delta_f
	delta_f=fs/new_N
	print(delta_f)
	return new_N,delta_f


#Function that calculates the masking index
#ISO 20065 5.3.6. Masking index (Formula 13)
#Param: 
#	Inputs: ft - tone frequency: frequency of the spectral line (or mid-band frequency of the narrow-band filter), to the level of
#								 which the tone contributes most strongly
#	Output: av - masking index: audibility threshold for a specific sound in the presence of a masking sound
def _masking_index(ft):
	av=-2-np.log10(1+(np.power(ft/502, 2.5)))
	return av


#Function that calculates the critical band level
#ISO 20065 5.3.5 Critical band level, LG, of the masking noise (Formula 12)
#Param: 
#	Inputs: LS - mean narrow band level: energy mean value of all narrow-band levels in a critical band that does not exceed
#										 this mean value by more than 6 dB
#			delta_f - line spacing: distance between neighbouring spectral lines
#			delta_fc - bandwith of the critical band
#	Output: LG - critical band level: level of noise that is assigned to the critical band that describes the masking 
#									  characteristic of the noise for one or more tones of the noise in this critical band
def _critical_band_level(LS, delta_f, delta_fc):
	LG=LS+(10*np.log10(delta_fc/delta_f))
	return LG


#Function that calculates the audibility
#ISO 20065 5.3.7 Determination of the audibility, ΔL (Formula 14)
#Param: 
#	Inputs: LT - tone level: energy summation of the narrow-band level with the tone frequency, fT, and the lateral lines
#							 about fT, assignable to this tone
#			LG - critical band level: level of noise that is assigned to the critical band that describes the masking 
#			av - masking index: audibility threshold for a specific sound in the presence of a masking sound
#	Output: delta_L - audibility: difference between the tone level and the masking threshold				
def _audibility(LT, LG, av):
	delta_L=(LT-LG-av)
	return delta_L



#Function that calculates LS 
#ISO 20065 5.3.2 Determination of the mean narrow-band level LS of the masking noise (Formula 6)
#Param: 
#	Inputs: M - number of spectral lines except the one under study:
#			listTones_Li - list of the levels Li of the tones within the CB except for ft
#			delta_f - line spacing: distance between neighbouring spectral lines
#			delta_fe - effective bandwidth: is the effective bandwidth in Hz; if a Hanning window is used then the effective bandwidth, Δfe,
#											is 1,5 times the frequency resolution (line spacing), Δf.
#	Output: LS - mean narrow band level after the first iteration. Initial LS
def _mean_narrow_band_level(M, listTones_ini, delta_f, delta_fe):
	Sum=0
	for i in range(0,len(listTones_ini)):
		Sum=Sum+(np.power(10,0.1*listTones_ini[i]))
	LS=(10*np.log10((1/M)*Sum))+(10*np.log10(1/delta_fe))
	return LS


#Function that calculates the tone level
#ISO 20065 5.3.3 Determination of the tone level LT of a tone in a critical band (Formula 8)
#Param: 
#	Inputs: listTones - list of the levels Li of the tones within the CB that are under LS+6dB
#			delta_f - line spacing: distance between neighbouring spectral lines
#			LS - mean narrow band level: energy mean value of all narrow-band levels in a critical band that does not exceed
#										 this mean value by more than 6 dB
#			ft_index - index of the tone under study
#			delta_fe - effective bandwidth: is the effective bandwidth in Hz; if a Hanning window is used then the effective bandwidth, Δfe,
#											is 1,5 times the frequency resolution (line spacing), Δf.
#	Output: LT - tone level: energy summation of the narrow-band level with the tone frequency, fT, and the lateral lines
#							 about fT, assignable to this tone
#			Tone_BW - tone bandwidth: sum of the bandwidths of the spectral lines contributing to the tone
#			LT_max - maximum narrow-band level (Li) of the tone			
def _tone_level(listTones, delta_f, LS, ft, Li, ft_index, delta_fe, dict_lines_assigned):
	list_lines_assigned=[]
	list_lines_assigned.append(Li)
	Sum=np.power(10,0.1*Li) #Add ft's Li to the summatory 
	LT_max=Li #for distinctness criteria
	Tone_BW=delta_f #Tone bandwith necessasry for distinctness criteria
	index_aux=ft_index
	#below the tone
	for j in range(ft_index-1,0,-1):
		if (listTones[j]>Li-10) and (listTones[j]>LS+6):
			if (j==index_aux-1): 
				index_aux=j
				Sum=Sum+(np.power(10,0.1*listTones[j]))
				list_lines_assigned.append(listTones[j])
				Tone_BW=Tone_BW+delta_f
	index_aux=ft_index
	#over the tone
	for x in range(ft_index+1,len(listTones)):
		if (listTones[x]>Li-10) and (listTones[x]>LS+6): 
			if (x==index_aux+1):
				index_aux=x
				list_lines_assigned.append(listTones[x])
				Sum=Sum+(np.power(10,0.1*listTones[x]))
				Tone_BW=Tone_BW+delta_f
	dict_lines_assigned[ft]=list_lines_assigned
	if Tone_BW>delta_f: 
		LT=(10*np.log10(Sum))+(10*np.log10(1/delta_fe))
	else: #if only ft's Li is in the summation
		LT=10*np.log10(Sum)
	return LT, Tone_BW, LT_max, dict_lines_assigned


#Function that adds the tone level (LT) of all the audible tones within ftm's critical band
#ISO 20065 5.3.8. Determination of the decisive audibility, ΔLj, of a narrow-band spectrum -Step 3 (Formula 17)
def _sum_tone_level(list_LT, list_Li):
	Sum=0
	for z in range(0,len(list_Li)):
		Sum=Sum+(np.power(10,0.1*list_Li[z]))
	if len(list_Li)>2*len(list_LT):
		LTm=10*np.log10(Sum)-1.76
	else:
		LTm=10*np.log10(Sum)
	return LTm


#Function for the determination of the mean audibility of a number of spectra
#ISO 20065 5.3.9 Determination of the mean audibility ΔL of a number of spectra (Formula 20)
#The decisive audibility ΔLj is calculated for each narrow-band averaged spectrum (run
#index j, J is the number). These J audibilities are averaged in energy terms to yield the mean audibility
#Param:
#	Inputs: list_decisve_aud - decisive audibility of each spectrum, to be averaged
#	Output: mean_aud - mean audibility
def _mean_aud(list_decisive_aud):
	Sum=0
	J=len(list_decisive_aud)
	for i in range(0,len(list_decisive_aud)):
		Sum=Sum+np.power(10,0.1*list_decisive_aud[i])
	mean_aud=10*np.log10((1/J)*Sum)
	return mean_aud

