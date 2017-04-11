# -*- coding: utf-8 -*-
#
import helpers


def plot():
    from matplotlib import pyplot as plt
    import numpy as np
    fig = plt.figure()

    N = 10
    t = np.linspace(0, 1, N)
    x = np.arange(N)
    plt.plot(t, x, '-o', fillstyle='none')
    plt.tight_layout()
    return fig


def test():
    helpers.assert_phash(plot(), 'a103fa09ee613e9e')
