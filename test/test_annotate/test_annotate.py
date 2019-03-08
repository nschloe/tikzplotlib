# -*- coding: utf-8 -*-
#
import os

import matplotlib.pyplot as plt
import numpy as np

import matplotlib2tikz as m2t


def plot():
    fig = plt.figure(1, figsize=(8, 5))
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1, 5), ylim=(-4, 3))
    t = np.arange(0.0, 5.0, 0.01)
    s = np.cos(2 * np.pi * t)
    ax.plot(t, s, color="blue")
    ax.annotate(
        "text",
        xy=(4.0, 1.0),
        xycoords="data",
        xytext=(4.5, 1.5),
        textcoords="data",
        arrowprops=dict(arrowstyle="->", ec="r"),
    )
    ax.annotate(
        "arrowstyle",
        xy=(0, 1),
        xycoords="data",
        xytext=(-50, 30),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->"),
    )
    return fig


def test():
    plot()
    code = m2t.get_tikz_code(include_disclaimer=False)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, 'reference.tex'), 'r') as f:
        reference = f.read()[:-1]
    assert code == reference
    return
