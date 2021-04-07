# -*- coding: utf-8 -*-

from SciDataTool import DataLinspace, DataTime, DataFreq, Data1D

from mosqito.functions.loudness_zwicker.loudness_zwicker_stationary import (
    loudness_zwicker_stationary,
)
from mosqito.functions.loudness_zwicker.loudness_zwicker_time import (
    loudness_zwicker_time,
)


def compute_loudness(self, field_type="free"):
    """Method to compute the loudness according to Zwicker's method

    Parameter
    ----------
    field-type: string
        'free' by default or 'diffuse'

    """

    # Compute third octave band spetrum if necessary
    if self.third_spec == None:
        self.comp_3oct_spec()

    # define bark_axis
    barks = DataLinspace(
        name="cr_band",
        unit="Bark",
        initial=0.1,
        final=24,
        number=int(24 / 0.1),
        include_endpoint=True,
    )

    if self.is_stationary:
        third_spec_data = self.third_spec.get_along("freqs", unit="dB")
        N, N_specific = loudness_zwicker_stationary(
            third_spec_data["x"],
            third_spec_data["freqs"],
            field_type,
        )
        self.loudness_zwicker = N
        axes = [barks]
    else:
        N, N_specific = loudness_zwicker_time(
            self.third_spec.get_along("freqs", "time", unit="dB")["x"], field_type
        )
        # Get time axis
        # Decimation from temporal resolution 0.5 ms to 2ms
        time = Data1D(
            name="time", unit="s", values=self.third_spec.get_axes()[1].values[::4]
        )
        self.loudness_zwicker = DataTime(
            name="Loudness",
            symbol="N_{zw}",
            unit="sone",
            axes=[time],
            values=N,
        )
        axes = [barks, time]

    self.loudness_zwicker_specific = DataFreq(
        name="Specific Loudness",
        symbol="N'_{zw}",
        unit="sone/Bark",
        axes=axes,
        values=N_specific,
    )
