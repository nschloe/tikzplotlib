import matplotlib.pyplot as plt
import numpy as np


def plot():
    # Make plot with vertical (default) colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)

    np.random.seed(123)
    ax.hist(10 + 2 * np.random.randn(1000), label="men")
    ax.hist(12 + 3 * np.random.randn(1000), label="women", alpha=0.5)
    ax.legend()
    return fig


def test():
    from .helpers import assert_equality

    assert_equality(plot, "test_histogram_reference.tex")
