from helpers import assert_equality


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()

    x = np.ma.arange(0, 2 * np.pi, 0.4)
    y1 = np.sin(1 * x)
    y2 = np.sin(2 * x)
    y3 = np.sin(3 * x)

    plt.plot(x, y1, label="y1")
    plt.plot(x, y2, label=None)
    plt.plot(x, y3, label="y4")
    plt.legend()

    return fig


def test():
    assert_equality(plot, "test_legend_labels_reference.tex")
    return
