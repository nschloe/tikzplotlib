import matplotlib.pyplot as plt
import numpy as np

from helpers import assert_equality


def plot():
    fig = plt.figure()
    with plt.style.context(("ggplot")):
        t = np.arange(0.0, 2.0, 0.1)
        s = np.sin(2 * np.pi * t)
        s2 = np.cos(2 * np.pi * t)
        A = plt.cm.jet(np.linspace(0, 1, 10))
        plt.plot(t, s, "o-", lw=1.5, color=A[5], label="sin")
        plt.plot(t, s2, "o-", lw=3, alpha=0.3, label="cos")
        plt.xlabel("time(s)")
        # plt.xlabel('time(s) _ % $ \\')
        plt.ylabel("Voltage (mV)")
        plt.title("Simple plot $\\frac{\\alpha}{2}$")
        plt.legend()
        plt.grid(True)
    return fig


def test():
    assert_equality(plot, "test_basic_sin_reference.tex", table_row_sep="\\\\\n")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_latex(plot)
    # helpers.print_tree(plot())
