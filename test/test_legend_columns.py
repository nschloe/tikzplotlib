from helpers import assert_equality


def plot():
    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(17, 6))
    ax.plot(np.array([1, 5]), label="Test 1")
    ax.plot(np.array([5, 1]), label="Test 2")
    ax.legend(ncol=2, loc="upper center")
    return fig


def test():
    assert_equality(plot, "test_legend_columns_reference.tex")
    return
