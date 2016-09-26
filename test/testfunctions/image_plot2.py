# -*- coding: utf-8 -*-
#
desc = 'Another \\texttt{imshow} plot'
phash = 'fda50b4b0b5e035c'


def plot():
    import numpy as np
    import matplotlib.pyplot as plt

    da = np.random.random((512, 640))

    fig = plt.figure()
    ax = plt.gca()

    im = ax.imshow(da, cmap='viridis')
    plt.colorbar(im, aspect=10, shrink=0.5)

    plt.title('A new figure')

    return fig
