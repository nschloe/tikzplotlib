# -*- coding: utf-8 -*-
#
import helpers


def plot():
    from matplotlib import pyplot as pp
    import numpy as np

    # Make plot with horizontal colorbar
    fig = pp.figure()
    ax = fig.add_subplot(111)

    np.random.seed(123)
    data = np.clip(np.random.randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation='nearest')
    ax.set_title('Gaussian noise with horizontal colorbar')

    cbar = fig.colorbar(cax, ticks=[-1, 0, 1], orientation='horizontal')
    # horizontal colorbar
    cbar.ax.set_xticklabels(['Low', 'Medium', 'High'])

    return fig


def test():
    helpers.assert_phash(plot(), '5f5ca33da3816983')
