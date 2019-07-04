import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import multivariate_normal

from helpers import assert_equality


def plot():
    mean = np.array([1, 1])
    cov = np.eye(2)
    nbins = 5

    fig = plt.figure()
    ax = plt.gca()

    x_max = 2
    x_min = 0
    y_max = 2
    y_min = 0

    xi, yi = np.mgrid[x_min : x_max : nbins * 1j, y_min : y_max : nbins * 1j]
    pos = np.empty(xi.shape + (2,))
    pos[:, :, 0] = xi
    pos[:, :, 1] = yi
    zi = multivariate_normal(mean, cov, allow_singular=True, seed=0).pdf(pos)
    ax.contourf(xi, yi, zi, 250)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_latex(plot)
    # helpers.print_tree(plot())
