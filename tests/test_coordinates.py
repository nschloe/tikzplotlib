def plot():
    from matplotlib import pyplot as plt

    fig = plt.figure()
    plt.plot([1, 2, 3], [4, -2, 3])
    ax = plt.gca()
    ax._tikzplotlib_anchors = [((1.5, 2.5), "foo")]
    return fig


def test():
    from .helpers import assert_equality

    assert_equality(plot, __file__[:-3] + "_reference.tex")
