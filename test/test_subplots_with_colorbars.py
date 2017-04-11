# -*- coding: utf-8 -*-
#
import helpers


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    data = np.zeros((3, 3))
    data[:2, :2] = 1.0

    fig = plt.figure()

    ax1 = plt.subplot(131)
    ax2 = plt.subplot(132)
    ax3 = plt.subplot(133)
    axes = [ax1, ax2, ax3]

    for ax in axes:
        im = ax.imshow(data)
        fig.colorbar(im, ax=ax, orientation='horizontal')

    return fig


def test():
    helpers.assert_phash(plot(), '6bc42fd06a95c03f')
