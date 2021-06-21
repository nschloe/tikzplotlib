import datetime

import numpy as np
from matplotlib.dates import num2date

from . import _color as mycol
from . import _files
from . import _path as mypath
from ._markers import _mpl_marker2pgfp_marker
from ._util import get_legend_text, has_legend, transform_to_data_coordinates


def draw_line2d(data, obj):
    """Returns the PGFPlots code for an Line2D environment."""
    content = []
    addplot_options = []

    # If line is of length 0, do nothing.  Otherwise, an empty \addplot table will be
    # created, which will be interpreted as an external data source in either the file
    # '' or '.tex'.  Instead, render nothing.
    xdata = obj.get_xdata()
    if isinstance(xdata, int) or isinstance(xdata, float):
        # https://github.com/nschloe/tikzplotlib/issues/339
        xdata = [xdata]

    if len(xdata) == 0:
        return data, []

    # get the linewidth (in pt)
    line_width = mypath.mpl_linewidth2pgfp_linewidth(data, obj.get_linewidth())
    if line_width:
        addplot_options.append(line_width)

    # get line color
    color = obj.get_color()
    data, line_xcolor, _ = mycol.mpl_color2xcolor(data, color)
    addplot_options.append(line_xcolor)

    # get draw style
    drawstyle = obj.get_drawstyle()
    if drawstyle in [None, "default"]:
        pass
    else:
        if drawstyle == "steps-mid":
            style = "const plot mark mid"
        elif drawstyle in ["steps-pre", "steps"]:
            style = "const plot mark right"
        else:
            assert drawstyle == "steps-post"
            style = "const plot mark left"
        addplot_options.append(style)

    alpha = obj.get_alpha()
    if alpha is not None:
        addplot_options.append(f"opacity={alpha}")

    linestyle = mypath.mpl_linestyle2pgfplots_linestyle(
        data, obj.get_linestyle(), line=obj
    )
    if linestyle is not None and linestyle != "solid":
        addplot_options.append(linestyle)

    marker_face_color = obj.get_markerfacecolor()
    marker_edge_color = obj.get_markeredgecolor()

    is_filled = marker_face_color is not None and not (
        isinstance(marker_face_color, str) and marker_face_color.lower() == "none"
    )
    data, marker, extra_mark_options = _mpl_marker2pgfp_marker(
        data, obj.get_marker(), is_filled
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
    # Fixes <https://github.com/nschloe/tikzplotlib/issues/167>.
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
        content.append(f"\\addlegendentry{{{legend_text}}}\n")

    return data, content


def draw_linecollection(data, obj):
    """Returns Pgfplots code for a number of patch objects."""
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
        ff = data["float format"]
        # setting half size because pgfplots counts the radius/half-width
        pgf_size = 0.5 * mark_size
        addplot_options.append(f"mark size={pgf_size:{ff}}")

    mark_every = obj.get_markevery()
    if mark_every:
        if type(mark_every) is int:
            addplot_options.append(f"mark repeat={mark_every:d}")
        else:
            # python starts at index 0, pgfplots at index 1
            pgf_marker = [1 + m for m in mark_every]
            addplot_options.append(
                "mark indices = {" + ", ".join(map(str, pgf_marker)) + "}"
            )

    mark_options = ["solid"]
    mark_options += extra_mark_options
    if marker_face_color is None or (
        isinstance(marker_face_color, str) and marker_face_color == "none"
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


def _table(obj, data):  # noqa: C901
    # get_xydata() always gives float data, no matter what
    xdata, ydata = obj.get_xydata().T

    # get_{x,y}data gives datetime or string objects if so specified in the plotter
    xdata_alt = obj.get_xdata()
    if isinstance(xdata_alt, int) or isinstance(xdata, float):
        # https://github.com/nschloe/tikzplotlib/issues/339
        xdata_alt = [xdata_alt]

    ff = data["float format"]

    if isinstance(xdata_alt[0], datetime.datetime):
        xdata = xdata_alt
    elif isinstance(xdata_alt[0], str):
        data["current axes"].axis_options += [
            "xtick={{{}}}".format(",".join([f"{x:{ff}}" for x in xdata])),
            "xticklabels={{{}}}".format(",".join(xdata_alt)),
        ]
        xdata, ydata = transform_to_data_coordinates(obj, xdata, ydata)
    else:
        xdata, ydata = transform_to_data_coordinates(obj, xdata, ydata)

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
        _, ydata_alt = obj.get_data()
        ydata_mask = ydata_alt.mask
    except AttributeError:
        ydata_mask = []
    else:
        if isinstance(ydata_mask, np.bool_) and not ydata_mask:
            ydata_mask = []
        elif callable(ydata_mask):
            # pandas.Series have the method mask
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.mask.html
            ydata_mask = []

    axis_options = []

    content = []

    if isinstance(xdata[0], datetime.datetime):
        xdata = [date.strftime("%Y-%m-%d %H:%M") for date in xdata]
        xformat = ""
        col_sep = ","
        opts = ["header=false", "col sep=comma"]
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
        opts = []
        xformat = ff
        col_sep = " "

    if data["table_row_sep"] != "\n":
        # don't want the \n in the table definition, just in the data (below)
        opts.append("row sep=" + data["table_row_sep"].strip())
    if len(opts) > 0:
        content.append("table [{}] {{%\n".format(",".join(opts)))
    else:
        content.append("table {%\n")

    plot_table = []
    table_row_sep = data["table_row_sep"]
    ydata[ydata_mask] = np.nan
    if any(ydata_mask) or (~np.isfinite(ydata)).any():
        # matplotlib jumps at masked or nan values, while PGFPlots by default interpolates.
        # Hence, if we have a masked plot, make sure that PGFPlots jumps as well.
        if "unbounded coords=jump" not in data["current axes"].axis_options:
            data["current axes"].axis_options.append("unbounded coords=jump")

    for x, y in zip(xdata, ydata):
        plot_table.append(f"{x:{xformat}}{col_sep}{y:{ff}}{table_row_sep}")

    if data["externalize tables"]:
        filepath, rel_filepath = _files.new_filepath(data, "table", ".tsv")
        with open(filepath, "w") as f:
            # No encoding handling required: plot_table is only ASCII
            f.write("".join(plot_table))
        content.append(str(rel_filepath))
    else:
        content.extend(plot_table)

    content.append("};\n")
    return content, axis_options
