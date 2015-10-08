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
import wand.image
from PIL import Image
import imagehash

import matplotlib2tikz
import testfunctions


def test_generator():
    for name in testfunctions.__all__:
        print(name)
        test = import_module('testfunctions.' + name)
        yield check_hash, test


def check_hash(test):
    # import the test
    test.plot()
    # convert to tikz file
    handle, tikzfile = tempfile.mkstemp(suffix='_tikz.tex')
    matplotlib2tikz.save(
        tikzfile,
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
\\end{document}''' % tikzfile
    handle, tex_file = tempfile.mkstemp()
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
    pdf_file = tex_file + '.pdf'

    # Convert PDF to PNG.
    # Unfortunately, on some machines the background will be transparent, on
    # other it will be white. To remove this ambiguity, just ensure that the
    # background is white every time. See
    # <http://stackoverflow.com/a/27568049/353337> on how to do that.
    with wand.image.Image(filename=pdf_file, resolution=300) as img:
        with wand.image.Image(width=img.width, height=img.height,
                              background=wand.color.Color('white')) as bg:
            bg.composite(img, 0, 0)
            bg.format = 'png'
            bg.background_color = wand.color.Color('green')
            bg.alpha_channel = False
            png_file = tex_file + '.png'
            bg.save(filename=png_file)

    # compute the phash of the PNG
    phash = imagehash.phash(Image.open(png_file)).__str__()
    print(phash, type(phash))
    assert test.phash == phash
