# -*- coding: utf-8 -*-
#
desc = 'Plot with legends'
phash = 'fdfc810697a10e2b'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()

    x = np.ma.arange(0, 2*np.pi, 0.02)
    y = np.ma.sin(x)
    y1 = np.sin(2*x)
    y2 = np.sin(3*x)
    ym1 = np.ma.masked_where(y1 > 0.5, y1)
    ym2 = np.ma.masked_where(y2 < -0.5, y2)

    lines = plt.plot(x, y, 'r', x, ym1, 'g', x, ym2, 'bo')
    plt.setp(lines[0], linewidth=4)
    plt.setp(lines[1], linewidth=2)
    plt.setp(lines[2], markersize=10)

    plt.legend(
            ('No mask', 'Masked if > 0.5', 'Masked if < -0.5'),
            loc='upper right'
            )
    plt.title('Masked line demo')
    return fig
