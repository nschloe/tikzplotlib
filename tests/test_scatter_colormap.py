from helpers import assert_equality


def plot():
    import numpy as np
    from matplotlib import pyplot as plt

    fig = plt.figure()
    np.random.seed(123)
    plt.scatter(
        np.random.randn(10),
        np.random.randn(10),
        np.random.rand(10) * 90 + 10,
        np.random.randn(10),
    )
    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plot()
    plt.show()
