# -*- coding: utf-8 -*-
#
import os
import subprocess
import tempfile

import matplotlib
import matplotlib.pyplot as plt

import matplotlib2tikz


def print_tree(obj, indent=""):
    """Recursively prints the tree structure of the matplotlib object.
    """
    if isinstance(obj, matplotlib.text.Text):
        print(indent, type(obj).__name__, '("%s")' % obj.get_text())
    else:
        print(indent, type(obj).__name__)

    for child in obj.get_children():
        print_tree(child, indent + "   ")
    return


# https://stackoverflow.com/a/845432/353337
def _unidiff_output(expected, actual):
    import difflib

    expected = expected.splitlines(1)
    actual = actual.splitlines(1)
    diff = difflib.unified_diff(expected, actual)
    return "".join(diff)


def assert_equality(plot, filename):
    plot()
    code = matplotlib2tikz.get_tikz_code(include_disclaimer=False)
    plt.close()

    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, filename), "r", encoding="utf-8") as f:
        reference = f.read()
    assert reference == code, _unidiff_output(reference, code)

    assert _does_compile(code)
    return


def _does_compile(code):
    _, tmp_base = tempfile.mkstemp()
    matplotlib2tikz.get_tikz_code()

    # create a latex wrapper for the tikz
    # <https://tex.stackexchange.com/a/361070/13262>
    wrapper = """\\documentclass{{standalone}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{pgfplots}}
\\usepgfplotslibrary{{groupplots}}
\\usetikzlibrary{{shapes.arrows}}
\\pgfplotsset{{compat=newest}}
\\DeclareUnicodeCharacter{{2212}}{{-}}
\\begin{{document}}
{}
\\end{{document}}""".format(
        code
    )
    tex_file = tmp_base + ".tex"
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(wrapper)

    # change into the directory of the TeX file
    os.chdir(os.path.dirname(tex_file))

    # compile the output to pdf
    try:
        subprocess.check_output(
            ["pdflatex", "--interaction=nonstopmode", tex_file],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        print("Command output:")
        print("=" * 70)
        print(e.output)
        print("=" * 70)
        does_compile = False
    else:
        does_compile = True

    return does_compile
