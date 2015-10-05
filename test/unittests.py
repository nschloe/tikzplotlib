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
import os
import tempfile
from importlib import import_module
import hashlib

import matplotlib2tikz
import testfunctions


def test_generator():
    for name in testfunctions.__all__:
        print(name)
        test = import_module('testfunctions.' + name)
        yield check_md5, test


def check_md5(test):
    # import the test
    test.plot()
    # convert to tikz file
    handle, filename = tempfile.mkstemp()
    # convert to tikz
    matplotlib2tikz.save(
        filename,
        figurewidth='7.5cm',
        show_info=False
        )
    # compute hash
    print(filename)
    with open(filename, 'rb') as f:
        sha = hashlib.sha1(f.read()).hexdigest()
    print(sha)
    assert test.sha == sha
