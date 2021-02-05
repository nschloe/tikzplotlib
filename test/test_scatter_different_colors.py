from helpers import assert_equality


def plot():
    import numpy as np
    from matplotlib import pyplot as plt

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


if __name__ == "__main__":
    # import helpers
    # helpers.compare_mpl_tex(plot)
    # helpers.print_tree(plot())
    plot()
    import matplotlib.pyplot as plt

    # plt.show()
    # plt.savefig('out.pgf')
    import tikzplotlib

    tikzplotlib.save("out.tex", standalone=True)
