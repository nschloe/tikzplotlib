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
desc = 'Another legend plot'
sha = ''


def plot():
    from matplotlib import pyplot as pp
    import numpy as np
    t1 = np.arange(0.0, 2.0, 0.1)
    t2 = np.arange(0.0, 2.0, 0.01)

    # note that plot returns a list of lines.  The 'l1, = plot' usage
    # extracts the first element of the list inot l1 using tuple
    # unpacking.  So l1 is a Line2D instance, not a sequence of lines
    l1,    = pp.plot(t2, np.exp(-t2))
    l2, l3 = pp.plot(t2, np.sin(2*np.pi*t2), '--go', t1, np.log(1+t1), '.')
    l4,    = pp.plot(t2, np.exp(-t2)*np.sin(2*np.pi*t2), 'rs-.')

    pp.legend(
            (l2, l4),
            ('oscillatory', 'damped'),
            loc='upper right',
            shadow=True
            )
    pp.xlabel('time')
    pp.ylabel('volts')
    pp.title('Damped oscillation')
    return
