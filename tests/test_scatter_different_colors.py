import matplotlib.pyplot as plt
import numpy as np

from .helpers import assert_equality


def plot():
    fig = plt.figure()
    np.random.seed(123)
    n = 4
    plt.scatter(
        np.random.rand(n),
        np.random.rand(n),
        color=np.array(
            [
                [1.0, 0.6, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.0, 1.0, 1.0],
            ]
        ),
        edgecolors=np.array(
            [
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.0, 1.0, 1.0],
                [1.0, 0.0, 0.0],
            ]
        ),
    )
    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
