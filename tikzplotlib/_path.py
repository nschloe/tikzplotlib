import matplotlib as mpl
import numpy
from matplotlib.dates import DateConverter, num2date
from matplotlib.markers import MarkerStyle

from . import _color
from ._axes import _mpl_cmap2pgf_cmap
from ._hatches import _mpl_hatch2pgfp_pattern
from ._markers import _mpl_marker2pgfp_marker
from ._util import get_legend_text, has_legend


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

    x_is_date = isinstance(data["current mpl axes obj"].xaxis.converter, DateConverter)
    nodes = []
    ff = data["float format"]
    xformat = "" if x_is_date else ff
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
        marker0 = None
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

        # "solution" from
        # <https://github.com/matplotlib/matplotlib/issues/4672#issuecomment-378702670>
        p = obj.get_paths()[0]
        ms = {style: MarkerStyle(style) for style in MarkerStyle.markers}
        paths = {
            style: marker.get_path().transformed(marker.get_transform())
            for style, marker in ms.items()
        }
        marker0 = None
        for marker, path in paths.items():
            if (
                numpy.array_equal(path.codes, p.codes)
                and (path.vertices.shape == p.vertices.shape)
                and numpy.max(numpy.abs(path.vertices - p.vertices)) < 1.0e-10
            ):
                marker0 = marker
                break

    is_contour = len(dd) == 1
    if is_contour:
        draw_options = ["draw=none"]

    if marker0 is not None:
        data, pgfplots_marker, marker_options = _mpl_marker2pgfp_marker(
            data, marker0, fc
        )
        draw_options += [f"mark={pgfplots_marker}"] + marker_options

    # `only mark` plots don't need linewidth
    data, extra_draw_options = get_draw_options(data, obj, ec, fc, ls, None)
    draw_options += extra_draw_options

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
        content.append(f"\\addplot{do}\n")

        to = " [{}]".format(", ".join(table_options)) if table_options else ""
        content.append(f"table{to}{{%\n")

        content.append((" ".join(labels)).strip() + "\n")
        ff = data["float format"]
        fmt = (" ".join(dd.shape[1] * ["{:" + ff + "}"])) + "\n"
        for d in dd:
            content.append(fmt.format(*tuple(d)))
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
            draw_options - list, to be ",".join(draw_options) to produce the
                           draw options passed to PGF
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
                h_col, h_rgba = "black", numpy.array([0, 0, 0, 1])
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
            ff = data["float format"]
            return f"line width={line_width:{ff}}pt"

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
        ff = data["float format"]
        out = f"line width={0.4 * line_width:{ff}}pt"

    return out


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
