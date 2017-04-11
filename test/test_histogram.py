# -*- coding: utf-8 -*-
#


def plot():
    import matplotlib.pyplot as plt
    import numpy as np

    # Make plot with vertical (default) colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.hist(10 + 2 * np.random.randn(1000), label='men')
    ax.hist(12 + 3 * np.random.randn(1000), label='women', alpha=0.5)
    ax.legend()
    return fig


# def test():
#     helpers.assert_phash(plot(), '')
