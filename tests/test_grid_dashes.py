from functools import partial

import matplotlib.pyplot as plt
import pytest

import tikzplotlib


def plot(linestyle):
    fig = plt.figure()
    plt.plot([0, 1])
    plt.grid(color="g", linestyle=linestyle)
    return fig


def test_dashed():
    from .helpers import assert_equality

    assert_equality(partial(plot, "--"), __file__[:-3] + "_reference.tex")


@pytest.mark.parametrize(
    "mpl, pgfplots",
    [
        ("-", ""),
        ("--", "dashed"),
        ("-.", "dash pattern=on 1pt off 3pt on 3pt off 3pt"),
        (":", "dotted"),
        ((0, (10, 1)), "dash pattern=on 10pt off 1pt"),
        ((5, (10, 1)), "dash pattern=on 10pt off 1pt, dash phase=5pt"),
        ((0, (1, 2, 3, 4)), "dash pattern=on 1pt off 2pt on 3pt off 4pt"),
    ],
)
def test_linestyle(mpl, pgfplots):
    plot(mpl)
    code = tikzplotlib.get_tikz_code(
        include_disclaimer=False,
        float_format=".8g",
    )
    plt.close("all")

    if pgfplots:
        assert f"grid style={{green01270, {pgfplots}}}" in code
    else:
        assert "grid style={green01270}" in code
