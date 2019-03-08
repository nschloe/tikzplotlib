# -*- coding: utf-8 -*-
#
import os

import matplotlib.pyplot as plt
import numpy as np

import matplotlib2tikz as m2t


def plot():
    da = np.zeros((3, 3))
    da[:2, :2] = 1.0

    fig = plt.figure()
    ax = plt.gca()

    im = ax.imshow(da, cmap="viridis")
    plt.colorbar(im, aspect=5, shrink=0.5)
    return fig


def test():
    plot()
    code = m2t.get_tikz_code(include_disclaimer=False)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, 'reference.tex'), 'r') as f:
        reference = f.read()[:-1]
    assert code == reference
    return
