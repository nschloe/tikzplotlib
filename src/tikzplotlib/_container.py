import matplotlib as mpl
import datetime
import numpy as np
from matplotlib.dates import num2date
from matplotlib.lines import Line2D

from . import _color as mycol
from ._markers import _mpl_marker2pgfp_marker
from ._line2d import _marker
from . import _path as mypath
from . import _files
from ._util import get_legend_text, has_legend, transform_to_data_coordinates

def sort(obj):
    if isinstance(obj, mpl.container.BarContainer):
        return 0
    elif isinstance(obj,  mpl.container.ErrorbarContainer):
        return 1
    elif isinstance(obj, mpl.container.StemContainer):
        return 2
    

def draw_container(data, mpl_container):
    """
    Takes a matplotlib Container object and produces the corresponding pgfplots
    output. zorder is taken from the "main" component of each container object.

    """
    if isinstance(mpl_container,  mpl.container.ErrorbarContainer):
        container = ErrorBarContainer(data, mpl_container)
        data, content = container(data)
    elif isinstance(mpl_container,  mpl.container.BarContainer):
        container = BarContainer(data, mpl_container)
        data, content = container(data)        
    else:
        content = []   
    
    return data, content, mpl_container[0].get_zorder()

class Container:
    """
    Parentclass for all representations of mpl container objects.
    """
    def __init__(self, data, mpl_container):
        self.get_label = mpl_container.get_label
        self.mpl_container = mpl_container
        self.error_data = {}
        self.extra_options = []
        self.errorbar_options = []
        # ensure children are not printed twice
        data["container elements"].update(mpl_container.get_children()) 
            
    
    def extract_errorbar_data(self, data, errorbar_container, xy_data=None):
        """
        Error data can be included both in pure errorbar containers as well as 
        in bar plots. This method takes an ErrorBarContainer object as input 
        and extracts the actual error data as well as all required pgfplots 
        options.
        """
        data_line, caplines, barlinecols = errorbar_container
        
        if data_line is None:
            xdata, ydata = xy_data.T
            color = "none"
        else:   
            color = data_line.get_color()
            xdata, ydata = data_line.get_xydata().T
        data, line_xcolor, _ = mycol.mpl_color2xcolor(data, color)
        
        style_options = []
        error_data = {}
        
        # Extract the actual numeric error values from the bar objects
        if errorbar_container.has_xerr:
            bar = barlinecols[0]
            data, style_options, xplus, xminus = _extract_error_from_barline(data, bar)
            error_data["x error plus"] = xplus - xdata
            error_data["x error minus"] = xdata - xminus
        if errorbar_container.has_yerr:
            if errorbar_container.has_xerr:
                bar = barlinecols[1]
            else:
                bar = barlinecols[0]
            data, style_options, yplus, yminus = _extract_error_from_barline(data, bar)
            error_data["y error plus"] = yplus - ydata
            error_data["y error minus"] = ydata - yminus
        
        self.error_data = error_data
        
        # Gather all pgfplots options
        caps_obj = caplines[0] if caplines else None        
        self.errorbar_options += _errorbar_options(data, error_data, line_xcolor, caps_obj)
        self.errorbar_options.append(f"error bar style={{{', '.join(style_options)}}}")
        data["container elements"].update(errorbar_container.get_children())
        

class ErrorBarContainer(Container):
    """
    Contains error data and plot options to produce an errorbar plot in pgfplots.
    """
    
    def __init__(self, data, mpl_container):
        super().__init__(data, mpl_container)
        self.extract_errorbar_data(data, mpl_container)     
    
    def __call__(self, data):
        """
        Print out the pgfplots commands and options as a list.
        """
        data, content = draw_line2d_errorbars(data, self.mpl_container[0], self)        
        return data, content


class BarContainer(Container):
    """
    Contains error data and plot options to produce a bar plot in pgfplots.
    """
    
    def __init__(self, data, mpl_container):
        super().__init__(data, mpl_container)
    
        if mpl_container.orientation == "vertical":
            self.extra_options += ["ybar", "ybar legend"]
        elif mpl_container.orientation == "horizontal":
            self.extra_options += ["xbar", "xbar legend"]
        
        ydata = mpl_container.datavalues
        xdata = []
        for patch in mpl_container.get_children():
        # Gather the draw options.
            data, draw_options = mypath.get_draw_options(
                data,
                patch,
                patch.get_edgecolor(),
                patch.get_facecolor(),
                patch.get_linestyle(),
                patch.get_linewidth(),
                patch.get_hatch(),
            )
            width = patch.get_width()
            xdata.append(patch.get_x() + 0.5 * width)
        xdata = np.array(xdata)
        
        if mpl_container.errorbar:
            xy_data = np.vstack([xdata,ydata]).T
            self.extract_errorbar_data(data, mpl_container.errorbar, xy_data)
            data["container elements"].add(mpl_container.errorbar) 
        
        ff = data["float format"]
        self.extra_options.append(f"bar width={width:{ff}}")
        self.extra_options += draw_options
        self.xdata = np.array(xdata)
        self.ydata = ydata
                
    
    def __call__(self, data):
        """
        Print out the pgfplots commands and options as a list.
        """
        # create dummy Line2D object to be able to use draw_line2d
        line_obj = Line2D(self.xdata, self.ydata)
        line_obj.set_label(self.get_label())
        line_obj.axes = data["current mpl axes obj"]
        line_obj.set_transform(line_obj.axes.transData)
        line_obj.set_color(self.mpl_container[0].get_facecolor())
        data, content = draw_line2d_errorbars(data, line_obj, self)
    
        return data, content
        
    
def _errorbar_options(data, error_data, line_xcolor, caps_obj):
    """
    Collects all necessary options for the formating of the error bars 
    including caps.
    """
    content = ['error bars/.cd']
    
    # define error bar directions from the error data
    for xy in ['x','y']:
        content.extend(_collect_error_directions(error_data, xy))
    
    if not caps_obj:
        content.append("error mark=none")
    else:
        content.extend(_extract_from_caps(data, caps_obj, line_xcolor))
    
    return content
    
        
def _extract_error_from_barline(data, line_collection):
    """
    Takes a line collection object as used by an errorbar plot, collects the 
    drawing options and the upper and lower error data.
    """
    color = line_collection.get_edgecolors()[0]
    style = line_collection.get_linestyles()[0]
    width = line_collection.get_linewidths()[0]
    paths = line_collection.get_paths()
    
    data, options = mypath.get_draw_options(data, paths[0], color, None, style, width)
    
    upper_err, lower_err = [], []
    for path in paths:
        errs = path.vertices
        # the error dimension (x or y) is determined form the difference that is not zero
        upper_err.append(max(errs[errs - errs[::-1] != 0]))
        lower_err.append(min(errs[errs - errs[::-1] != 0]))
    
    return data, options, np.array(upper_err), np.array(lower_err)

def _extract_from_caps(data, caps_obj, line_xcolor):
    """
    caps_obj is actually a mpl Line2D object that holds the error markers. 
    Marker shape as well as drawing options are extracted and returned.
    """
    content = []
    marker_face_color = caps_obj.get_markerfacecolor()

    is_filled = marker_face_color is not None and not (
        isinstance(marker_face_color, str) and marker_face_color.lower() == "none"
    )
    data, marker, extra_mark_options = _mpl_marker2pgfp_marker(
        data, caps_obj.get_marker(), is_filled
    )
    
    if marker:
        # pgfplot rotates the marker, mpl does not
        if marker == "-":
            marker = "|"
        content.append("error mark=" + marker)
        marker_options = _collect_error_marker_options(data, caps_obj, marker, 
                                                     line_xcolor, 
                                                     extra_mark_options)
        content.append(f"error mark options={{{', '.join(marker_options)}}}")

    return content


def _collect_error_directions(error_data, xy):
    """
    Helper function to add the error bar directions to the plot options if the
    corresponding data is in present in the error_data dict.
    """
    content = []
    if f'{xy} error plus' in error_data or f'{xy} error minus' in error_data:
        content.append(f'{xy} explicit')
    if f'{xy} error plus' in error_data:
        if f'{xy} error plus' in error_data:
            content.append(f'{xy} dir=both')
        else:
            content.append(f'{xy} dir=plus, ')
    elif f'{xy} error minus' in error_data:
        content.append(f'{xy} dir=minus')
    return content
    

def _collect_error_marker_options(data, obj, marker, line_xcolor, extra_mark_options=[]):
    """
    Collects marker options, derived from _line2d.marker.
    """
    content = []
    content.append("solid")
    
    mark_size = obj.get_markersize()
    if mark_size:
        ff = data["float format"]
        # setting half size because pgfplots counts the radius/half-width
        pgf_size = 0.25 * mark_size
        content.append(f"mark size={pgf_size:{ff}}")
    
    mark_every = obj.get_markevery()
    if mark_every:
        if type(mark_every) is int:
            content.append(f"mark repeat={mark_every:d}")
        else:
            # python starts at index 0, pgfplots at index 1
            pgf_marker = [1 + m for m in mark_every]
            content.append(
                "mark indices = {" + ", ".join(map(str, pgf_marker)) + "}"
            )
            
    content += extra_mark_options
    
    marker_face_color = obj.get_markerfacecolor()
    marker_edge_color = obj.get_markeredgecolor()
    
    for color, filltype in zip([marker_face_color,marker_edge_color], ["fill","draw"]):
        if color is None or (
            isinstance(color, str) and color == "none"
        ):
            content.append("fill opacity=0")
        else:
            data, xcolor, _ = mycol.mpl_color2xcolor(data, color)
            if xcolor != line_xcolor:
                content.append(f"{filltype}=" + xcolor)
    return content
    

def draw_line2d_errorbars(data, obj, container=None):
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
    legend_text = get_legend_text(container, data["current mpl axes obj"]) if container else get_legend_text(obj)
    if legend_text is None and has_legend(data["current mpl axes obj"]):
        addplot_options.append("forget plot")

    # process options
    content.append("\\addplot ")
    if container:
        addplot_options += container.extra_options + container.errorbar_options
    opts = ", ".join(addplot_options)
    content.append(f"[{opts}]\n")

    c, axis_options = _table_errors(obj, data, container.error_data)
    content += c
    
    if legend_text is not None:
        content.append(f"\\addlegendentry{{{legend_text}}}\n")

    return data, content

def _table_errors(obj, data, error_data=None):  # noqa: C901
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
            data["current axes"].axis_options.append(
                "xtick={{{}}}".format(",".join([f"{x:{ff}}" for x in xdata])),
                "xticklabels={{{}}}".format(",".join(xdata_alt)),
            )
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
    if error_data:
        opts.extend(["x=x", "y=y"])
        plot_table[0] += f"x{col_sep}y"
        for key, value in error_data.items():
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