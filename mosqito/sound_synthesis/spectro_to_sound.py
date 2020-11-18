# -*- coding: utf-8 -*-

from numpy import zeros, linspace, pi, cos, interp, array, float64
from scipy.integrate import cumtrapz
from scipy.io.wavfile import write


def spectro_to_sound(spectrum, freqs, cut_indices=[], time=[0,10], fs=44100, file_name="spectro_wave.wav"):
    """Synthesize wave file from spectrogram

    Parameters
    ----------
    spectrum : ndarray
        stft spectrum (depending on orders and speed)
    freqs : ndarray
        frequencies for each order and speed
    cut_indices : list
        list of indices where a cut occurs
    time : list
        span of the time vector, including time of the cuts
    fs : int
        sampling frequency
    file_name : str
        name of the .wav file to save

    Outputs
    -------
    wave file
    """
    
    W0 = 1e-12

    (Norders, Nspeed) = spectrum.shape
    wave = []
    
    phase_0 = zeros(Norders)
    cut_indices = [0] + cut_indices + [Nspeed-1]
    
    for i in range(len(cut_indices)-1): # Interpolate on each segment of signal
        
        # Extract data for each segment of the signal
        time_i = linspace(time[i], time[i+1], int((time[i+1]-time[i])*fs))
        spectrum_i = spectrum.take(range(cut_indices[i],cut_indices[i+1]),axis=1)
        freqs_i = freqs.take(range(cut_indices[i],cut_indices[i+1]),axis=1)
        
        # Prepare interpolations
        (Norders, Nspeed) = spectrum_i.shape
        time_interp = linspace(time_i[0], time_i[-1], Nspeed)
        wave_i = 0
    
        for order in range(Norders):
            
            # Interpolate frequencies and spectrum
            freqs_interp = interp(time_i, time_interp, freqs_i[order,:])
            spectrum_interp = interp(time_i, time_interp, spectrum_i[order,:])
            
            # Compute phase and wave
            phase = phase_0[order] + cumtrapz(2*pi*freqs_interp, time_i, initial=0)
            wave_i += W0*10**(spectrum_interp/10.0)*cos(phase)
            
            # Ensure continuity of the phase between each segment
            phase_0[i] += phase[-1]
        
        # Concatenate waves
        wave += wave_i[1:].tolist()
    
    # Normalize wave
    m = max(wave)
    wave_f = [0.9*w/m for w in wave]
    
    # Write wave file
    write(file_name, fs, array(wave_f, dtype=float64))