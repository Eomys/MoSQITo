# -*- coding: utf-8 -*-

from scipy.signal import welch

# Optional package import
try:
    import SciDataTool
except ImportError:
    SciDataTool = None


def compute_welch(self, N=None, noverlap=None):
    """
        Method to compute an estimate of the power spectral density computing
        a modified periodogram per segment and then averaging them.
    
        Parameters
        ----------
        N : int, optional
            Length of each segment. The default is None.
        noverlap : float, optional
            Number of points to overlap between segments. The default is None.
    
        Returns
        -------
        None.

    """
    if SciDataTool is None:
        raise RuntimeError(
            "In order to create an audio object you need the 'SciDataTool' package."
            )


    f, Pxx = welch(
        self.signal.values,
        fs=self.fs,
        nperseg=N,
        noverlap=noverlap,
        scaling="spectrum",
    )

    # Define axis objects
    frequency = SciDataTool.Data1D(
        name="freqs",
        unit="Hz",
        values=f,
    )

    # Define Data object
    self.welch = SciDataTool.DataFreq(
        name="Audio signal",
        symbol="x",
        axes=[frequency],
        values=Pxx ** 0.5,
        unit="Pa",
        normalizations={"ref": 2e-5},
    )
