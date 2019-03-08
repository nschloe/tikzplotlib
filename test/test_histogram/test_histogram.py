# -*- coding: utf-8 -*-
#
import os

import matplotlib.pyplot as plt
import numpy as np

import matplotlib2tikz as m2t


def plot():
    # Make plot with vertical (default) colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)

    np.random.seed(123)
    ax.hist(10 + 2 * np.random.randn(1000), label="men")
    ax.hist(12 + 3 * np.random.randn(1000), label="women", alpha=0.5)
    ax.legend()
    return fig


def test():
    plot()
    code = m2t.get_tikz_code(include_disclaimer=False)
    print(code)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, 'reference.tex'), 'r') as f:
        reference = f.read()[:-1]
    assert reference == code
    return
