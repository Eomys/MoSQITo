# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 14:15:28 2021

@author: Salomé
"""
# Import SciDataTool objects
from SciDataTool import Data1D, DataFreq

# import Mosqito functions
from mosqito.functions.tonality_tnr_pr.comp_tnr import comp_tnr
from mosqito.functions.tonality_tnr_pr.comp_pr import comp_pr


def compute_tnr_pr(self, method, prominence=True):
    """Method to compute tonality metrics according to the given method

    Parameter
    ---------
    method : string
        'tnr' for the tone-to-noise ratio,
        'pr' for the prominence ratio,
        'all' for both
    prominence : boolean
        give only the prominent tones
    """

    if method == "tnr" or method == "all":
        T = comp_tnr(
            self.is_stationary,
            self.signal.values,
            self.fs,
            prominence=prominence,
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
