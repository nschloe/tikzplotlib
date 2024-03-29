import matplotlib.pyplot as plt


# https://github.com/nschloe/tikzplotlib/issues/414
def plot():
    _, ax = plt.subplots()
    ax.scatter(
        [1, 2, 3],
        [5, 7, 1],
        s=[300, 300, 300],
        facecolors="none",
        edgecolors="black",
        linewidths=3.0,
    )


def test():
    from .helpers import assert_equality

    assert_equality(plot, __file__[:-3] + "_reference.tex")
