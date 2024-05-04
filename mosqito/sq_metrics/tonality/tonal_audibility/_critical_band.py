
import numpy as np

#Function that determines the width and limiting frequencies of the critical band with centre at ft
#(considering the line spacing for the values of f1 and f2)
#ISO 20065 5.2 Width Δfc of the critical band (Formulas 2,4,5)
#Param:
#	Inputs: ft - frequency of the tone under study, center of the CB
#			total_list_f - complete list of frequencies of the spectra to determine which freqs lie within the CB
#	Output: delta_fc - Bandwidth of the critical band
#			f1 and f2 - limit frequencies of teh CB
def _critical_band(ft, total_list_f):
	delta_fc = 25 + 75 * np.power(1 + 1.4 * np.power(ft/ 1000, 2), 0.69)
	f1=(-delta_fc/2)+(np.power((np.power(delta_fc,2)+4*np.power(ft,2)),1/2))/2
	f2=f1+delta_fc
	if f1<total_list_f[0]:
		f1_=total_list_f[0]
	else:
		for i in range(0,len(total_list_f)):
			if f1>=total_list_f[i]:
				f1_=total_list_f[i]
				
	max=len(total_list_f)-1	
	if f2>total_list_f[max]:
		f2_=total_list_f[max]
	else:
		for m in range(0, len(total_list_f)):
			if f2>=total_list_f[m]:
				f2_=total_list_f[m]
	return delta_fc,f1_,f2_




		
