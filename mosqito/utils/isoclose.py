# -*- coding: utf-8 -*-

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
    )

import numpy as np


def isoclose(actual, desired, rtol=1e-7, atol=0, is_plot=False, tol_label=None, xaxis=None):
    """
    Check if two arrays are equal up to desired tolerance.

    The test is inspired from section 5.1 of ISO 532-1. It compares 
    ``actual`` to ``desired +/- min(atol, rtol * abs(desired))``.

    Parameters
    ----------
    actual : array_like
        Array obtained.
    desired : array_like
        Array desired.
    rtol : float, optional
        Relative tolerance.
        Default to 1e-7
    atol : float, optional
        Absolute tolerance.
        Default to 0
    is_plot : bool, optional
        To generate a "compliance" plot.
        Default to False
    tol_label: str
        Label for the tolerance curves
        Default to None
    xaxis : array_like, optional
        x axis for the "compliance" plot.
        Default to None

    Returns
    ------
    is_isoclose: bool
        False if actual and desired are not equal up to specified tolerance.

    """

    # Tolerances
    range_pos = np.amin(
        [desired * (1 - abs(rtol)), desired - abs(atol)], axis=0)
    range_neg = np.amax(
        [desired * (1 + abs(rtol)), desired + abs(atol)], axis=0)

    # Test for ISO 532-1 comformance (section 5.1)
    is_isoclose = (actual >= range_pos).all() and (actual <= range_neg).all()

    if is_plot:
        # Define xaxis
        if xaxis is None:
            xaxis = np.arange(actual.shape[0])

        # Plot desired range
        plt.plot(
            xaxis,
            range_neg,
            color="tab:red",
            linestyle="solid",
            label=tol_label,
            linewidth=1,
        )
        plt.plot(
            xaxis,
            range_pos,
            color="tab:red",
            linestyle="solid",
            # label="",
            linewidth=1,
        )

        # Plot actual value
        plt.plot(xaxis, actual)
        plt.legend()

    return is_isoclose
