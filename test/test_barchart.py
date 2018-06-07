# -*- coding: utf-8 -*-
"""Bar Chart test

This tests plots a simple bar chart.  Bar charts are plotted as
rectangle patches witch are difficult to tell from other rectangle
patches that should not be plotted in PGFPlots (e.g. axis, legend)
"""
from helpers import Phash


def plot():
    import matplotlib.pyplot as plt
    import numpy as np

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = np.arange(3)
    y1 = [1, 2, 3]
    y2 = [3, 2, 4]
    y3 = [5, 3, 1]
    w = 0.25

    ax.bar(x - w, y1, w, color="b", align="center")
    ax.bar(x, y2, w, color="g", align="center")
    ax.bar(x + w, y3, w, color="r", align="center")

    return fig


def test():
    phash = Phash(plot())
    assert phash.phash == "5f09a9e6b172874a", phash.get_details()
