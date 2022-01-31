import matplotlib.pyplot as plt
import pandas as pd


def plot():
    fig = plt.figure(1, figsize=(8, 5))
    df = pd.DataFrame(index=["one", "two", "three"], data={"data": [1, 2, 3]})
    plt.plot(df, "o")
    return fig


def test():
    from .helpers import assert_equality

    assert_equality(plot, __file__[:-3] + "_reference.tex")


if __name__ == "__main__":
    plot()
    plt.show()
