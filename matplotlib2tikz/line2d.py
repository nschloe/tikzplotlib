# -*- coding: utf-8 -*-
#
from __future__ import print_function

from matplotlib.dates import num2date
import datetime
import six

from . import color as mycol
from . import path as mypath
from . import files

from .util import get_legend_text, has_legend


def draw_line2d(data, obj):
    """Returns the PGFPlots code for an Line2D environment.
    """
    content = []
    addplot_options = []

    # If line is of length 0, do nothing.  Otherwise, an empty \addplot table
    # will be created, which will be interpreted as an external data source
    # in either the file '' or '.tex'.  Instead, render nothing.
    if len(obj.get_xdata()) == 0:
        return data, []

    # get the linewidth (in pt)
    line_width = mypath.mpl_linewidth2pgfp_linewidth(data, obj.get_linewidth())
    if line_width:
        addplot_options.append(line_width)

    # get line color
    color = obj.get_color()
    data, line_xcolor, _ = mycol.mpl_color2xcolor(data, color)
    addplot_options.append(line_xcolor)

    alpha = obj.get_alpha()
    if alpha is not None:
        addplot_options.append("opacity={}".format(alpha))

    linestyle = mypath.mpl_linestyle2pgfplots_linestyle(obj.get_linestyle())
    if linestyle is not None and linestyle != "solid":
        addplot_options.append(linestyle)

    marker_face_color = obj.get_markerfacecolor()
    marker_edge_color = obj.get_markeredgecolor()
    data, marker, extra_mark_options = _mpl_marker2pgfp_marker(
        data, obj.get_marker(), marker_face_color
    )
    if marker:
        _marker(
            obj,
            data,
            marker,
            addplot_options,
            extra_mark_options,
            marker_face_color,
            marker_edge_color,
            line_xcolor,
        )

    if marker and linestyle is None:
        addplot_options.append("only marks")

    # Check if a line is in a legend and forget it if not.
    # Fixes <https://github.com/nschloe/matplotlib2tikz/issues/167>.
    legend_text = get_legend_text(obj)
    if legend_text is None and has_legend(obj.axes):
        addplot_options.append("forget plot")

    # process options
    content.append("\\addplot ")
    if addplot_options:
        content.append("[{}]\n".format(", ".join(addplot_options)))

    c, axis_options = _table(obj, data)
    content += c

    if legend_text is not None:
        content.append("\\addlegendentry{{{}}}\n".format(legend_text))

    return data, content


def draw_linecollection(data, obj):
    """Returns Pgfplots code for a number of patch objects.
    """
    content = []

    edgecolors = obj.get_edgecolors()
    linestyles = obj.get_linestyles()
    linewidths = obj.get_linewidths()
    paths = obj.get_paths()

    for i, path in enumerate(paths):
        color = edgecolors[i] if i < len(edgecolors) else edgecolors[0]
        style = linestyles[i] if i < len(linestyles) else linestyles[0]
        width = linewidths[i] if i < len(linewidths) else linewidths[0]

        data, options = mypath.get_draw_options(data, obj, color, None, style, width)

        # TODO what about masks?
        data, cont, _, _ = mypath.draw_path(
            data, path, draw_options=options, simplify=False
        )
        content.append(cont + "\n")

    return data, content


# for matplotlib markers, see: http://matplotlib.org/api/markers_api.html
_MP_MARKER2PGF_MARKER = {
    ".": "*",  # point
    "o": "o",  # circle
    "+": "+",  # plus
    "x": "x",  # x
    "None": None,
    " ": None,
    "": None,
}

# the following markers are only available with PGF's plotmarks library
_MP_MARKER2PLOTMARKS = {
    "v": ("triangle", "rotate=180"),  # triangle down
    "1": ("triangle", "rotate=180"),
    "^": ("triangle", None),  # triangle up
    "2": ("triangle", None),
    "<": ("triangle", "rotate=270"),  # triangle left
    "3": ("triangle", "rotate=270"),
    ">": ("triangle", "rotate=90"),  # triangle right
    "4": ("triangle", "rotate=90"),
    "s": ("square", None),
    "p": ("pentagon", None),
    "*": ("asterisk", None),
    "h": ("star", None),  # hexagon 1
    "H": ("star", None),  # hexagon 2
    "d": ("diamond", None),  # diamond
    "D": ("diamond", None),  # thin diamond
    "|": ("|", None),  # vertical line
    "_": ("-", None),  # horizontal line
}


def _mpl_marker2pgfp_marker(data, mpl_marker, marker_face_color):
    """Translates a marker style of matplotlib to the corresponding style
    in PGFPlots.
    """
    # try default list
    try:
        pgfplots_marker = _MP_MARKER2PGF_MARKER[mpl_marker]
    except KeyError:
        pass
    else:
        if (marker_face_color is not None) and pgfplots_marker == "o":
            pgfplots_marker = "*"
            data["tikz libs"].add("plotmarks")
        marker_options = None
        return (data, pgfplots_marker, marker_options)

    # try plotmarks list
    try:
        data["tikz libs"].add("plotmarks")
        pgfplots_marker, marker_options = _MP_MARKER2PLOTMARKS[mpl_marker]
    except KeyError:
        # There's no equivalent for the pixel marker (,) in Pgfplots.
        pass
    else:
        if (
            marker_face_color is not None
            and (
                not isinstance(marker_face_color, str)
                or marker_face_color.lower() != "none"
            )
            and pgfplots_marker not in ["|", "-", "asterisk", "star"]
        ):
            pgfplots_marker += "*"
        return (data, pgfplots_marker, marker_options)

    return data, None, None


# def _transform_to_data_coordinates(obj, xdata, ydata):
#     '''The coordinates might not be in data coordinates, but could be partly
#     in axes coordinates.  For example, the matplotlib command
#       axes.axvline(2)
#     will have the y coordinates set to 0 and 1, not to the limits. Therefore,
#     a two-stage transform has to be applied:
#       1. first transforming to display coordinates, then
#       2. from display to data.
#     In case of problems (non-invertible, or whatever), print a warning and
#     continue anyways.
#     '''
#     try:
#         import matplotlib.transforms
#         points = numpy.array(zip(xdata, ydata))
#         transform = matplotlib.transforms.composite_transform_factory(
#             obj.get_transform(),
#             obj.axes.transData.inverted()
#             )
#         points_data = transform.transform(points)
#         xdata, ydata = zip(*points_data)
#     except Exception as e:
#         print(xdata, ydata)
#         print(('Problem during transformation:\n' +
#                '   %s\n' +
#                'Continuing with original data.')
#               % e
#               )
#     return (xdata, ydata)


def _marker(
    obj,
    data,
    marker,
    addplot_options,
    extra_mark_options,
    marker_face_color,
    marker_edge_color,
    line_xcolor,
):
    addplot_options.append("mark=" + marker)

    mark_size = obj.get_markersize()
    if mark_size:
        # setting half size because pgfplots counts the radius/half-width
        pgf_size = int(0.5 * mark_size)
        # make sure we didn't round off to zero by accident
        if pgf_size == 0 and mark_size != 0:
            pgf_size = 1
        addplot_options.append("mark size={:d}".format(pgf_size))

    mark_every = obj.get_markevery()
    if mark_every:
        if type(mark_every) is int:
            addplot_options.append("mark repeat={:d}".format(mark_every))
        else:
            # python starts at index 0, pgfplots at index 1
            pgf_marker = [1 + m for m in mark_every]
            addplot_options.append(
                "mark indices = {" + ", ".join(map(str, pgf_marker)) + "}"
            )

    mark_options = ["solid"]
    if extra_mark_options:
        mark_options.append(extra_mark_options)
    if marker_face_color is None or (
        isinstance(marker_face_color, six.string_types) and marker_face_color == "none"
    ):
        mark_options.append("fill opacity=0")
    else:
        data, face_xcolor, _ = mycol.mpl_color2xcolor(data, marker_face_color)
        if face_xcolor != line_xcolor:
            mark_options.append("fill=" + face_xcolor)

    face_and_edge_have_equal_color = marker_edge_color == marker_face_color
    # Sometimes, the colors are given as arrays. Collapse them into a
    # single boolean.
    try:
        face_and_edge_have_equal_color = all(face_and_edge_have_equal_color)
    except TypeError:
        pass

    if not face_and_edge_have_equal_color:
        data, draw_xcolor, _ = mycol.mpl_color2xcolor(data, marker_edge_color)
        if draw_xcolor != line_xcolor:
            mark_options.append("draw=" + draw_xcolor)
    addplot_options.append("mark options={{{}}}".format(",".join(mark_options)))

    return


def _table(obj, data):
    # TODO nschloe, Oct 2, 2015:
    #   The transform call yields warnings and it is unclear why. Perhaps the input data
    #   is not suitable? Anyhow, this should not happen. Comment out for now.
    # xdata, ydata = _transform_to_data_coordinates(obj, *obj.get_data())
    xdata, ydata = obj.get_data()

    # matplotlib allows plotting of data containing `astropy.units`, but they will break
    # the formatted string here. Try to strip the units from the data.
    try:
        xdata = xdata.value
    except AttributeError:
        pass
    try:
        ydata = ydata.value
    except AttributeError:
        pass

    try:
        has_mask = ydata.mask.any()
    except AttributeError:
        has_mask = False

    axis_options = []

    content = []

    ff = data["float format"]
    if isinstance(xdata[0], datetime.datetime):
        xdata = [date.strftime("%Y-%m-%d %H:%M") for date in xdata]
        xformat = "{}"
        col_sep = ","
        content.append("table [header=false,col sep=comma] {%\n")
        data["current axes"].axis_options.append("date coordinates in=x")
        # Replace float xmin/xmax by datetime
        # <https://github.com/matplotlib/matplotlib/issues/13727>.
        data["current axes"].axis_options = [
            option
            for option in data["current axes"].axis_options
            if not option.startswith("xmin")
        ]
        xmin, xmax = data["current mpl axes obj"].get_xlim()
        data["current axes"].axis_options.append(
            "xmin={}, xmax={}".format(
                num2date(xmin).strftime("%Y-%m-%d %H:%M"),
                num2date(xmax).strftime("%Y-%m-%d %H:%M"),
            )
        )
    else:
        xformat = ff
        col_sep = " "
        content.append("table {%\n")

    plot_table = []
    if has_mask:
        # matplotlib jumps at masked images, while PGFPlots by default interpolates.
        # Hence, if we have a masked plot, make sure that PGFPlots jumps as well.
        if "unbounded coords=jump" not in data["current axes"].axis_options:
            data["current axes"].axis_options.append("unbounded coords=jump")

        for (x, y, is_masked) in zip(xdata, ydata, ydata.mask):
            if is_masked:
                plot_table.append((xformat + col_sep + "nan\n").format(x))
            else:
                plot_table.append((xformat + col_sep + ff + "\n").format(x, y))
    else:
        for (x, y) in zip(xdata, ydata):
            plot_table.append((xformat + col_sep + ff + "\n").format(x, y))

    if data["externalize tables"]:
        filename, rel_filepath = files.new_filename(data, "table", ".tsv")
        with open(filename, "w") as f:
            # No encoding handling required: plot_table is only ASCII
            f.write("".join(plot_table))
        content.append(rel_filepath)
    else:
        content.extend(plot_table)

    content.append("};\n")
    return content, axis_options
