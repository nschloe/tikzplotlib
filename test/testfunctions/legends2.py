# -*- coding: utf-8 -*-
#
desc = 'Another legend plot'
phash = '5f31c1ceb43c2c72'


def plot():
    from matplotlib import pyplot as pp
    import numpy as np
    fig = pp.figure()

    t1 = np.arange(0.0, 2.0, 0.1)
    t2 = np.arange(0.0, 2.0, 0.01)

    # note that plot returns a list of lines.  The 'l1, = plot' usage
    # extracts the first element of the list inot l1 using tuple
    # unpacking.  So l1 is a Line2D instance, not a sequence of lines
    l1,    = pp.plot(t2, np.exp(-t2))
    l2, l3 = pp.plot(t2, np.sin(2*np.pi*t2), '--go', t1, np.log(1+t1), '.')
    l4,    = pp.plot(t2, np.exp(-t2)*np.sin(2*np.pi*t2), 'rs-.')

    pp.legend(
            (l2, l4),
            ('oscillatory', 'damped'),
            loc='upper right',
            shadow=True
            )
    pp.xlabel('time')
    pp.ylabel('volts')
    pp.title('Damped oscillation')
    return fig
