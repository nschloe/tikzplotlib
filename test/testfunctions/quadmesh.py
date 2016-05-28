# -*- coding: utf-8 -*-
#
desc = 'Plot Taylor--Green Vortex using pcolormesh'
phash = 'ff6c26a669560546'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    x = np.linspace(0*np.pi, 2*np.pi, 128)
    y = np.linspace(0*np.pi, 2*np.pi, 128)
    X, Y = np.meshgrid(x,y)
    nu = 1e-5
    F = lambda t: np.exp(-2*nu*t)
    u = lambda x,y,t:  np.sin(x)*np.cos(y)*F(t)
    v = lambda x,y,t: -np.cos(x)*np.sin(y)*F(t)

    fig, ax = plt.subplots()
    p = ax.pcolormesh(X, Y, u(X,Y,0))
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(y[0], y[-1])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Taylor--Green Vortex (u-velocity component)')

    return fig
