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
desc = 'Regular plot with overlay text'
phash = '5db46c09f46c8bf0'


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
