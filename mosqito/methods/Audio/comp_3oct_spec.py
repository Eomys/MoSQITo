# -*- coding: utf-8 -*-

# Optional package import
try:
    import SciDataTool
except ImportError:
    SciDataTool = None

from mosqito.functions.loudness_zwicker.calc_third_octave_levels import (
    calc_third_octave_levels,
)
from mosqito.functions.noct_spectrum.comp_noct_spectrum import comp_noct_spectrum


def comp_3oct_spec(
    self,
    fc_min=25,
    fc_max=12800,
):
    """Method to compute third-octave spectrum according to ISO

    Parameter
    ---------
    fc_min : float
        Filter center frequency of the lowest 1/3 oct. band [Hz]
    fc_max : float
        Filter center frequency of the highest 1/3 oct. band [Hz]

    """
    
    if SciDataTool is None:
        raise RuntimeError(
            "In order to create an audio object you need the 'SciDataTool' package."
            )


    # Compute third octave band spectrum
    if self.is_stationary:
        third_spec, freq_val = comp_noct_spectrum(
            self.signal.values, self.fs, fmin=fc_min, fmax=fc_max, n=3
        )
    else:
        third_spec, freq_val, time_val = calc_third_octave_levels(
            self.signal.values, self.fs
        )
        # dB -> lin
        # Todo clean all code related to db to lin, use SciDataTool if possible
        third_spec = 2e-5 * 10 ** (third_spec / 20)

    # Define axis objects
    frequency = SciDataTool.Data1D(
        name="freqs",
        unit="Hz",
        values=freq_val,
    )
    axes = [frequency]
    if not self.is_stationary:
        time = SciDataTool.Data1D(
            name="time",
            unit="s",
            values=time_val,
        )
        axes.append(time)

    # Define Data object
    self.third_spec = SciDataTool.DataFreq(
        name="Audio signal",
        symbol="x",
        axes=axes,
        values=third_spec,
        unit="Pa",
        normalizations={"ref": 2e-5},
    )
