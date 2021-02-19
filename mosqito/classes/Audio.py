# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 15:25:12 2020

@author: wantysal
"""

# import SciDataTool objects
from SciDataTool import Data1D, DataTime, DataFreq, DataLinspace

# import methods
from mosqito.functions.shared.load import load
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

    def __init__(self, file, is_stationary=False, calib=1, mat_signal="", mat_fs=""):
        """Constructor of the class. Loads the signal from a .wav .mat or .uff file

        Parameters
        ----------
        self : Audio object
            Object from the Audio class
        file : string
            string path to the signal file
        is_stationary : boolean
            TRUE if the signal is stationary, FALSE if it is time-varying
        calib : float
            calibration factor for the signal to be in [pa]
        mat_signal : string
            in case of a .mat file, name of the signal variable
        mat_fs : string
            in case of a .mat file, name of the sampling frequency variable

        """

        # Import audio signal
        values, fs = load(
            is_stationary,
            file,
            calib=calib,
            mat_signal=mat_signal,
            mat_fs=mat_fs,
        )

        # Create Data object for time axis
        time_axis = DataLinspace(
            name="time",
            unit="s",
            initial=0,
            final=(len(values) - 1) / fs,
            number=len(values),
            include_endpoint=True,
        )

        # Create audio signal Data object and populate the object
        self.fs = fs
        self.is_stationary = is_stationary
        self.signal = DataTime(
            name="Audio signal",
            symbol="x",
            unit="Pa",
            axes=[time_axis],
            values=values,
        )

        # Init physical metrics attributes
        self.third_spec = None
        self.level_db = None
        self.level_dba = None

        # Init physiological metrics attributes
        self.loudness_zwicker = None
        self.loudness_zwicker_specific = None
        self.sharpness = dict()
        self.roughness_dw = None
        self.tonality_tnr = None
        self.tonality_pr = None

    # Methods
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
