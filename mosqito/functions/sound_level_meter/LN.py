# -*- coding: utf-8 -*-
"""
Created on Wen Dic 1 18:08:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from mosqito.utils.load import load
from mosqito.utils.conversion import amp2db

def LN(signal):
    """Calculate the percentile value of the series of levels (dB) of the one signal.  

    Parameters
    ----------
    signal : numpy.array
        time signal values

    Outputs
    -------
    percentiles : numpy.ndarray
        The values in dB of L90, L50 and L25 of the signal.
    """
    # Empty array to store the values in dB of the signal.
    dB_values = np.zeros(signal.shape[0])
    # Performs the conversion to dB with all the values of the signal.
    print("Ruido Rosa en Tiempo")
    print(signal)
    print(signal.shape)
    for i in range(signal.shape[0]):
        #If the value is negative value.
        if signal[i] <= 0:
            # we convert it to positive.
            signal[i] = np.sqrt(np.mean(signal[i] ** 2))
        # Conversion Pa to dB.
        dB = amp2db(np.array(signal[i]))
        # Save all values in dB of the third octave in another array.
        dB_values[i] = dB
    print("Ruido rosa tiempo dB")
    print(dB_values)
    print('percentiles using interpolation = ', "linear")
    # Calculate the percentiles with the values. "q" of np.percentile = 100 - N (N of LN).
    L90 = np.percentile(dB_values, 10,interpolation='linear') 
    L50 = np.percentile(dB_values, 50,interpolation='linear') 
    L25 = np.percentile(dB_values, 75,interpolation='linear')
    print("The values of L90, L50 and L25 of the signalthirds octaves")
    # Save the calculated percentile values.
    percentiles = np.array([L90,L50,L25])

    print("Los percentiles de 90, 50 y 25")
    return percentiles


if __name__ == "__main__":
    
    sig, fs = load(r"tests\input\white_noise_200_2000_Hz_stationary.wav")
    print(sig)
    print(sig.shape)
    print(fs)

    signal = np.array(sig)

    # [10, 20, 30, ... 100]
    validacion = np.array([0.00006324555320337, 0.0002, 0.0006324555320337, 0.002, 0.006324555320337, 0.02, 
    0.06324555320337, 0.2, 0.6324555320337, 2])
    print(validacion)
    # [20, 40, 60, 80, 100]
    validacion_2 = np.array([0.0002, 0.002, 0.02, 0.2, 2])
    print(validacion_2)

    percentiles = LN(signal)
    print(percentiles)
    
    pass