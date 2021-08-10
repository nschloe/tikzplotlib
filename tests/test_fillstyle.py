import matplotlib.pyplot as plt
import numpy as np


def plot():
    fig = plt.figure()

    N = 10
    t = np.linspace(0, 1, N)
    x = np.arange(N)
    plt.plot(t, x, "-o", fillstyle="none")
    plt.tight_layout()
    return fig


def test():
    from .helpers import assert_equality

    assert_equality(plot, "test_fillstyle_reference.tex")
