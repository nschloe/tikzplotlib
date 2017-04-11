# -*- coding: utf-8 -*-
#
import helpers


def plot():
    import matplotlib
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()
    x, y = np.ogrid[-10:10:100j, -10:10:100j]
    extent = (x.min(), x.max(), y.min(), y.max())
    cmap = matplotlib.cm.get_cmap('gray')
    plt.imshow(x*y, extent=extent, cmap=cmap)
    plt.colorbar()

    return fig


def test():
    helpers.assert_phash(plot(), 'fda6837883788378')
