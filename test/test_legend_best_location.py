import matplotlib.pyplot as plt
import numpy as np

from helpers import assert_equality


def plot():
    fig, ax = plt.subplots(3, 3, sharex="col", sharey="row")
    axes = [ax[i][j] for i in range(len(ax)) for j in range(len(ax[i]))]
    t = np.arange(0.0, 2.0 * np.pi, 0.4)

    # Legend best location is "upper right"
    l, = axes[0].plot(t, np.cos(t) * np.exp(-t), linewidth=0.5)
    axes[0].legend((l,), ("UR",), loc=0)

    # Legend best location is "upper left"
    l, = axes[1].plot(t, np.cos(t) * np.exp(0.15 * t), linewidth=0.5)
    axes[1].legend((l,), ("UL",), loc=0)

    # Legend best location is "lower left"
    l, = axes[2].plot(t, np.cos(5.0 * t) + 1, linewidth=0.5)
    axes[2].legend((l,), ("LL",), loc=0)

    # Legend best location is "lower right"
    l, = axes[3].plot(
        t, 2 * np.cos(5.0 * t) * np.exp(-0.5 * t) + 0.2 * t, linewidth=0.5
    )
    axes[3].legend((l,), ("LR",), loc=0)

    # Legend best location is "center left"
    l, = axes[4].plot(t[30:], 2 * np.cos(10 * t[30:]), linewidth=0.5)
    axes[4].plot(t, -1.5 * np.ones_like(t), t, 1.5 * np.ones_like(t))
    axes[4].legend((l,), ("CL",), loc=0)

    # Legend best location is "center right"
    l, = axes[5].plot(t[:30], 2 * np.cos(10 * t[:30]), linewidth=0.5)
    axes[5].plot(t, -1.5 * np.ones_like(t), t, 1.5 * np.ones_like(t))
    axes[5].legend((l,), ("CR",), loc=0)

    # Legend best location is "lower center"
    l, = axes[6].plot(t, -3 * np.cos(t) * np.exp(-0.1 * t), linewidth=0.5)
    axes[6].legend((l,), ("LC",), loc=0)

    # Legend best location is "upper center"
    l, = axes[7].plot(t, 3 * np.cos(t) * np.exp(-0.1 * t), linewidth=0.5)
    axes[7].legend((l,), ("UC",), loc=0)

    # Legend best location is "center"
    loc = axes[8].plot(
        t[:10],
        2 * np.cos(10 * t[:10]),
        t[-10:],
        2 * np.cos(10 * t[-10:]),
        linewidth=0.5,
    )
    axes[8].plot(t, -2 * np.ones_like(t), t, 2 * np.ones_like(t))
    axes[8].legend((loc,), ("C",), loc=0)

    return fig


def test():
    assert_equality(plot, "test_legend_best_location_reference.tex")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_latex(plot)
    # helpers.print_tree(plot())
