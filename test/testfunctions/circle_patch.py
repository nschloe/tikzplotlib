# -*- coding: utf-8 -*-
#
desc = 'A circle path'
phash = 'fda9095a93b22366'


def plot():
    from matplotlib import pyplot as pp
    from matplotlib.patches import Circle
    fig = pp.figure()
    ax = fig.add_subplot(111)
    ax.add_patch(Circle((0, 0), 1))
    return fig
