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
desc = 'Two subplots on top of each other'
phash = '559e2bd19f629191'


def plot():
    from matplotlib import pyplot as pp
    import numpy as np

    def f(t):
        s1 = np.cos(2*np.pi*t)
        e1 = np.exp(-t)
        return np.multiply(s1, e1)

    fig = pp.figure()

    t1 = np.arange(0.0, 5.0, 0.1)
    t2 = np.arange(0.0, 5.0, 0.02)
    t3 = np.arange(0.0, 2.0, 0.01)

    pp.subplot(211)
    pp.plot(t1, f(t1), 'bo', t2, f(t2), 'k--', markerfacecolor='green')
    pp.grid(True)
    pp.title('A tale of 2 subplots')
    pp.ylabel('Damped oscillation')

    pp.subplot(212)
    pp.plot(t3, np.cos(2*np.pi*t3), 'r.')
    pp.grid(True)
    pp.xlabel('time (s)')
    pp.ylabel('Undamped')

    return fig
