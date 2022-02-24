# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 08:59:34 2020

@author: wantysal
"""

# Standard library imports
import numpy as np
from scipy.io import wavfile, loadmat
from scipy.signal import resample

# Optional package import
try:
    import pyuff
except ImportError:
    pyuff = None


def load(file, calib=1, mat_signal="", mat_fs=""):
    """Extract the signal and its time axis from .wav or .uff file,
    resample the signal to 48 kHz, and affects its sampling frequency
    and time signal values.

    Parameters
    ----------
    file : string
        string path to the signal file
    calib : float, optional
        Amplification factor. Shall be equal to 1 if the imported signal
        is already in Pascal [pa]. In some cases (while working with .wav
        files, for instance) the original signal in Pa, of amplitude A, is
        scaled to A/factor before being exported. When using the present
        function with such file, the factor shall be defined as input parameter
        (calib=factor) to be able to scale the signal back to Pascal.
    mat_signal : string
        in case of a .mat file, name of the signal variable
    mat_fs : string
        in case of a .mat file, name of the sampling frequency variable

    Outputs
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
        if isinstance(signal[0], np.int16):
            signal = calib * signal / (2 ** 15 - 1)
        elif isinstance(signal[0], np.int32):
            signal = calib * signal / (2 ** 31 - 1)
        elif isinstance(signal[0], np.float):
            signal = calib * signal

    # load the .uff file content
    elif file[-3:].lower() == "uff" or file[-3:].lower() == "unv":
        data = uff_load(file)

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

    # load the .txt file content
    elif file[-3:] == "txt":
        # extract the values
        data = np.loadtxt(file)
        signal = data[:,1]
        time = data[:,0]

        # calibration for for the signal to be in Pa
        signal = signal * calib
        
        # calculate sampling frequency
        fs = 1/(time[1]-time[0])

    else:
        raise ValueError("""ERROR: only .wav .mat .uff or .txt files are supported""")

    # resample to 48kHz to allow calculation
    if fs != 48000:
        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000
        print("[Info] Signal resampled to 48 kHz to allow calculation.")

    return signal, fs


# def load2oct3(is_stationary, file, calib=1):
#     """Load .wav signal and output its third-octave band spectrum

#     Parameters
#     ----------
#     is_stationary: boolean
#         True if the signal is stationary, False if it is time-varying
#     file : string
#         full path to the signal file
#     calib : float
#         calibration factor for the signal to be in [pa]


#     Outputs
#     -------
#     spec : numpy.ndarray
#         Third octave band spectrum of signal sig [dB re.2e-5 Pa]
#     fpref : numpy.ndarray
#         Corresponding preferred third octave band center frequencies
#     """

#     # Load the signal from its file
#     signal, fs = load(is_stationary, file, calib)

#     # Compute third-octave spectrum
#     output = comp_third_spec(is_stationary, signal, fs)

#     return output


# def load2wav(
#     is_stationary, file, sampling_freq, calib=1, encodage=16, mat_signal="", mat_fs=""
# ):
#     """Load .uff or .mat file and create the corresponding .wav audio file

#     Parameters
#     ----------
#     is_stationary: boolean
#         True if the signal is stationary, False if it is time-varying
#     file : string
#         full path to the signal file
#     sampling_freq : integer
#         sampling frequency of the created .wav file
#     calib : float
#         calibration factor for the signal to be in [pa]
#     encodage : integer
#         encodage of the signal, 16 for np.int16, 32 for np.int32
#     mat_signal : string
#         in case of a .mat file, name of the signal variable
#     mat_fs : string
#         in case of a .mat file, name of the sampling frequency variable
#     Output
#     ------
#     None
#     """

#     # Load the .uff file content
#     if file[-3:].lower() == "uff" or file[-3:].lower() == "unv":
#         data = uff_load(file)

#         # extract the signal values
#         signal = data["data"]

#         # calculate the sampling frequency
#         fs = int(1 / data["abscissa_inc"])

#     # Load the .mat file content
#     elif file[-3:] == "mat":
#         matfile = loadmat(file)

#         # extract the signal values and sampling frequency
#         signal = matfile[mat_signal][:, 0]
#         fs = matfile[mat_fs]
#         fs = fs[:, 0]

#     else:
#         raise ValueError("""ERROR: only .mat or .uff file are supported""")

#     # Resample
#     if fs != sampling_freq:
#         signal = resample(signal, sampling_freq * int(len(signal) / fs))

#     # calibration factor for the signal to be in Pa
#     if encodage == 16:
#         signal = signal * (2 ** 15 - 1) / calib
#         signal = signal.astype(np.int16)

#     elif encodage == 32:
#         signal = signal * (2 ** 31 - 1) / calib
#         signal = signal.astype(np.int32)
#     # create the .wav file
#     newfile = file[:-3] + "wav"
#     wavfile.write(newfile, sampling_freq, signal)


def uff_load(file):
    if pyuff is None:
        raise RuntimeError(
            "In order to load UFF files you need the 'pyuff' " "package."
        )
    uff_file = pyuff.UFF(file)
    data = uff_file.read_sets()
    return data
