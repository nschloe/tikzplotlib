# -*- coding: utf-8 -*-
#
desc = 'Simple $\sin$ plot with some labels'
phash = '5f34a1cea1caa1d9'


def plot():
    from matplotlib import pyplot as plt
    from matplotlib import style
    import numpy as np
    fig = plt.figure()
    with plt.style.context(('ggplot')):
        t = np.arange(0.0, 2.0, 0.1)
        s = np.sin(2*np.pi*t)
        s2 = np.cos(2*np.pi*t)
        plt.plot(t, s, 'o-', lw=4.1)
        plt.plot(t, s2, 'o-', lw=4.1)
        plt.xlabel('time(s)')
        # plt.xlabel('time(s) _ % $ \\')
        plt.ylabel('Voltage (mV)')
        plt.title('Simple plot $\\frac{\\alpha}{2}$')
        plt.grid(True)
    return fig
