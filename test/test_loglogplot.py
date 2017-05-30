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
    helpers.assert_phash(plot(), 'abc35ec96e21be80')
