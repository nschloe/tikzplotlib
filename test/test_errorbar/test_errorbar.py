# -*- coding: utf-8 -*-
#
import os

import matplotlib.pyplot as plt

import matplotlib2tikz as m2t


def plot():
    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = [7.14, 7.36, 7.47, 7.52]
    y = [3.3, 4.4, 8.8, 5.5]
    ystd = [0.1, 0.5, 0.8, 0.3]

    ax.errorbar(x, y, yerr=ystd)

    return fig


def test():
    plot()
    code = m2t.get_tikz_code(include_disclaimer=False)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, 'reference.tex'), 'r') as f:
        reference = f.read()[:-1]
    assert code == reference
    return
