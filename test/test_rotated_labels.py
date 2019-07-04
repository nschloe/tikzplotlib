import os
import tempfile

import pytest
from matplotlib import pyplot as plt

import tikzplotlib


def __plot():
    fig, ax = plt.subplots()

    x = [1, 2, 3, 4]
    y = [1, 4, 9, 6]

    plt.plot(x, y, "ro")
    plt.xticks(x, rotation="horizontal")

    return fig, ax


@pytest.mark.parametrize(
    "x_alignment, y_alignment, x_tick_label_width, y_tick_label_width, rotation",
    [
        (None, None, "1rem", "3rem", 90),
        (None, "center", "1rem", "3rem", 90),
        ("center", None, "1rem", "3rem", 90),
        ("center", "center", None, "3rem", 90),
        ("left", "left", None, "3rem", 90),
        ("right", "right", None, "3rem", 90),
        ("center", "center", "1rem", None, 90),
        ("left", "left", "2rem", None, 90),
        ("right", "right", "3rem", None, 90),
        ("center", "center", "1rem", "3rem", 90),
        ("left", "left", "2rem", "3rem", 90),
        ("right", "right", "3rem", "3rem", 90),
        ("left", "right", "2rem", "3rem", 90),
        ("right", "left", "3rem", "3rem", 90),
    ],
)
def test_rotated_labels_parameters(
    x_alignment, y_alignment, x_tick_label_width, y_tick_label_width, rotation
):
    fig, _ = __plot()

    if x_alignment:
        plt.xticks(ha=x_alignment, rotation=rotation)
    if y_alignment:
        plt.yticks(ha=y_alignment, rotation=rotation)

    # convert to tikz file
    _, tmp_base = tempfile.mkstemp()
    tikz_file = tmp_base + "_tikz.tex"

    extra_dict = {}

    if x_tick_label_width:
        extra_dict["x tick label text width"] = x_tick_label_width
    if y_tick_label_width:
        extra_dict["y tick label text width"] = y_tick_label_width

    tikzplotlib.save(tikz_file, figurewidth="7.5cm", extra_axis_parameters=extra_dict)

    # close figure
    plt.close(fig)

    # delete file
    os.unlink(tikz_file)
    return


@pytest.mark.parametrize(
    "x_tick_label_width, y_tick_label_width",
    [(None, None), ("1rem", None), (None, "3rem"), ("2rem", "3rem")],
)
def test_rotated_labels_parameters_different_values(
    x_tick_label_width, y_tick_label_width
):
    fig, ax = __plot()

    plt.xticks(ha="left", rotation=90)
    plt.yticks(ha="left", rotation=90)
    ax.xaxis.get_majorticklabels()[0].set_rotation(20)
    ax.yaxis.get_majorticklabels()[0].set_horizontalalignment("right")

    # convert to tikz file
    _, tmp_base = tempfile.mkstemp()
    tikz_file = tmp_base + "_tikz.tex"

    extra_dict = {}

    if x_tick_label_width:
        extra_dict["x tick label text width"] = x_tick_label_width
    if y_tick_label_width:
        extra_dict["y tick label text width"] = y_tick_label_width

    tikzplotlib.save(tikz_file, figurewidth="7.5cm", extra_axis_parameters=extra_dict)

    # close figure
    plt.close(fig)

    # delete file
    os.unlink(tikz_file)
    return


def test_rotated_labels_parameters_no_ticks():
    fig, ax = __plot()

    ax.xaxis.set_ticks([])

    plt.tick_params(axis="x", which="both", bottom="off", top="off")
    plt.tick_params(axis="y", which="both", left="off", right="off")

    # convert to tikz file
    _, tmp_base = tempfile.mkstemp()
    tikz_file = tmp_base + "_tikz.tex"

    tikzplotlib.save(tikz_file, figurewidth="7.5cm")

    # close figure
    plt.close(fig)

    # delete file
    os.unlink(tikz_file)
    return
