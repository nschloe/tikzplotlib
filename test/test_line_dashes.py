import matplotlib.pyplot as plt

from helpers import assert_equality


def plot():
    fig = plt.figure()
    linestyles = ["-", "--", "-.", ":", (0, (10, 1)), (5, (10, 1)), (0, (1, 2, 3, 4))]
    for idx, ls in enumerate(linestyles):
        plt.plot([idx, idx + 1], linestyle=ls)
    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_latex(plot)
    # helpers.print_tree(plot())
