import matplotlib.pyplot as plt
import numpy as np

from helpers import assert_equality


def plot():
    # Make plot with vertical (default) colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)

    np.random.seed(123)
    data = np.clip(np.random.randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation="nearest")
    ax.set_title("Gaussian noise with vertical colorbar")

    # Add colorbar, make sure to specify tick locations
    # to match desired ticklabels.
    cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
    # vertically oriented colorbar
    cbar.ax.set_yticklabels(["< -1", "0", "> 1"])
    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return
