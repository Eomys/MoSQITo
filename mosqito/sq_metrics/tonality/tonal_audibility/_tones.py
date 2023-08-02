#pruebas
import _mean_nblevel_lines
import _formula
import _critical_band
import _criteria
import _uncertainty

def _spectra_i_tones(SPECTRA_Li, SPECTRA_freqs,delta_f,delta_fe, ft, ft_index, dict_lines_assigned, not_distinct, dict_LS,dict_Lt, dict_Li_LS, dict_U):
	Li_ft=SPECTRA_Li[ft_index]
	print("Narrow band level, Li=", round(Li_ft,2), "dB")
		
	#To study the distinctness Lu and Lo are required, as well as their freq fu and fo
	fu=SPECTRA_freqs[ft_index-1] #f under ft
	fo=SPECTRA_freqs[ft_index+1] #f over ft
	Lu=SPECTRA_Li[ft_index-1] 
	Lo=SPECTRA_Li[ft_index+1] 
	#print("Under ft. Lu=",Lu," en fu=", fu)	
	#print("Over ft. Lo=",Lo," en fo=", fo)
	#print("\n")	

	#Function called to determine the critic band bandwith as well as the corner frequencies
	#delta_fc,f1,f2=_critical_band_20065._critical_band_20065(ft)
	delta_fc,f1,f2=_critical_band._critical_band(ft, SPECTRA_freqs)
	print("Bandwidth of the Critical Band=", round(delta_fc,2), "Hz")
	print("f1=",round(f1,2), "Hz")
	print("f2=",round(f2,2), "Hz")

	#Function called to get a list of the levels of the spectral lines contained in the critical band, 
	#as well as their index and the value M, which is the count of the spectral lines on the list except 
	#for ft's spectral line, i.e. except the line under study
	list_Li, list_index, M=_mean_nblevel_lines._list_levels_ini(ft,f1,f2,SPECTRA_freqs,SPECTRA_Li)
	#list of spectral lines of a CB without counting ft
	#print("List of Li of the spectral lines within the CB of",ft, "=", list_Li) 
	#print("List of their respective indexes: ", list_index)
	#print("number of lines to be averaged(M)=", M)

	#Function called to carry out the first iteration to determine LS
	LS=_formula._mean_narrow_band_level(M, list_Li, delta_f, delta_fe)
	#print("Mean-Narrow Initial level for the critical band centred on",ft, ", LS=", round(LS,2), "dB")
	list_iteration=[round(LS,2)]
	list_Li_inicial=list_Li
	list_LS_final=[]
	criteria=_criteria._iteration_criteria_LS(list_index,ft_index)
	criteria2=False #set to false until there are no values to compare

	while criteria==True and criteria2==False:
	#while in an iteration step, the new energy mean value isn´t equal within a tolerance of ±0,005 dB to that
	#of the previous iteration step and while the number of lines contributing to the mean narrow-band level to 
	#the right or left of the line under investigation stays over or equal to 5, the iteration continues
		list_aux=list_Li
		list_Li, list_index, M=_mean_nblevel_lines._list_levels_LS(list_aux, list_index, delta_f, LS)
		#print("List of Li of the spectral lines within the CB after it=", list_Li) 
		#print("List of their respective indexes: ", list_index)
		
		LS=_formula._mean_narrow_band_level(M, list_Li, delta_f, delta_fe)
		list_iteration.append(LS)
		#print("List of LS", list_iteration)
		#print("\n")

		if len(list_iteration)>2:
			criteria2=_criteria._iteration_criteria_LS_2(list_iteration)
			criteria=_criteria._iteration_criteria_LS(list_index, ft_index)
			if criteria2==True or criteria==False:
				list_LS_final=list_aux #lista anterior, al igual que LS anterior
				LS=list_iteration[len(list_iteration)-2]
		else:
			criteria=_criteria._iteration_criteria_LS(list_index,ft_index)
	dict_LS[ft]=LS
	print("After the iteration, LS=",round(LS,2), "dB")
	dict_Li_LS[ft]=list_LS_final
	#print(list_LS_final)

	tone_criteria=_criteria._tone_criteria(LS, Li_ft)
	if tone_criteria==False:
		print("\nAs for ft=",round(ft,2), "Hz Li(ft)<LS+6, it can't be defined as a tone")
		delta_L=0
	else:
		#Function called to determine the tone level at the CB, which spectral lines contribute to the tone level
		#Careful not to introduce the list without the tone level, if so the results are not correct
		LT, Tone_BW, LT_max, dict_lines_assigned=_formula._tone_level(SPECTRA_Li, delta_f, LS, ft, Li_ft, ft_index, delta_fe, dict_lines_assigned)
		print("LT en",round(ft,2), "es =", round(LT,2), "dB")
		dict_Lt[ft]=LT
		#Function called to determine the tone's (ft) distinctness
		distinct_criteria=_criteria._distinctness_criteria(ft,Lu,Lo,fu,fo, LT_max, Tone_BW)
		#print("Tone Bandwidth:", round(Tone_BW,2))
		#print("LT_max:", LT_max)
		#print("(If the distinctness function returns False, the tone is NOT audible for an individual with normal hearing)")
		print("Are the distinctness conditions for the tone fulfilled?", distinct_criteria)

		if distinct_criteria==True:
			#At last, functions called to find out the critical band level. the masking index and the audibility 
			LG=_formula._critical_band_level(LS,delta_f,delta_fc)
			av=_formula._masking_index(ft)
			delta_L=_formula._audibility(LT, LG, av)
			#uncertainty 
			U_ft, sigma=_uncertainty._aud_uncertainty(list_LS_final, dict_lines_assigned[ft], delta_fc, delta_f)
			#print(dict_lines_assigned)
			dict_U[ft]=U_ft
			print("LT=", round(LT,2), "dB")
			print("For a masking index of av=",round(av,2), "dB and a critical band level LG=",round(LG,2), "dB ,the audibility is", round(delta_L,2), "dB")
			print("Audibility ", round(delta_L,2),"dB  U=", round(U_ft,2), "dB")
		else:
			#Issue: should not be the case, according to the standard, if distinctness is not met, neither LG nor av is calculated 
			#(therefore aud is not calculated either).
			LG=_formula._critical_band_level(LS,delta_f,delta_fc)
			av=_formula._masking_index(ft)
			delta_L=_formula._audibility(LT, LG, av)
			if delta_L>0:
				not_distinct.append(ft)
			U_ft,sigma=_uncertainty._aud_uncertainty(list_LS_final, dict_lines_assigned[ft], delta_fc, delta_f)
			dict_U[ft]=U_ft
			print("As the distinctness criteria are not met, the audibility of the tone ft=", round(ft,2),"Hz won't be studied.")
			print("But it can be considered for tone addition.")
			print("Not distinct. ¿Audibility? ", round(delta_L,2),"dB, with LG=", round(LG,2), "dB, av=", round(av,2), "dB and U=", round(U_ft,2))
	return delta_L, dict_lines_assigned, not_distinct, dict_LS, dict_Lt, dict_Li_LS, dict_U

