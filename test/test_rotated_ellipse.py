# -*- coding: utf-8 -*-
#
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from helpers import assert_equality


def plot():
    fig = plt.figure()

    x = 1.0
    y = 1.0

    plt.plot(x, y, "ro")

    ellip = Ellipse(
        xy=[x, y], width=16.0, height=4.0, angle=-160, alpha=0.5, color="green"
    )
    ax = plt.gca()
    ax.add_artist(ellip)

    plt.xlim([-9, 10])
    plt.ylim([-3, 5])
    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_latex(plot)
    # helpers.print_tree(plot())
