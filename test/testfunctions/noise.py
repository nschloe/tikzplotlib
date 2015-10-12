# -*- coding: utf-8 -*-
#
desc = 'Noise with a color bar'
sha = ''


def plot():
    from numpy.random import randn
    from matplotlib import pyplot as pp
    import numpy as np

    # Make plot with vertical (default) colorbar
    fig = pp.figure()
    ax = fig.add_subplot(111)

    data = np.clip(randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation='nearest')
    ax.set_title('Gaussian noise with vertical colorbar')

    # Add colorbar, make sure to specify tick locations
    # to match desired ticklabels.
    cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
    # vertically oriented colorbar
    cbar.ax.set_yticklabels(['< -1', '0', '> 1'])

    return fig
