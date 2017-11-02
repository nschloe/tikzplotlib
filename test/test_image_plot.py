# -*- coding: utf-8 -*-
#
import helpers

import matplotlib.pyplot as plt
import pytest

# the picture 'lena.png' with origin='lower' is flipped upside-down.
# So it has to be upside-down in the pdf-file as well.


def plot_upper():
    from matplotlib import rcParams
    import matplotlib.image as mpimg
    import os

    this_dir = os.path.dirname(os.path.realpath(__file__))
    img = mpimg.imread(os.path.join(this_dir, 'lena.png'))

    dpi = rcParams['figure.dpi']
    figsize = img.shape[0]/dpi, img.shape[1]/dpi
    fig = plt.figure(figsize=figsize)
    ax = plt.axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()

    plt.imshow(img, cmap='viridis', origin='upper')

    # Set the current color map to HSV.
    plt.hsv()
    plt.colorbar()
    return fig


def plot_lower():
    from matplotlib import rcParams
    import matplotlib.image as mpimg
    import os

    this_dir = os.path.dirname(os.path.realpath(__file__))
    img = mpimg.imread(os.path.join(this_dir, 'lena.png'))

    dpi = rcParams['figure.dpi']
    figsize = img.shape[0] / dpi, img.shape[1] / dpi

    fig = plt.figure(figsize=figsize)
    ax = plt.axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()
    plt.imshow(img, cmap='viridis', origin='lower')
    # Set the current color map to HSV.
    plt.hsv()
    plt.colorbar()
    return fig


@pytest.mark.parametrize(
    'plot, reference_phash', [
        (plot_upper, '75c3d36d1f090ba1'),
        (plot_lower, '7548d3b34f234b07'),
    ]
    )
def test(plot, reference_phash):
    phash = helpers.Phash(plot())
    assert phash.phash == reference_phash, phash.get_details()
    return


if __name__ == '__main__':
    plot_upper()
    plt.show()
