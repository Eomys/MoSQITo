import numpy as np

#Function to determine the uncertainty of each audible tone and of the decisive tones 
#ISO-20065. 6.Calculation of the uncertainty of the audibility ΔL (Formula 27)
#Param: 
#	Inputs: list_Li_LS - list of Lis to be averaged to determine LS for each tone
#			list_Li_Lt - list of Lis to be added to obtain LT for each tone, or list of LT calculated for each tone that are
#						to be summed for Ltm
#			delta_fc - bandwith of the critical band
#			delta_f - line spacing
#	Output: Uncertainty with a cover factor k=1.645 for a 90 % coverage probability in a bilateral confidence interval
def _aud_uncertainty(list_Li_LS, list_Li_LT, delta_fc, delta_f):
	#list of Li for ft's Lt calculation
	#list of Li that are averaged to form ft's LS
	#bandwidth of the CB
	num_LS=0
	den_LS=0
	num_LT=0
	den_LT=0
	sigma_L=3
	k=1.645
	#print(list_Li_LT)
	#print(list_Li_LS)
	if list_Li_LS: #not empty
		for i in range(0,len(list_Li_LS)):
			num_LS=num_LS+(np.power(np.power(10,0.1*list_Li_LS[i]),2))
			den_LS=den_LS+(np.power(10,0.1*list_Li_LS[i]))
		den_LS=np.power(den_LS,2)
		unc_p1=(num_LS/den_LS)
	else: 
		unc_p1=0
	if list_Li_LT:
		for j in range(0,len(list_Li_LT)):
			num_LT=num_LT+(np.power(np.power(10,0.1*list_Li_LT[j]),2))
			den_LT=den_LT+(np.power(10,0.1*list_Li_LT[j]))
		den_LT=np.power(den_LT,2)
		unc_p2=(num_LT/den_LT)
	else:
		unc_p2=0
	unc_p3=np.power(4.34*(delta_f/delta_fc),2)
	sigma=np.sqrt((unc_p1+unc_p2)*np.power(sigma_L,2)+unc_p3)
	uncertainty=k*sigma
	#print(unc_p1, unc_p2, unc_p3, sigma, uncertainty)
	return uncertainty, sigma


def _mean_aud_uncertainty(list_aud, list_sigmas):
	num=0
	den=0
	k=1.645
	for j in range(0, len(list_aud)):
		num=num+np.power((np.power(10,0.1*list_aud[j])*list_sigmas[j]),2)
		den=den+np.power(10,0.1*list_aud[j])
	mean_U=k*(np.sqrt(num)/den)
	return mean_U




