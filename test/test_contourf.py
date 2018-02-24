# -*- coding: utf-8 -*-
#
import matplotlib.pyplot as plt
import numpy as np

import helpers


def plot():

    delta = 0.025
    x = y = np.arange(-3.0, 3.01, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = plt.mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
    Z2 = plt.mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
    Z = 10 * (Z1 - Z2)
    levels = [-2,-1.5,-1.2,-0.9,-0.6,-0.3,0.0,0.3,0.6,0.9,1.2,1.5]
    fig = plt.figure()
    CS = plt.contourf(X, Y, Z, 10, levels=levels)
    plt.contour(CS, levels=levels, colors='r')
    return fig


def test():
    phash = helpers.Phash(plot())
    assert phash.phash == 'ff7e052c093e0716', phash.get_details()


if __name__ == '__main__':
    test()
    #helpers.compare_with_latex(plot())
