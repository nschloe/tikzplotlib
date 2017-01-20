# -*- coding: utf-8 -*-
#
desc = 'Scatter plot'
#phash = 'cf316c4e70cc738c'
phash = 'cb616ccae54c738c'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np
    fig = plt.figure()
    np.random.seed(123)
    plt.scatter(
            np.random.randn(10),
            np.random.randn(10),
            np.random.rand(10)*90 + 10,
            np.random.randn(10)
            )
    return fig
