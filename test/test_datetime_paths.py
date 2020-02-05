import datetime as date

import matplotlib.pyplot as plt
from matplotlib import dates

from helpers import assert_equality


def plot():
    fig = plt.figure()

    times = [date.datetime(2020, 1, 1, 12, 00), date.datetime(2020, 1, 2, 12, 00)]
    line = [2, 2]
    upper = [3, 4]
    lower = [1, 0]

    plt.plot(times, line)
    plt.fill_between(times, lower, upper)
    ax = plt.gca()
    ax.fmt_xdata = dates.DateFormatter("%d %b %Y %H:%M:%S")

    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_tex(plot)
