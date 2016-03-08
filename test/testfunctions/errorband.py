# -*- coding: utf-8 -*-
#
desc = 'Simple $\sin$ plot with an errorband, which generates a \
        mpl.collections.PolyCollection'
phash = '3333000f555454c6'


def plot():
    from matplotlib import pyplot as plt
    from matplotlib import style
    import numpy as np

    fig, ax = plt.subplots()
    with plt.style.context(('ggplot')):
        t = np.linspace(0, 2*np.pi, 101)
        s = np.sin(t)
        ax.plot(t, s, 'k-')
        ax.fill_between(t, s+0.1, s-0.1, facecolor='k', alpha=0.2)
        ax.set_xlim(t[0], t[-1])
        ax.set_xlabel('t')
        ax.set_ylabel('sin(t)')
        ax.set_title('Simple plot')
        ax.grid(True)
    return fig
