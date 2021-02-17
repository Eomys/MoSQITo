# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 09:19:35 2020

@author: wantysal
"""


def cut_signal(signal, fs, start, stop):
    """Cut the input signal before 'start' and after 'stop'

    Parameters
    ----------
    signal : numpy.array
        time signal values
    fs : integer
        sampling frequency
    start : float
        beginning of the new signal in [s]
    stop : float
        end of the new signal in [s]

    """
    return signal[int(start * fs) : int(stop * fs)]
