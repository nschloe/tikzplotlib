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
import subprocess
from PIL import Image
import imagehash

import matplotlib2tikz
import testfunctions


def test_generator():
    for name in testfunctions.__all__:
        print(name)
        test = import_module('testfunctions.' + name)
        yield check_hash, test, name


def check_hash(test, name):
    # import the test
    test.plot()
    # convert to tikz file
    handle, tmp_base = tempfile.mkstemp(prefix=name)
    tikz_file = tmp_base + '_tikz.tex'
    matplotlib2tikz.save(
        tikz_file,
        figurewidth='7.5cm',
        show_info=False
        )
    # create a latex wrapper for the tikz
    wrapper = '''\\documentclass{standalone}
\\usepackage{pgfplots}
\\usepgfplotslibrary{groupplots}
\\pgfplotsset{compat=newest}
\\begin{document}
\\input{%s}
\\end{document}''' % tikz_file
    tex_file = tmp_base + '.tex'
    with open(tex_file, 'w') as f:
        f.write(wrapper)

    # change into the directory of the TeX file
    os.chdir(os.path.dirname(tex_file))

    # compile the output to pdf
    FNULL = open(os.devnull, 'w')
    subprocess.check_call(
        # use pdflatex for now until travis features a more modern lualatex
        ['pdflatex', '--interaction=nonstopmode', tex_file],
        stdout=FNULL,
        stderr=subprocess.STDOUT
        )
    pdf_file = tmp_base + '.pdf'

    # Convert PDF to PNG.
    png_file = tmp_base + '-1.png'
    subprocess.check_call(
        ['pdftoppm', '-rx', '600', '-ry', '600', '-png', pdf_file, tmp_base],
        stdout=FNULL,
        stderr=subprocess.STDOUT
        )

    # compute the phash of the PNG
    phash = imagehash.phash(Image.open(png_file)).__str__()

    if test.phash != phash:
        # Compute the Hamming distance between the two 64-bit numbers
        hamming_dist = bin(int(phash, 16) ^ int(test.phash, 16)).count('1')
        print('Output file: %s' % png_file)
        print('pHash: %s' % phash)
        print('Hamming distance to the reference pHash: %s ' % hamming_dist)
        if 'DISPLAY' not in os.environ:
            # upload to chunk.io if we're on a headless client
            subprocess.check_call(
                ['curl', '-sT', pdf_file, 'chunk.io'],
                stderr=subprocess.STDOUT
                )
            subprocess.check_call(
                ['curl', '-sT', png_file, 'chunk.io'],
                stderr=subprocess.STDOUT
                )

    assert test.phash == phash
