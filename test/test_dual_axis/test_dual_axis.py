# -*- coding: utf-8 -*-
#
import os

import matplotlib.pyplot as plt
import numpy as np

import matplotlib2tikz as m2t


def plot():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    dat = np.linspace(0, 10, 20)
    ax.plot(dat, dat ** 2)
    ax2 = ax.twinx()
    ax2.plot(20 * dat, 20 * dat ** 2)
    ax.xaxis.tick_top()
    return fig


def test():
    plot()
    code = m2t.get_tikz_code(include_disclaimer=False)
    print(code)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, 'reference.tex'), 'r') as f:
        reference = f.read()[:-1]
    assert code == reference
    return
