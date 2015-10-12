# -*- coding: utf-8 -*-
#
desc = 'Plot with legends'
phash = 'fdfc810617a12e2b'


def plot():
    from matplotlib import pyplot as pp
    import numpy as np

    fig = pp.figure()

    x = np.ma.arange(0, 2*np.pi, 0.02)
    y = np.ma.sin(x)
    y1 = np.sin(2*x)
    y2 = np.sin(3*x)
    ym1 = np.ma.masked_where(y1 > 0.5, y1)
    ym2 = np.ma.masked_where(y2 < -0.5, y2)

    lines = pp.plot(x, y, 'r', x, ym1, 'g', x, ym2, 'bo')
    pp.setp(lines[0], linewidth=4)
    pp.setp(lines[1], linewidth=2)
    pp.setp(lines[2], markersize=10)

    pp.legend(('No mask', 'Masked if > 0.5', 'Masked if < -0.5'),
              loc='upper right'
              )
    pp.title('Masked line demo')
    return fig
