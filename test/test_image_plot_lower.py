# -*- coding: utf-8 -*-
#
import matplotlib.pyplot as plt

from helpers import assert_equality

# the picture 'lena.png' with origin='lower' is flipped upside-down.
# So it has to be upside-down in the pdf-file as well.


def plot():
    from matplotlib import rcParams
    import matplotlib.image as mpimg
    import os

    this_dir = os.path.dirname(os.path.realpath(__file__))
    img = mpimg.imread(os.path.join(this_dir, "lena.png"))

    dpi = rcParams["figure.dpi"]
    figsize = img.shape[0] / dpi, img.shape[1] / dpi

    fig = plt.figure(figsize=figsize)
    ax = plt.axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()
    plt.imshow(img, cmap="viridis", origin="lower")
    # Set the current color map to HSV.
    plt.hsv()
    plt.colorbar()
    return fig


def test():
    assert_equality(plot, "test_image_plot_lower_reference.tex")
    return
