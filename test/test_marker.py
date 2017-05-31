# -*- coding: utf-8 -*-
#
import helpers


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig, ax = plt.subplots()
    with plt.style.context(('ggplot')):
        t = np.linspace(0, 2*np.pi, 101)
        s = np.sin(t)
        c = np.cos(t)
        ax.plot(t, s, 'ko-', mec='r', markevery=20)
        ax.plot(t, c, 'ks--', mec='r', markevery=20)
        ax.set_xlim(t[0], t[-1])
        ax.set_xlabel('t')
        ax.set_ylabel('y')
        ax.set_title('Simple plot')
        ax.grid(True)
    return fig


def test():
    phash = helpers.Phash(plot())
    assert phash.phash == 'ff2c47a6a1564545', phash.get_details()
    return
