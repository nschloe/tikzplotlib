# -*- coding: utf-8 -*-
#
import os

import matplotlib.pyplot as plt
import numpy as np

import matplotlib2tikz as m2t


def plot():
    fig = plt.figure()
    with plt.style.context(("ggplot")):
        t = np.arange(0.0, 2.0, 0.1)
        s = np.sin(2 * np.pi * t)
        s2 = np.cos(2 * np.pi * t)
        A = plt.cm.jet(np.linspace(0, 1, 10))
        plt.plot(t, s, "o-", lw=1.5, color=A[5])
        plt.plot(t, s2, "o-", lw=3, alpha=0.3)
        plt.xlabel("time(s)")
        # plt.xlabel('time(s) _ % $ \\')
        plt.ylabel("Voltage (mV)")
        plt.title("Simple plot $\\frac{\\alpha}{2}$")
        plt.grid(True)
    return fig


def test():
    plot()
    code = m2t.get_tikz_code(include_disclaimer=False)
    print(code)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, "reference.tex"), "r") as f:
        reference = f.read()[:-1]
    assert reference == code
    return
