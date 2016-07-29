# -*- coding: utf-8 -*-
#
desc = 'Another legend plot'
phash = '5731c1ce31b46c7a'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np
    fig = plt.figure()

    t1 = np.arange(0.0, 2.0, 0.1)
    t2 = np.arange(0.0, 2.0, 0.01)

    # note that plot returns a list of lines.  The 'l1, = plot' usage
    # extracts the first element of the list inot l1 using tuple
    # unpacking.  So l1 is a Line2D instance, not a sequence of lines
    l1,    = plt.plot(t2, np.exp(-t2), linewidth=0.5)
    l2, l3 = plt.plot(t2, np.sin(2*np.pi*t2), '--go', t1, np.log(1+t1), '.')
    l4,    = plt.plot(t2, np.exp(-t2)*np.sin(2*np.pi*t2), 'rs-.')

    leg1 = plt.legend(
            (l2, l4),
            ('oscillatory', 'damped'),
            loc='upper right',
            shadow=True
            )
    plt.gca().add_artist(leg1)

    for loc in range(2, 11):
        leg = plt.legend((l1,), ('loc %d' % loc,), loc=loc)
        leg.get_frame().set_facecolor('#00FFCC')
        leg.get_frame().set_edgecolor('#0000FF')
        plt.gca().add_artist(leg)

    plt.xlabel('time')
    plt.ylabel('volts')
    plt.title('Damped oscillation')
    return fig
