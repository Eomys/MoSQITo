# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 18:06:47 2021

@author: Mesure_07
"""
import pytest
from mosqito.classes.SoundQuality import SoundQuality

out_path = "./mosqito/tests/SoundQuality/output/"
is_show_fig = False


@pytest.fixture(scope="module")
def fixture_import_signal():
    SQ = SoundQuality()
    SQ.import_signal(
        True,
        "./mosqito/validations/loudness_zwicker/data/ISO_532-1/Test signal 5 (pinknoise 60 dB).wav",
        calib=2 * 2 ** 0.5,
    )
    return SQ


@pytest.fixture(scope="module")
def fixture_import_signal_time():
    SQ = SoundQuality()
    SQ.import_signal(
        False,
        "./mosqito/validations/loudness_zwicker/data/ISO_532-1/Annex B.4/Test signal 6 (tone 250 Hz 30 dB - 80 dB).wav",
        calib=2 * 2 ** 0.5,
    )
    return SQ


@pytest.mark.SQ
def test_import_signal():
    SQ = SoundQuality()
    SQ.import_signal(
        True,
        "./mosqito/validations/loudness_zwicker/data/ISO_532-1/Test signal 5 (pinknoise 60 dB).wav",
        calib=2 * 2 ** 0.5,
    )
    SQ.signal.plot_2D_Data(
        "time", is_show_fig=is_show_fig, save_path=out_path + "test_import_signal.png"
    )


@pytest.mark.SQ
def test_comp_3oct_spec(fixture_import_signal):
    SQ = fixture_import_signal
    SQ.comp_3oct_spec()
    SQ.third_spec.plot_2D_Data(
        "freqs",
        is_logscale_x=True,
        type_plot="curve",
        y_min=0,
        y_max=40,
        unit="dB",
        is_show_fig=is_show_fig,
        save_path=out_path + "test_comp_3oct_spec.png",
    )


@pytest.mark.SQ
def test_compute_loudness(fixture_import_signal):
    SQ = fixture_import_signal
    SQ.compute_loudness()
    SQ.loudness_zwicker_specific.plot_2D_Data(
        "cr_band",
        type_plot="curve",
        is_show_fig=is_show_fig,
        save_path=out_path + "test_compute_loudness.png",
    )


@pytest.mark.SQ
def test_compute_loudness_time(fixture_import_signal_time):
    SQ = fixture_import_signal_time
    SQ.compute_loudness()
    SQ.loudness_zwicker.plot_2D_Data(
        "time",
        type_plot="curve",
        is_show_fig=is_show_fig,
        save_path=out_path + "test_compute_loudness_time_1.png",
    )
    SQ.loudness_zwicker_specific.plot_2D_Data(
        "time",
        "cr_band=2.5",
        type_plot="curve",
        is_show_fig=is_show_fig,
        save_path=out_path + "test_compute_loudness_time_2.png",
    )
    SQ.loudness_zwicker_specific.plot_3D_Data(
        "cr_band",
        "time",
        is_2D_view=True,
        is_switch_axes=True,
        is_show_fig=is_show_fig,
        save_path=out_path + "test_compute_loudness_time_3.png",
    )
