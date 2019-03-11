# -*- coding: utf-8 -*-
#
import matplotlib.pyplot as plt
import numpy as np

import helpers


def plot():
    fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(8, 5))
    t = np.arange(0.0, 5.0, 0.1)
    s = np.cos(2 * np.pi * t)

    axes[0][0].plot(t, s, color="blue")
    axes[0][1].plot(t, s, color="red")
    axes[1][0].plot(t, s, color="green")
    axes[1][1].plot(t, s, color="black")
    return fig


def test():
    phash = helpers.Phash(plot())
    assert phash.phash == "ffed6c02bb944c02", phash.get_details()
    return


if __name__ == "__main__":
    plot()
    plt.show()
