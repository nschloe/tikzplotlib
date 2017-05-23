# -*- coding: utf-8 -*-
#
import helpers


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = fig.add_subplot(111)
    dat = np.linspace(0, 10, 20)
    ax.plot(dat, dat**2)
    ax2 = ax.twinx()
    ax2.plot(20*dat, 20*dat**2)
    ax.xaxis.tick_top()
    return fig


def test():
    helpers.assert_phash(plot(), '5382544c16bdde75')
