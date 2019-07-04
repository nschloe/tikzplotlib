import matplotlib.pyplot as plt
import numpy as np

from helpers import assert_equality


def plot():
    da = np.zeros((3, 3))
    da[:2, :2] = 1.0

    fig = plt.figure()
    ax = plt.gca()

    im = ax.imshow(da, cmap="viridis")
    plt.colorbar(im, aspect=5, shrink=0.5)
    return fig


def test():
    assert_equality(plot, "test_fancy_colorbar_reference.tex")
    return
