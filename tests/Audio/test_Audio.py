# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 18:06:47 2021

@author: Mesure_07
"""

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package."
        )


from mosqito.classes.Audio import Audio
from mosqito import COLORS

out_path = "./tests/output/"
is_show_fig = False


@pytest.fixture(scope="module")
def fixture_import_signal():
    audio = Audio(
        "./tests/input/Test signal 3 (1 kHz 60 dB).wav",
        is_stationary=True,
        calib=2 * 2 ** 0.5,
    )
    return audio


@pytest.fixture(scope="module")
def fixture_import_signal_time():
    audio = Audio(
        "./tests/input/Test signal 6 (tone 250 Hz 30 dB - 80 dB).wav",
        calib=2 * 2 ** 0.5,
    )
    return audio


@pytest.mark.audio
def test_import_signal():
    audio = Audio(
        "./tests/input/Test signal 3 (1 kHz 60 dB).wav",
        is_stationary=True,
        calib=2 * 2 ** 0.5,
    )
    audio.signal.plot_2D_Data(
        "time",
        is_show_fig=is_show_fig,
        save_path=out_path + "test_Audio_import_signal.png",
        color_list=COLORS,
    )


@pytest.mark.audio
def test_comp_3oct_spec():
    audio1 = Audio(
        "./tests/input/Test signal 3 (1 kHz 60 dB).wav",
        is_stationary=True,
        calib=2 * 2 ** 0.5,
    )
    audio1.comp_3oct_spec(fc_min=20, fc_max=20000)
    audio1.third_spec.plot_2D_Data(
        "freqs",
        type_plot="octave",
        is_logscale_x=True,
        # x_min=20,
        # y_min=0,
        # y_max=40,
        unit="dB",
        is_show_fig=is_show_fig,
        save_path=out_path + "test_Audio_comp_3oct_spec.png",
    )


@pytest.mark.audio
def test_level(fixture_import_signal_time):
    audio = fixture_import_signal_time
    audio.compute_level(nb_points=20, start=0.5, stop=4)
    audio.level.plot_2D_Data(
        "time",
        type_plot="curve",
        unit="dB",
        is_show_fig=is_show_fig,
        save_path=out_path + "test_Audio_level.png",
    )


@pytest.mark.audio
def test_compute_loudness(fixture_import_signal):
    audio = fixture_import_signal
    audio.compute_loudness()
    audio.loudness_zwicker_specific.plot_2D_Data(
        "cr_band",
        type_plot="curve",
        is_show_fig=is_show_fig,
        save_path=out_path + "test_Audio_compute_loudness.png",
        color_list=COLORS,
    )


@pytest.mark.audio
def test_compute_loudness_time(fixture_import_signal_time):
    audio = fixture_import_signal_time
    audio.compute_loudness()
    audio.loudness_zwicker.plot_2D_Data(
        "time",
        type_plot="curve",
        is_show_fig=is_show_fig,
        save_path=out_path + "test_Audio_compute_loudness_time_1.png",
        color_list=COLORS,
    )
    audio.loudness_zwicker_specific.plot_2D_Data(
        "time",
        "cr_band=2.5",
        type_plot="curve",
        is_show_fig=is_show_fig,
        save_path=out_path + "test_Audio_compute_loudness_time_2.png",
        color_list=COLORS,
    )
    audio.loudness_zwicker_specific.plot_3D_Data(
        "cr_band",
        "time",
        is_2D_view=True,
        is_switch_axes=True,
        is_show_fig=is_show_fig,
        save_path=out_path + "test_Audio_compute_loudness_time_3.png",
    )


@pytest.mark.audio
def test_compute_sharpness(fixture_import_signal):
    audio = fixture_import_signal
    audio.compute_sharpness(method="all")


@pytest.mark.audio
def test_compute_sharpness_time(fixture_import_signal_time):
    audio = fixture_import_signal_time
    audio.compute_sharpness(method="all")
    audio.sharpness["din"].plot_2D_Data(
        "time",
        type_plot="curve",
        is_show_fig=is_show_fig,
        save_path=out_path + "test_Audio_compute_sharpness_time.png",
        color_list=COLORS,
    )


@pytest.mark.audio
def test_compute_roughness(fixture_import_signal):
    audio = fixture_import_signal
    audio.compute_roughness(overlap=0)


@pytest.mark.audio
def test_compute_roughness_time(fixture_import_signal_time):
    audio = fixture_import_signal_time
    audio.compute_roughness(overlap=0)
    audio.roughness["Daniel Weber"].plot_2D_Data(
        "time",
        type_plot="curve",
        is_show_fig=is_show_fig,
        save_path=out_path + "test_Audio_compute_roughness_time.png",
        color_list=COLORS,
    )


@pytest.mark.audio
def test_compute_tnr_pr(fixture_import_signal):
    audio = fixture_import_signal
    audio.compute_tnr_pr(method="all")


@pytest.mark.audio
def test_compute_tnr_pr_time(fixture_import_signal_time):
    audio = fixture_import_signal_time

    audio.compute_tnr_pr(method="all")
    audio.tonality["tnr"].plot_3D_Data(
        "freqs",
        "time",
        is_2D_view=True,
        is_show_fig=is_show_fig,
        save_path=out_path + "test_Audio_compute_tnr_pr_time.png",
    )


# test of the function
if __name__ == "__main__":
    test_compute_tnr_pr_time()