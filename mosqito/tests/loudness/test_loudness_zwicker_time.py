# -*- coding: utf-8 -*-
"""
@date Created on Mon May 25 2020
@author martin_g for Eomys
"""

# Standard library imports

# Third party imports
import numpy as np
import matplotlib.pyplot as plt
import pytest
from pandas import ExcelFile, read_excel

# Local application imports
from mosqito.loudness.loudness_zwicker_time import loudness_zwicker_time
from mosqito.generic.wav_to_oct3 import wav_to_oct3

@pytest.mark.loudness_zwtv  # to skip or run only loudness zwicker time-varying tests
@pytest.mark.parametrize(
    # Test signal as input for time-varying loudness
    # (from ISO 532-1 annex B4)
    "signal",
    [
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.4/Test signal 6 (tone 250 Hz 30 dB - 80 dB).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.4/Results and tests for synthetic signals (time varying loudness).xlsx",
            "tab": "Test signal 6",
            "N_specif_bark": 2.5,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.4/Test signal 7 (tone 1 kHz 30 dB - 80 dB).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.4/Results and tests for synthetic signals (time varying loudness).xlsx",
            "tab": "Test signal 7",
            "N_specif_bark": 8.5,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.4/Test signal 8 (tone 4 kHz 30 dB - 80 dB).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.4/Results and tests for synthetic signals (time varying loudness).xlsx",
            "tab": "Test signal 8",
            "N_specif_bark": 17.5,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.4/Test signal 9 (pink noise 0 dB - 50 dB).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.4/Results and tests for synthetic signals (time varying loudness).xlsx",
            "tab": "Test signal 9",
            "N_specif_bark": 17.5,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.4/Test signal 10 (tone pulse 1 kHz 10 ms 70 dB).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.4/Results and tests for synthetic signals (time varying loudness).xlsx",
            "tab": "Test signal 10",
            "N_specif_bark": 8.5,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.4/Test signal 11 (tone pulse 1 kHz 50 ms 70 dB).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.4/Results and tests for synthetic signals (time varying loudness).xlsx",
            "tab": "Test signal 11",
            "N_specif_bark": 8.5,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.4/Test signal 12 (tone pulse 1 kHz 500 ms 70 dB).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.4/Results and tests for synthetic signals (time varying loudness).xlsx",
            "tab": "Test signal 12",
            "N_specif_bark": 8.5,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.4/Test signal 13 (combined tone pulses 1 kHz).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.4/Results and tests for synthetic signals (time varying loudness).xlsx",
            "tab": "Test signal 13",
            "N_specif_bark": 8.5,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 14 (propeller-driven airplane).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 14",
            "N_specif_bark": -1,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 15 (vehicle interior 40 kmh).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 15",
            "N_specif_bark": -1,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 16 (hairdryer).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 16",
            "N_specif_bark": -1,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 17 (machine gun).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 17",
            "N_specif_bark": -1,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 18 (hammer).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 18",
            "N_specif_bark": -1,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 19 (door creak).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 19",
            "N_specif_bark": -1,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 20 (shaking coins).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 20",
            "N_specif_bark": -1,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 21 (jackhammer).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 21",
            "N_specif_bark": -1,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 22 (ratchet wheel (large)).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 22",
            "N_specif_bark": -1,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 23 (typewriter).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 23",
            "N_specif_bark": -1,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 24 (woodpecker).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 24",
            "N_specif_bark": -1,
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Annex B.5/Test signal 25 (full can rattle).wav",
            "xls": "mosqito/tests/data/ISO_532-1/Annex B.5/Results and tests for technical signals (time varying loudness).xlsx",
            "tab": "Test signal 25",
            "N_specif_bark": -1,
        },
    ],
)

@pytest.mark.loudness_zwtv  # to skip or run only loudness zwicker time-varying tests
def test_loudness_zwicker_time(signal):
    """Test function for the script loudness_zwicker_time

    Test function for the script loudness_zwicker_time with
    .wav file as input. The input file is provided by ISO 532-1 annex 
    B4 and B5, the compliance is assessed according to section 6.1 of the 
    standard. One .png compliance plot is generated.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """
    #
    # Load signal and compute third octave band spectrum
    third_octave_levels, freq = wav_to_oct3(signal["data_file"], calib = 2 * 2**0.5, out_type='time_iso')
    # third_octave_levels = 20 * np.log10((third_octave_levels + 1e-12) / (2*10**-5))
    #
    # Compute Loudness
    N, N_specific, bark_axis = loudness_zwicker_time(third_octave_levels, 'free')
    #
    # Check ISO 532-1 compliance
    assert check_compliance(N, N_specific, bark_axis, signal)


def check_compliance(N, N_specific, bark_axis, iso_ref):
    """Check the comppiance of loudness calc. to ISO 532-1

    Check the compliance of the input data N and N_specific
    to section 6.1 of ISO 532-1 by using the reference data
    described in dictionary iso_ref.

    Parameters
    ----------
    N : float
        Calculated loudness [sones]
    N_specific : numpy.ndarray
        Specific loudness [sones/bark]
    bark_axis : numpy.ndarray
        Corresponding bark axis
    iso_ref : dict
        {
            "data_file": <Path to reference input signal>,
            "N_file": <Path to reference calculated loudness versus time> 
            "N_specif_file": <Path to reference calculated specific loudness>    
            "N_specif_bark": <Bark value of the reference calculation>
        }
        Dictionary containing link to ref. data

    Outputs
    -------
    tst : bool
        Compliance to the reference data
    """
    tst = 1
    #
    # Load ISO reference outputs
    xls_file = ExcelFile(iso_ref["xls"])
    N_iso = np.transpose(read_excel(xls_file, sheet_name=iso_ref["tab"], header=None, 
        skiprows=10, usecols = 'B', squeeze=True).to_numpy())
    N_specif_iso = np.transpose(read_excel(xls_file, sheet_name=iso_ref["tab"], header=None, 
        skiprows=10, usecols = 'L', squeeze=True).to_numpy())
    #
    # Correct eventual 1 sample length difference between MoSQITo and ISO results
    if N_iso.size - N.size == 1:
        N_iso = N_iso[:-1]
        N_specif_iso = N_specif_iso[:,:-1]            
    elif N_iso.size - N.size == -1:
        N = N[:-1]
        N_specific = N_specific[:,:-1]
    elif np.abs(N_iso.size - N.size) > 1:
        tst = 0

    if tst:
        #
        # Define time vector
        time = np.linspace(0,0.002*(N.size - 1),N.size)
        #
        # Formating
        tolerances = [ 
            [0.9, 0.95, 1.05, 1.1], 
            [-0.2, -0.1, 0.1, 0.2] 
            ]
        style = ['solid', 'dashed', 'dashed', 'solid']
        lab = ['10% tolerance', '5% tolerance', '', '']
        clrs = ['red', 'orange', 'orange', 'red']
        #
        # +/- 2ms temporal tolerance
        if sum(abs(N[1:] - N_iso[:-1])) < sum(abs(N - N_iso)):
            N = N[1:]
            N_specific = N_specific[:,1:]
            N_iso = N_iso[:-1]
            N_specif_iso = N_specif_iso[:-1]
            time = time[:-1]
        elif sum(abs(N[:-1] - N_iso[1:])) < sum(abs(N - N_iso)):
            N = N[:-1]
            N_specific = N_specific[:,:-1]
            N_iso = N_iso[1:]
            N_specif_iso = N_specif_iso[1:]
            time = time[1:]
        #
        # Generate compliance plot for loudness and specific loudness
        comp = np.zeros((4,N.size))
        if iso_ref["N_specif_bark"] != -1:
            #
            # Find index of the iso reference signal bark value
            bark = iso_ref["N_specif_bark"]
            i_bark = np.where((np.abs(bark_axis - bark)) == np.amin(np.abs(bark_axis - bark)))[0][0]
            #
            # Data to plot
            Ni = [N, N_specific[i_bark,:]]
            Ni_ref = [N_iso, N_specif_iso]
            Ni_label = ['Loudness', 'Specific loudness at ' + str(bark) + ' Bark']
        else:
            #
            # Data to plot
            Ni = [N]
            Ni_ref = [N_iso]
            Ni_label = ['Loudness']
        for N, N_ref, N_label in zip(Ni, Ni_ref, Ni_label):
            for i in np.arange(4):
                # 
                # Define the tolerance curves and build compliance matrix
                if i in [0, 1]:
                    tol_curve = np.amin([N_ref * tolerances[0][i], N_ref + tolerances[1][i]], axis=0)
                    comp[i,:] = N >= tol_curve
                else:
                    tol_curve = np.amax([N_ref * tolerances[0][i], N_ref + tolerances[1][i]], axis=0)
                    comp[i,:] = N <= tol_curve
                tol_curve[tol_curve < 0] = 0
                #
                # Plot tolerance curves
                plt.plot(time, tol_curve, color=clrs[i], linestyle = style[i], label=lab[i], linewidth=1)
            #
            # Check compliance
            comp_10 = np.array([comp[0,i] and comp[3,i] for i in np.arange(N.size)])
            comp_5 = np.array([comp[1,i] and comp[2,i] for i in np.arange(N.size)])
            ind_10 = np.nonzero(comp_10 == 0)[0]
            ind_5 = np.nonzero(comp_5 == 0)[0]
            if ind_5.size == 0:
                plt.text(0.5, 0.5, 'Test passed (5% tolerance not exceeded)', horizontalalignment='center',
                    verticalalignment='center', transform=plt.gca().transAxes,
                    bbox=dict(facecolor='green', alpha=0.3))
            elif ind_5.size / N.size <= 0.01: 
                plt.text(0.5, 0.5, 'Test passed (5% tolerance exceeded in maximum 1% of time)', horizontalalignment='center',
                    verticalalignment='center', transform=plt.gca().transAxes,
                    bbox=dict(facecolor='orange', alpha=0.3), wrap=True)
            else:
                tst = 0
                plt.text(0.5, 0.5, 'Test not passed', horizontalalignment='center',
                    verticalalignment='center', transform=plt.gca().transAxes, 
                    bbox=dict(facecolor='red', alpha=0.3))
            #
            # Highlights non-compliant area
            for i in ind_10:
                plt.axvspan(time[i]-0.001, time[i]+0.001, facecolor="red", alpha=0.3)
            for i in ind_5:
                if not i in ind_10:
                    plt.axvspan(time[i]-0.001, time[i]+0.001, facecolor="orange", alpha=0.3)
            #
            # Plot the calculated loudness
            plt.plot(time, N,label="MoSQITo")
            plt.title(N_label + ' vs. time - ' + 
                iso_ref["data_file"].split("(")[1].split(")")[0] + ' (' +
                iso_ref["data_file"].split("Test ")[1].split(" (")[0] + ')',
                fontsize=10)
            plt.legend()
            file_name = "_".join(iso_ref["data_file"].split(" "))
            if tst:
                flag = ''
            else:
                flag = 'FAILED_'
            plt.savefig(
                "mosqito/tests/output/" + flag + "test_loudness_zwicker_time_"
                + file_name.split("/")[-1][:-4]
                + "_" + N_label.split(" ")[0]
                + ".png",
                format="png",
            )
            plt.clf()
    return tst