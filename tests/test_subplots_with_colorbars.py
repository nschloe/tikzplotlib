import pytest


def plot():
    import numpy as np
    from matplotlib import pyplot as plt

    data = np.zeros((3, 3))
    data[:2, :2] = 1.0

    fig = plt.figure()

    ax1 = plt.subplot(131)
    ax2 = plt.subplot(132)
    ax3 = plt.subplot(133)
    axes = [ax1, ax2, ax3]

    for ax in axes:
        im = ax.imshow(data)
        fig.colorbar(im, ax=ax, orientation="horizontal")

    return fig


# TODO reintroduce
@pytest.mark.skip("Fails?")
def test():
    from .helpers import assert_equality

    assert_equality(plot, __file__[:-3] + "_reference.tex")
