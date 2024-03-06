# -*- coding: utf-8 -*-
"""
Validation script of Roughness ECMA 418-2, 2nd Ed (2022) standard [1]. 

Creates a series of amplitude-modulated sine waves at varying carrier
frequencies 'fc' and modulation frequencies 'fm', and compares with values
taken from Fastl & Zwicker [2], Figure 11.2 (similar to Figure C.1 from
ECMA-418-2 [1]).

References:
    
    [1] ECMA International, "Psychoacoustic metrics for ITT equipment - Part 2
    (models based on human perception)", Standard ECMA-418-2, 2nd edition,
    Dec 2022.
    URL: https://ecma-international.org/publications-and-standards/standards/ecma-418/
    
    [2] H Fastl, E Zwicker, "Psychoacoustics: Facts and Models" (3rd Ed),
    Springer, 2007.

Author:
    Fabio Casagrande Hirono
    Jan 2024
"""

# Standard imports
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

# Local application imports
from mosqito.sq_metrics import roughness_dw, roughness_ecma
from mosqito.sq_metrics.roughness.utils._create_am_sin import _create_am_sin

# must be run from 'MoSQITo/validations/sq_metrics/roughness_ecma' folder!
from input.references import ref_zf

save_fig = False

def signal_test(fc, fmod, mdepth, fs, d, dB):
    # time axis definition
    dt = 1 / fs
    time = np.arange(0, d, dt)

    signal = (
        0.5
        * (1 + mdepth * (np.sin(2 * np.pi * fmod * time)))
        * np.sin(2 * np.pi * fc * time)
    )    
    
    rms = np.sqrt(np.mean(np.power(signal, 2)))
    ampl = 0.00002 * np.power(10, dB / 20) / rms
    signal = signal * ampl
    return signal, time



# %% preliminary definitions
fs = 48000
dt = 1/fs

T = 1.5
t = np.linspace(0, T-dt, int(T*fs))

spl = 60

# %% Fig. 11.2 - Define ranges of fc and fm

fc_all = np.array([125, 250, 500, 1000, 2000, 4000, 8000])

# lower, upper frequency in range for each fc
fm_all = np.array([[10,  10,  10,  10,  15,  15,  20],
                   [100, 150, 200, 400, 350, 300, 250]])


# Recreate Figure 11.2 from Fastl & Zwicker
N_interp_fm = 21

linestyles = [':', ':', ':', '-', '--', '--', '--',]

plt.figure()

for i, fc in enumerate(fc_all):
    
    fm = np.logspace(np.log10(fm_all[0, i]),
                     np.log10(fm_all[1, i]), N_interp_fm, base=10)

    R = ref_zf(fc, fm)
    
    plt.loglog(fm, R, label=f'fc = {fc} Hz', linestyle=linestyles[i])

plt.xlim([10, 400])
plt.ylim([0.07, 1])
plt.legend()
plt.xlabel(r'Modulation frequency $f_{m} [Hz]$')
plt.ylabel('Roughness [asper]')
plt.title('Fastl & Zwicker, Fig. 11.2')


if save_fig:
    plt.savefig('Fast_Zwicker_Fig_11_2.png')

# %% create test signals

for i, fc in enumerate(fc_all):
    
    print(f'Testing fc = {fc} Hz...')
    
    fm_array = np.logspace(np.log10(fm_all[0, i]),
                           np.log10(fm_all[1, i]), N_interp_fm, base=10)
    
    # get values from Fastl & Zwicker
    R_fz = ref_zf(fc, fm_array)
    
    R_dw = np.zeros(fm_array.shape)
    R_ecma = np.zeros(fm_array.shape)
    
    for j, fm in enumerate(fm_array):
        
        # modulating signal
        xm = 1.0*np.sin(2*np.pi*fm*t)
        print(f'Testing fmod = {fm} Hz...')
        # test signal - amplitude-modulated sine wave
        #x = _create_am_sin(spl, fc, xm, fs)
        x, _ = signal_test(fc, fm, 1, fs, 1.5, 60)
        # calculate Roughness using DW model
        R_dw_temp, _, _, _ = roughness_dw(x, fs=fs, overlap=0.5)
        R_dw[j] = np.mean(R_dw_temp)
        
        # calculate Roughness using ECMA model
        R_ecma_temp, _, _ = roughness_ecma(x, fs)
        R_ecma[j] = np.percentile(R_ecma_temp[16:], 90)
        
        # test for 0.1 asper tolerance relative to Fastl & Zwicker
        test = ((R_ecma < R_fz + 0.1).all()
                and (R_ecma > R_fz - 0.1).all())
        
    # plot comparison
    plt.figure()
    
    plt.loglog(fm_array, R_ecma, 'o', color='C0', 
               label='MoSQITo [ECMA-418-2]')
    
    plt.loglog(fm_array, R_dw, 's', fillstyle='none', linewidth=1.5, color='C1',
               label='MoSQITo [Daniel & Weber]')

    plt.loglog(fm_array, R_fz, '--', linewidth=2, color='0.45',
               label='Fastl & Zwicker [interp]')
    plt.loglog(fm_array, R_fz+0.1, ':', linewidth=1, color='0.25',
               label='0.1 asper tolerance')
    plt.loglog(fm_array, R_fz-0.1, ':', linewidth=1, color='0.25')
    
    plt.legend()
    plt.grid(which='both')
    
    plt.yticks(ticks=[0.1, 0.2, 0.5, 1.],
               labels=['0.1', '0.2', '0.5', '1'])
    plt.xticks(ticks=[10, 20, 50, 100, 200, 400],
               labels=['10', '20', '50', '100', '200', '400'])
    
    plt.xlim([10, 400])
    plt.ylim([0.07, 2])
    plt.xlabel(r'Modulation Frequency $f_m$ [Hz]', fontsize=13)
    plt.ylabel('Roughness [asper]', fontsize=13)
    plt.title(rf'Roughness for AM sine wave, $f_c$={fc} Hz', fontsize=14)
    
    if test:
        plt.text( 0.5, 0.5, "Test passed (0.1 asper tolerance not exceeded)", fontsize=13,
            horizontalalignment="center", verticalalignment="center",
            transform=plt.gca().transAxes, bbox=dict(facecolor="green", alpha=0.3))
    else:
        plt.text(0.5, 0.5, "Test not passed", fontsize=13,
                 horizontalalignment="center", verticalalignment="center",
                 transform=plt.gca().transAxes, bbox=dict(facecolor="red", alpha=0.3))
    
    plt.tight_layout()
    
    if save_fig:
        plt.savefig('validation_roughness_ecma_fc' + f'{fc}' + 'Hz.png')
    
plt.show(block=True)
print('\tDone!')
