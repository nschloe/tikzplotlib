import pathlib

import matplotlib.pyplot as plt
import pytest

# the picture 'lena.png' with origin='lower' is flipped upside-down.
# So it has to be upside-down in the pdf-file as well.


def plot():
    import matplotlib.image as mpimg
    from matplotlib import rcParams

    this_dir = pathlib.Path(__file__).resolve().parent
    img = mpimg.imread(this_dir / "lena.png")

    dpi = rcParams["figure.dpi"]
    figsize = img.shape[0] / dpi, img.shape[1] / dpi
    fig = plt.figure(figsize=figsize)
    ax = plt.axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()

    plt.imshow(img, cmap="viridis", origin="upper")

    # Setting the current color map to HSV messes up other plots
    # plt.hsv()
    plt.colorbar()
    return fig


# TODO reintroduce
pytest.mark.skip("Fails?")


def test():
    from helpers import assert_equality

    assert_equality(plot, __file__[:-3] + "_reference.tex")
