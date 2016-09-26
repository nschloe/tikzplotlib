# -*- coding: utf-8 -*-
#
desc = 'Another \\texttt{imshow} plot'
phash = 'f5a10b4b0b5e03fc'


def plot():
    import numpy as np
    import matplotlib.pyplot as plt

    da = np.zeros((512, 640))
    da[1:100, 1:100] = 1.0

    fig = plt.figure()
    ax = plt.gca()

    im = ax.imshow(da, cmap='viridis')
    plt.colorbar(im, aspect=5, shrink=0.5)

    plt.title('A new figure')

    return fig
