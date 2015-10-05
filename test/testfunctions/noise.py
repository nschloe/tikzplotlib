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
desc = 'Noise with a color bar'
sha = ''


def plot():
    from numpy.random import randn
    from matplotlib import pyplot as pp
    import numpy as np

    # Make plot with vertical (default) colorbar
    fig = pp.figure()
    ax = fig.add_subplot(111)

    data = np.clip(randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation='nearest')
    ax.set_title('Gaussian noise with vertical colorbar')

    # Add colorbar, make sure to specify tick locations
    # to match desired ticklabels.
    cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
    # vertically oriented colorbar
    cbar.ax.set_yticklabels(['< -1', '0', '> 1'])

    # Make plot with horizontal colorbar
    fig = pp.figure()
    ax = fig.add_subplot(111)

    data = np.clip(np.random.randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation='nearest')
    ax.set_title('Gaussian noise with horizontal colorbar')

    cbar = fig.colorbar(cax, ticks=[-1, 0, 1], orientation='horizontal')
    # horizontal colorbar
    cbar.ax.set_xticklabels(['Low', 'Medium', 'High'])
    return
