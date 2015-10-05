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
desc = 'Loglog plot with large ticks dimensions'
sha = ''


def plot():
    from matplotlib import pyplot as pp
    import numpy as np

    x = np.logspace(0, 6, num=5)
    pp.loglog(x, x**2)
    return
