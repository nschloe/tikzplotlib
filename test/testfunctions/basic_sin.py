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
desc = 'Simple $\sin$ plot with some labels'
phash = 'f7300fcc3332c52e'


def plot():
    from matplotlib import pyplot as pp
    from matplotlib import style
    import numpy as np
    style.use('ggplot')
    t = np.arange(0.0, 2.0, 0.1)
    s = np.sin(2*np.pi*t)
    s2 = np.cos(2*np.pi*t)
    pp.plot(t, s, 'o-', lw=4.1)
    pp.plot(t, s2, 'o-', lw=4.1)
    pp.xlabel('time(s)')
    # pp.xlabel('time(s) _ % $ \\')
    pp.ylabel('Voltage (mV)')
    pp.title('Easier than easy $\\frac{1}{2}$')
    pp.grid(True)
    return
