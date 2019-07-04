import datetime as date

import matplotlib.pyplot as plt
from matplotlib import dates

from helpers import assert_equality


def plot():
    fig = plt.figure()

    values = [50, 50.02]
    time = [date.datetime(2016, 10, 10, 18, 00), date.datetime(2016, 10, 10, 18, 15)]
    plt.plot(time, values)
    hfmt = dates.DateFormatter("%H:%M")
    ax = plt.gca()
    ax.xaxis.set_major_formatter(hfmt)
    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_latex(plot)
    # helpers.print_tree(plot())
