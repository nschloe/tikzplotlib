import matplotlib as mpl
import datetime
import numpy as np
from matplotlib.dates import num2date

from . import _color as mycol
from ._markers import _mpl_marker2pgfp_marker
from ._line2d import _marker
from . import _path as mypath
from . import _files
from ._util import get_legend_text, has_legend, transform_to_data_coordinates


def _extract_error_barline_data(data, bar):
    color = bar.get_edgecolors()[0]
    style = bar.get_linestyles()[0]
    width = bar.get_linewidths()[0]
    paths = bar.get_paths()
    
    data, options = mypath.get_draw_options(data, paths[0], color, None, style, width)
    
    abs_upper_err, abs_lower_err = [], []
    for path in paths:
        errs = path.vertices
        abs_upper_err.append(max(errs[errs - errs[::-1] != 0]))
        abs_lower_err.append(min(errs[errs - errs[::-1] != 0]))
    
    return data, options, np.array(abs_upper_err), np.array(abs_lower_err)
    

def draw_container(data, container):
    
    if isinstance(container, mpl.container.BarContainer):
        pass
    elif isinstance(container, mpl.container.ErrorbarContainer):        
        
        # errorbar_options = ['error bars/.cd']
        errorbar_data = {"general":[]}
        
        errorbar_data["label"] = container.get_label()
        data_line, caplines, barlinecols = container
        
        if container.has_xerr or container.has_yerr:
            errorbar_data["error_data"] = {}
        
        if container.has_xerr:
            bar = barlinecols[0]
            data, draw_options, xerr_up, xerr_lo = _extract_error_barline_data(data, bar)
            errorbar_data["error_data"]["x error plus"] = xerr_up - data_line.get_xdata()
            errorbar_data["error_data"]["x error minus"] = data_line.get_xdata() - xerr_lo
        if container.has_yerr:
           if container.has_xerr:
               bar = barlinecols[1]
           else:
               bar = barlinecols[0]
           data, draw_options, yerr_up, yerr_lo = _extract_error_barline_data(data, bar)
           errorbar_data["error_data"]["y error plus"] = yerr_up - data_line.get_ydata()
           errorbar_data["error_data"]["y error minus"] = data_line.get_ydata() - yerr_lo         
        
        errorbar_data["style"] = draw_options
        
        if not caplines:
            errorbar_data["general"].append("error mark=none")
        else:
            errorbar_data["caps obj"] = caplines[0]
            
        data, cont = draw_line2d_errorbars(data, data_line, errorbar_data)
        zorder = data_line.get_zorder()
              
    elif isinstance(container, mpl.container.StemContainer):
        pass
    
    return data, cont, zorder



def _write_errorbar_options(data, errorbar_data, line_xcolor):
    def _fill_direction(xy):
        if f'{xy} error plus' in error_data or f'{xy} error minus' in error_data:
            content.append(f'{xy} explicit')
        if f'{xy} error plus' in error_data:
            if f'{xy} error plus' in error_data:
                content.append(f'{xy} dir=both')
            else:
                content.append(f'{xy} dir=plus, ')
        elif f'{xy} error minus' in error_data:
            content.append(f'{xy} dir=minus')
    
    content = []
    content.append('error bars/.cd')
    content.extend(errorbar_data["general"])
    error_data = errorbar_data['error_data']
    for xy in ['x','y']:
        _fill_direction(xy)
    content.append(f"error bar style={{{', '.join(errorbar_data['style'])}}}")
    
    if "caps obj" in errorbar_data:
        obj = errorbar_data["caps obj"]
        marker_face_color = obj.get_markerfacecolor()
        marker_edge_color = obj.get_markeredgecolor()
    
        is_filled = marker_face_color is not None and not (
            isinstance(marker_face_color, str) and marker_face_color.lower() == "none"
        )
        data, marker, extra_mark_options = _mpl_marker2pgfp_marker(
            data, obj.get_marker(), is_filled
        )
        if marker:
            _error_marker(
                obj,
                data,
                marker,
                content,
                extra_mark_options,
                marker_face_color,
                marker_edge_color,
                line_xcolor,
            )
    
    return content

def _error_marker(
    obj,
    data,
    marker,
    addplot_options,
    extra_mark_options,
    marker_face_color,
    marker_edge_color,
    line_xcolor,
):
    if marker == "-":
        marker = "|"
    addplot_options.append("error mark=" + marker)    
    mark_options = ["solid"]
    
    mark_size = obj.get_markersize()
    if mark_size:
        ff = data["float format"]
        # setting half size because pgfplots counts the radius/half-width
        pgf_size = 0.25 * mark_size
        mark_options.append(f"mark size={pgf_size:{ff}}")

    mark_every = obj.get_markevery()
    if mark_every:
        if type(mark_every) is int:
            mark_options.append(f"mark repeat={mark_every:d}")
        else:
            # python starts at index 0, pgfplots at index 1
            pgf_marker = [1 + m for m in mark_every]
            mark_options.append(
                "mark indices = {" + ", ".join(map(str, pgf_marker)) + "}"
            )

   
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
    opts = ", ".join(mark_options)
    addplot_options.append(f"error mark options={{{opts}}}")
    

def draw_line2d_errorbars(data, obj, errorbar_data=None):
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
    if errorbar_data:
        addplot_options.extend(_write_errorbar_options(data, errorbar_data, line_xcolor))
    if addplot_options:
        opts = ", ".join(addplot_options)
        content.append(f"[{opts}]\n")

    c, axis_options = _table_errors(obj, data, errorbar_data)
    content += c
    
    if errorbar_data and "label" in errorbar_data:
        content.append(f"\\addlegendentry{{{errorbar_data['label']}}}\n")
    elif legend_text is not None:
        content.append(f"\\addlegendentry{{{legend_text}}}\n")

    return data, content

def _table_errors(obj, data, errorbar_data=None):  # noqa: C901
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
    else:
        if isinstance(xdata_alt[0], str):
            data["current axes"].axis_options += [
                "xtick={{{}}}".format(",".join([f"{x:{ff}}" for x in xdata])),
                "xticklabels={{{}}}".format(",".join(xdata_alt)),
            ]
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
        mindate = num2date(xmin).strftime("%Y-%m-%d %H:%M")
        maxdate = num2date(xmax).strftime("%Y-%m-%d %H:%M")
        data["current axes"].axis_options.append(f"xmin={mindate}, xmax={maxdate}")
    else:
        opts = []
        xformat = ff
        col_sep = " "

    if data["table_row_sep"] != "\n":
        # don't want the \n in the table definition, just in the data (below)
        opts.append("row sep=" + data["table_row_sep"].strip())

    table_row_sep = data["table_row_sep"]
    ydata[ydata_mask] = np.nan
    if np.any(ydata_mask) or ~np.all(np.isfinite(ydata)):
        # matplotlib jumps at masked or nan values, while PGFPlots by default
        # interpolates. Hence, if we have a masked plot, make sure that PGFPlots jumps
        # as well.
        if "unbounded coords=jump" not in data["current axes"].axis_options:
            data["current axes"].axis_options.append("unbounded coords=jump")
    
    ydata_plus_err = [ydata]
    plot_table = [""]
    if errorbar_data and "error_data" in errorbar_data:
        opts.extend(["x=x", "y=y"])
        plot_table[0] += f"x{col_sep}y"
        for key, value in errorbar_data["error_data"].items():
            opts.append(f"{key}={key.replace(' ','')}")
            plot_table[0] += f"{col_sep}{key.replace(' ','')}"
            ydata_plus_err.append(value)
        plot_table[0] += f"{table_row_sep}"
    
    for x, *y in zip(xdata, *ydata_plus_err):
        plot_table.append(f"{x:{xformat}}{col_sep}"+f"{col_sep}".join(f"{y_:{ff}}" for y_ in y)+f"{table_row_sep}")
        

    min_extern_length = 3

    if data["externalize tables"] and len(xdata) >= min_extern_length:
        filepath, rel_filepath = _files.new_filepath(data, "table", ".dat")
        with open(filepath, "w") as f:
            # No encoding handling required: plot_table is only ASCII
            f.write("".join(plot_table))

        if data["externals search path"] is not None:
            esp = data["externals search path"]
            opts.append(f"search path={{{esp}}}")

        opts_str = ("[" + ",".join(opts) + "] ") if len(opts) > 0 else ""
        posix_filepath = rel_filepath.as_posix()
        content.append(f"table {opts_str}{{{posix_filepath}}};\n")
    else:
        if len(opts) > 0:
            opts_str = ",".join(opts)
            content.append(f"table [{opts_str}] {{%\n")
        else:
            content.append("table {%\n")
        content.extend(plot_table)
        content.append("};\n")

    return content, axis_options