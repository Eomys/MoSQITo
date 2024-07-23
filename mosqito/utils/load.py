# -*- coding: utf-8 -*-

# Standard library imports
from numpy import int16, int32
from scipy.io import wavfile, loadmat
from scipy.signal import resample
import pyuff


def load(file, wav_calib=None, mat_signal="", mat_fs=""):
    """
    Signal loading
    
    This function extracts the signal and its time axis from .wav or .uff file,
    resamples the signal to 48 kHz, and affects its sampling frequency
    and time signal values.

    Parameters
    ----------
    file : string
        String path to the signal file.
    wav_calib : float, optional
        Wav file calibration factor [Pa/FS]. Level of the signal in Pa_peak
        corresponding to the full scale of the .wav file. If None, a
        calibration factor of 1 is considered. 
        Default to None
    mat_signal : string
        In case of a .mat file, name of the signal variable.
        Default to ""
    mat_fs : string
        In case of a .mat file, name of the sampling frequency variable.
        Default to ""
        
    Returns
    -------
    signal : numpy.array
        time signal values
    fs : integer
        sampling frequency
    """

    # load the .wav file content
    if file[-3:] == "wav" or file[-3:] == "WAV":
        fs, signal = wavfile.read(file)

        # manage multichannel files
        if signal.ndim > 1:
            signal = signal[:, 0]
            print("[Info] Multichannel signal loaded. Keeping only first channel")

        # calibration factor for the signal to be in Pa
        if wav_calib is None:
            wav_calib = 1
            print("[Info] A calibration of 1 Pa/FS is considered")
        if isinstance(signal[0], int16):
            signal = wav_calib * signal / (2**15 - 1)
        elif isinstance(signal[0], int32):
            signal = wav_calib * signal / (2**31 - 1)
        elif isinstance(signal[0], float):
            signal = wav_calib * signal

    # load the .uff file content
    elif file[-3:].lower() == "uff" or file[-3:].lower() == "unv":
        uff_file = pyuff.UFF(file)
        data = uff_file.read_sets()

        # extract the signal values
        signal = data["data"]

        # calculate the sampling frequency
        fs = int(1 / data["abscissa_inc"])

    # load the .mat file content
    elif file[-3:] == "mat":
        matfile = loadmat(file)

        # extract the signal values and sampling frequency
        signal = matfile[mat_signal][:, 0]
        fs = matfile[mat_fs]
        fs = fs[:, 0]

    else:
        raise ValueError("""ERROR: only .wav .mat or .uff files are supported""")

    # resample to 48kHz to allow calculation
    if fs != 48000:
        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000
        print("[Info] Signal resampled to 48 kHz to allow calculation.")

    return signal, fs
