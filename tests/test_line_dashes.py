import matplotlib.pyplot as plt


def plot():
    fig = plt.figure()
    linestyles = ["-", "--", "-.", ":", (0, (10, 1)), (5, (10, 1)), (0, (1, 2, 3, 4))]
    for idx, ls in enumerate(linestyles):
        plt.plot([idx, idx + 1], linestyle=ls)
    return fig


def test():
    from .helpers import assert_equality

    assert_equality(plot, __file__[:-3] + "_reference.tex")
