# -*- coding: utf-8 -*-
""" Bar Chart With Errorbar test

This tests plots a bar chart with error bars.  The errorbars need to be drawn
at the correct z-order to be sucessful.

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
    y1err = [0.1, 0.2, 0.5]
    y2 = [3, 2, 4]
    y2err = [0.4, 0.2, 0.5]
    y3 = [5, 3, 1]
    y3err = [0.1, 0.2, 0.1]
    w = 0.25

    errBarStyle = dict(ecolor='black', lw=5, capsize=8, capthick=5)

    ax.bar(
        x-w, y1, w, color='b', yerr=y1err, align='center', error_kw=errBarStyle
        )
    ax.bar(
        x, y2, w, color='g', yerr=y2err, align='center', error_kw=errBarStyle
        )
    ax.bar(
        x+w, y3, w, color='r', yerr=y3err, align='center', error_kw=errBarStyle
        )

    return fig


def test():
    phash = Phash(plot())
    assert phash.phash == '5f09a9e6b1728746', phash.get_details()
