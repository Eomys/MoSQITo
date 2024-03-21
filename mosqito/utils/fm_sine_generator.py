# -*- coding: utf-8 -*-
"""
Generate frequency-modulated (FM) sine wave

Author:
    Fabio Casagrande Hirono
    Mar 2024
"""

import numpy as np

def fm_sine_generator(spl_level, fc, xm, k, fs, return_aux_params=False,
                      print_info=False):
    """
    Creates a frequency-modulated (FM) signal of level 'spl_level' (in dB SPL)
    with sinusoidal carrier of frequency 'fc', arbitrary modulating signal
    'xm', frequency sensitivity 'k', and sampling frequency 'fs'. The FM signal
    length is the same as the length of 'xm'. 
    
    Parameters
    ----------
    spl_level: float
        Sound Pressure Level [ref 20 uPa RMS] of the modulated signal.
        
    fc: float
        Carrier frequency, in Hz. Must be less than 'fs/2'.
        
    xm: (N,)-shaped numpy.array
        Numpy array containing the modulating signal.
    
    k: float
        Frequency sensitivity of the modulator. This is equal to the frequency
        deviation in Hz away from 'fc' per unit amplitude of the modulating
        signal 'xm'.

    fs: float
        Sampling frequency, in Hz.
    
    return_aux_params: bool, optional
        Flag declaring whether to return a dict containing auxiliary parameters.
        See notes for details. Default is False.
    
    print_info: bool, optional
        Flag declaring whether to print values for maximum frequency deviation
        and FM modulation index. Default is False.
    
    
    Returns
    -------
    y_fm: (N,)-shaped numpy.array
        Frequency-modulated signal with sine carrier.
    
    aux_params: dict
        Dictionary of auxiliary parameters, containing:
            'inst_freq': (N,)-shaped numpy.array of instantaneous frequency of
                output signal;
            'max_freq_deviation': float, maximum frequency deviation from 'fc';
            'FM_modulation_index': float, FM modulation index.
    """
    
    assert fc < fs/2, "Carrier frequency 'fc' must be less than 'fs/2'!"
    
     # sampling interval in seconds
    dt = 1/fs

    # instantaneous frequency of FM signal
    inst_freq = fc + k*xm
    
    # unit-amplitude FM signal
    y_fm = np.sin(2*np.pi * np.cumsum(inst_freq)*dt)
    
    # max frequency deviation
    f_delta = k * np.max(np.abs(xm))
    
    # FM modulation index
    m_FM = np.max(np.abs(2*np.pi * k * np.cumsum(xm)*dt))
    
    # Apply amplitude factor to obtain 'spl_level'
    p_ref = 20e-6
    A_rms = p_ref * 10**(spl_level/20)
    y_fm *= A_rms/np.std(y_fm)

    # # signal power check - must be close to 'spl_level
    # sig_power_dB = 10*np.log10(np.var(y_fm)/(p_ref**2))

    if print_info:
        print(f'\tMax freq deviation: {f_delta} Hz')
        print(f'\tFM modulation index: {m_FM:.2f}')

    aux_params = {
        'inst_freq': inst_freq,
        'max_freq_deviation': f_delta,
        'FM_modulation_index': m_FM}

    if return_aux_params:
        return y_fm, aux_params
    else:
        return y_fm


# %% run example for FM sine generator

if __name__ == "__main__":
    
    import matplotlib.pyplot as plt
    
    # preliminary definitions
    fs = 48000  # [Hz]
    dt = 1/fs
    
    T = 0.1     # [s]
    t = np.linspace(0, T-dt, int(T*fs))
    
    spl = 60        # [dB SPL]
    p_ref = 20e-5   # [Pa RMS]
    
    # sine carrier frequency
    fc = 500
    
    # freq sensitivity
    k = 400
    
    # modulating signal: low frequency sine wave
    fm = 50
    xm = np.sin(2*np.pi*t*fm)
    
    y_fm, aux_params = fm_sine_generator(spl, fc, xm, k, fs,
                                         return_aux_params=True)

    inst_freq = aux_params['inst_freq']

    # plot signal
    fig, plots = plt.subplots(3, 1)
    
    plots[0].set_title('Test signal - frequency-modulated sine wave')
    
    plots[0].plot(t, xm, 'C0', label='Modulating signal')
    plots[0].legend(loc='upper right')
    plots[0].grid()
    plots[0].set_ylabel('Amplitude')
    plots[0].set_xlim([0, T])
    
    plots[1].plot(t, y_fm, 'C1', label='FM signal')
    plots[1].legend(loc='upper right')
    plots[1].grid()
    plots[1].set_ylabel('Amplitude')
    plots[1].set_xlim([0, T])
    
    plots[2].plot(t, inst_freq, 'C2', label='Inst Frequency')
    plots[2].legend(loc='upper right')
    plots[2].grid()
    plots[2].hlines(fc, -0.1, 1.2*T, color='k', linestyle='--')
    plots[2].text(0.0025, fc*0.7, 'carrier freq $f_c$', fontsize=12)
    plots[2].set_ylim([0, 1.1*(fc+k)])
    plots[2].set_xlim([0, T])
    plots[2].set_ylabel('Frequency')
    plots[2].set_xlabel('Time [s]')
    
    fig.set_tight_layout('tight')
    