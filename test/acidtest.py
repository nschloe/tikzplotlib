#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pylab import *

from os import path

import sys

from matplotlib2tikz import *
from testfunctions import *

# =============================================================================
def acidtest():    
    tex_file_path = "./tex/acid.tex"
    data_dir = "./data" # directory where all the generated files will end up
    tex_relative_path_to_data = "../data" # how to get from the LaTeX file to the data

    figure_width = "5cm"

    # open file for writing
    file_handle = open( tex_file_path, "w" )

    write_document_header( file_handle, figure_width )

    test_functions = [ basic_sin, subplots, image_plot,
                       noise, patches, legends, legends2, logplot, subplot4x4 ]
    
    # see if the command line options tell which subset of the
    # tests are to be run
    test_list = []
    for arg in sys.argv:
        try:
            test_list.append( int(arg) )
        except:
            pass
    
    if len(test_list)!=0: # actually treat a sublist of test_functions
        # remove duplicates:
        test_list = list(set(test_list))
        # create the sublist
        tmp = test_functions
        test_functions = []
        for i in test_list:
            test_functions.append( tmp[i] )

    k = 0
    for fun in test_functions:
        # plot the test example
        comment = fun()

        # convert to TikZ
        tikz_path = data_dir + "/test" + repr(k) + ".tikz"
        matplotlib2tikz( tikz_path,
                         figurewidth=figure_width, 
                         tex_relative_path_to_data = tex_relative_path_to_data )

        # plot reference figure
        pdf_path  = data_dir + "/test" + repr(k) + ".pdf"
        savefig(pdf_path)

        # update the LaTeX file
        write_file_comparison_entry( file_handle,
                                     path.join( tex_relative_path_to_data,  path.basename(pdf_path) ),
                                     path.join( tex_relative_path_to_data,  path.basename(tikz_path) ),
                                     k,
                                     comment )
        k = k+1

    write_document_closure( file_handle )
    file_handle.close()

    return
# =============================================================================
def write_document_header( file_handle, figure_width ):
    file_handle.write( "\\documentclass{scrartcl}\n \
                        \\pdfminorversion=5\n \
                        \\pdfobjcompresslevel=2\n\n \
                        \\usepackage{graphicx}\n \
                        \\usepackage{subfig}\n \
                        \\usepackage{pgfplots}\n \
                        \\usepgfplotslibrary{groupplots}\n \
                        \\pgfplotsset{compat=newest}\n\n \
                        \\newlength\\figwidth\n \
                        \\setlength\\figwidth{" + figure_width +"}\n\n \
                        \\begin{document}\n\n"
                     )
    return
# =============================================================================
def write_document_closure( file_handle ):
    file_handle.write( "\\end{document}" )
    return
# =============================================================================
def write_file_comparison_entry( file_handle,
                                 pdf_path,
                                 tikz_path,
                                 test_id,
                                 comment ):
    file_handle.write(   "% test plot " + str(test_id) + "\n"
                       + "\\begin{figure}%\n"
                       + "\\centering%\n"
                       + "\\subfloat[][Reference PDF figure.]{\includegraphics[width=\\figwidth]"
                          + "{" + str(pdf_path) + "}}%\n"
                       + "\\qquad%\n"
                       + "\\subfloat[][\\texttt{matplotlib2tikz}-generated]{\input{" + str(tikz_path) + "}}%\n"
                       + "\\caption{" + str(comment) + " (test ID " + str(test_id) + ").}%\n"
                       + "\\end{figure}\n\n"
                     )
    return
# =============================================================================
if __name__=="__main__":
    # execute the test
    acidtest()
# =============================================================================