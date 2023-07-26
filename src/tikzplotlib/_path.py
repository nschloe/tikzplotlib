import matplotlib as mpl
import numpy as np
from matplotlib.dates import DateConverter, num2date
from matplotlib.markers import MarkerStyle

from . import _color, _files
from ._axes import _mpl_cmap2pgf_cmap
from ._hatches import _mpl_hatch2pgfp_pattern
from ._markers import _mpl_marker2pgfp_marker
from ._util import get_legend_text, has_legend


def draw_path(data, path, draw_options=None, simplify=None):
    """Adds code for drawing an ordinary path in PGFPlots (TikZ)."""
    # For some reasons, matplotlib sometimes adds void paths which consist of
    # only one point and have 0 fill opacity. To not let those clutter the
    # output TeX file, bail out here.
    if (
        len(path.vertices) == 2
        and all(path.vertices[0] == path.vertices[1])
        and "fill opacity=0" in draw_options
    ):
        return data, "", None, False

    x_is_date = isinstance(data["current mpl axes obj"].xaxis.converter, DateConverter)
    nodes = []
    ff = data["float format"]
    xformat = "" if x_is_date else ff
    prev = None
    is_area = None
    for vert, code in path.iter_segments(simplify=simplify):
        # nschloe, Oct 2, 2015:
        #   The transform call yields warnings and it is unclear why. Perhaps
        #   the input data is not suitable? Anyhow, this should not happen.
        #   Comment out for now.
        # vert = np.asarray(
        #         _transform_to_data_coordinates(obj, [vert[0]], [vert[1]])
        #         )
        # For path codes see: http://matplotlib.org/api/path_api.html
        #
        # if code == mpl.path.Path.STOP: pass
        is_area = False
        if code == mpl.path.Path.MOVETO:
            if x_is_date:
                vert = [num2date(vert[0]), vert[1]]
            nodes.append(f"(axis cs:{vert[0]:{xformat}},{vert[1]:{ff}})")
        elif code == mpl.path.Path.LINETO:
            if x_is_date:
                vert = [num2date(vert[0]), vert[1]]
            nodes.append(f"--(axis cs:{vert[0]:{xformat}},{vert[1]:{ff}})")
        elif code == mpl.path.Path.CURVE3:
            # Quadratic Bezier curves aren't natively supported in TikZ, but
            # can be emulated as cubic Beziers.
            # From
            # http://www.latex-community.org/forum/viewtopic.php?t=4424&f=45:
            # If you really need a quadratic Bézier curve on the points P0, P1
            # and P2, then a process called 'degree elevation' yields the cubic
            # control points (Q0, Q1, Q2 and Q3) as follows:
            #   CODE: SELECT ALL
            #   Q0 = P0
            #   Q1 = 1/3 P0 + 2/3 P1
            #   Q2 = 2/3 P1 + 1/3 P2
            #   Q3 = P2
            #
            # P0 is the point of the previous step which is needed to compute
            # Q1.
            #
            # Cannot draw quadratic Bezier curves as the beginning of of a path
            assert prev is not None
            Q1 = 1.0 / 3.0 * prev + 2.0 / 3.0 * vert[0:2]
            Q2 = 2.0 / 3.0 * vert[0:2] + 1.0 / 3.0 * vert[2:4]
            Q3 = vert[2:4]
            if x_is_date:
                Q1 = [num2date(Q1[0]), Q1[1]]
                Q2 = [num2date(Q2[0]), Q2[1]]
                Q3 = [num2date(Q3[0]), Q3[1]]
            nodes.append(
                ".. controls "
                f"(axis cs:{Q1[0]:{xformat}},{Q1[1]:{ff}}) and "
                f"(axis cs:{Q2[0]:{xformat}},{Q2[1]:{ff}}) .. "
                f"(axis cs:{Q3[0]:{xformat}},{Q3[1]:{ff}})"
            )
        elif code == mpl.path.Path.CURVE4:
            # Cubic Bezier curves.
            if x_is_date:
                vert = [
                    num2date(vert[0]),
                    vert[1],
                    num2date(vert[2]),
                    vert[3],
                    num2date(vert[4]),
                    vert[5],
                ]
            nodes.append(
                ".. controls "
                f"(axis cs:{vert[0]:{xformat}},{vert[1]:{ff}}) and "
                f"(axis cs:{vert[2]:{xformat}},{vert[3]:{ff}}) .. "
                f"(axis cs:{vert[4]:{xformat}},{vert[5]:{ff}})"
            )
        else:
            assert code == mpl.path.Path.CLOSEPOLY
            nodes.append("--cycle")
            is_area = True

        # Store the previous point for quadratic Beziers.
        prev = vert[0:2]

    do = "[{}]".format(", ".join(draw_options)) if draw_options else ""
    path_command = "\\path {}\n{};\n".format(do, "\n".join(nodes))

    return data, path_command, draw_options, is_area


def draw_pathcollection(data, obj):
    """Returns PGFPlots code for a number of patch objects."""
    content = []
    # gather data
    assert obj.get_offsets() is not None
    labels = ["x", "y"]
    dd = obj.get_offsets()

    fmt = "{:" + data["float format"] + "}"
    dd_strings = np.array([[fmt.format(val) for val in row] for row in dd])

    draw_options = ["only marks"]
    table_options = []

    is_filled = False

    if obj.get_array() is not None:
        dd_strings = np.column_stack([dd_strings, obj.get_array()])
        labels.append("colordata")
        draw_options.append("scatter src=explicit")
        table_options.extend(["x=x", "y=y", "meta=colordata"])
        ec = None
        fc = None
        ls = None
        marker0 = None
        if obj.get_cmap():
            mycolormap, is_custom_cmap = _mpl_cmap2pgf_cmap(obj.get_cmap(), data)
            draw_options.append("scatter")
            draw_options.append(
                "colormap" + ("=" if is_custom_cmap else "/") + mycolormap
            )
    else:
        # gather the draw options
        add_individual_color_code = False

        try:
            ec = obj.get_edgecolors()
        except TypeError:
            ec = None
        else:
            if len(ec) == 0:
                ec = None
            elif len(ec) == 1:
                ec = ec[0]
            else:
                assert len(ec) == len(dd)
                labels.append("draw")
                ec_strings = [
                    ",".join(fmt.format(item) for item in row)
                    for row in ec[:, :3] * 255
                ]
                dd_strings = np.column_stack([dd_strings, ec_strings])
                add_individual_color_code = True
                ec = None

        try:
            fc = obj.get_facecolors()
        except TypeError:
            fc = None
        else:
            if len(fc) == 0:
                fc = None
            elif len(fc) == 1:
                fc = fc[0]
                is_filled = True
            else:
                assert len(fc) == len(dd)
                labels.append("fill")
                fc_strings = [
                    ",".join(fmt.format(item) for item in row)
                    for row in fc[:, :3] * 255
                ]
                dd_strings = np.column_stack([dd_strings, fc_strings])
                add_individual_color_code = True
                fc = None
                is_filled = True

        try:
            ls = obj.get_linestyle()[0]
        except (TypeError, IndexError):
            ls = None

        if add_individual_color_code:
            draw_options.extend(
                [
                    "scatter",
                    "visualization depends on={value \\thisrow{draw} \\as \\drawcolor}",
                    "visualization depends on={value \\thisrow{fill} \\as \\fillcolor}",
                    "scatter/@pre marker code/.code={%\n"
                    + "  \\expanded{%\n"
                    + "  \\noexpand\\definecolor{thispointdrawcolor}{RGB}{\\drawcolor}%\n"
                    + "  \\noexpand\\definecolor{thispointfillcolor}{RGB}{\\fillcolor}%\n"
                    + "  }%\n"
                    + "  \\scope[draw=thispointdrawcolor, fill=thispointfillcolor]%\n"
                    + "}",
                    "scatter/@post marker code/.code={%\n  \\endscope\n}",
                ]
            )

        # "solution" from
        # <https://github.com/matplotlib/matplotlib/issues/4672#issuecomment-378702670>
        marker0 = None
        if obj.get_paths():
            p = obj.get_paths()[0]
            ms = {style: MarkerStyle(style) for style in MarkerStyle.markers}
            paths = {
                style: marker.get_path().transformed(marker.get_transform())
                for style, marker in ms.items()
            }
            for marker, path in paths.items():
                if (
                    np.array_equal(path.codes, p.codes)
                    and (path.vertices.shape == p.vertices.shape)
                    and np.max(np.abs(path.vertices - p.vertices)) < 1.0e-10
                ):
                    marker0 = marker
                    break

    is_contour = len(dd) == 1
    if is_contour:
        draw_options = ["draw=none"]

    if marker0 is not None:
        data, pgfplots_marker, marker_options = _mpl_marker2pgfp_marker(
            data, marker0, is_filled
        )
        draw_options += [f"mark={pgfplots_marker}"]
        if marker_options:
            draw_options += ["mark options={{{}}}".format(",".join(marker_options))]

    # `only mark` plots don't need linewidth
    data, extra_draw_options = get_draw_options(data, obj, ec, fc, ls, None)
    draw_options += extra_draw_options

    legend_text = get_legend_text(obj)
    if legend_text is None and has_legend(obj.axes):
        draw_options.append("forget plot")

    for path in obj.get_paths():
        if is_contour:
            dd = path.vertices
            # https://matplotlib.org/stable/api/path_api.html
            codes = (
                path.codes
                if path.codes is not None
                else np.array([1] + [2] * (len(dd) - 1))
            )
            dd_strings = []
            for row, code in zip(dd, codes):
                if code == 1:  # MOVETO
                    # Inserts a newline to trigger "move to" in pgfplots
                    dd_strings.append([])
                dd_strings.append([fmt.format(val) for val in row])
            dd_strings = np.array(dd_strings[1:], dtype=object)

        if len(obj.get_sizes()) == len(dd):
            # See Pgfplots manual, chapter 4.25.
            # In Pgfplots, \mark size specifies radii, in matplotlib circle areas.
            radii = np.sqrt(obj.get_sizes() / np.pi)
            dd_strings = np.column_stack([dd_strings, radii])
            labels.append("sizedata")
            draw_options.extend(
                [
                    "visualization depends on="
                    + "{\\thisrow{sizedata} \\as\\perpointmarksize}",
                    "scatter",
                    "scatter/@pre marker code/.append style="
                    + "{/tikz/mark size=\\perpointmarksize}",
                    # "scatter/@post marker code/.style={}"
                ]
            )

        # remove duplicates
        draw_options = sorted(list(set(draw_options)))

        len_row = sum(len(item) for item in draw_options)
        j0, j1, j2 = ("", ", ", "") if len_row < 80 else ("\n  ", ",\n  ", "\n")
        do = f" [{j0}{{}}{j2}]".format(j1.join(draw_options)) if draw_options else ""
        content.append(f"\\addplot{do}\n")

        if data["externals search path"] is not None:
            esp = data["externals search path"]
            table_options.append(f"search path={{{esp}}}")

        if len(table_options) > 0:
            table_options_str = ", ".join(table_options)
            content.append(f"table [{table_options_str}]{{")
        else:
            content.append("table{")

        plot_table = []
        plot_table.append("  ".join(labels) + "\n")
        for row in dd_strings:
            plot_table.append(" ".join(row) + "\n")

        if data["externalize tables"]:
            filepath, rel_filepath = _files.new_filepath(data, "table", ".dat")
            with open(filepath, "w") as f:
                # No encoding handling required: plot_table is only ASCII
                f.write("".join(plot_table))
            content.append(str(rel_filepath))
        else:
            content.append("%\n")
            content.extend(plot_table)

        content.append("};\n")

    if legend_text is not None:
        content.append(f"\\addlegendentry{{{legend_text}}}\n")

    return data, content


def get_draw_options(data, obj, ec, fc, ls, lw, hatch=None):
    """Get the draw options for a given (patch) object.
    Get the draw options for a given (patch) object.
    Input:
        data -
        obj -
        ec - edge color
        fc - face color
        ls - linestyle
        lw - linewidth
        hatch=None - hatch, i.e., pattern within closed path
    Output:
        draw_options - list
    """
    draw_options = []

    if ec is not None:
        data, ec_col, ec_rgba = _color.mpl_color2xcolor(data, ec)
        if ec_rgba[3] > 0:
            draw_options.append(f"draw={ec_col}")
        else:
            draw_options.append("draw=none")

    if fc is not None:
        data, fc_col, fc_rgba = _color.mpl_color2xcolor(data, fc)
        if fc_rgba[3] > 0.0:
            # Don't draw if it's invisible anyways.
            draw_options.append(f"fill={fc_col}")

    # handle transparency
    ff = data["float format"]
    if (
        ec is not None
        and fc is not None
        and ec_rgba[3] != 1.0
        and ec_rgba[3] == fc_rgba[3]
    ):
        draw_options.append(f"opacity={ec[3]:{ff}}")
    else:
        if ec is not None and 0 < ec_rgba[3] < 1.0:
            draw_options.append(f"draw opacity={ec_rgba[3]:{ff}}")
        if fc is not None and 0 < fc_rgba[3] < 1.0:
            draw_options.append(f"fill opacity={fc_rgba[3]:{ff}}")

    if lw is not None:
        lw_ = mpl_linewidth2pgfp_linewidth(data, lw)
        if lw_:
            draw_options.append(lw_)

    if ls is not None:
        ls_ = mpl_linestyle2pgfplots_linestyle(data, ls)
        if ls_ is not None and ls_ != "solid":
            draw_options.append(ls_)

    if hatch is not None:
        # In matplotlib hatches are rendered with edge color and linewidth
        # In PGFPlots patterns are rendered in 'pattern color' which defaults to
        # black and according to opacity fill.
        # No 'pattern line width' option exist.
        # This can be achieved with custom patterns, see _hatches.py

        # There exist an obj.get_hatch_color() method in the mpl API,
        # but it seems to be unused
        try:
            hc = obj._hatch_color
        except AttributeError:  # Fallback to edge color
            if ec is None or ec_rgba[3] == 0.0:
                # Assuming that a hatch marker indicates that hatches are wanted, also
                # when the edge color is (0, 0, 0, 0), i.e., the edge is invisible
                h_col, h_rgba = "black", np.array([0, 0, 0, 1])
            else:
                h_col, h_rgba = ec_col, ec_rgba
        else:
            data, h_col, h_rgba = _color.mpl_color2xcolor(data, hc)
        finally:
            if h_rgba[3] > 0:
                data, pattern = _mpl_hatch2pgfp_pattern(data, hatch, h_col, h_rgba)
                draw_options += pattern

    return data, draw_options


def mpl_linewidth2pgfp_linewidth(data, line_width):
    # PGFplots gives line widths in pt, matplotlib in axes space. Translate.
    # Scale such that the default mpl line width (1.5) is mapped to the PGFplots
    # line with semithick, 0.6. From a visual comparison, semithick or even thick
    # matches best with the default mpl style.
    # Keep the line with in units of decipoint to make sure we stay in integers.
    line_width_decipoint = line_width * 4  # 4 = 10 * 0.6 / 1.5
    try:
        # https://github.com/pgf-tikz/pgf/blob/e9c22dc9fe48f975b7fdb32181f03090b3747499/tex/generic/pgf/frontendlayer/tikz/tikz.code.tex#L1574
        return {
            1: "ultra thin",
            2: "very thin",
            4: None,  # "thin",
            6: "semithick",
            8: "thick",
            12: "very thick",
            16: "ultra thick",
        }[line_width_decipoint]
    except KeyError:
        # explicit line width
        ff = data["float format"]
        return f"line width={line_width_decipoint / 10:{ff}}pt"


def mpl_linestyle2pgfplots_linestyle(data, line_style, line=None):
    """Translates a line style of matplotlib to the corresponding style
    in PGFPlots.
    """
    # linestyle is a string or dash tuple. Legal string values are
    # solid|dashed|dashdot|dotted.  The dash tuple is (offset, onoffseq) where onoffseq
    # is an even length tuple of on and off ink in points.
    #
    # solid: [(None, None), (None, None), ..., (None, None)]
    # dashed: (0, (6.0, 6.0))
    # dotted: (0, (1.0, 3.0))
    # dashdot: (0, (3.0, 5.0, 1.0, 5.0))
    ff = data["float format"]
    if isinstance(line_style, tuple):
        if line_style[0] is None or line_style[1] is None:
            return None

        if len(line_style[1]) == 2:
            return (
                "dash pattern="
                f"on {line_style[1][0]:{ff}}pt off {line_style[1][1]:{ff}}pt"
            )

        assert len(line_style[1]) == 4
        return (
            "dash pattern="
            f"on {line_style[1][0]:{ff}}pt "
            f"off {line_style[1][1]:{ff}}pt "
            f"on {line_style[1][2]:{ff}}pt "
            f"off {line_style[1][3]:{ff}}pt"
        )

    if isinstance(line, mpl.lines.Line2D) and line.is_dashed():
        # see matplotlib.lines.Line2D.set_dashes

        # get defaults
        default_dashOffset, default_dashSeq = mpl.lines._get_dash_pattern(line_style)

        # get dash format of line under test
        try:
            dashOffset, dashSeq = line._unscaled_dash_pattern[:2]
        except AttributeError:
            # backwards-compatibility with matplotlib < 3.6.0
            dashSeq = line._us_dashSeq
            dashOffset = line._us_dashOffset

        lst = list()
        if dashSeq != default_dashSeq:
            # generate own dash sequence
            lst.append(
                "dash pattern="
                + " ".join(
                    f"on {a:{ff}}pt off {b:{ff}}pt"
                    for a, b in zip(dashSeq[0::2], dashSeq[1::2])
                )
            )

        if dashOffset != default_dashOffset:
            lst.append(f"dash phase={dashOffset}pt")

        if len(lst) > 0:
            return ", ".join(lst)

    return {
        "": None,
        "None": None,
        "none": None,  # happens when using plt.boxplot()
        "-": "solid",
        "solid": "solid",
        ":": "dotted",
        "--": "dashed",
        "-.": "dash pattern=on 1pt off 3pt on 3pt off 3pt",
    }[line_style]
