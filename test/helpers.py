import os
import subprocess
import tempfile

import matplotlib
import matplotlib.pyplot as plt

import tikzplotlib


def print_tree(obj, indent=""):
    """Recursively prints the tree structure of the matplotlib object.
    """
    if isinstance(obj, matplotlib.text.Text):
        print(indent, type(obj).__name__, '("{}")'.format(obj.get_text()))
    else:
        print(indent, type(obj).__name__)

    for child in obj.get_children():
        print_tree(child, indent + "   ")


# https://stackoverflow.com/a/845432/353337
def _unidiff_output(expected, actual):
    import difflib

    expected = expected.splitlines(1)
    actual = actual.splitlines(1)
    diff = difflib.unified_diff(expected, actual)
    return "".join(diff)


def assert_equality(
    plot, filename, assert_compilation=True, flavor="latex", **extra_get_tikz_code_args
):
    plot()
    code = tikzplotlib.get_tikz_code(
        include_disclaimer=False,
        float_format=".8g",
        flavor=flavor,
        **extra_get_tikz_code_args,
    )
    plt.close()

    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, filename), "r", encoding="utf-8") as f:
        reference = f.read()
    assert reference == code, _unidiff_output(code, reference)

    if assert_compilation:
        plot()
        code = tikzplotlib.get_tikz_code(
            include_disclaimer=False,
            standalone=True,
            flavor=flavor,
            **extra_get_tikz_code_args,
        )
        plt.close()
        assert _compile(code, flavor) is not None, code


def _compile(code, flavor):
    _, tmp_base = tempfile.mkstemp()

    tex_file = tmp_base + ".tex"
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(code)

    # change into the directory of the TeX file
    os.chdir(os.path.dirname(tex_file))

    # compile the output to pdf
    cmdline = dict(
        latex=["pdflatex", "--interaction=nonstopmode"],
        context=["context", "--nonstopmode"],
    )[flavor]
    try:
        subprocess.check_output(cmdline + [tex_file], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"{cmdline[0]} output:")
        print("=" * 70)
        print(e.output.decode("utf-8"))
        print("=" * 70)
        output_pdf = None
    else:
        output_pdf = tmp_base + ".pdf"

    return output_pdf


def compare_mpl_tex(plot, flavor="latex"):
    plot()
    code = tikzplotlib.get_tikz_code(standalone=True)
    directory = os.getcwd()
    filename = "test-0.png"
    plt.savefig(filename)
    plt.close()

    pdf_file = _compile(code, flavor)
    pdf_dirname = os.path.dirname(pdf_file)

    # Convert PDF to PNG.
    subprocess.check_output(
        ["pdftoppm", "-r", "1000", "-png", pdf_file, "test"], stderr=subprocess.STDOUT
    )
    png_path = os.path.join(pdf_dirname, "test-1.png")

    os.rename(png_path, os.path.join(directory, "test-1.png"))
