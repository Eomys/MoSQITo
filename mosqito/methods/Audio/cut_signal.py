# -*- coding: utf-8 -*-

from mosqito.functions.shared.cut import cut_signal as cut_signal_fct


def cut_signal(self, start, stop):
    """Method to keep only the signal values between 'start' and 'stop'

    TODO : replace by SciDataTool slicing

    Parameters
    ----------
    start : float
        beginning of the new signal in [s]
    stop : float
        end of the new signal in [s]

    """

    self.signal.values = cut_signal_fct(self.signal.values, self.fs, start, stop)
