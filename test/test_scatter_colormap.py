# -*- coding: utf-8 -*-
#
import helpers


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


def test():
    phash = helpers.Phash(plot())
    assert phash.phash == 'cf616c42e4ec738c', phash.get_details()
    return
