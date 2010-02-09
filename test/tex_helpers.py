# -*- coding: utf-8 -*-
# =============================================================================
def write_tex_header( fh ):
        fh.write( '\\documentclass{scrartcl}\n'
                  '\\usepackage{tikz,pgfplots}\n'
                  '\\begin{document}\n'
                )
# =============================================================================
def insert_test_plots( fh, rel_tikz_file_path ):
        fh.write( '\\input{'+rel_tikz_file_path+'}\n' )
# =============================================================================
def write_tex_closure( fh ):
        fh.write( '\\end{document}' )
# =============================================================================