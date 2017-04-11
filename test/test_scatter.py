# -*- coding: utf-8 -*-
#
import helpers


def plot():
    from matplotlib import pyplot as plt
    from matplotlib import style
    import numpy as np
    fig = plt.figure()
    with plt.style.context(('fivethirtyeight')):
        np.random.seed(123)
        plt.scatter(
                np.linspace(0, 100, 101),
                np.linspace(0, 100, 101) + 15 * np.random.rand(101)
                )
    return fig


def test():
    helpers.assert_phash(plot(), '7f425b584d603f85')
