# -*- coding: utf-8 -*-
#
desc = 'Another \\texttt{imshow} plot'
phash = '7558d3b30f634b02'


def plot():
    import numpy as np
    import matplotlib.pyplot as plt

    da = np.random.random((512, 640))

    fig = plt.figure()
    ax = plt.gca()

    im = ax.imshow(da, cmap='viridis')
    plt.colorbar(im, aspect=10, shrink=0.8)

    plt.title('A new figure')

    return fig
