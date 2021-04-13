# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 15:25:12 2020

@author: wantysal
"""

# import SciDataTool objects
from SciDataTool import DataTime, DataLinspace

# import methods
from mosqito.functions.shared.load import load
from mosqito.methods.Audio.cut_signal import cut_signal
from mosqito.methods.Audio.comp_3oct_spec import comp_3oct_spec
from mosqito.methods.Audio.compute_welch import compute_welch
from mosqito.methods.Audio.compute_level import compute_level
from mosqito.methods.Audio.compute_loudness import compute_loudness
from mosqito.methods.Audio.compute_sharpness import compute_sharpness
from mosqito.methods.Audio.compute_roughness import compute_roughness
from mosqito.methods.Audio.compute_tnr_pr import compute_tnr_pr


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
            normalizations={"ref": 2e-5},
            axes=[time_axis],
            values=values,
        )

        # Init physical metrics attributes
        self.third_spec = None
        self.level = None
        self.welch = None

        # Init physiological metrics attributes
        self.loudness_zwicker = None
        self.loudness_zwicker_specific = None
        self.sharpness = dict()
        self.roughness = dict()
        self.tonality = dict()

    # Methods
    cut_signal = cut_signal
    comp_3oct_spec = comp_3oct_spec
    compute_welch = compute_welch
    compute_level = compute_level
    compute_loudness = compute_loudness
    compute_sharpness = compute_sharpness
    compute_roughness = compute_roughness
    compute_tnr_pr = compute_tnr_pr
