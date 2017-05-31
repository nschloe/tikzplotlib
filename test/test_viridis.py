# -*- coding: utf-8 -*-
#
import helpers


def plot():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    x, y = np.meshgrid(np.linspace(0, 1), np.linspace(0, 1))
    z = x**2 - y**2

    fig = plt.figure()
    plt.pcolormesh(x, y, z, cmap=cm.viridis)
    # plt.colorbar()

    return fig


def test():
    helpers.assert_phash(plot(), 'fd7e03fc03bc0381')


if __name__ == '__main__':
    helpers.print_tree(plot())
