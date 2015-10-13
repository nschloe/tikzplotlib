# -*- coding: utf-8 -*-
#
desc = 'Two subplots on top of each other'
phash = '1f61d562e19d2666'


def plot():
    from matplotlib import pyplot as pp
    import numpy as np

    def f(t):
        s1 = np.cos(2*np.pi*t)
        e1 = np.exp(-t)
        return np.multiply(s1, e1)

    fig = pp.figure()

    t1 = np.arange(0.0, 5.0, 0.1)
    t2 = np.arange(0.0, 5.0, 0.02)
    t3 = np.arange(0.0, 2.0, 0.01)

    pp.subplot(211)
    pp.plot(t1, f(t1), 'bo', t2, f(t2), 'k--', markerfacecolor='green')
    pp.grid(True)
    pp.title('A tale of 2 subplots')
    pp.ylabel('Damped oscillation')

    pp.subplot(212)
    pp.plot(t3, np.cos(2*np.pi*t3), 'r.')
    pp.grid(True)
    pp.xlabel('time (s)')
    pp.ylabel('Undamped')

    return fig
