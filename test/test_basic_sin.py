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
        A = plt.cm.jet(np.linspace(0, 1, 10))
        plt.plot(t, s, 'o-', lw=1.5, color=A[5])
        plt.plot(t, s2, 'o-', lw=3, alpha=0.3)
        plt.xlabel('time(s)')
        # plt.xlabel('time(s) _ % $ \\')
        plt.ylabel('Voltage (mV)')
        plt.title('Simple plot $\\frac{\\alpha}{2}$')
        plt.grid(True)
    return fig


def test():
    phash = helpers.Phash(plot())
    assert phash.phash == '1f36e5ce21c1e5c1', phash.get_details()


if __name__ == '__main__':
    helpers.compare_with_latex(plot())
