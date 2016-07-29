# -*- coding: utf-8 -*-
#
desc = 'Heat map with color bar'
phash = 'f5a6f27809780b78'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()
    x, y = np.ogrid[-10:10:100j, -10:10:100j]
    extent = (x.min(), x.max(), y.min(), y.max())
    plt.imshow(x*y, extent=extent)
    plt.colorbar()

    return fig
