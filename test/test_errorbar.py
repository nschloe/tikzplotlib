# -*- coding: utf-8 -*-
#
import helpers


def plot():
    import matplotlib.pyplot as plt

    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = [7.14, 7.36, 7.47, 7.52]
    y = [3.3, 4.4, 8.8, 5.5]
    ystd = [0.1, 0.5, 0.8, 0.3]

    ax.errorbar(x, y, yerr=ystd)

    return fig


def test():
    phash = helpers.Phash(plot())
    assert phash.phash == 'ab435e25bea866b0', phash.get_details()
