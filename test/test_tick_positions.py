from helpers import assert_equality


def plot():
    from matplotlib import pyplot as plt

    x = [1, 2, 3, 4]
    y = [1, 4, 9, 6]

    fig = plt.figure()

    ax = plt.subplot(4, 4, 1)
    plt.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="off", top="off")
    plt.tick_params(axis="y", which="both", left="off", right="off")

    ax = plt.subplot(4, 4, 2)
    plt.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="off", top="off")
    plt.tick_params(axis="y", which="both", left="off", right="on")

    ax = plt.subplot(4, 4, 3)
    plt.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="off", top="off")
    plt.tick_params(axis="y", which="both", left="on", right="off")

    ax = plt.subplot(4, 4, 4)
    ax.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="off", top="off")
    plt.tick_params(axis="y", which="both", left="on", right="on")

    ax = plt.subplot(4, 4, 5)
    ax.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="off", top="on")
    plt.tick_params(axis="y", which="both", left="off", right="off")

    ax = plt.subplot(4, 4, 6)
    plt.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="off", top="on")
    plt.tick_params(axis="y", which="both", left="off", right="on")

    ax = plt.subplot(4, 4, 7)
    plt.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="off", top="on")
    plt.tick_params(axis="y", which="both", left="on", right="off")

    ax = plt.subplot(4, 4, 8)
    ax.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="off", top="on")
    plt.tick_params(axis="y", which="both", left="on", right="on")

    ax = plt.subplot(4, 4, 9)
    ax.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="on", top="off")
    plt.tick_params(axis="y", which="both", left="off", right="off")

    ax = plt.subplot(4, 4, 10)
    plt.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="on", top="off")
    plt.tick_params(axis="y", which="both", left="off", right="on")

    ax = plt.subplot(4, 4, 11)
    plt.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="on", top="off")
    plt.tick_params(axis="y", which="both", left="on", right="off")

    ax = plt.subplot(4, 4, 12)
    ax.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="on", top="off")
    plt.tick_params(axis="y", which="both", left="on", right="on")

    ax = plt.subplot(4, 4, 13)
    ax.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="on", top="on")
    plt.tick_params(axis="y", which="both", left="off", right="off")

    ax = plt.subplot(4, 4, 14)
    ax.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="on", top="on")
    plt.tick_params(axis="y", which="both", left="off", right="on")

    ax = plt.subplot(4, 4, 15)
    ax.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="on", top="on")
    plt.tick_params(axis="y", which="both", left="on", right="off")

    ax = plt.subplot(4, 4, 16)
    ax.plot(x, y, "ro")
    plt.tick_params(axis="x", which="both", bottom="on", top="on")
    plt.tick_params(axis="y", which="both", left="on", right="on")

    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return
