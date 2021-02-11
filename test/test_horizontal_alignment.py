import numpy as np
import matplotlib.pyplot as plt

from helpers import assert_equality


def plot():
    labels = ["lab1", "label 2", "another super label"]
    n = len(labels)
    x = np.arange(n)
    y = 1 / (x + 1)

    ax = plt.gca()
    ax.bar(x, y, 0.5)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    plt.xticks(rotation=45, ha="right")


def test():
    assert_equality(plot, "test_horizontal_alignment_reference.tex")


if __name__ == "__main__":
    # import helpers
    # helpers.compare_mpl_tex(plot)
    plot()
    plt.show()
