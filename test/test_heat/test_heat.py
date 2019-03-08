# -*- coding: utf-8 -*-
#
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import matplotlib2tikz as m2t


def plot():
    fig = plt.figure()
    x, y = np.ogrid[-10:10:100j, -10:10:100j]
    extent = (x.min(), x.max(), y.min(), y.max())
    cmap = matplotlib.cm.get_cmap("gray")
    plt.imshow(x * y, extent=extent, cmap=cmap)
    plt.colorbar()
    return fig


def test():
    plot()
    code = m2t.get_tikz_code(include_disclaimer=False)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, 'reference.tex'), 'r') as f:
        reference = f.read()[:-1]
    assert code == reference
    return
