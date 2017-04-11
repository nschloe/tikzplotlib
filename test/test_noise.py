# -*- coding: utf-8 -*-
#
import helpers


def plot():
    from numpy.random import randn
    from matplotlib import pyplot as plt
    import numpy as np

    # Make plot with vertical (default) colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)

    np.random.seed(123)
    data = np.clip(randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation='nearest')
    ax.set_title('Gaussian noise with vertical colorbar')

    # Add colorbar, make sure to specify tick locations
    # to match desired ticklabels.
    cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
    # vertically oriented colorbar
    cbar.ax.set_yticklabels(['< -1', '0', '> 1'])

    return fig


def test():
    helpers.assert_phash(plot(), 'f55a0bb503fd0354')
