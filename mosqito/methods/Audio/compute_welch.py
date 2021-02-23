# -*- coding: utf-8 -*-

from scipy.signal import welch

from SciDataTool import Data1D, DataFreq


def compute_welch(self, N=None, noverlap=None):

    f, Pxx = welch(
        self.signal.values,
        fs=self.fs,
        nperseg=N,
        noverlap=noverlap,
        scaling="spectrum",
    )

    # Define axis objects
    frequency = Data1D(
        name="freqs",
        unit="Hz",
        values=f,
    )

    # Define Data object
    self.welch = DataFreq(
        name="Audio signal",
        symbol="x",
        axes=[frequency],
        values=Pxx ** 0.5,
        unit="Pa",
        normalizations={"ref": 2e-5},
    )
