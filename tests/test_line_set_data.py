# from <https://github.com/nschloe/tikzplotlib/issues/339>
import matplotlib.pyplot as plt
from helpers import assert_equality


def plot():
    fig = plt.figure()
    line = plt.plot(0, 0, "kx")[0]
    line.set_data(0, 0)
    return fig


def test():
    assert_equality(plot, "test_line_set_data_reference.tex")
    return
