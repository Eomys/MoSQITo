# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 15:25:12 2020

@author: wantysal
"""
import sys

sys.path.append("..")

# Standard library import
import numpy as np

# import SciDataTool objects
from SciDataTool import Data1D, DataTime, DataFreq

# import methods
from mosqito.methods.SoundQuality.import_signal import import_signal
from mosqito.methods.SoundQuality.cut_signal import cut_signal
from mosqito.methods.SoundQuality.comp_3oct_spec import comp_3oct_spec
from mosqito.methods.SoundQuality.compute_level import compute_level
from mosqito.methods.SoundQuality.compute_loudness import compute_loudness

# import Mosqito functions
from mosqito.functions.sharpness.sharpness_aures import comp_sharpness_aures
from mosqito.functions.sharpness.sharpness_din import comp_sharpness_din
from mosqito.functions.sharpness.sharpness_bismarck import comp_sharpness_bismarck
from mosqito.functions.sharpness.sharpness_fastl import comp_sharpness_fastl
from mosqito.functions.roughness_danielweber.comp_roughness import comp_roughness
from mosqito.functions.tonality_tnr_pr.comp_tnr import comp_tnr
from mosqito.functions.tonality_tnr_pr.comp_pr import comp_pr


class SoundQuality:
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
        self.sharpness_aures = None
        self.sharpness_bismarck = None
        self.sharpness_din = None
        self.sharpness_fastl = None
        self.roughness_dw = None
        self.tonality_tnr = None
        self.tonality_pr = None

    import_signal = import_signal
    cut_signal = cut_signal
    comp_3oct_spec = comp_3oct_spec
    compute_level = compute_level
    compute_loudness = compute_loudness

    def compute_sharpness(self, method="din", skip=0.2):
        """Method to cumpute the sharpness according to the given method

        Parameter
        ---------
        method: string
            'din' by default, 'aures', 'bismarck', 'fastl', 'all'
        skip : float
            number of second to be cut at the beginning of the analysis

        """
        if (
            method != "din"
            and method != "aures"
            and method != "fastl"
            and method != "bismarck"
        ):
            raise ValueError(
                "ERROR: method must be 'din', 'aures', 'bismarck' or 'fastl"
            )

        if self.loudness_zwicker == None:
            self.compute_loudness()

        if method == "din" or method == "all":
            S = comp_sharpness_din(
                self.loudness_zwicker.values,
                self.loudness_zwicker_specific.values,
                self.is_stationary,
            )

            if self.is_stationary == True:
                self.sharpness_din = Data1D(values=[S], name="Sharpness", unit="Acum")
            elif self.is_stationary == False:
                # Cut transient effect
                time = np.linspace(0, len(self.signal.values) / self.fs, len(S))
                cut_index = np.argmin(np.abs(time - skip))
                S = S[cut_index:]

                time = Data1D(
                    symbol="T",
                    name="Time axis",
                    unit="s",
                    values=np.linspace(
                        skip, len(self.signal.values) / self.fs, num=S.size
                    ),
                )

                self.sharpness_din = DataTime(
                    symbol="S", axes=[time], values=S, name="Sharpness", unit="Acum"
                )

        elif method == "aures" or method == "all":
            S = comp_sharpness_aures(
                self.loudness_zwicker.values,
                self.loudness_zwicker_specific.values,
                self.is_stationary,
            )

            if self.is_stationary == True:
                self.sharpness_aures = Data1D(values=[S], name="Sharpness", unit="Acum")
            elif self.is_stationary == False:
                # Cut transient effect
                time = np.linspace(0, len(self.signal.values) / self.fs, len(S))
                cut_index = np.argmin(np.abs(time - skip))
                S = S[cut_index:]

                time = Data1D(
                    symbol="T",
                    name="Time axis",
                    unit="s",
                    values=np.linspace(
                        skip, len(self.signal.values) / self.fs, num=S.size
                    ),
                )

                self.sharpness_aures = DataTime(
                    symbol="S", axes=[time], values=S, name="Sharpness", unit="Acum"
                )

        elif method == "bismarck" or method == "all":
            S = comp_sharpness_bismarck(
                self.loudness_zwicker.values,
                self.loudness_zwicker_specific.values,
                self.is_stationary,
            )

            if self.is_stationary == True:
                self.sharpness_bismarck = Data1D(
                    values=[S], name="Sharpness", unit="Acum"
                )
            elif self.is_stationary == False:
                # Cut transient effect
                time = np.linspace(0, len(self.signal.values) / self.fs, len(S))
                cut_index = np.argmin(np.abs(time - skip))
                S = S[cut_index:]

                time = Data1D(
                    symbol="T",
                    name="Time axis",
                    unit="s",
                    values=np.linspace(
                        skip, len(self.signal.values) / self.fs, num=S.size
                    ),
                )

                self.sharpness_bismarck = DataTime(
                    symbol="S", axes=[time], values=S, name="Sharpness", unit="Acum"
                )

        elif method == "fastl" or method == "all":
            S = comp_sharpness_fastl(
                self.loudness_zwicker.values,
                self.loudness_zwicker_specific.values,
                self.is_stationary,
            )

            if self.is_stationary == True:
                self.sharpness_fastl = Data1D(values=[S], name="Sharpness", unit="Acum")
            elif self.is_stationary == False:
                # Cut transient effect
                time = np.linspace(0, len(self.signal.values) / self.fs, len(S))
                cut_index = np.argmin(np.abs(time - skip))
                S = S[cut_index:]

                time = Data1D(
                    symbol="T",
                    name="Time axis",
                    unit="s",
                    values=np.linspace(
                        skip, len(self.signal.values) / self.fs, num=S.size
                    ),
                )

                self.sharpness_fastl = DataTime(
                    symbol="S", axes=[time], values=S, name="Sharpness", unit="Acum"
                )

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
