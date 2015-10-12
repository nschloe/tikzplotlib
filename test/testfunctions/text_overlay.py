# -*- coding: utf-8 -*-
#
desc = 'Regular plot with overlay text'
phash = 'b74b937449936c0b'


def plot():
    from matplotlib import pyplot as pp
    import numpy as np

    fig = pp.figure()

    xxx = np.linspace(0, 5)
    yyy = xxx**2
    pp.text(1, 5, 'test1', size=50, rotation=30.,
            ha='center', va='bottom', color='r', style='italic',
            bbox=dict(boxstyle='round, pad=0.2',
                      ec=(1., 0.5, 0.5),
                      fc=(1., 0.8, 0.8),
                      ls='dashdot'
                      )
            )
    pp.text(3, 6, 'test2', size=50, rotation=-30.,
            ha='center', va='center', color='b', weight='bold',
            bbox=dict(boxstyle='square',
                      ec=(1., 0.5, 0.5),
                      fc=(1., 0.8, 0.8),
                      )
            )
    pp.plot(xxx, yyy, label='a graph')
    pp.legend()

    return fig
