# -*- coding: utf-8 -*-
#
from helpers import Phash


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = fig.add_subplot(111)
    dat = np.linspace(0, 10, 20)
    ax.plot(dat, dat ** 2)
    ax2 = ax.twinx()
    ax2.plot(20 * dat, 20 * dat ** 2)
    ax.xaxis.tick_top()
    return fig


def test():
    phash = Phash(plot())
    assert phash.phash == "5b82544c169dde75", phash.get_details()
