# -*- coding: utf-8 -*-

from numpy import squeeze

from SciDataTool import Data1D, DataTime, DataFreq

from mosqito.functions.shared.A_weighting import A_weighting
from mosqito.functions.oct3filter.calc_third_octave_levels import (
    calc_third_octave_levels,
)
from mosqito.functions.oct3filter.oct3spec import oct3spec


def comp_3oct_spec(self, unit="dB"):
    """Method to compute third-octave spectrum according to ISO

    Parameter
    ---------
    unit : string
        'dB' or 'dBA'

    """

    # Compute third octave band spectrum
    if self.is_stationary:
        third_spec, freq_val = oct3spec(self.signal.values, self.fs)
    else:
        third_spec, freq_val, time_val = calc_third_octave_levels(
            self.signal.values, self.fs
        )

    # dB -> lin
    # Todo clean all code related to db to lin, use SciDataTool if possible
    third_spec = 2e-5 * 10 ** (third_spec / 20)

    # Define axis objects
    frequency = Data1D(
        name="freqs",
        unit="Hz",
        values=freq_val,
    )
    axes = [frequency]
    if not self.is_stationary:
        time = Data1D(
            name="time",
            unit="s",
            values=time_val,
        )
        axes.append(time)

    # Define Data object
    self.third_spec = DataFreq(
        name="Audio signal",
        symbol="x",
        axes=axes,
        values=third_spec,
        unit="Pa",
        normalizations={"ref": 2e-5},
    )
