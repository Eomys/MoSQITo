# -*- coding: utf-8 -*-

from numpy import log10, linspace, mean, sqrt

from SciDataTool import Data1D, DataTime


def compute_level(self, nb_points=[], start=[], stop=[]):
    """Overall Sound Pressure Level calculation from the time signal
    The SPL can be computed according to a specified number of points or
    during a given time frame

    Parameter:
    ----------
    signal : numpy.array
        time signal value
    fs: integer
        sampling frequency

    Output:
    -------
    level : numpy.array
        SPL in dB

    """
    # Check the inputs
    if nb_points != []:
        if type(nb_points) != int:
            raise TypeError("ERROR : Number of points should be an integer")

        if nb_points < 1 or nb_points > len(self.signal.values):
            raise ValueError(
                "ERROR : Number of points should be between 1 and the length of the given signal"
            )

    if start != [] and stop != []:
        if type(start) != int and type(start) != float:
            raise TypeError("ERROR : Start (in sec) should be an integer or a float ")

        if type(stop) != int and type(stop) != float:
            raise TypeError("ERROR : Stop (in sec) should be an integer or a float ")

        if (
            start < 0
            or stop < 0
            or start > len(self.signal.values) / self.fs
            or stop > len(self.signal.values) / self.fs
        ):
            raise ValueError(
                "ERROR : Time frame should be between 0s and the duration of the signal"
            )

        if start == stop:
            raise ValueError("ERROR : Start and stop values must be different")

    # Initialization
    level = []

    # Case of a given time frame
    if start != [] and stop != []:
        frame = self.signal.values[int(start * self.fs) : int(stop * self.fs)]
    else:
        start = 0
        stop = len(self.signal.values) / self.fs
        frame = self.signal.values

    # Case of a given number of points
    if nb_points != []:

        time = Data1D(
            name="time", unit="s", values=linspace(start, stop, num=nb_points)
        )

        frame_size = int(len(frame) / nb_points)
        for i in range(nb_points):
            frame_i = frame[i * frame_size : i * frame_size + frame_size]
            peff = sqrt(mean(frame_i ** 2))
            level.append(10 * log10((peff ** 2 / (2e-05) ** 2)))

        self.level = DataTime(
            name="Sound Pressure Level",
            symbol="SPL",
            unit="dB",
            axes=[time],
            values=level,
        )

    else:
        peff = sqrt(mean(frame ** 2))
        self.level = 10 * log10((peff ** 2 / (2e-05) ** 2))
