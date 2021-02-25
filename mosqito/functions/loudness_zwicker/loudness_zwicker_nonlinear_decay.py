# -*- coding: utf-8 -*-
"""
@date Created on Fri May 22 2020
@author martin_g for Eomys
"""

# Standard library imports
import math

# Third party import
import numpy as np


def calc_nl_loudness(core_loudness):
    """Simulate the nonlinear temporal decay of the hearing system

    Parameters
    ----------
    core_loudness : numpy.ndarray
        Core loudness

    Outputs
    -------
    nl_loudness :  numpy.ndarray
        Loudness with non linear temporal decay
    """
    # Initialization
    sample_rate = 2000
    nl_loudness = core_loudness
    # Factor for virtual upsampling/inner iterations
    nl_iter = 24
    # Time constants for non_linear temporal decay
    t_short = 0.005
    t_long = 0.015
    t_var = 0.075
    # Initializes constants B and states of capacitors C1 and C2
    delta_t = 1 / (sample_rate * nl_iter)
    P = (t_var + t_long) / (t_var * t_short)
    Q = 1 / (t_short * t_var)
    lambda_1 = -P / 2 + math.sqrt(P * P / 4 - Q)
    lambda_2 = -P / 2 - math.sqrt(P * P / 4 - Q)
    den = t_var * (lambda_1 - lambda_2)
    e1 = math.exp(lambda_1 * delta_t)
    e2 = math.exp(lambda_2 * delta_t)
    B = [
        (e1 - e2) / den,
        ((t_var * lambda_2 + 1) * e1 - (t_var * lambda_1 + 1) * e2) / den,
        ((t_var * lambda_1 + 1) * e1 - (t_var * lambda_2 + 1) * e2) / den,
        (t_var * lambda_1 + 1) * (t_var * lambda_2 + 1) * (e1 - e2) / den,
        math.exp(-delta_t / t_long),
        math.exp(-delta_t / t_var),
    ]
    nl_lp = {"B": B}

    for i_cl in np.arange(np.shape(core_loudness)[0]):
        # At beginning capacitors C1 and C2 are discharged
        nl_lp["uo_last"] = 0
        nl_lp["u2_last"] = 0

        for i_time in np.arange(np.shape(core_loudness)[1] - 1):
            # interpolation steps between current and next sample
            delta = (
                core_loudness[i_cl, i_time + 1] - core_loudness[i_cl, i_time]
            ) / nl_iter
            ui = core_loudness[i_cl, i_time]
            nl_lp = calc_nl_lp(ui, nl_lp)
            nl_loudness[i_cl, i_time] = nl_lp["uo_last"]
            ui += delta

            # inner iterations
            for i_in in np.arange(1, nl_iter):
                nl_lp = calc_nl_lp(ui, nl_lp)
                ui += delta
        nl_lp = calc_nl_lp(core_loudness[i_cl, i_time + 1], nl_lp)
        nl_loudness[i_cl, i_time + 1] = nl_lp["uo_last"]
    return core_loudness


def calc_nl_lp(ui, nl_lp):
    """Calculates Uo(t) from Ui(t) using UoLast and U2Last

    Parameters
    ----------
    ui : float
        TODO: description cf. standard
    nl_lp : dict
        Parameters for non_linear temporal decay
    Outputs
    -------
    nl_lp : dict
        Updated parameters for non_linear temporal decay
    """
    if ui < nl_lp["uo_last"]:  # case 1 (discharge)
        if nl_lp["uo_last"] > nl_lp["u2_last"]:  # case 1.1
            u2 = nl_lp["uo_last"] * nl_lp["B"][0] - nl_lp["u2_last"] * nl_lp["B"][1]
            uo = nl_lp["uo_last"] * nl_lp["B"][2] - nl_lp["u2_last"] * nl_lp["B"][3]
            if uo < ui:  # uo can't become
                uo = ui  # lower than ui
            if u2 > uo:  # u2 can't become
                u2 = uo  # higher than uo
        else:  # case 1.2
            uo = nl_lp["uo_last"] * nl_lp["B"][4]
            if uo < ui:  # uo can't become
                uo = ui  # lower than ui
            u2 = uo
    else:
        if abs(ui - nl_lp["uo_last"] < 1e-5):  # case 2 (charge)
            uo = ui
            if uo > nl_lp["u2_last"]:  # case 2.1
                u2 = (nl_lp["u2_last"] - ui) * nl_lp["B"][5] + ui
            else:  # case 2.2
                u2 = ui
        else:
            uo = ui
            u2 = (nl_lp["u2_last"] - ui) * nl_lp["B"][5] + ui
    # Preparation for next step
    nl_lp["uo_last"] = uo
    nl_lp["u2_last"] = u2

    return nl_lp
