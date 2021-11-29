# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:43:45 2020

@author: pc
"""

# Standard imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from mosqito.tests.roughness.signals_test_generation import signal_test
from mosqito.validations.roughness_danielweber.reference_values.references import (
    ref_zf,
    ref_dw,
    ref_ps,
)
from mosqito.functions.roughness_danielweber.comp_roughness import comp_roughness


def comparison_roughness():

    # Parameters definition for signals generation
    fs = 44100
    carrier = np.array([250, 1000, 4000])
    fmod = np.array(
        [10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160, 180, 200, 300, 400]
    )
    mdepth = 1
    duration = 0.2
    dB = 60

    # Overlapping definition for roughness calculation
    overlap = 0

    # Initialization
    r_zf = np.zeros((len(carrier), len(fmod)))
    r_dw = np.zeros((len(carrier), len(fmod)))
    r_ps = np.zeros((len(carrier), len(fmod)))
    R = np.zeros((len(carrier), len(fmod)))

    # Each carrier frequency is considered separately
    for ind_fc in range(3):
        # Roughness reference values
        r_zf[ind_fc, :] = ref_zf(carrier[ind_fc], fmod)
        r_dw[ind_fc, :] = ref_dw(carrier[ind_fc], fmod)
        r_ps[ind_fc, :] = ref_ps(carrier[ind_fc], fmod)
        # Roughness calculation for each modulation frequency
        for ind_fmod in range(fmod.size):
            signal = signal_test(
                carrier[ind_fc], fmod[ind_fmod], mdepth, fs, duration, dB
            )
            rtemp = comp_roughness(signal, fs, overlap)
            R[ind_fc, ind_fmod] = rtemp["values"]

    fig, (axs1, axs2, axs3) = plt.subplots(
        3, 1, figsize=(6, 6), constrained_layout=True
    )

    axs1.plot(
        fmod[0:12], r_zf[0, 0:12], linestyle="dotted", color="black", label="reference"
    )
    axs1.plot(
        fmod[0:12], r_dw[0, 0:12], marker="x", color="red", label="Daniel and Weber"
    )
    axs1.plot(fmod[0:12], r_ps[0, 0:12], marker="o", color="#0069a1", label="Psysound")
    axs1.plot(fmod[0:12], R[0, 0:12], marker="s", color="#69c3c5", label="mosqito")
    axs1.set(xlim=(0, 170), ylim=(0, 1.1))
    axs1.set_title("Carrier frequency of 250 Hz", fontsize=11)
    axs1.legend(loc="upper right", shadow=True)
    axs1.set_ylabel("Roughness [asper]")
    axs1.set_xlabel("Modulation frequency [Hz]")

    axs2.plot(fmod[0:12], r_zf[1, 0:12], linestyle="dotted", color="black")
    axs2.plot(fmod[0:12], r_dw[1, 0:12], marker="x", color="red")
    axs2.plot(fmod[0:12], r_ps[1, 0:12], marker="o", color="#0069a1")
    axs2.plot(fmod[0:12], R[1, 0:12], marker="s", color="#69c3c5")
    axs2.set(xlim=(0, 170), ylim=(0, 1.1))
    axs2.set_ylabel("Roughness [asper]")
    axs2.set_xlabel("Modulation frequency [Hz]")
    axs2.set_title("Carrier frequency of 1000 Hz", fontsize=11)

    axs3.plot(fmod[0:12], r_zf[2, 0:12], linestyle="dotted", color="black")
    axs3.plot(fmod[0:12], r_dw[2, 0:12], marker="x", color="red")
    axs3.plot(fmod[0:12], r_ps[2, 0:12], marker="o", color="#0069a1")
    axs3.plot(fmod[0:12], R[2, 0:12], marker="s", color="#69c3c5")
    axs3.set(xlim=(0, 170), ylim=(0, 1.1))
    axs3.set_ylabel("Roughness [asper]")
    axs3.set_xlabel("Modulation frequency [Hz]")
    axs3.set_title("Carrier frequency of 4000 Hz", fontsize=11)

    fig.savefig("roughness_implementations_comparison" + ".png", format="png")
    # plt.clf()


if __name__ == "__main__":
    comparison_roughness()
