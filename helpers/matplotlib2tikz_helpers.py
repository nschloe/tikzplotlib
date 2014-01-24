# -*- coding: utf-8 -*-
#
# Copyright (C) 2010--2014 Nico Schlömer
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


def print_tree(obj, indent=''):
    '''Recursively prints the tree structure of the matplotlib object.
    '''
    print indent, type(obj)
    for child in obj.get_children():
            print_tree(child, indent + '   ')
    return
