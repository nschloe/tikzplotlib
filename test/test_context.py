from helpers import assert_equality


def plot():
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
    import numpy as np

    x, y = np.meshgrid(np.linspace(0, 1), np.linspace(0, 1))
    z = x ** 2 - y ** 2

    fig = plt.figure()
    plt.pcolormesh(x, y, z, cmap=cm.viridis)

    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex", flavor="context")
    return
