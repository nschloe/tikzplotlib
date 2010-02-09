#!/usr/bin/env python
# -*- coding: utf-8 -*-

import test_functions
import matplotlib2tikz
import tex_helpers

tex_file = 'tex/acid.tex'
data_dir = 'data'

fh = open( tex_file, 'w' )

tex_helpers.write_tex_header( fh )

test_functions.simple_sin()
matplotlib2tikz.matplotlib2tikz( data_dir + '/test0.tikz' )
tex_helpers.insert_test_plots( fh, '../'+ data_dir + '/test0.tikz' )

test_functions.subplots()
matplotlib2tikz.matplotlib2tikz( data_dir + '/test1.tikz' )
tex_helpers.insert_test_plots( fh, '../'+ data_dir + '/test1.tikz' )

tex_helpers.write_tex_closure( fh )