# -*- coding: utf-8 -*-
#
from __future__ import print_function

import helpers

import numpy as np
import matplotlib.pyplot as plt
import pytest


def plot1():
    # Make plot with vertical (default) colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)

    np.random.seed(123)
    data = np.clip(np.random.randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation='nearest')
    ax.set_title('Gaussian noise with vertical colorbar')

    # Add colorbar, make sure to specify tick locations
    # to match desired ticklabels.
    cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
    # vertically oriented colorbar
    cbar.ax.set_yticklabels(['< -1', '0', '> 1'])
    return fig


def plot2():
    # Make plot with horizontal colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)

    np.random.seed(123)
    data = np.clip(np.random.randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation='nearest')
    ax.set_title('Gaussian noise with horizontal colorbar')

    cbar = fig.colorbar(cax, ticks=[-1, 0, 1], orientation='horizontal')
    # horizontal colorbar
    cbar.ax.set_xticklabels(['Low', 'Medium', 'High'])
    return fig


@pytest.mark.parametrize(
    'plot, reference_phash', [
        (plot1, 'fd5a0ba503fd0354'),
        (plot2, '5f5ca33da3816983'),
    ]
    )
def test(plot, reference_phash):
    phash = helpers.Phash(plot())
    assert phash.phash == reference_phash, phash.get_details()
    return


if __name__ == '__main__':
    # plot1()
    # plt.show()
    ph, _, _, _, _, _, _ = helpers.compute_phash(plot2())
    print(ph)
