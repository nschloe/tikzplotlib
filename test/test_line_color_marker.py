# -*- coding: utf-8 -*-
#
import helpers


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig = plt.figure()
    with plt.style.context(('ggplot')):
        t = np.arange(0.0, 2.0, 0.1)
        s = np.sin(2*np.pi*t)
        s2 = np.cos(2*np.pi*t)
        plt.plot(t, s, '.-', lw=1.5, color='C0')
        plt.plot(t, s2, '^-', lw=3, color='C1')
        plt.xlabel('time(s)')
        # plt.xlabel('time(s) _ % $ \\')
        plt.ylabel('Voltage (mV)')
        plt.title('Simple plot $\\frac{\\alpha}{2}$')
        plt.grid(True)
    return fig


def test():
    phash = helpers.Phash(plot())
    print('phash', phash.phash)
    assert phash.phash == '1fb4f1ce2141e7c1', phash.get_details()


if __name__ == '__main__':
    helpers.compare_with_latex(plot())
