"""Bar Chart test
This tests plots a simple bar chart.  Bar charts are plotted as
rectangle patches witch are difficult to tell from other rectangle
patches that should not be plotted in PGFPlots (e.g. axis, legend)
"""
import matplotlib.pyplot as plt
import numpy as np

from helpers import assert_equality


def plot():
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
    assert_equality(plot, "test_barchart_reference.tex")
    return
