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
desc = 'An \\texttt{imshow} plot'
phash = '0b4bfc01f40bfc4b'


def plot():
    from matplotlib import rcParams
    from matplotlib import pyplot as pp
    import os
    try:
        import Image
    except ImportError:
        raise RuntimeError('PIL must be installed to run this example')

    this_dir = os.path.dirname(os.path.realpath(__file__))
    lena = Image.open(os.path.join(this_dir, 'lena.png'))
    dpi = rcParams['figure.dpi']
    figsize = lena.size[0]/dpi, lena.size[1]/dpi
    fig = pp.figure(figsize=figsize)
    ax = pp.axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()
    pp.imshow(lena, origin='lower')
    # Set the current color map to HSV.
    pp.hsv()
    pp.colorbar()
    return fig
