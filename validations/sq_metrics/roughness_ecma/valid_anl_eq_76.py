import numpy as np
import matplotlib.pyplot as plt

from mosqito import COLORS as clr
    
def valid_eq_76(Phi_E):    
    
    K = [10,20,30,40,50,60,70,80,90,100]
    F_ecma = np.empty(len(K))
    F_anl = np.empty(len(K))
    
    # frequency resolution [Hz]
    delta_f = 1500/512        

    for i, kpi in enumerate(K):
        # Refinement step
        Km = np.array([[(kpi-1)**2, kpi-1, 1],[kpi**2, kpi, 1],[(kpi+1)**2, kpi+1, 1]])
        if kpi == 0:
            Phi = np.array([0, Phi_E[kpi], Phi_E[kpi+1]])
        elif kpi == 255:
            Phi = np.array([Phi_E[kpi-1], Phi_E[kpi], 0])
        else:
            Phi = np.array([Phi_E[kpi-1], Phi_E[kpi], Phi_E[kpi+1]])

        # Solver formulation (ECMA 418-2)
        C = np.linalg.solve(Km, Phi)  
        F_ecma[i] = -C[1]/(2*C[0]) * delta_f

        # Analytical formulation
        F_anl[i] = (kpi - (Phi_E[kpi+1]-Phi_E[kpi-1])/(2*Phi_E[kpi-1]+2*Phi_E[kpi+1]-4*Phi_E[kpi])) * delta_f
        
    fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
    ax.plot(K, F_ecma, 's:', label='ECMA 418-2', color=clr[0], mfc='none', markersize=8)
    ax.plot(K, F_anl, 'o:', label='Analytical', color=clr[2], markersize=4)
    ax.legend()
    ax.set_xlabel(r'Modulation index $k_{p,i}(l,z)$')
    ax.set_ylabel(r'Corrected modulation rate $\tilde{f}_{p,i}(l,z)$')
    plt.tight_layout()
    
    path = "./validations/sq_metrics/roughness_ecma/output/"
    plt.savefig(path+'\\output\\06_mod_rate_estimation_eq_76.png')        
    print('done')

if __name__ =="__main__":
    Phi_E = np.random.rand(150)
    valid_eq_76(Phi_E)

