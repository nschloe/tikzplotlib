# -*- coding: utf-8 -*-
#
desc = 'Multiple legend positions'
# phash = 'd558f444f0542bbb'
phash = '55d454d47ed4892b'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(3, 3,  sharex='col', sharey='row')
    axes = [ax[i][j] for i in range(len(ax)) for j in range(len(ax[i]))]
    for k, loc in enumerate(range(2, 11)):
        t1 = np.arange(0.0, 2.0, 0.1)
        t2 = np.arange(0.0, 2.0, 0.1)

        # note that plot returns a list of lines.  The 'l1, = plot' usage
        # extracts the first element of the list inot l1 using tuple unpacking.
        # So l1 is a Line2D instance, not a sequence of lines
        l1, = axes[k].plot(
            t2, np.exp(-t2), linewidth=0.5
            )
        l2, l3 = axes[k].plot(
            t2, np.sin(2*np.pi*t2), '--go', t1, np.log(1+t1), '.'
            )
        l4, = axes[k].plot(
            t2, np.exp(-t2)*np.sin(2*np.pi*t2), 'rs-.'
            )

        axes[k].legend((l1,), ('loc %d' % loc,), loc=loc)
    return fig
