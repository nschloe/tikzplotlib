from helpers import assert_equality


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    def f(t):
        s1 = np.cos(2 * np.pi * t)
        e1 = np.exp(-t)
        return np.multiply(s1, e1)

    fig = plt.figure()

    t1 = np.arange(0.0, 5.0, 0.4)
    t2 = np.arange(0.0, 5.0, 0.1)
    t3 = np.arange(0.0, 2.0, 0.1)

    plt.subplot(211)
    plt.plot(t1, f(t1), "bo", t2, f(t2), "k--", markerfacecolor="green")
    plt.grid(True)
    plt.title("A tale of 2 subplots")
    plt.ylabel("Damped oscillation")

    plt.subplot(212)
    plt.plot(t3, np.cos(2 * np.pi * t3), "r.")
    plt.grid(True)
    plt.xlabel("time (s)")
    plt.ylabel("Undamped")

    fig.suptitle("PLOT TITLE", fontsize=18, fontweight="bold")

    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return
