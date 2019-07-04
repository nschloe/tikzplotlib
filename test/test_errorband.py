import matplotlib.pyplot as plt
import numpy as np

from helpers import assert_equality


def plot():
    fig, ax = plt.subplots()
    with plt.style.context(("ggplot")):
        t = np.linspace(0, 2 * np.pi, 11)
        s = np.sin(t)
        ax.plot(t, s, "k-")
        ax.fill_between(t, s + 0.1, s - 0.1, facecolor="k", alpha=0.2)
        ax.set_xlim(t[0], t[-1])
        ax.set_xlabel("t")
        ax.set_ylabel("sin(t)")
        ax.set_title("Simple plot")
        ax.grid(True)
    return fig


def test():
    assert_equality(plot, "test_errorband_reference.tex")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_latex(plot)
    # helpers.print_tree(plot())
