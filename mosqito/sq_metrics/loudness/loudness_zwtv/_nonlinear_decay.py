# -*- coding: utf-8 -*-
"""
@date Created on Fri May 22 2020
@author martin_g for Eomys
"""

# Standard library imports
import math

# Third party import
import numpy as np


def _nl_loudness(core_loudness):
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
    nl_loudness = np.copy(core_loudness)
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
    #nl_lp["uo_last"] = 0
    #nl_lp["u2_last"] = 0

    delta = np.copy(core_loudness,)
    delta = np.roll(delta, -1, axis=1)
    delta[:, -1] = 0
    delta = (delta - nl_loudness)/nl_iter
    ui_delta = np.zeros(core_loudness.size*nl_iter).reshape(
        core_loudness.shape[0], core_loudness.shape[1], nl_iter)
    ui_delta[:, :, 0] = core_loudness

    for i_in in np.arange(1, nl_iter):
        ui_delta[:, :, i_in] = ui_delta[:, :, i_in-1] + delta

    ui_delta = ui_delta.reshape(
        core_loudness.shape[0], core_loudness.shape[1]*nl_iter)
    uo_mat = np.copy(ui_delta,)
    # create u2_mat (equivalent to u2 last) and fill the first col.
    u2_mat = np.zeros(uo_mat.shape[0]*uo_mat.shape[1]
                      ).reshape(uo_mat.shape[0], uo_mat.shape[1])
    mask = core_loudness[:, 0] >= 1e-5
    u2_mat[mask, 0] = core_loudness[mask, 0]*(1 - nl_lp["B"][5])

    '''
    Truth Table for u2 & uo
    u2 = nl_lp["uo_last"] * nl_lp["B"][0] - nl_lp["u2_last"] * nl_lp["B"][1]
    u2' = (nl_lp["u2_last"] - ui) * nl_lp["B"][5] + ui
    ui < uo(j-1) | uo(j-1) > u2(j-1) | uo < ui  |u2 > uo  |uo' < ui  |abs(ui -  uo(j-1)) < 1e-5 | ui > u2(j-1) | uo                                      |  u2
    ---------------------------------------------------------------
        Truth           Truth           Truth      Truth       --             --                                 ui                                       ui
        Truth           Truth           False      Truth       --             --                                 uo=f(uo(j-1),u2(j-1),B(2),B(3))          uo=f(uo(j-1),u2(j-1),B(2),B(3))
        Truth           Truth           Truth      False       --             --                                 ui                                       u2=f(uo(j-1),u2(j-1),B(0),B(1))
        Truth           Truth           False      False       --             --                                 uo=f(uo(j-1),u2(j-1),B(2),B(3))          u2=f(uo(j-1),u2(j-1),B(0),B(1))
        Truth           False                                  Truth                                             ui                                       ui
        Truth           False                                  False                                             uo=f(uo(j-1),B(4)                        uo=f(uo(j-1),B(4) 
        False                                                                Truth                  Truth        ui                                       u2=f(u2(j-1),B(5),ui(j)
        False                                                                Truth                  False        ui                                       ui
        False                                                                False                  Truth        ui                                       u2=f(u2(j-1),B(5),ui(j)
        False                                                                False                  False        ui                                       u2=f(u2(j-1),B(5),ui(j)
 
    '''
    for col in np.arange(core_loudness.shape[1]*nl_iter):
        uo2 = uo_mat[:, col-1] * nl_lp["B"][2] - \
            u2_mat[:, col-1] * nl_lp["B"][3]
        mask = np.logical_and(
            uo_mat[:, col-1] > u2_mat[:, col-1], uo2 >= ui_delta[:, col])
        uo_mat[mask, col] = uo2[mask]  # in case uo higher than ui

        uo2 = uo_mat[:, col-1] * nl_lp["B"][4]
        mask = np.logical_and(uo_mat[:, col-1] <=
                              u2_mat[:, col-1], uo2 >= ui_delta[:, col])
        uo_mat[mask, col] = uo2[mask]  # in case uo_2 higher than ui

        u2_mat[:, col] = uo_mat[:, col]  # higher than uo
        u22 = uo_mat[:, col-1] * nl_lp["B"][0] - \
            u2_mat[:, col-1] * nl_lp["B"][1]
        mask = np.logical_and(np.logical_and(
            ui_delta[:, col] < uo_mat[:, col-1], uo_mat[:, col-1] > u2_mat[:, col-1]), u22 <= uo_mat[:, col])
        u2_mat[mask, col] = u22[mask]  # in case u22 lower than uo_last

        u2_2 = (u2_mat[:, col-1] - ui_delta[:, col]) * \
            nl_lp["B"][5] + ui_delta[:, col]
        mask = np.logical_and(ui_delta[:, col] >= uo_mat[:, col-1], np.logical_not(np.logical_and(
            abs(ui_delta[:, col] - uo_mat[:, col-1]) < 1e-5,  uo_mat[:, col] <= u2_mat[:, col-1])))
        u2_mat[mask, col] = u2_2[mask]  # lower than ui

    nl_loudness = uo_mat.reshape(
        core_loudness.shape[0], core_loudness.shape[1], nl_iter)[:, :, 0]
    uo_mat = uo_mat.reshape(
        core_loudness.shape[0], core_loudness.shape[1]*nl_iter)

    return nl_loudness
