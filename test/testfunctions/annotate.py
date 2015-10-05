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
desc = 'Annotations'
md5 = '49389526476d0a45cdb71bb2fc3a2b32'


def plot():
    from matplotlib import pyplot as pp
    import numpy as np

    fig = pp.figure(1, figsize=(8, 5))
    ax = fig.add_subplot(
            111,
            autoscale_on=False,
            xlim=(-1, 5),
            ylim=(-4, 3)
            )
    t = np.arange(0.0, 5.0, 0.01)
    s = np.cos(2*np.pi*t)
    line, = ax.plot(t, s, color='blue')
    ax.annotate(
            'text',
            xy=(4., 1.),
            xycoords='data',
            xytext=(4.5, 1.5),
            textcoords='data',
            arrowprops=dict(arrowstyle='->', ec='r')
            )
    ax.annotate(
            'arrowstyle',
            xy=(0, 1),
            xycoords='data',
            xytext=(-50, 30),
            textcoords='offset points',
            arrowprops=dict(arrowstyle='->')
            )
    return
