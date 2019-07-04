from helpers import assert_equality


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

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
    return
