# -*- coding: utf-8 -*-
#
desc = 'Test colorbar options'
# phash = 'b733c9dc03dc4952'
phash = 'b733c9fc03dc4942'


def plot():
    import numpy as np
    import matplotlib.pyplot as plt

    da = np.zeros((3, 3))
    da[:2, :2] = 1.0

    fig = plt.figure()
    ax = plt.gca()

    im = ax.imshow(da, cmap='viridis')
    plt.colorbar(im, aspect=5, shrink=0.5)

    return fig
