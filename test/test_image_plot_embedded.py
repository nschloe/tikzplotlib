import matplotlib.pyplot as plt
import numpy as np

from helpers import assert_equality


def plot():
    fig = plt.figure()
    ax = plt.axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()

    # a small dummy matrix as image

    img = np.array(
        [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 1, 1, 1],
        ]
    )

    plot_image = plt.imshow(img, cmap="viridis")

    # one more line of test coverage
    plot_image.set_extent(np.array(plot_image.get_extent()))

    return fig


def test():
    assert_equality(
        plot, "test_image_plot_embedded.tex", flavor="lualatex", embed_images=True
    )
    return
