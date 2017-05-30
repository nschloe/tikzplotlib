# -*- coding: utf-8 -*-
#
import helpers


def plot():
    from matplotlib import pyplot as plt

    a = [pow(10, i) for i in range(10)]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    line, = ax.semilogy(a, color='blue', lw=0.25)

    plt.grid(b=True, which='major', color='g', linestyle='-', linewidth=0.25)
    plt.grid(b=True, which='minor', color='r', linestyle='--', linewidth=0.5)
    return fig


def test():
    helpers.assert_phash(plot(), 'e9e25eea7eea1400')
