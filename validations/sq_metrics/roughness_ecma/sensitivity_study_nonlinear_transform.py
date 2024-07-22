import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl   

from roughness_ecma_intermediate_results import roughness_ecma_validation_plots
from mosqito.sq_metrics.roughness.roughness_ecma._lowpass_filter import _lowpass_filter
from mosqito.sq_metrics.roughness.roughness_ecma._non_linear_transform import _non_linear_transform
from input.references import ref_zf


def ecma_non_linear_transform(R_est): 
    """Function to apply the non-linear transform on the intermediate roughness results.
    
    This version is from section 7.1.7 of ECMA 418-2 (2nd edition, 2022).
    """
    N50, CBF = R_est.shape
    R_sq_mean = np.sqrt( np.sum(R_est**2, axis=1) / CBF )
    R_lin_mean = np.mean(R_est, axis=1)
    
    # Eq. 106
    B = np.zeros((N50))
    B[R_lin_mean!=0] = R_sq_mean[R_lin_mean!=0] / R_lin_mean[R_lin_mean!=0]
    
    # !!! ~Eq. 105 !!!
    E = 0.95555 * (np.tanh(1.6407 * (B-2.5804))+1)*0.5 + 0.58449
    c_R = 0.0180909

    return c_R * np.power(R_est,E[...,np.newaxis])

def internoise_non_linear_transform(R_est): 
    """Function to apply the non-linear transform on the intermediate roughness results.
    
    This version is from [1] R. Sottek, J. Becker, T. Lobato, "Progress in Roughness Calculation", 
    Proceedings of Internoise 2020, p.2835, 2846, Seoul, South Korea..
    """
    
    N50, CBF = R_est.shape
    R_sq_mean = np.sqrt( np.sum(R_est**2, axis=1) / CBF )
    R_lin_mean = np.mean(R_est, axis=1)
    
    # Eq. 106
    B = np.zeros((N50))
    B[R_lin_mean!=0] = R_sq_mean[R_lin_mean!=0] / R_lin_mean[R_lin_mean!=0]
    
    # !!! ~Eq. 105 !!!
    E = 0.2532 * np.tanh(1.7543 * (B-2.4954) ) + 0.7083
    c_R = 0.0358556

    return c_R * np.power(R_est,E[...,np.newaxis]) #0.426492*


def comp_roughness(R_time_spec_temp):
    # Lowpass filtering
    R_time_spec = _lowpass_filter(R_time_spec_temp)
    # CALCULATION OF REPRESENTATIVE VALUES (7.1.8)
    # CBF dependent value
    R_spec = np.mean(R_time_spec[10:,:], axis=0) 
    # Time_dependent value
    R_time = 0.5 * np.sum(R_time_spec, axis=1)
    # Single representative value
    R = np.percentile(R_time, 90)
    return R

    
if __name__ == "__main__":

    # Set the default color cycle
    from mosqito import COLORS as clr
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=clr)
    
    from mosqito.utils import am_sine_generator
    
    fs = 48000
    duration = 1
    time = np.linspace(0,duration, int(duration*fs), endpoint=False)
    fc = 1000
    f_mod = [20,40,60,70,80,100,120,150,200,300]
    dB = 60
    N = len(f_mod)
    R_est = np.empty((N), dtype=object)
    
    R_ecma = np.empty((N))
    R_internoise = np.empty((N))
    R_mosqito = np.empty((N))
    R_ref = np.empty((N))

    for i, fm in enumerate(f_mod):
        xmod = np.sin(2*np.pi*fm*time)
        signal, _ = am_sine_generator(xmod, fs, fc, dB)
        _, _, _, bark_axis, t_50, R_est[i] = roughness_ecma_validation_plots(signal, fs, show=False, save=False)
        R_ref[i] = ref_zf(fc, fm)

        R_ecma[i] = comp_roughness(ecma_non_linear_transform(R_est[i]))
        R_internoise[i] = comp_roughness(internoise_non_linear_transform(R_est[i]))
        R_mosqito[i] = comp_roughness(_non_linear_transform(R_est[i]))

    fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
    ax.plot(f_mod, R_ref, '--', color='grey',
               label='Fastl & Zwicker ref')
    ax.plot(f_mod, R_ref+0.1, ':', linewidth=1, color='grey',
               label='0.1 asper tolerance')
    ax.plot(f_mod, R_ref-0.1, ':', linewidth=1, color='grey')
    ax.plot(f_mod, R_ecma, 's:', label='ECMA 418-2', color=clr[1])
    ax.plot(f_mod, R_internoise, '^:', label='Paper 2020', color=clr[2])
    ax.plot(f_mod, R_mosqito, 'o:', label='MOSQITO', color=clr[0])

    ax.set_xlabel('Modulation frequency [Hz]')
    ax.set_ylabel('Roughness [asper]')
    ax.legend()
    plt.tight_layout()
    plt.grid()
    
    plt.savefig('Implementation_comparison.png')
    plt.show(block=True)
    


    print('done')