# -*- coding: utf-8 -*-
#
import os

import matplotlib.pyplot as plt

import matplotlib2tikz as m2t


def plot():
    a = [pow(10, i) for i in range(10)]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.semilogy(a, color="blue", lw=0.25)

    plt.grid(b=True, which="major", color="g", linestyle="-", linewidth=0.25)
    plt.grid(b=True, which="minor", color="r", linestyle="--", linewidth=0.5)
    return fig


def test():
    plot()
    code = m2t.get_tikz_code(include_disclaimer=False)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, 'reference.tex'), 'r') as f:
        reference = f.read()[:-1]
    assert reference == code
    return
