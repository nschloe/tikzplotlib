# -*- coding: utf-8 -*-
#
desc = 'Log scaled plot'
phash = 'a9837a09ee29bfa0'


def plot():
    from matplotlib import pyplot as pp

    a = [pow(10, i) for i in range(10)]
    fig = pp.figure()
    ax = fig.add_subplot(1, 1, 1)
    line, = ax.semilogy(a, color='blue', lw=2)

    return fig
