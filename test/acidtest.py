#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==============================================================================
#
# Copyright (C) 2010, 2011 Nico Schl"omer
#
# This file is part of matplotlib2tikz.
#
# matplotlib2tikz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# matplotlib2tikz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# ==============================================================================
from os import path
import sys
from matplotlib import pyplot as pp
import matplotlib2tikz
import testfunctions as tf
# ==============================================================================
# XXX: There seems to be an issue with the legends that do not
# appear in the pdf versions. The old legends are carried over from
# the previous run and are transfered to the next run. I believe this is
# a problem with the testing method, because if one adds print text in
# _draw_legend pyplot returns the correct legends when this test is run
# ==============================================================================
def _main():

    # get command line arguments
    test_list = _parse_options()

    tex_file_path = "./tex/acid.tex"

    # directory where all the generated files will end up
    data_dir = "./data"

    # how to get from the LaTeX file to the data
    tex_relative_path_to_data = "../data"

    figure_width = "7.5cm"

    # open file for writing
    file_handle = open( tex_file_path, "w" )

    write_document_header( file_handle, figure_width )

    test_functions = [ tf.basic_sin,
                       tf.subplots,
                       tf.image_plot,
                       tf.noise,
                       tf.circle_patch,
                       tf.patches,
                       tf.legends,
                       tf.legends2,
                       tf.logplot,
                       tf.loglogplot,
                       tf.subplot4x4,
                       tf.text_overlay,
                       tf.annotate,
                       tf.histogram,
                       tf.contourf_with_logscale
                     ]

    if not test_list is None: # actually treat a sublist of test_functions
        # remove duplicates and sort
        test_list = sorted( set(test_list) )
    else:
        # all indices
        test_list = xrange( 0, len(test_functions) )

    for k in test_list:
        print 'Test function %d...' % k,
        pp.cla()
        pp.clf()
        # plot the test example
        comment = test_functions[k]()

        # convert to TikZ
        tikz_path = data_dir + "/test" + repr(k) + ".tikz"
        matplotlib2tikz.save( tikz_path,
                              figurewidth = figure_width,
                              tex_relative_path_to_data = \
                                                     tex_relative_path_to_data
                            )

        # plot reference figure
        pdf_path  = data_dir + "/test" + repr(k) + ".pdf"
        pp.savefig(pdf_path)

        # update the LaTeX file
        write_file_comparison_entry( file_handle,
                                     path.join( tex_relative_path_to_data,
                                                path.basename(pdf_path) ),
                                     path.join( tex_relative_path_to_data,
                                                path.basename(tikz_path) ),
                                     k,
                                     comment
                                   )
        print 'done.'

    write_document_closure( file_handle )
    file_handle.close()

    return
# ==============================================================================
def write_document_header( file_handle, figure_width ):
    '''Write the LaTeX document header to the file.
    '''
    file_handle.write( "\\documentclass{scrartcl}\n"
                       "\\pdfminorversion=5\n"
                       "\\pdfobjcompresslevel=2\n\n"
                       "\\usepackage{graphicx}\n"
                       "\\usepackage{subfig}\n"
                       "\\usepackage{pgfplots}\n"
                       "\\usepgfplotslibrary{groupplots}\n"
                       "\\pgfplotsset{compat=newest}\n\n"
                       "\\newlength\\figwidth\n"
                       "\\setlength\\figwidth{" + figure_width +"}\n\n"
                       "\\begin{document}\n\n"
                     )
    return
# ==============================================================================
def write_document_closure( file_handle ):
    '''Write the LaTeX document closure to the file.
    '''
    file_handle.write( "\\end{document}" )
    return
# ==============================================================================
def write_file_comparison_entry( file_handle,
                                 pdf_path,
                                 tikz_path,
                                 test_id,
                                 comment ):
    '''Write the Tikz vs. PDF comparison figures to the LaTeX file.
    '''
    file_handle.write(   "% test plot " + str(test_id) + "\n"
                       + "\\begin{figure}%\n"
                       + "\\centering%\n"
                       + "\\subfloat[][Reference PDF figure.]{" \
                                            "\includegraphics[width=\\figwidth]"
                          + "{" + str(pdf_path) + "}}%\n"
                       + "\\quad%\n"
                       #+ "\\\\"
                       + "\\subfloat[][\\texttt{matplotlib2tikz}-generated]{" \
                                            "\input{" + str(tikz_path) + "}}%\n"
                       + "\\caption{" + str(comment) + " (test ID " \
                       + str(test_id) + ").}%\n"
                       + "\\end{figure}\\clearpage\n\n"
                     )
    return
# ==============================================================================
def _parse_options():
    '''Parse input options.'''
    import argparse

    parser = argparse.ArgumentParser( description =
                                              'Acid test for matplotlib2tikz.' )

    parser.add_argument( '--tests', '-t',
                         metavar = 'TEST_INDICES',
                         nargs   = '+',
                         type    = int,
                         help    = 'tests to perform'
                       )

    args = parser.parse_args()

    return args.tests
# ==============================================================================
if __name__ == "__main__":
    # execute the test
    _main()
# ==============================================================================
