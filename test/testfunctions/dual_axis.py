# -*- coding: utf-8 -*-
#
desc = 'Dual axis plot'
# phash = '43a35c4b76a94eb8'
phash = '5bab54492628de7c'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = fig.add_subplot(111)
    dat = np.linspace(0, 10, 20)
    ax.plot(dat, dat**2)
    ax2 = ax.twinx()
    ax2.plot(20*dat, 20*dat**2)

    ax.xaxis.tick_top()

    return fig
