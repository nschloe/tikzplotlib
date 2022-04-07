# https://github.com/nschloe/tikzplotlib/issues/332
import matplotlib.pyplot as plt


def plot():
    fig = plt.figure()
    plt.plot(0, 0, "kx", label="Foo & Bar Dogs_N_Cats")
    plt.title("Foo & Bar Dogs_N_Cats")
    plt.xlabel("Foo & Bar Dogs_N_Cats")
    plt.ylabel("Foo & Bar Dogs_N_Cats")
    plt.gca().legend()
    return fig


def test():
    from .helpers import assert_equality

    assert_equality(plot, "test_escape_chars_reference.tex")
