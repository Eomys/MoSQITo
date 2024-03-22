import _tones
import _formula
import _criteria
import _critical_band
import numpy as np
import _uncertainty

#Annex E(informative) - Example for the determination of the tonal audibility
#Consider that these lists are: Frequencies fi and A-weighted narrow-band levels Li in the critical band with the
#centre frequency 137,3 Hz of the first spectrum (not a full spectrum)

#SPECTRA_freqs=[96.9, 99.6, 102.3, 105.0, 107.7, 110.4, 113.0, 115.7, 118.4, 121.1, 
#123.8, 126.5, 129.2, 131.9, 134.6, 137.3, 140.0, 142.7, 145.3, 148.0, 150.7, 153.4, 156.1, 158.8, 
#161.5, 164.2, 166.9, 169.6, 172.3, 175.0, 177.6, 180.3, 183.0, 185.7, 188.4, 191.1, 193.8, 196.5]

#SPECTRA_i_Li=[49.40, 50.68, 50.09, 53.37, 44.47, 50.91, 51.41, 59.40, 64.54, 57.57,
#51.02, 50.76, 59.93, 62.94, 58.49, 65.87, 62.66, 50.25, 51.32, 52.30, 52.58, 53.15, 67.04, 67.27, 
#57.40, 57.17, 52.56, 51.39, 52.49, 47.68, 51.26, 49.03, 61.42, 59.52, 48.43, 50.84, 48.20, 55.95]

def _spectra_i_tonal_audibility(SPECTRA_freqs,SPECTRA_i_Li, delta_f):
	delta_fe=1.5 	#effective bandwith (Hanning window)
	k=1.645
	list_deltaLm=[] #list of final audibilities, the greatest will be the dec. aud.
	dict_lines_assigned={} #this dictionary is used to see what lines are assigned to each tone for Lt calculation, 
	#so they are not added twice in Ltm. keys-ft, values-list of Lis assigned to get ft's Lt
	dict_Lt={} #dictionary keys-ft, values-Lt
	dict_LS={}	#dictionary keys-ft, values-LS
	dict_aud={} #dictionary keys-ft, values-delta_L (audibilities)
	dict_Li_LS={} #dictionary with the final list of Lis used to determine ft's LS after LS iteration
	list_ft=[] #list of audible tones
	list_not_distinct=[] #list of audible tones that do not meet the distinctness conditions
	dict_U={}# dictionary of uncertainties for the cases where there is only 1 tone in a CB
	list_decisive_sigma=[]

	#First we find the index in which there is maxima on the spectrum, i.e. a Li value which is higher that 
	#the previous and the next one
	list_index_max=[]
	for i in range(0,len(SPECTRA_i_Li)-1):
		if SPECTRA_i_Li[i-1] < SPECTRA_i_Li[i]> SPECTRA_i_Li[i+1]:
			list_index_max.append(i)

	#Study of each maximum. Calculation of the parameters for each maximum and study of the 
	#fulfilment of conditions to consider said maximum as an audible tone.
	for j in range(0, len(list_index_max)):
		ft=SPECTRA_freqs[list_index_max[j]]
		print("\n************************************************************************************************************")
		print("ft=",round(ft,2), "Hz")
		aud_i, dict_lines_assigned, list_not_distinct, dict_LS, dict_Lt, dict_Li_LS, dict_U=_tones._spectra_i_tones(SPECTRA_i_Li, SPECTRA_freqs,delta_f, delta_fe, ft, list_index_max[j], dict_lines_assigned, list_not_distinct, dict_LS, dict_Lt, dict_Li_LS, dict_U)
		if aud_i>0: #tones which audibility is to be studied
			dict_aud[ft]=round(aud_i,2)
			list_ft.append(ft)

	#check the dictionary for the tones that are distinct but not audible, and erase them from it
	#Erase from the list of audible tones those that are not supposed to be studied even though they are audible 
	#I.e. those which do not meet distinctness criteria
	dict_lines_assigned, list_ft, dict_aud=_criteria._discard_not_distinct(dict_lines_assigned, list_ft, dict_aud,list_not_distinct)

	#print("LIST AUDIBLE TONES (and distinct):", list_ft)
	print("*********DECISIVE AUDIBILITY**********")
	#Now we check that the spectral lines are not used for Ltm more than once, and if so the least pronounced tone is dismissed
	dict_lines_assigned, list_ft, dict_aud=_criteria._single_addition_lines(dict_lines_assigned, dict_aud, list_ft, SPECTRA_freqs, SPECTRA_i_Li)
	print("AUDIBLE tones after single addition condition", list_ft)
	#print("DICT Lineas assigned", dict_lines_assigned)
	#If there are more than one tone in a CB, check the ft2-t1>fd criteria to see if the tones must be evaluated separetely
	list_ft, dict_aud=_criteria._aud_tones_within_critical_band(list_ft, dict_aud, SPECTRA_freqs)
	print("FINAL LIST OF TONES TO BE STUDIED FOR DEC. AUD:", list_ft)

	#Calculate delta_L again for (each) the tone ftm
	for n in range(0,len(list_ft)):
		list_Li_ft=[] #list used to get the Lis used to obtain Lt in each case, for the uncertainty calculation and Ltm
		list_Li=[] #list to concatenate list_Li_ft to get the Lis of each Lt summed for Ltmn (final tone level, tones in a CB)
		list_LT=[] #empty this list for each tone
		ftm=list_ft[n]
		ftm_index=SPECTRA_freqs.index(ftm)
		Li_ftm=SPECTRA_i_Li[ftm_index]
		LSm=dict_LS.get(ftm)
		print("\n-------------------------------------------------------------------------------------------------------------------")
		print("Study of the DECISIVE AUD. for tone ", round(ftm,2), "Hz with Li=", round(Li_ftm,2) , "dB and its calculated LS=", round(LSm,2))
		print("LSITA DE NO DISTNIGUIBLES DE ESTE ESPCTRO: ", list_not_distinct)
		#critical band 
		delta_fm,f1,f2=_critical_band._critical_band(ftm, SPECTRA_freqs)
		#Obtain the applicable Lts, to calculate Ltm of the tone under study, from the dictionary of Lts
		for f in dict_lines_assigned:
			if f>=f1 and f<=f2:
				Lt=dict_Lt.get(f)
				list_LT.append(round(Lt,2))
				list_Li_ft=dict_lines_assigned.get(f)
				list_Li=list_Li+list_Li_ft
		
		LTm=_formula._sum_tone_level(list_LT, list_Li)
		LGm=_formula._critical_band_level(LSm,delta_f,delta_fm)
		avm=_formula._masking_index(ftm)
		delta_Lm=_formula._audibility(LTm, LGm, avm)
		list_deltaLm.append(delta_Lm)
		#Uncertainty
		#print("LIST LT UNC:", list_LT)
		if len(list_LT)==1:
			U_ftm=dict_U.get(ftm)
			list_decisive_sigma.append(U_ftm/k)
		else:
			U_ftm, sigma=_uncertainty._aud_uncertainty(dict_Li_LS.get(ftm), list_Li, delta_fm, delta_f)
			list_decisive_sigma.append(sigma)
		print("Tone:", round(ftm,2), "Hz -> For a summation level of", round(LTm,2),"dB, a masking index of av=",round(avm,2), "dB and a critical band level LGm=",round(LGm,2), "dB, the DECISIVE audibility is", round(delta_Lm,2))	
		print("Final audibility: ", round(delta_Lm,2), "dB  U=", round(U_ftm,2), "dB")

	#Get the decisive audibility of the spectra, which is the highest delta_L obtained for the audible tones
	greatest_deltaLm=0
	dec_sigma=0
	for c in range(0,len(list_deltaLm)):
		if list_deltaLm[c]>greatest_deltaLm:
			greatest_deltaLm=list_deltaLm[c]
			tone_decisive_aud=list_ft[c]
			dec_sigma=list_decisive_sigma[c]

	print("\nDECISIVE AUDIBILITY OF THE SPECTRA")
	print("The greatest decisive audibility is", round(greatest_deltaLm,2), "dB for the tone ftm=", round(tone_decisive_aud,2), "Hz")
	return greatest_deltaLm, dec_sigma