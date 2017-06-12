# -*- coding: utf-8 -*-
#
import helpers

from matplotlib import pyplot as plt
import numpy as np


def plot():
    fig = plt.figure()
    x = np.logspace(0, 6, num=5)
    plt.loglog(x, x**2, lw=2.1)
    return fig


def test():
    phash = helpers.Phash(plot())
    assert phash.phash == 'e9c37e896e21be80', phash.get_details()
    return
