# -*- coding: utf-8 -*-
#
desc = 'Tick label visibility with sharex and sharey'
phash = '9bed5812ff11a892'


def plot():
    from matplotlib import pyplot as pp
    import numpy as np

    fig, axes = pp.subplots(2, 2, sharex=True, sharey=True, figsize=(8, 5))
    t = np.arange(0.0, 5.0, 0.01)
    s = np.cos(2 * np.pi * t)

    axes[0][0].plot(t, s, color='blue')
    axes[0][1].plot(t, s, color='red')
    axes[1][0].plot(t, s, color='green')
    axes[1][1].plot(t, s, color='black')

    return fig
