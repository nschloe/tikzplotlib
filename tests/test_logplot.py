import matplotlib.pyplot as plt


def plot():
    a = [pow(10, i) for i in range(10)]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.semilogy(a, color="blue", lw=0.25)

    plt.grid(visible=True, which="major", color="g", linestyle="-")
    plt.grid(visible=True, which="minor", color="r", linestyle="-")
    return fig


def test():
    from .helpers import assert_equality

    assert_equality(plot, __file__[:-3] + "_reference.tex")
