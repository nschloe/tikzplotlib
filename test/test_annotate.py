# -*- coding: utf-8 -*-
#
from helpers import Phash

import matplotlib.pyplot as plt
import numpy as np


def plot():
    fig = plt.figure(1, figsize=(8, 5))
    ax = fig.add_subplot(
            111,
            autoscale_on=False,
            xlim=(-1, 5),
            ylim=(-4, 3)
            )
    t = np.arange(0.0, 5.0, 0.01)
    s = np.cos(2*np.pi*t)
    ax.plot(t, s, color='blue')
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


def test():
    plt.close('all')
    phash = Phash(plot())
    assert phash.phash == 'ab8a71a1549e54be', phash.get_details()


if __name__ == '__main__':
    plot()
    plt.show()
