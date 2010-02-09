#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

from pylab import *
import matplotlib

from matplotlib2tikz import *
from testfunctions import *

# =============================================================================
def acidtest():

        tex_file_path = "./tex/acid.tex"
        data_dir = "./data" # directory where all the gerenated files will end up

        figure_width = "5cm"

        # open file for writing
        file_handle = open( tex_file_path, "w" )

        write_document_header( file_handle, figure_width )

        test_functions = [ basic_sin, subplots ]
        k = 0
        for fun in test_functions:
                k = k+1

                # plot the test example
                comment = fun()

                # convert to TikZ
                tikz_path = data_dir + "/test" + repr(k) + ".tikz"
                matplotlib2tikz(tikz_path,figurewidth=figure_width)

                # plot reference figure
                pdf_path  = data_dir + "/test" + repr(k) + ".pdf"
                savefig(pdf_path)

                # update the LaTeX file
                write_file_comparison_entry( file_handle,
                                             "../"+pdf_path,
                                             "../"+tikz_path,
                                             k,
                                             comment )

        write_document_closure( file_handle )
        file_handle.close()

        return
# =============================================================================
def write_document_header( file_handle, figure_width ):
        file_handle.write(   "\\documentclass{scrartcl}\n"
                           + "\\pdfminorversion=5\n"
                           + "\\pdfobjcompresslevel=2\n\n"
                           + "\\usepackage{graphicx}\n"
                           + "\\usepackage{subfig}\n"
                           + "\\usepackage{tikz,pgfplots}\n"
                           + "\\pgfplotsset{compat=newest}\n\n"
                           + "\\newlength\\figwidth\n"
                           + "\\setlength\\figwidth{" + figure_width +"}\n\n"
                           + "\\begin{document}\n\n"
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
        file_handle.write(   "% test plot " + repr(test_id) + "\n"
                           + "\\begin{figure}%\n"
                           + "\\centering%\n"
                           + "\\subfloat[][Reference PDF figure.]{\includegraphics[width=\\figwidth]"
                              + "{" + pdf_path + "}}%\n"
                           + "\\qquad%\n"
                           + "\\subfloat[][\\texttt{matplotlib2tikz}-generated]{\input{" + tikz_path + "}}%\n"
                           + "\\caption{" + comment + " (test ID " + repr(test_id) + ").}%\n"
                           + "\\end{figure}\n\n"
                         )
        return
# =============================================================================

# execute the test
acidtest()
