# -*- coding: utf-8 -*-
#
desc = 'Scatter plot'
phash = '5fd219cc653c85a5'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np
    fig = plt.figure()
    plt.scatter(
            np.random.randn(10),
            np.random.randn(10),
            np.random.rand(10)*90 + 10,
            np.random.randn(10)
            )
    return fig
