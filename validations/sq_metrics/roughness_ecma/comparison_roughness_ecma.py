# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:43:45 2020

@author: pc
"""

# Standard imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from mosqito.utils.am_sine_wave_generator import am_sine_wave_generator
from input.references import (
    ref_zf,
    ref_dw,
    ref_ps,
)
from mosqito.sq_metrics import roughness_dw, roughness_ecma
from mosqito import COLORS as clr

def comparison_roughness():

    # Parameters definition for signals generation
    fs = 48000
    carrier = np.array([250, 1000, 4000])
    fmod = np.array(
        [20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200, 300, 400]
    )
    mdepth = 1
    duration = 1
    dB = 60

    # Overlapping definition for roughness calculation
    overlap = 0

    # Initialization
    r_zf = np.zeros((len(carrier), len(fmod)))
    r_dw = np.zeros((len(carrier), len(fmod)))
    r_ps = np.zeros((len(carrier), len(fmod)))
    R_dw = np.zeros((len(carrier), len(fmod)))
    R_ecma = np.zeros((len(carrier), len(fmod)))
    
    # Each carrier frequency is considered separately
    for ind_fc, fc in enumerate(carrier):
        # Roughness reference values
        r_zf[ind_fc, :] = ref_zf(fc, fmod)
        r_dw[ind_fc, :] = ref_dw(fc, fmod)
        r_ps[ind_fc, :] = ref_ps(fc, fmod)
        # Roughness calculation for each modulation frequency
        for ind_fmod, fm in enumerate(fmod):
            signal = am_sine_wave_generator(duration, fs, fc, fm, mdepth, dB)
            rtemp, _, _, _ = roughness_dw(signal, fs, overlap)
            R_dw[ind_fc, ind_fmod] = np.mean(rtemp)
            R_ecma[ind_fc, ind_fmod], _, _, _, _ = roughness_ecma(signal, fs)

    fig, (axs1, axs2, axs3) = plt.subplots(3, 1, figsize=(6, 6), constrained_layout=True)
    axs1.plot(fmod[0:12], r_zf[0, 0:12], linestyle="dotted", color="black", label="reference")
    axs1.plot(fmod[0:12], r_dw[0, 0:12], marker="x", color=clr[2], label="Daniel and Weber")
    axs1.plot(fmod[0:12], r_ps[0, 0:12], marker="o", color=clr[1], label="Psysound")
    axs1.plot(fmod[0:12], R_dw[0, 0:12], marker="s", color=clr[0], label="mosqito DW")
    axs1.plot(fmod[0:12], R_ecma[0, 0:12], marker="^", color=clr[3], label="mosqito ECMA")
    axs1.set(xlim=(0, 170), ylim=(0, 1.1))
    axs1.set_title("Carrier frequency of 250 Hz", fontsize=11)
    axs1.legend(loc="upper right", shadow=True)
    axs1.set_ylabel("Roughness [asper]")
    axs1.set_xlabel("Modulation frequency [Hz]")

    axs2.plot(fmod[0:12], r_zf[1, 0:12], linestyle="dotted", color="black")
    axs2.plot(fmod[0:12], r_dw[1, 0:12], marker="x", color=clr[2])
    axs2.plot(fmod[0:12], r_ps[1, 0:12], marker="o", color=clr[1])
    axs2.plot(fmod[0:12], R_dw[1, 0:12], marker="s", color=clr[0])
    axs2.plot(fmod[0:12], R_ecma[1, 0:12], marker="^", color=clr[3])
    axs2.set(xlim=(0, 170), ylim=(0, 1.1))
    axs2.set_ylabel("Roughness [asper]")
    axs2.set_xlabel("Modulation frequency [Hz]")
    axs2.set_title("Carrier frequency of 1000 Hz", fontsize=11)

    axs3.plot(fmod[0:12], r_zf[2, 0:12], linestyle="dotted", color="black")
    axs3.plot(fmod[0:12], r_dw[2, 0:12], marker="x", color=clr[2])
    axs3.plot(fmod[0:12], r_ps[2, 0:12], marker="o", color=clr[1])
    axs3.plot(fmod[0:12], R_dw[2, 0:12], marker="s", color=clr[0])
    axs3.plot(fmod[0:12], R_ecma[2, 0:12], marker="^", color=clr[3])
    axs3.set(xlim=(0, 170), ylim=(0, 1.1))
    axs3.set_ylabel("Roughness [asper]")
    axs3.set_xlabel("Modulation frequency [Hz]")
    axs3.set_title("Carrier frequency of 4000 Hz", fontsize=11)

    fig.savefig(
        "./validations/sq_metrics/roughness_dw/output/"
        + "roughness_implementations_comparison"
        + ".png",
        format="png",
    )
    plt.clf()


if __name__ == "__main__":
    comparison_roughness()
