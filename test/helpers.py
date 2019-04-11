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
        print(indent, type(obj).__name__, '("{}")'.format(obj.get_text()))
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


def assert_equality(plot, filename, **extra_get_tikz_code_args):
    plot()
    code = matplotlib2tikz.get_tikz_code(
        include_disclaimer=False, **extra_get_tikz_code_args
    )
    plt.close()

    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, filename), "r", encoding="utf-8") as f:
        reference = f.read()
    assert reference == code, _unidiff_output(reference, code)

    code = matplotlib2tikz.get_tikz_code(
        include_disclaimer=False, standalone=True, **extra_get_tikz_code_args
    )
    assert _compile(code) is not None
    return


def _compile(code):
    _, tmp_base = tempfile.mkstemp()

    tex_file = tmp_base + ".tex"
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(code)

    # change into the directory of the TeX file
    os.chdir(os.path.dirname(tex_file))

    # compile the output to pdf
    try:
        subprocess.check_output(
            ["pdflatex", "--interaction=nonstopmode", tex_file],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        print("pdflatex output:")
        print("=" * 70)
        print(e.output.decode("utf-8"))
        print("=" * 70)
        output_pdf = None
    else:
        output_pdf = tmp_base + ".pdf"

    return output_pdf


def compare_mpl_latex(plot):
    plot()
    code = matplotlib2tikz.get_tikz_code(standalone=True)
    directory = os.getcwd()
    filename = "test-0.png"
    plt.savefig(filename)
    plt.close()

    pdf_file = _compile(code)
    pdf_dirname = os.path.dirname(pdf_file)

    # Convert PDF to PNG.
    subprocess.check_output(
        ["pdftoppm", "-r", "1000", "-png", pdf_file, "test"], stderr=subprocess.STDOUT
    )
    png_path = os.path.join(pdf_dirname, "test-1.png")

    os.rename(png_path, os.path.join(directory, "test-1.png"))
    return
