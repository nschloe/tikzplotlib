# -*- coding: utf-8 -*-
#
desc = 'Simple $\sin$ plot with some labels'
phash = '5f34a7ce21ce2196'


def plot():
    from matplotlib import pyplot as pp
    from matplotlib import style
    import numpy as np
    fig = pp.figure()
    style.use('ggplot')
    t = np.arange(0.0, 2.0, 0.1)
    s = np.sin(2*np.pi*t)
    s2 = np.cos(2*np.pi*t)
    pp.plot(t, s, 'o-', lw=4.1)
    pp.plot(t, s2, 'o-', lw=4.1)
    pp.xlabel('time(s)')
    # pp.xlabel('time(s) _ % $ \\')
    pp.ylabel('Voltage (mV)')
    pp.title('Easier than easy $\\frac{1}{2}$')
    pp.grid(True)
    return fig
