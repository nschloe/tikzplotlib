import matplotlib.pyplot as plt
from helpers import assert_equality


def plot():
    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = [0, 1, 2, 3]
    y1 = [1, 2, 3, 4]
    y1std = [0.8, 0.5, 0.8, 0.3]
    y2 = [2, 2, 2, 2]
    y2std = [0.1, 0.2, 0.3, 0.2]

    ax.errorbar(x, y1, yerr=y1std, label='y1')
    ax.errorbar(x, y2, yerr=y2std, label='y2')
    ax.legend()
    return fig

def test():
    assert_equality(plot, "test_errorbar_label_reference.tex")

