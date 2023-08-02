
#Function that from the limit frequencies of the CB, f1 and f2, obtains all spectral lines that are part of that BC 
#excluding the central one ft. Their levels are stored in a list so that LS can be calculated.
#It also returns the number of lines to be averaged (M = all the lines except ft)
#Param
#	Inputs:
#			ft - tone frequency
#			f1 , f2 - corner frequencys of the critical band
#			list_f - complete list of frequencies given in the ISO example spectrum 
#			list_Li - complete list of tone levels of the frequencies given in the ISO example spectrum
#	Outputs:
#			list_out_Li - list of the spectral lines' tone levels that are part of ft's critical band
#			list_index - list of indexes of list_out_Li values
#			n_lines - M: number of lines to be averaged 
def _list_levels_ini(ft,f1,f2, list_f, list_Li):
	list_index=[]
	list_out_Li=[]
	n_lines=0
	for i in range(0,len(list_f)):
		if list_f[i]>=f1 and list_f[i]<=f2 and list_f[i]!=ft:
			list_index.append(i)
			n_lines=n_lines+1
	for j in list_index:
			list_out_Li.append(list_Li[j])
	return list_out_Li, list_index, n_lines



#From the list of levels obtained for the first LS iteration (all the levels of the CB except the ft level), only those 
#that fulfill the LS_ini+6 criteria are taken
#Param
#	Inputs:
#			listTones - list of the spectral lines' tone levels that are part of ft's critical band
#			listIndex - list of indexes of list_out_Li values
#			delta_f - line spacing: distance between neighbouring spectral lines
#			LS_ini - mean narrow band level after the first iteration. Initial LS
#	Outputs:
#			list_LS - list of the spectral lines' tone levels that fulfill the LS_ini+6 criteria 
#			new_list_index - list of indexes of list_LS values
#			num_lines - M: NEW number of lines to be averaged
def _list_levels_LS(listTones, listIndex, delta_f, LS):
	list_LS=[]
	new_list_index=[]
	num_lines=0;
	for k in range(0,len(listTones)):
		if listTones[k]<=LS+6:
			num_lines=num_lines+1 
			list_LS.append(listTones[k])
			new_list_index.append(listIndex[k])
	return list_LS, new_list_index, num_lines

