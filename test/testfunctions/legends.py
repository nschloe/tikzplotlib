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
desc = 'Plot with legends'
phash = 'dd8907766666252d'


def plot():
    from matplotlib import pyplot as pp
    import numpy as np

    fig = pp.figure()

    x = np.ma.arange(0, 2*np.pi, 0.02)
    y = np.ma.sin(x)
    y1 = np.sin(2*x)
    y2 = np.sin(3*x)
    ym1 = np.ma.masked_where(y1 > 0.5, y1)
    ym2 = np.ma.masked_where(y2 < -0.5, y2)

    lines = pp.plot(x, y, 'r', x, ym1, 'g', x, ym2, 'bo')
    pp.setp(lines[0], linewidth=4)
    pp.setp(lines[1], linewidth=2)
    pp.setp(lines[2], markersize=10)

    pp.legend(('No mask', 'Masked if > 0.5', 'Masked if < -0.5'),
              loc='upper right'
              )
    pp.title('Masked line demo')
    return fig
