# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 16:36:37 2020

@author: wantysal
"""

import sys
sys.path.append('../../..')

# Third party imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from mosqito.functions.sharpness.comp_sharpness import comp_sharpness
from mosqito.functions.shared.load import load

    # Signals and results from DIN 45692_2009E, chapter 6
broadband_noise = np.zeros((20), dtype = dict)

broadband_noise[0] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC250.wav",
            "type": "Broadband noise",
            "S": 2.70
        }
broadband_noise[1] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC350.wav",
            "S": 2.74
        }
broadband_noise[2] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC450.wav",
            "S": 2.78
        }
broadband_noise[3] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC570.wav",
            "S": 2.85
        }
broadband_noise[4] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC700.wav",
            "S": 2.91
        }
broadband_noise[5] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC840.wav",
            "S": 2.96
        }
broadband_noise[6] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC1000.wav",
            "S": 3.05
        }
broadband_noise[7] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC1170.wav",
            "S": 3.12
        }
broadband_noise[8] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC1370.wav",
            "S": 3.20
        }
broadband_noise[9] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC1600.wav",
            "S": 3.30
        }
broadband_noise[10] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC1850.wav",
            "S": 3.42
        }
broadband_noise[11] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC2150.wav",
            "S": 3.53
        }
broadband_noise[12] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC2500.wav",
            "S": 3.69
        }
broadband_noise[13] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC2900.wav",
            "S": 3.89
        }
broadband_noise[14] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC3400.wav",
            "S": 4.12
        }
broadband_noise[15] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC4000.wav",
            "S": 4.49
        }
broadband_noise[16] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC4800.wav",
            "S": 5.04
        }
broadband_noise[17] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC5800.wav",
            "S": 5.69
        }
broadband_noise[18] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC7000.wav",
            "S": 6.47
        }
broadband_noise[19] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Broadband_noise(fo=10kHz_fu=variabel)\LC8500.wav",
            "S": 7.46
        }

# Test signal as input for sharpness (from DIN 45692)

narrowband_noise = np.zeros((21), dtype = dict)

narrowband_noise[0] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP250.wav",
            "type": "Narrowband noise",
            "S": 0.38
        }
narrowband_noise[1] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP350.wav",
            "S": 0.49
        }
narrowband_noise[2] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP450.wav",
            "S": 0.6
        }
narrowband_noise[3] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP570.wav",
            "S": 0.71
        }
narrowband_noise[4] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP700.wav",
            "S": 0.82
        }
narrowband_noise[5] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP840.wav",
            "S": 0.93
        }
narrowband_noise[6] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP1000.wav",
            "S": 1.00
        }
narrowband_noise[7] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP1170.wav",
            "S": 1.13
        }
narrowband_noise[8] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP1370.wav",
            "S": 1.26
        }
narrowband_noise[9] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP1600.wav",
            "S": 1.35
        }
narrowband_noise[10] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP1850.wav",
            "S": 1.49
        }
narrowband_noise[11] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP2150.wav",
            "S": 1.64
        }
narrowband_noise[12] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP2500.wav",
            "S": 1.78
        }
narrowband_noise[13] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP2900.wav",
            "S": 2.06
        }
narrowband_noise[14] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP3400.wav",
            "S": 2.40
        }
narrowband_noise[15] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP4000.wav",
            "S": 2.82
        }
narrowband_noise[16] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP4800.wav",
            "S": 3.48
        }
narrowband_noise[17] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP5800.wav",
            "S": 4.43
        }
narrowband_noise[18] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP7000.wav",
            "S": 5.52
        }
narrowband_noise[19] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP8500.wav",
            "S": 6.81
        }
narrowband_noise[20] = {
            "data_file": r"data\Check_signals_DIN_45692_(Schaerfe)\Narrowband_noise (frequency group width)\BP10500.wav",
            "S": 8.55
        }

def validation_sharpness(noise):
    """Test function for the script sharpness_din

    Test function for the script sharpness_din with .wav filesas input. 
    The input files are provided by DIN 45692_2009E
    The compliance is assessed according to chapter 6 of the standard. 
    One .png compliance plot is generated.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """
    
    sharpness = np.zeros((len(noise)))
    reference = np.zeros((len(noise)))
    
    for i in range(len(noise)):
        # Load signal 
        sig, fs = load(True, noise[i]["data_file"], calib = 1)
    
        # Compute sharpness
        S = comp_sharpness(True, sig, fs, method ='din')
        sharpness[i] = S['values']
    
        # Load reference value
        reference[i] = noise[i]['S']
        
    noise_type = noise[0]["type"]
    
    check_compliance(sharpness, reference, noise_type)    
    
    

    

def check_compliance(sharpness, reference, noise_type):
    """Check the compliance of sharpness calc. to DIN 45692

    The compliance is assessed according to chapter 6 of the 
    standard DIN 45692_2009E. 
    One .png compliance plot is generated.


    Parameters
    ----------
    sharpness : numpy.array  
        computed sharpness values
    reference : numpy.array    
        reference sharpness values
        

    Outputs
    -------
    tst : bool
        Compliance to the reference data
    """ 
    plt.figure()
    
    # Frequency bark axis
    barks = np.arange(2.5, len(sharpness)+2.5,1)
    
    # Test for DIN 45692_2009E comformance (chapter 6)
    S = sharpness
    tstS = (
        (S >= np.amin([reference * 0.95, reference - 0.05], axis=0)).all()
        and (S <= np.amax([reference * 1.05, reference + 0.05], axis=0)).all()

    )

    # Tolerance curves definition
    tol_low = np.amin([reference * 0.95, reference - 0.05], axis=0)
    tol_high = np.amax([reference * 1.05, reference + 0.05], axis=0)
                            
    # Plot tolerance curves
    plt.plot(barks, tol_low, color='red', linestyle = 'solid', label='tolerance', linewidth=1)
    plt.plot(barks, tol_high, color='red', linestyle = 'solid', linewidth=1)
    
    if tstS:
        plt.text(0.5, 0.5, 'Test passed ', horizontalalignment='center',
             verticalalignment='center', transform=plt.gca().transAxes,
             bbox=dict(facecolor='green', alpha=0.3))
    
    else:                
        plt.text(0.5, 0.5, 'Test not passed', horizontalalignment='center',
                    verticalalignment='center', transform=plt.gca().transAxes, 
                    bbox=dict(facecolor='red', alpha=0.3))
    
    # Plot the calculated sharpness
    plt.plot(barks, sharpness, label="MoSQITo")
    plt.title("Sharpness of " + noise_type ,fontsize=10)
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Sharpness, [acum]")

    plt.savefig(
        "output/" + "validation_sharpness_"
        + noise_type 
        + ".png",
        format="png",
            )
    plt.clf()
    



# test de la fonction
if __name__ == "__main__":

# generate compliance plot for broadband noise 
    validation_sharpness(broadband_noise)
    validation_sharpness(narrowband_noise)
        
    
    
    
    
    