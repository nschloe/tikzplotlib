import matplotlib.pyplot as plt
import numpy as np


def plot():
    plt.figure()
    x = np.arange(5)
    y1 = np.array([1, 2, 1, 4, 2])
    y2 = np.array([1, 2, 1, 4, 2])
    y3 = np.array([1, 2, 1, 4, 2])
    y4 = np.array([1, 2, 1, 4, 2])
    y5 = np.array([2, 3, 2, 5, 3])

    plt.step(x, y1, "r-")
    plt.step(x, y2, "b--", where="pre")
    plt.step(x, y3, "g-.", where="post")
    plt.step(x, y4, "y:", where="mid")
    plt.plot(x, y5, "c.",)
    plt.legend(["default", "pre", "post", "mid", "default"])

    return plt.gcf()


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_latex(plot)
