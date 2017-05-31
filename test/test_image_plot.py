# -*- coding: utf-8 -*-
#
import helpers
import pytest

# the picture 'lena.png' with origin='lower' is flipped upside-down.
# So it has to be upside-down in the pdf-file as well.


# test for monochrome picture
def plot1():
    from matplotlib import rcParams
    import matplotlib.pyplot as plt
    from PIL import Image
    import os

    this_dir = os.path.dirname(os.path.realpath(__file__))
    lena = Image.open(os.path.join(this_dir, 'lena.png'))
    lena = lena.convert('L')
    dpi = rcParams['figure.dpi']
    figsize = lena.size[0]/dpi, lena.size[1]/dpi
    fig = plt.figure(figsize=figsize)
    ax = plt.axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()
    plt.imshow(lena, cmap='viridis', origin='lower')
    # Set the current color map to HSV.
    plt.hsv()
    plt.colorbar()
    return fig


# test for rgb picture
def plot2():
    from matplotlib import rcParams
    import matplotlib.pyplot as plt
    from PIL import Image
    import os

    this_dir = os.path.dirname(os.path.realpath(__file__))
    lena = Image.open(os.path.join(this_dir, 'lena.png'))
    dpi = rcParams['figure.dpi']
    figsize = lena.size[0] / dpi, lena.size[1] / dpi
    fig = plt.figure(figsize=figsize)
    ax = plt.axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()
    plt.imshow(lena, cmap='viridis', origin='lower')
    # Set the current color map to HSV.
    plt.hsv()
    plt.colorbar()
    return fig


@pytest.mark.parametrize(
    'plot, phash', [
        (plot1, '455361ec211d72fb'),
        (plot2, '7558d3b30f634b06'),
    ]
    )
def test(plot, phash):
    phash = helpers.Phash(plot())
    assert phash.phash == phash, phash.get_details()
    return
