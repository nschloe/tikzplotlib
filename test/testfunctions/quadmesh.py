# -*- coding: utf-8 -*-
#
desc = 'Plot Taylor--Green Vortex using pcolormesh'
phash = 'ff6c26a669560546'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    x = np.linspace(0*np.pi, 2*np.pi, 128)
    y = np.linspace(0*np.pi, 2*np.pi, 128)
    X, Y = np.meshgrid(x, y)
    nu = 1e-5
    F = lambda t: np.exp(-2*nu*t)
    u = lambda x, y, t:  np.sin(x)*np.cos(y)*F(t)
    v = lambda x, y, t: -np.cos(x)*np.sin(y)*F(t)

    fig, axs = plt.subplots(2, figsize=(8, 12))
    axs[0].pcolormesh(X, Y, u(X, Y, 0))
    axs[1].pcolormesh(X, Y, v(X, Y, 0))
    for ax in axs:
        ax.set_xlim(x[0], x[-1])
        ax.set_ylim(y[0], y[-1])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    axs[0].set_title('Taylor--Green Vortex')

    return fig
