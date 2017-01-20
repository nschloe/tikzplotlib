# -*- coding: utf-8 -*-
#
desc = 'Simple $\sin$ plot with an errorband, which generates an \
        mpl.collections.PolyCollection'
# phash = 'af2cd712256457ac'
phash = '6f2c9d922172672d'


def plot():
    from matplotlib import pyplot as plt
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
