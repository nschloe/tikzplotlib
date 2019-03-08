# -*- coding: utf-8 -*-
#
import os

import matplotlib.pyplot as plt
import numpy as np

import matplotlib2tikz as m2t


def plot():
    fig, ax = plt.subplots()
    with plt.style.context(("ggplot")):
        t = np.linspace(0, 2 * np.pi, 101)
        s = np.sin(t)
        ax.plot(t, s, "k-")
        ax.fill_between(t, s + 0.1, s - 0.1, facecolor="k", alpha=0.2)
        ax.set_xlim(t[0], t[-1])
        ax.set_xlabel("t")
        ax.set_ylabel("sin(t)")
        ax.set_title("Simple plot")
        ax.grid(True)
    return fig


def test():
    plot()
    code = m2t.get_tikz_code(include_disclaimer=False)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, 'reference.tex'), 'r') as f:
        reference = f.read()[:-1]
    assert code == reference
    return
