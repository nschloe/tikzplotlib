# -*- coding: utf-8 -*-
#
desc = 'Loglog plot with large ticks dimensions'
#phash = 'c103fa59ce6f3e80'
phash = 'ebc35e096e21bec0'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()

    x = np.logspace(0, 6, num=5)
    plt.loglog(x, x**2, lw=2.1)

    return fig
