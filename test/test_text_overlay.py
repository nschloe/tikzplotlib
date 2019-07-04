import matplotlib.pyplot as plt
import numpy

from helpers import assert_equality


def plot():
    fig = plt.figure()

    xxx = numpy.linspace(0, 5)
    yyy = xxx ** 2
    plt.text(
        1,
        5,
        "test1",
        size=50,
        rotation=30.0,
        ha="center",
        va="bottom",
        color="r",
        style="italic",
        weight="light",
        bbox=dict(
            boxstyle="round, pad=0.2",
            ec=(1.0, 0.5, 0.5),
            fc=(1.0, 0.8, 0.8),
            ls="dashdot",
        ),
    )
    plt.text(
        3,
        6,
        "test2",
        size=50,
        rotation=-30.0,
        ha="center",
        va="center",
        color="b",
        weight="bold",
        bbox=dict(boxstyle="square", ec=(1.0, 0.5, 0.5), fc=(1.0, 0.8, 0.8)),
    )
    plt.text(
        4,
        8,
        "test3",
        size=20,
        rotation=90.0,
        ha="center",
        va="center",
        color="b",
        weight="demi",
        bbox=dict(
            boxstyle="rarrow", ls="dashed", ec=(1.0, 0.5, 0.5), fc=(1.0, 0.8, 0.8)
        ),
    )
    plt.text(
        4,
        16,
        "test4",
        size=20,
        rotation=90.0,
        ha="center",
        va="center",
        color="b",
        weight="heavy",
        bbox=dict(
            boxstyle="larrow", ls="dotted", ec=(1.0, 0.5, 0.5), fc=(1.0, 0.8, 0.8)
        ),
    )
    plt.text(
        2,
        18,
        "test5",
        size=20,
        ha="center",
        va="center",
        color="b",
        bbox=dict(boxstyle="darrow", ec=(1.0, 0.5, 0.5), fc=(1.0, 0.8, 0.8)),
    )
    plt.text(
        1,
        20,
        "test6",
        size=20,
        ha="center",
        va="center",
        color="b",
        bbox=dict(boxstyle="circle", ec=(1.0, 0.5, 0.5), fc=(1.0, 0.8, 0.8)),
    )
    plt.text(
        3,
        23,
        "test7",
        size=20,
        ha="center",
        va="center",
        color="b",
        bbox=dict(boxstyle="roundtooth", ec=(1.0, 0.5, 0.5), fc=(1.0, 0.8, 0.8)),
    )
    plt.text(
        3,
        20,
        "test8",
        size=20,
        ha="center",
        va="center",
        color="b",
        bbox=dict(boxstyle="sawtooth", ec=(1.0, 0.5, 0.5), fc=(1.0, 0.8, 0.8)),
    )
    plt.plot(xxx, yyy, label="a graph")
    plt.legend()

    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return
