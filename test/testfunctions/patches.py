# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Nico Schlömer
#
# This file is part of matplotlib2tikz.
#
# matplotlib2tikz is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# matplotlib2tikz is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# matplotlib2tikz.  If not, see <http://www.gnu.org/licenses/>.
#
desc = 'Some patches and a color bar'
sha = ''


def plot():
    from matplotlib.patches import Circle, Wedge, Polygon
    from matplotlib.collections import PatchCollection
    from matplotlib import pyplot as pp
    import numpy as np
    import matplotlib as mpl

    fig = pp.figure()
    ax = fig.add_subplot(111)

    N = 3
    x = np.random.rand(N)
    y = np.random.rand(N)
    radii = 0.1*np.random.rand(N)
    patches = []
    for x1, y1, r in zip(x, y, radii):
        circle = Circle((x1, y1), r)
        patches.append(circle)

    x = np.random.rand(N)
    y = np.random.rand(N)
    radii = 0.1*np.random.rand(N)
    theta1 = 360.0*np.random.rand(N)
    theta2 = 360.0*np.random.rand(N)
    for x1, y1, r, t1, t2 in zip(x, y, radii, theta1, theta2):
        wedge = Wedge((x1, y1), r, t1, t2)
        patches.append(wedge)

    # Some limiting conditions on Wedge
    patches += [
        Wedge((0.3, 0.7), .1, 0, 360),  # Full circle
        Wedge((0.7, 0.8), .2, 0, 360, width=0.05),  # Full ring
        Wedge((0.8, 0.3), .2, 0, 45),  # Full sector
        Wedge((0.8, 0.3), .2, 45, 90, width=0.10),  # Ring sector
        ]

    for i in range(N):
        polygon = Polygon(np.random.rand(N, 2), True)
        patches.append(polygon)

    colors = 100*np.random.rand(len(patches))
    p = PatchCollection(patches,
                        cmap=mpl.cm.jet,
                        alpha=0.4
                        )
    p.set_array(np.array(colors))
    ax.add_collection(p)
    pp.colorbar(p)

    return fig
