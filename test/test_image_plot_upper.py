import matplotlib.pyplot as plt

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

    plt.imshow(img, cmap="viridis", origin="upper")

    # Setting the current color map to HSV messes up other plots
    # plt.hsv()
    plt.colorbar()
    return fig


# TODO reintroduce
# from helpers import assert_equality
# def test():
#     assert_equality(plot, __file__[:-3] + "_reference.tex")
#     return
