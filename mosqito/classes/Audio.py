# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 15:25:12 2020

@author: wantysal
"""
import sys

sys.path.append("..")

# import SciDataTool objects
from SciDataTool import Data1D, DataTime, DataFreq

# import methods
from mosqito.methods.Audio.import_signal import import_signal
from mosqito.methods.Audio.cut_signal import cut_signal
from mosqito.methods.Audio.comp_3oct_spec import comp_3oct_spec
from mosqito.methods.Audio.compute_level import compute_level
from mosqito.methods.Audio.compute_loudness import compute_loudness
from mosqito.methods.Audio.compute_sharpness import compute_sharpness

# import Mosqito functions
from mosqito.functions.roughness_danielweber.comp_roughness import comp_roughness
from mosqito.functions.tonality_tnr_pr.comp_tnr import comp_tnr
from mosqito.functions.tonality_tnr_pr.comp_pr import comp_pr


class Audio:
    """Audio signal loading and analysis: from .wav or .uff files compute
    loudness, sharpness and roughness values thanks to the Mosqito package,
    Results plotting thanks to the SciDataTool package."""

    def __init__(self):
        """Constructor of the class."""

        self.signal = None
        self.is_stationary = bool()
        self.fs = int()
        self.time_axis = None
        self.third_spec = None
        self.level_db = None
        self.level_dba = None
        self.loudness_zwicker = None
        self.loudness_zwicker_specific = None
        self.sharpness = dict()
        self.roughness_dw = None
        self.tonality_tnr = None
        self.tonality_pr = None

    import_signal = import_signal
    cut_signal = cut_signal
    comp_3oct_spec = comp_3oct_spec
    compute_level = compute_level
    compute_loudness = compute_loudness
    compute_sharpness = compute_sharpness

    def compute_roughness(self, method="danielweber", overlap=0):
        """Method to compute roughness according to the Daniel and Weber implementation

        Parameter
        ---------
        method : string
            method used to do the computation 'danielweber' is the only one for now
        overlap : float
            overlapping coefficient for the time windows of 200ms
        """
        roughness = comp_roughness(self.signal.values, self.fs, overlap)

        time = Data1D(name="Time", unit="s", values=roughness["time"])

        self.roughness_dw = DataTime(
            symbol="R",
            axes=[time],
            values=roughness["values"],
            name="Roughness",
            unit="Asper",
        )

    def compute_tonality(self, method, prominence=True, plot=True):
        """Method to compute tonality metrics according to the given method

        Parameter
        ---------
        method : string
            'tnr' for the tone-to-noise ratio,
            'pr' for the prominence ratio,
            'all' for both
        prominence : boolean
            give only the prominent tones
        plot : boolean
            if True the results are plotted
        """

        if method == "tnr" or method == "all":
            T = comp_tnr(
                self.is_stationary,
                self.signal.values,
                self.fs,
                prominence=prominence,
                plot=plot,
            )

            freqs = Data1D(
                symbol="F", name="Tones frequencies", unit="Hz", values=T["freqs"]
            )

            if self.is_stationary == True:

                self.tonality_tnr = DataFreq(
                    symbol="TNR",
                    axes=[freqs],
                    values=T["values"],
                    name="Tone-to-noise ratio",
                    unit="dB",
                )

                self.tonality_ttnr = Data1D(
                    symbol="T-TNR",
                    name="Total TNR value",
                    unit="dB",
                    values=[T["global value"]],
                )

            elif self.is_stationary == False:

                time = Data1D(symbol="T", name="Time axis", unit="s", values=T["time"])

                self.tonality_tnr = DataFreq(
                    symbol="TNR",
                    axes=[freqs, time],
                    values=T["values"],
                    name="Tone-to-noise ratio",
                    unit="dB",
                )

                self.tonality_ttnr = Data1D(
                    symbol="T-TNR",
                    name="Total TNR value",
                    unit="dB",
                    values=T["global value"],
                )

        if method == "pr" or method == "all":
            T = comp_pr(
                self.is_stationary,
                self.signal.values,
                self.fs,
                prominence=prominence,
                plot=plot,
            )

            freqs = Data1D(
                symbol="F", name="Tones frequencies", unit="Hz", values=T["freqs"]
            )

            if self.is_stationary == True:

                self.tonality_pr = DataFreq(
                    symbol="PR",
                    axes=[freqs],
                    values=T["values"],
                    name="Prominence ratio",
                    unit="dB",
                )

                self.tonality_tpr = Data1D(
                    symbol="T-TNR",
                    name="Total TNR value",
                    unit="dB",
                    values=[T["global value"]],
                )

            elif self.is_stationary == False:
                time = Data1D(symbol="T", name="Time axis", unit="s", values=T["time"])

                self.tonality_pr = DataFreq(
                    symbol="PR",
                    axes=[freqs, time],
                    values=T["values"],
                    name="Prominence ratio",
                    unit="dB",
                )

                self.tonality_tpr = Data1D(
                    symbol="T-TNR",
                    name="Total TNR value",
                    unit="dB",
                    values=T["global value"],
                )
