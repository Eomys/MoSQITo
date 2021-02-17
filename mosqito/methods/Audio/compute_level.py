# -*- coding: utf-8 -*-

from numpy import log10, power, linspace

from SciDataTool import Data1D, DataTime


def compute_level(self, unit):
    """Overall Sound Pressure Level calculation in the chosen unit

    TODO: modify to use get_rms of SciDataTool or even remove

    Parameter:
    ----------
    unit : string
         'dB' or 'dBA' to apply A-weighting
    plot : boolean
        if True, the overall level is plotted along time (non-steady signals)
    """

    if unit == "dB":
        # Third octave spectrum calculation
        if self.third_spec_db == None:
            self.comp_3oct_spec()

        L = 10 * log10(sum(power(10, self.third_spec_db.values / 10)))

        if self.is_stationary == True:
            self.level_db = Data1D(
                values=[L], name="Overall Sound Pressure Level", unit="dB"
            )

        else:
            time = Data1D(
                symbol="T",
                name="Time axis",
                unit="s",
                values=linspace(
                    0,
                    len(self.signal.values) / self.fs,
                    self.third_spec_db.values.shape[1],
                ),
            )

            self.level_db = DataTime(
                symbol="dB",
                axes=[time],
                values=L,
                name="Overall Sound Pressure Level",
                unit="dB",
            )

    elif unit == "dBA":
        # Third octave spectrum calculation
        if self.third_spec_dba == None:
            self.comp_3oct_spec(unit="dBA")

            L = 10 * log10(sum(power(10, self.third_spec_dba.values / 10)))

        if self.is_stationary == True:
            self.level_dba = Data1D(
                values=[L], name="Overall Sound Pressure Level", unit="dBA"
            )
        else:
            time = Data1D(
                symbol="T",
                name="Time axis",
                unit="s",
                values=linspace(
                    0,
                    len(self.signal.values) / self.fs,
                    self.third_spec_dba.values.shape[1],
                ),
            )

            self.level_dba = DataTime(
                symbol="dBA",
                axes=[time],
                values=L,
                name="Overall Sound Pressure Level",
                unit="dBA",
            )
