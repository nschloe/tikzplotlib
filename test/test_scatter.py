# -*- coding: utf-8 -*-
#
import helpers


def plot():
    from matplotlib import pyplot as plt
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
    phash = helpers.Phash(plot())
    assert phash.phash == '7f425b584d603f85', phash.get_details()
    return
