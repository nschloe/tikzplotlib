# -*- coding: utf-8 -*-
#
desc = 'Heat map with color bar'
phash = '5f34a1cea1caa1d9'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()
    x, y = np.ogrid[-10:10:100j, -10:10:100j]
    extent = (x.min(), x.max(), y.min(), y.max())
    plt.imshow(x*y, extent=extent)
    plt.colorbar()

    return fig
