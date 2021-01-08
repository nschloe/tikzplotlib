from helpers import assert_equality


def plot():
    import numpy as np
    from matplotlib import pyplot as plt

    fig = plt.figure()
    with plt.style.context("fivethirtyeight"):
        np.random.seed(123)
        plt.scatter(
            np.linspace(0, 100, 101),
            np.linspace(0, 100, 101) + 15 * np.random.rand(101),
        )
    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_tex(plot)
    # helpers.print_tree(plot())
