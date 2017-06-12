# -*- coding: utf-8 -*-
#
import helpers


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()

    x = np.ma.arange(0, 2*np.pi, 0.02)
    y1 = np.sin(1*x)
    y2 = np.sin(2*x)
    y3 = np.sin(3*x)

    plt.plot(x, y1, label='y1')
    plt.plot(x, y2, label=None)
    plt.plot(x, y3, label='y4')
    plt.legend()

    return fig


def test():
    phash = helpers.Phash(plot())
    assert phash.phash == 'fb7c5e0aaed60094', phash.get_details()
    return


if __name__ == '__main__':
    print(helpers.Phash(plot()).phash)
    # helpers.compare_with_latex(plot())
