import matplotlib as mpl
import numpy

from . import color
from .axes import _mpl_cmap2pgf_cmap
from .util import get_legend_text, has_legend


def draw_path(data, path, draw_options=None, simplify=None):
    """Adds code for drawing an ordinary path in PGFPlots (TikZ).
    """
    # For some reasons, matplotlib sometimes adds void paths which consist of
    # only one point and have 0 fill opacity. To not let those clutter the
    # output TeX file, bail out here.
    if (
        len(path.vertices) == 2
        and all(path.vertices[0] == path.vertices[1])
        and "fill opacity=0" in draw_options
    ):
        return data, "", None, False

    nodes = []
    ff = data["float format"]
    prev = None
    for vert, code in path.iter_segments(simplify=simplify):
        # nschloe, Oct 2, 2015:
        #   The transform call yields warnings and it is unclear why. Perhaps
        #   the input data is not suitable? Anyhow, this should not happen.
        #   Comment out for now.
        # vert = numpy.asarray(
        #         _transform_to_data_coordinates(obj, [vert[0]], [vert[1]])
        #         )
        # For path codes see: http://matplotlib.org/api/path_api.html
        #
        # if code == mpl.path.Path.STOP: pass
        is_area = False
        if code == mpl.path.Path.MOVETO:
            nodes.append(("(axis cs:" + ff + "," + ff + ")").format(*vert))
        elif code == mpl.path.Path.LINETO:
            nodes.append(("--(axis cs:" + ff + "," + ff + ")").format(*vert))
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
            nodes.append(
                (
                    ".. controls (axis cs:"
                    + ff
                    + ","
                    + ff
                    + ") "
                    + "and (axis cs:"
                    + ff
                    + ","
                    + ff
                    + ") "
                    + ".. (axis cs:"
                    + ff
                    + ","
                    + ff
                    + ")"
                ).format(Q1[0], Q1[1], Q2[0], Q2[1], Q3[0], Q3[1])
            )
        elif code == mpl.path.Path.CURVE4:
            # Cubic Bezier curves.
            nodes.append(
                (
                    ".. controls (axis cs:"
                    + ff
                    + ","
                    + ff
                    + ") "
                    + "and (axis cs:"
                    + ff
                    + ","
                    + ff
                    + ") "
                    + ".. (axis cs:"
                    + ff
                    + ","
                    + ff
                    + ")"
                ).format(*vert)
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
    """Returns PGFPlots code for a number of patch objects.
    """
    content = []
    # gather data
    assert obj.get_offsets() is not None
    labels = ["x" + 21 * " ", "y" + 21 * " "]
    dd = obj.get_offsets()

    draw_options = ["only marks"]
    table_options = []

    if obj.get_array() is not None:
        draw_options.append("scatter")
        dd = numpy.column_stack([dd, obj.get_array()])
        labels.append("colordata" + 13 * " ")
        draw_options.append("scatter src=explicit")
        table_options.extend(["x=x", "y=y", "meta=colordata"])
        ec = None
        fc = None
        ls = None
    else:
        # gather the draw options
        try:
            ec = obj.get_edgecolors()[0]
        except (TypeError, IndexError):
            ec = None

        try:
            fc = obj.get_facecolors()[0]
        except (TypeError, IndexError):
            fc = None

        try:
            ls = obj.get_linestyle()[0]
        except (TypeError, IndexError):
            ls = None

    is_contour = len(dd) == 1
    if is_contour:
        draw_options = ["draw=none"]

    # `only mark` plots don't need linewidth
    data, extra_draw_options = get_draw_options(data, obj, ec, fc, ls, None)
    draw_options.extend(extra_draw_options)

    if obj.get_cmap():
        mycolormap, is_custom_cmap = _mpl_cmap2pgf_cmap(obj.get_cmap(), data)
        draw_options.append("colormap" + ("=" if is_custom_cmap else "/") + mycolormap)

    legend_text = get_legend_text(obj)
    if legend_text is None and has_legend(obj.axes):
        draw_options.append("forget plot")

    for path in obj.get_paths():
        if is_contour:
            dd = path.vertices

        if len(obj.get_sizes()) == len(dd):
            # See Pgfplots manual, chapter 4.25.
            # In Pgfplots, \mark size specifies raddi, in matplotlib circle areas.
            radii = numpy.sqrt(obj.get_sizes() / numpy.pi)
            dd = numpy.column_stack([dd, radii])
            labels.append("sizedata" + 14 * " ")
            draw_options.extend(
                [
                    "visualization depends on="
                    "{\\thisrow{sizedata} \\as\\perpointmarksize}",
                    "scatter/@pre marker code/.append style="
                    "{/tikz/mark size=\\perpointmarksize}",
                ]
            )

        do = " [{}]".format(", ".join(draw_options)) if draw_options else ""
        content.append("\\addplot{}\n".format(do))

        to = " [{}]".format(", ".join(table_options)) if table_options else ""
        content.append("table{}{{%\n".format(to))

        content.append((" ".join(labels)).strip() + "\n")
        ff = data["float format"]
        fmt = (" ".join(dd.shape[1] * [ff])) + "\n"
        for d in dd:
            content.append(fmt.format(*tuple(d)))
        content.append("};\n")

    if legend_text is not None:
        content.append("\\addlegendentry{{{}}}\n".format(legend_text))

    return data, content


def get_draw_options(data, obj, ec, fc, style, width):
    """Get the draw options for a given (patch) object.
    """
    draw_options = []

    if ec is not None:
        data, col, ec_rgba = color.mpl_color2xcolor(data, ec)
        if ec_rgba[3] != 0.0:
            # Don't draw if it's invisible anyways.
            draw_options.append("draw={}".format(col))

    if fc is not None:
        data, col, fc_rgba = color.mpl_color2xcolor(data, fc)
        if fc_rgba[3] != 0.0:
            # Don't draw if it's invisible anyways.
            draw_options.append("fill={}".format(col))

    # handle transparency
    ff = data["float format"]
    if (
        ec is not None
        and fc is not None
        and ec_rgba[3] != 1.0
        and ec_rgba[3] == fc_rgba[3]
    ):
        draw_options.append(("opacity=" + ff).format(ec[3]))
    else:
        if ec is not None and ec_rgba[3] != 1.0:
            draw_options.append(("draw opacity=" + ff).format(ec_rgba[3]))
        if fc is not None and fc_rgba[3] != 1.0:
            draw_options.append(("fill opacity=" + ff).format(fc_rgba[3]))

    if width is not None:
        w = mpl_linewidth2pgfp_linewidth(data, width)
        if w:
            draw_options.append(w)

    if style is not None:
        ls = mpl_linestyle2pgfplots_linestyle(style)
        if ls is not None and ls != "solid":
            draw_options.append(ls)

    return data, draw_options


def mpl_linewidth2pgfp_linewidth(data, line_width):
    if data["strict"]:
        # Takes the matplotlib linewidths, and just translate them into PGFPlots.
        try:
            return {
                0.1: "ultra thin",
                0.2: "very thin",
                0.4: "thin",
                0.6: "semithick",
                0.8: "thick",
                1.2: "very thick",
                1.6: "ultra thick",
            }[line_width]
        except KeyError:
            # explicit line width
            return "line width={}pt".format(line_width)

    # The following is an alternative approach to line widths.
    # The default line width in matplotlib is 1.0pt, in PGFPlots 0.4pt
    # ('thin').
    # Match the two defaults, and scale for the rest.
    scaled_line_width = line_width / 1.0  # scale by default line width
    try:
        out = {
            0.25: "ultra thin",
            0.5: "very thin",
            1.0: None,  # default, 'thin'
            1.5: "semithick",
            2: "thick",
            3: "very thick",
            4: "ultra thick",
        }[scaled_line_width]
    except KeyError:
        # explicit line width
        out = "line width={}pt".format(0.4 * line_width)

    return out


def mpl_linestyle2pgfplots_linestyle(line_style, line=None):
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
    if isinstance(line_style, tuple):
        if line_style[0] is None:
            return None

        if len(line_style[1]) == 2:
            return "dash pattern=on {}pt off {}pt".format(*line_style[1])

        assert len(line_style[1]) == 4
        return "dash pattern=on {}pt off {}pt on {}pt off {}pt".format(*line_style[1])

    if isinstance(line, mpl.lines.Line2D) and line.is_dashed():
        # see matplotlib.lines.Line2D.set_dashes

        # get defaults
        default_dashOffset, default_dashSeq = mpl.lines._get_dash_pattern(line_style)

        # get dash format of line under test
        dashSeq = line._us_dashSeq
        dashOffset = line._us_dashOffset

        lst = list()
        if dashSeq != default_dashSeq:
            # generate own dash sequence
            format_string = " ".join(len(dashSeq) // 2 * ["on {}pt off {}pt"])
            lst.append("dash pattern=" + format_string.format(*dashSeq))

        if dashOffset != default_dashOffset:
            lst.append("dash phase={}pt".format(dashOffset))

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
