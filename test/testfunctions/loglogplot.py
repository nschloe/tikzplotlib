# -*- coding: utf-8 -*-
#
desc = 'Loglog plot with large ticks dimensions'
# phash = 'c103fa59ce6f3e80'
phash = 'abc35ec96e21be80'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()

    x = np.logspace(0, 6, num=5)
    plt.loglog(x, x**2, lw=2.1)

    return fig
