# -*- coding: utf-8 -*-
#
desc = 'Two subplots on top of each other'
phash = '5f61d562619d2666'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    def f(t):
        s1 = np.cos(2*np.pi*t)
        e1 = np.exp(-t)
        return np.multiply(s1, e1)

    fig = plt.figure()

    t1 = np.arange(0.0, 5.0, 0.1)
    t2 = np.arange(0.0, 5.0, 0.02)
    t3 = np.arange(0.0, 2.0, 0.01)

    plt.subplot(211)
    plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k--', markerfacecolor='green')
    plt.grid(True)
    plt.title('A tale of 2 subplots')
    plt.ylabel('Damped oscillation')

    plt.subplot(212)
    plt.plot(t3, np.cos(2*np.pi*t3), 'r.')
    plt.grid(True)
    plt.xlabel('time (s)')
    plt.ylabel('Undamped')

    fig.suptitle('PLOT TITLE', fontsize=18, fontweight='bold')

    return fig
