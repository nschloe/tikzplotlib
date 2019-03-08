# -*- coding: utf-8 -*-
#
import helpers


def plot():
    from matplotlib import pyplot as plt

    a = [pow(10, i) for i in range(10)]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.semilogy(a, color="blue", lw=0.25)

    plt.grid(b=True, which="major", color="g", linestyle="-", linewidth=0.25)
    plt.grid(b=True, which="minor", color="r", linestyle="--", linewidth=0.5)
    return fig


def test():
    phash = helpers.Phash(plot())
    assert phash.phash == "a9eb5eaa7eea1400", phash.get_details()
    return
