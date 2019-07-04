import codecs
import os
import tempfile
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt

from . import axes
from . import image as img
from . import legend, line2d, patch, path
from . import quadmesh as qmsh
from . import text
from .__about__ import __version__


def get_tikz_code(
    figure="gcf",
    filepath=None,
    figurewidth=None,
    figureheight=None,
    textsize=10.0,
    tex_relative_path_to_data=None,
    externalize_tables=False,
    override_externals=False,
    strict=False,
    wrap=True,
    add_axis_environment=True,
    extra_axis_parameters=None,
    extra_tikzpicture_parameters=None,
    dpi=None,
    show_info=False,
    include_disclaimer=True,
    standalone=False,
    float_format="{:.15g}",
    table_row_sep="\n",
):
    """Main function. Here, the recursion into the image starts and the
    contents are picked up. The actual file gets written in this routine.

    :param figure: either a Figure object or 'gcf' (default).

    :param figurewidth: If not ``None``, this will be used as figure width
                        within the TikZ/PGFPlots output. If ``figureheight``
                        is not given, ``tikzplotlib`` will try to preserve
                        the original width/height ratio.
                        Note that ``figurewidth`` can be a string literal,
                        such as ``'\\figurewidth'``.
    :type figurewidth: str

    :param figureheight: If not ``None``, this will be used as figure height
                         within the TikZ/PGFPlots output. If ``figurewidth`` is
                         not given, ``tikzplotlib`` will try to preserve
                         the original width/height ratio.  Note that
                         ``figurewidth`` can be a string literal, such as
                         ``'\\figureheight'``.
    :type figureheight: str

    :param textsize: The text size (in pt) that the target latex document is
                     using.  Default is 10.0.
    :type textsize: float

    :param tex_relative_path_to_data: In some cases, the TikZ file will have to
                                      refer to another file, e.g., a PNG for
                                      image plots. When ``\\input`` into a
                                      regular LaTeX document, the additional
                                      file is looked for in a folder relative
                                      to the LaTeX file, not the TikZ file.
                                      This arguments optionally sets the
                                      relative path from the LaTeX file to the
                                      data.
    :type tex_relative_path_to_data: str

    :param externalize_tables: Whether or not to externalize plot data tables
                               into tsv files.
    :type externalize_tables: bool

    :param override_externals: Whether or not to override existing external
                               files (such as tsv or images) with conflicting
                               names (the alternative is to choose other
                               names).
    :type override_externals: bool

    :param strict: Whether or not to strictly stick to matplotlib's appearance.
                   This influences, for example, whether tick marks are set
                   exactly as in the matplotlib plot, or if TikZ/PGFPlots
                   can decide where to put the ticks.
    :type strict: bool

    :param wrap: Whether ``'\\begin{tikzpicture}'`` and
                 ``'\\end{tikzpicture}'`` will be written. One might need to
                 provide custom arguments to the environment (eg. scale= etc.).
                 Default is ``True``.
    :type wrap: bool

    :param add_axis_environment: Whether ``'\\begin{axis}[...]'`` and
                                 ``'\\end{axis}'`` will be written. One needs to
                                 set the environment in the document. If ``False``
                                 additionally sets ``wrap=False``. Default is ``True``.
    :type add_axis_environment: bool

    :param extra_axis_parameters: Extra axis options to be passed (as a list or set)
                                  to pgfplots. Default is ``None``.
    :type extra_axis_parameters: a list or set of strings for the pfgplots axes.

    :param extra_tikzpicture_parameters: Extra tikzpicture options to be passed
                                         (as a set) to pgfplots.

    :type extra_tikzpicture_parameters: a set of strings for the pfgplots
                                        tikzpicture.

    :param dpi: The resolution in dots per inch of the rendered image in case
                of QuadMesh plots. If ``None`` it will default to the value
                ``savefig.dpi`` from matplotlib.rcParams. Default is ``None``.
    :type dpi: int

    :param show_info: Show extra info on the command line. Default is ``False``.
    :type show_info: bool

    :param include_disclaimer: Include tikzplotlib disclaimer in the output.
                               Set ``False`` to make tests reproducible.
                               Default is ``True``.
    :type include_disclaimer: bool

    :param standalone: Include wrapper code for a standalone LaTeX file.
    :type standalone: bool

    :param float_format: Format for float entities. Default is ```"{:.15g}"```.
    :type float_format: str

    :param table_row_sep: Row separator for table data. Default is ```"\\n"```.
    :type table_row_sep: str

    :returns: None

    The following optional attributes of matplotlib's objects are recognized
    and handled:

     - axes.Axes._tikzplotlib_anchors
       This attribute can be set to a list of ((x,y), anchor_name) tuples.
       Invisible nodes at the respective location will be created which  can be
       referenced from outside the axis environment.
    """
    # not as default value because gcf() would be evaluated at import time
    if figure == "gcf":
        figure = plt.gcf()
    data = {}
    data["fwidth"] = figurewidth
    data["fheight"] = figureheight
    data["rel data path"] = tex_relative_path_to_data
    data["externalize tables"] = externalize_tables
    data["override externals"] = override_externals

    if filepath:
        data["output dir"] = os.path.dirname(filepath)
    else:
        directory = tempfile.mkdtemp()
        data["output dir"] = directory

    data["base name"] = (
        os.path.splitext(os.path.basename(filepath))[0] if filepath else "tmp"
    )
    data["strict"] = strict
    data["tikz libs"] = set()
    data["pgfplots libs"] = set()
    data["font size"] = textsize
    data["custom colors"] = {}
    data["legend colors"] = []
    data["extra tikzpicture parameters"] = extra_tikzpicture_parameters
    data["add axis environment"] = add_axis_environment
    data["show_info"] = show_info
    # rectangle_legends is used to keep track of which rectangles have already
    # had \addlegendimage added. There should be only one \addlegenimage per
    # bar chart data series.
    data["rectangle_legends"] = set()
    if extra_axis_parameters:
        data["extra axis options [base]"] = set(extra_axis_parameters).copy()
    else:
        data["extra axis options [base]"] = set()

    if dpi:
        data["dpi"] = dpi
    else:
        savefig_dpi = mpl.rcParams["savefig.dpi"]
        data["dpi"] = (
            savefig_dpi if isinstance(savefig_dpi, int) else mpl.rcParams["figure.dpi"]
        )

    data["float format"] = float_format
    data["table_row_sep"] = table_row_sep

    # print message about necessary pgfplot libs to command line
    if show_info:
        _print_pgfplot_libs_message(data)

    # gather the file content
    data, content = _recurse(data, figure)

    # Check if there is still an open groupplot environment. This occurs if not
    # all of the group plot slots are used.
    if "is_in_groupplot_env" in data and data["is_in_groupplot_env"]:
        content.extend("\\end{groupplot}\n\n")

    # write disclaimer to the file header
    code = """"""

    if include_disclaimer:
        disclaimer = "This file was created by tikzplotlib v{}.".format(__version__)
        code += _tex_comment(disclaimer)

    # write the contents
    if wrap and add_axis_environment:
        code += "\\begin{tikzpicture}\n\n"
        if extra_tikzpicture_parameters:
            code += ",\n".join(data["extra tikzpicture parameters"])
            code += "\n"

    coldefs = _get_color_definitions(data)
    if coldefs:
        code += "\n".join(coldefs)
        code += "\n\n"

    code += "".join(content)

    if wrap and add_axis_environment:
        code += "\\end{tikzpicture}"

    if standalone:
        # create a latex wrapper for the tikz
        # <https://tex.stackexchange.com/a/361070/13262>
        code = """\\documentclass{{standalone}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{pgfplots}}
\\usepgfplotslibrary{{groupplots}}
\\usepgfplotslibrary{{dateplot}}
\\pgfplotsset{{compat=newest}}
\\DeclareUnicodeCharacter{{2212}}{{−}}
\\begin{{document}}
{}
\\end{{document}}""".format(
            code
        )

    return code


def save(filepath, *args, encoding=None, **kwargs):
    """Same as `get_tikz_code()`, but actually saves the code to a file.

    :param filepath: The file to which the TikZ output will be written.
    :type filepath: str

    :param encoding: Sets the text encoding of the output file, e.g. 'utf-8'.
                     For supported values: see ``codecs`` module.
    :returns: None
    """
    code = get_tikz_code(*args, filepath=filepath, **kwargs)
    file_handle = codecs.open(filepath, "w", encoding)
    file_handle.write(code)
    file_handle.close()
    return


def _tex_comment(comment):
    """Prepends each line in string with the LaTeX comment key, '%'.
    """
    return "% " + str.replace(comment, "\n", "\n% ") + "\n"


def _get_color_definitions(data):
    """Returns the list of custom color definitions for the TikZ file.
    """
    definitions = []
    fmt = "\\definecolor{{{}}}{{rgb}}{{" + ",".join(3 * [data["float format"]]) + "}}"
    for name, rgb in data["custom colors"].items():
        definitions.append(fmt.format(name, rgb[0], rgb[1], rgb[2]))
    return definitions


def _print_pgfplot_libs_message(data):
    """Prints message to screen indicating the use of PGFPlots and its
    libraries."""
    pgfplotslibs = ",".join(list(data["pgfplots libs"]))
    tikzlibs = ",".join(list(data["tikz libs"]))

    print(70 * "=")
    print("Please add the following lines to your LaTeX preamble:\n")
    print("\\usepackage[utf8]{inputenc}")
    print("\\usepackage{fontspec}  % This line only for XeLaTeX and LuaLaTeX")
    print("\\usepackage{pgfplots}")
    if tikzlibs:
        print("\\usetikzlibrary{" + tikzlibs + "}")
    if pgfplotslibs:
        print("\\usepgfplotslibrary{" + pgfplotslibs + "}")
    print(70 * "=")
    return


class _ContentManager:
    """Basic Content Manager for tikzplotlib

    This manager uses a dictionary to map z-order to an array of content
    to be drawn at the z-order.
    """

    def __init__(self):
        self._content = dict()

    def extend(self, content, zorder):
        """ Extends with a list and a z-order
        """
        if zorder not in self._content:
            self._content[zorder] = []
        self._content[zorder].extend(content)

    def flatten(self):
        content_out = []
        all_z = sorted(self._content.keys())
        for z in all_z:
            content_out.extend(self._content[z])
        return content_out


def _recurse(data, obj):
    """Iterates over all children of the current object, gathers the contents
    contributing to the resulting PGFPlots file, and returns those.
    """
    content = _ContentManager()
    for child in obj.get_children():
        # Some patches are Spines, too; skip those entirely.
        # See <https://github.com/nschloe/tikzplotlib/issues/277>.
        if isinstance(child, mpl.spines.Spine):
            continue

        if isinstance(child, mpl.axes.Axes):
            ax = axes.Axes(data, child)

            if ax.is_colorbar:
                continue

            # add extra axis options
            if data["extra axis options [base]"]:
                ax.axis_options.extend(data["extra axis options [base]"])

            data["current mpl axes obj"] = child
            data["current axes"] = ax

            # Run through the child objects, gather the content.
            data, children_content = _recurse(data, child)

            # populate content and add axis environment if desired
            if data["add axis environment"]:
                content.extend(
                    ax.get_begin_code() + children_content + [ax.get_end_code(data)], 0
                )
            else:
                content.extend(children_content, 0)
                # print axis environment options, if told to show infos
                if data["show_info"]:
                    print("=========================================================")
                    print("These would have been the properties of the environment:")
                    print("".join(ax.get_begin_code()[1:]))
                    print("=========================================================")
        elif isinstance(child, mpl.lines.Line2D):
            data, cont = line2d.draw_line2d(data, child)
            content.extend(cont, child.get_zorder())
        elif isinstance(child, mpl.image.AxesImage):
            data, cont = img.draw_image(data, child)
            content.extend(cont, child.get_zorder())
        elif isinstance(child, mpl.patches.Patch):
            data, cont = patch.draw_patch(data, child)
            content.extend(cont, child.get_zorder())
        elif isinstance(
            child, (mpl.collections.PatchCollection, mpl.collections.PolyCollection)
        ):
            data, cont = patch.draw_patchcollection(data, child)
            content.extend(cont, child.get_zorder())
        elif isinstance(child, mpl.collections.PathCollection):
            data, cont = path.draw_pathcollection(data, child)
            content.extend(cont, child.get_zorder())
        elif isinstance(child, mpl.collections.LineCollection):
            data, cont = line2d.draw_linecollection(data, child)
            content.extend(cont, child.get_zorder())
        elif isinstance(child, mpl.collections.QuadMesh):
            data, cont = qmsh.draw_quadmesh(data, child)
            content.extend(cont, child.get_zorder())
        elif isinstance(child, mpl.legend.Legend):
            data = legend.draw_legend(data, child)
            if data["legend colors"]:
                content.extend(data["legend colors"], 0)
        elif isinstance(child, (mpl.text.Text, mpl.text.Annotation)):
            data, cont = text.draw_text(data, child)
            content.extend(cont, child.get_zorder())
        elif isinstance(child, (mpl.axis.XAxis, mpl.axis.YAxis)):
            pass
        else:
            warnings.warn(
                "tikzplotlib: Don't know how to handle object {}.".format(type(child))
            )
    return data, content.flatten()
