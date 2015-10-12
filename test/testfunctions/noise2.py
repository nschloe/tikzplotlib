# -*- coding: utf-8 -*-
#
desc = 'Noise with a color bar'
sha = ''


def plot():
    from numpy.random import randn
    from matplotlib import pyplot as pp
    import numpy as np

    # Make plot with horizontal colorbar
    fig = pp.figure()
    ax = fig.add_subplot(111)

    data = np.clip(np.random.randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation='nearest')
    ax.set_title('Gaussian noise with horizontal colorbar')

    cbar = fig.colorbar(cax, ticks=[-1, 0, 1], orientation='horizontal')
    # horizontal colorbar
    cbar.ax.set_xticklabels(['Low', 'Medium', 'High'])

    return fig
