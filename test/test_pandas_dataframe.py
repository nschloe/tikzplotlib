import matplotlib.pyplot as plt
import pandas as pd

from helpers import assert_equality


def plot():
    fig = plt.figure(1, figsize=(8, 5))
    df = pd.DataFrame(index=["one", "two", "three"], data={"data": [1, 2, 3]})
    plt.plot(df, "o")
    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_latex(plot)
    # helpers.print_tree(plot())
