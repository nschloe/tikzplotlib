import matplotlib.pyplot as plt
import numpy as np

from helpers import assert_equality


def plot():
    fig = plt.figure()
    np.random.seed(123)
    s = np.random.normal(0, 1, 10)
    plt.gca().set_ylim(-1.0, +1.0)
    plt.hist(s, 30)
    plt.axvline(1.96)
    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_latex(plot)
    # helpers.print_tree(plot())
