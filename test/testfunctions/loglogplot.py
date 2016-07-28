# -*- coding: utf-8 -*-
#
desc = 'Loglog plot with large ticks dimensions'
phash = 'c103fe19ce6f3e80'


def plot():
    from matplotlib import pyplot as pp
    import numpy as np

    fig = pp.figure()

    x = np.logspace(0, 6, num=5)
    pp.loglog(x, x**2)

    return fig
