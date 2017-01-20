# -*- coding: utf-8 -*-
#
desc = 'Annotations'
# phash = 'ab8a78a1549654fe'
phash = 'ab8a71a1569654de'


def plot():
    from matplotlib import pyplot as pp
    import numpy as np

    fig = pp.figure(1, figsize=(8, 5))
    ax = fig.add_subplot(
            111,
            autoscale_on=False,
            xlim=(-1, 5),
            ylim=(-4, 3)
            )
    t = np.arange(0.0, 5.0, 0.01)
    s = np.cos(2*np.pi*t)
    line, = ax.plot(t, s, color='blue')
    ax.annotate(
            'text',
            xy=(4., 1.),
            xycoords='data',
            xytext=(4.5, 1.5),
            textcoords='data',
            arrowprops=dict(arrowstyle='->', ec='r')
            )
    ax.annotate(
            'arrowstyle',
            xy=(0, 1),
            xycoords='data',
            xytext=(-50, 30),
            textcoords='offset points',
            arrowprops=dict(arrowstyle='->')
            )
    return fig
