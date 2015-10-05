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
desc = '$4\\times 4$ subplots'
md5 = ''


def plot():
    from matplotlib import pyplot as pp
    import numpy as np

    an = np.linspace(0, 2*np.pi, 100)

    pp.subplot(221)
    pp.plot(3*np.cos(an), 3*np.sin(an))
    pp.title('not equal, looks like ellipse', fontsize=10)

    pp.subplot(222)
    pp.plot(3*np.cos(an), 3*np.sin(an))
    pp.axis('equal')
    pp.title('equal, looks like circle', fontsize=10)

    pp.subplot(223)
    pp.plot(3*np.cos(an), 3*np.sin(an))
    pp.axis('equal')
    pp.axis([-3, 3, -3, 3])
    pp.title('looks like circle, even after changing limits', fontsize=10)

    pp.subplot(224)
    pp.plot(3*np.cos(an), 3*np.sin(an))
    pp.axis('equal')
    pp.axis([-3, 3, -3, 3])
    pp.plot([0, 4], [0, 4])
    pp.title('still equal after adding line', fontsize=10)
    return
