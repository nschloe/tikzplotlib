# -*- coding: utf-8 -*-
#
import helpers


def plot():
    import matplotlib
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()
    # pylint: disable=invalid-slice-index
    x, y = np.ogrid[-10:10:100j, -10:10:100j]
    extent = (x.min(), x.max(), y.min(), y.max())
    cmap = matplotlib.cm.get_cmap('gray')
    plt.imshow(x*y, extent=extent, cmap=cmap)
    plt.colorbar()

    return fig


def test():
    phash = helpers.Phash(plot())
    assert phash.phash == 'fda6837883788378', phash.get_details()
