import matplotlib as mpl

from . import color


def draw_text(data, obj):
    """Paints text on the graph.
    """
    content = []
    properties = []
    style = []
    if isinstance(obj, mpl.text.Annotation):
        _annotation(obj, data, content)

    # 1: coordinates
    # 2: properties (shapes, rotation, etc)
    # 3: text style
    # 4: the text
    #                   -------1--------2---3--4--
    pos = obj.get_position()

    # from .util import transform_to_data_coordinates
    # pos = transform_to_data_coordinates(obj, *pos)

    text = obj.get_text()

    if text in ["", data["current axis title"]]:
        # Text nodes which are direct children of Axes are typically titles.  They are
        # already captured by the `title` property of pgfplots axes, so skip them here.
        return data, content

    size = obj.get_size()
    bbox = obj.get_bbox_patch()
    converter = mpl.colors.ColorConverter()
    # without the factor 0.5, the fonts are too big most of the time.
    # TODO fix this
    scaling = 0.5 * size / data["font size"]
    ff = data["float format"]
    if scaling != 1.0:
        properties.append(("scale=" + ff).format(scaling))

    if bbox is not None:
        _bbox(bbox, data, properties, scaling)

    ha = obj.get_ha()
    va = obj.get_va()
    anchor = _transform_positioning(ha, va)
    if anchor is not None:
        properties.append(anchor)
    data, col, _ = color.mpl_color2xcolor(data, converter.to_rgb(obj.get_color()))
    properties.append("text={}".format(col))
    properties.append("rotate={:.1f}".format(obj.get_rotation()))

    if obj.get_style() == "italic":
        style.append("\\itshape")
    else:
        assert obj.get_style() == "normal"

    # From matplotlib/font_manager.py:
    # weight_dict = {
    #     'ultralight' : 100,
    #     'light'      : 200,
    #     'normal'     : 400,
    #     'regular'    : 400,
    #     'book'       : 400,
    #     'medium'     : 500,
    #     'roman'      : 500,
    #     'semibold'   : 600,
    #     'demibold'   : 600,
    #     'demi'       : 600,
    #     'bold'       : 700,
    #     'heavy'      : 800,
    #     'extra bold' : 800,
    #     'black'      : 900}
    #
    # get_weights returns a numeric value in the range 0-1000 or one of
    # ‘light’, ‘normal’, ‘regular’, ‘book’, ‘medium’, ‘roman’, ‘semibold’,
    # ‘demibold’, ‘demi’, ‘bold’, ‘heavy’, ‘extra bold’, ‘black’
    weight = obj.get_weight()
    if weight in [
        "semibold",
        "demibold",
        "demi",
        "bold",
        "heavy",
        "extra bold",
        "black",
    ] or (isinstance(weight, int) and weight > 550):
        style.append("\\bfseries")

    # \lfseries isn't that common yet
    # elif weight == 'light' or (isinstance(weight, int) and weight < 300):
    #     style.append('\\lfseries')

    if obj.axes:
        # If the coordinates are relative to an axis, use `axis cs`.
        tikz_pos = ("(axis cs:" + ff + "," + ff + ")").format(*pos)
    else:
        # relative to the entire figure, it's a getting a littler harder. See
        # <http://tex.stackexchange.com/a/274902/13262> for a solution to the
        # problem:
        tikz_pos = (
            "({{$(current bounding box.south west)!" + ff + "!"
            "(current bounding box.south east)$}}"
            "|-"
            "{{$(current bounding box.south west)!" + ff + "!"
            "(current bounding box.north west)$}})"
        ).format(*pos)

    if "\n" in text:
        # http://tex.stackexchange.com/a/124114/13262
        properties.append("align={}".format(ha))
        # Manipulating the text here is actually against mpl2tikz's policy not
        # to do that. On the other hand, newlines should translate into
        # newlines.
        # We might want to remove this here in the future.
        text = text.replace("\n ", "\\\\")

    content.append(
        "\\node at {}[\n  {}\n]{{{}}};\n".format(
            tikz_pos, ",\n  ".join(properties), " ".join(style + [text])
        )
    )
    return data, content


def _transform_positioning(ha, va):
    """Converts matplotlib positioning to pgf node positioning.
    Not quite accurate but the results are equivalent more or less."""
    if ha == "center" and va == "center":
        return None

    ha_mpl_to_tikz = {"right": "east", "left": "west", "center": ""}
    va_mpl_to_tikz = {
        "top": "north",
        "bottom": "south",
        "center": "",
        "baseline": "base",
    }
    return "anchor={} {}".format(va_mpl_to_tikz[va], ha_mpl_to_tikz[ha]).strip()


def _annotation(obj, data, content):
    ann_xy = obj.xy
    ann_xycoords = obj.xycoords
    ann_xytext = obj.xyann
    ann_textcoords = obj.anncoords
    if ann_xycoords != "data" or ann_textcoords != "data":
        # Anything else except for explicit positioning is not supported yet
        return data, content
    else:  # Create a basic tikz arrow
        arrow_translate = {
            "-": ["-"],
            "->": ["->"],
            "<-": ["<-"],
            "<->": ["<->"],
            "|-|": ["|-|"],
            "-|>": ["-latex"],
            "<|-": ["latex-"],
            "<|-|>": ["latex-latex"],
            "]-[": ["|-|"],
            "-[": ["-|"],
            "]-": ["|-"],
            "fancy": ["-latex", "very thick"],
            "simple": ["-latex", "very thick"],
            "wedge": ["-latex", "very thick"],
        }
        arrow_style = []
        if obj.arrowprops is not None:
            if obj.arrowprops["arrowstyle"] is not None:
                if obj.arrowprops["arrowstyle"] in arrow_translate:
                    arrow_style += arrow_translate[obj.arrowprops["arrowstyle"]]
                    data, col, _ = color.mpl_color2xcolor(
                        data, obj.arrow_patch.get_ec()
                    )
                    arrow_style.append(col)

        ff = data["float format"]
        arrow_fmt = (
            "\\draw[{}] (axis cs:"
            + ff
            + ","
            + ff
            + ") -- (axis cs:"
            + ff
            + ","
            + ff
            + ");\n"
        )
        the_arrow = arrow_fmt.format(
            ",".join(arrow_style), ann_xytext[0], ann_xytext[1], ann_xy[0], ann_xy[1]
        )
        content.append(the_arrow)
    return


def _bbox(bbox, data, properties, scaling):
    bbox_style = bbox.get_boxstyle()
    if bbox.get_fill():
        data, fc, _ = color.mpl_color2xcolor(data, bbox.get_facecolor())
        if fc:
            properties.append("fill={}".format(fc))
    data, ec, _ = color.mpl_color2xcolor(data, bbox.get_edgecolor())
    if ec:
        properties.append("draw={}".format(ec))
    # XXX: This is ugly, too
    ff = data["float format"]
    properties.append(("line width=" + ff + "pt").format(bbox.get_lw() * 0.4))
    properties.append(
        ("inner sep=" + ff + "pt").format(bbox_style.pad * data["font size"])
    )
    # Rounded boxes
    if isinstance(bbox_style, mpl.patches.BoxStyle.Round):
        properties.append("rounded corners")
    elif isinstance(bbox_style, mpl.patches.BoxStyle.RArrow):
        data["tikz libs"].add("shapes.arrows")
        properties.append("single arrow")
    elif isinstance(bbox_style, mpl.patches.BoxStyle.LArrow):
        data["tikz libs"].add("shapes.arrows")
        properties.append("single arrow")
        properties.append("shape border rotate=180")
    elif isinstance(bbox_style, mpl.patches.BoxStyle.DArrow):
        data["tikz libs"].add("shapes.arrows")
        properties.append("double arrow")
    elif isinstance(bbox_style, mpl.patches.BoxStyle.Circle):
        properties.append("circle")
    elif isinstance(bbox_style, mpl.patches.BoxStyle.Roundtooth):
        properties.append("decorate")
        properties.append("decoration={snake,amplitude=0.5,segment length=3}")
    elif isinstance(bbox_style, mpl.patches.BoxStyle.Sawtooth):
        properties.append("decorate")
        properties.append("decoration={zigzag,amplitude=0.5,segment length=3}")
    else:
        # TODO Round4
        assert isinstance(bbox_style, mpl.patches.BoxStyle.Square)

    # Line style
    if bbox.get_ls() == "dotted":
        properties.append("dotted")
    elif bbox.get_ls() == "dashed":
        properties.append("dashed")
    # TODO Check if there is there any way to extract the dashdot
    # pattern from matplotlib instead of hardcoding
    # an approximation?
    elif bbox.get_ls() == "dashdot":
        properties.append(
            "dash pattern=on {:.3g}pt off {:.3g}pt on {:.3g}pt off {:.3g}pt".format(
                1.0 / scaling, 3.0 / scaling, 6.0 / scaling, 3.0 / scaling
            )
        )
    else:
        assert bbox.get_ls() == "solid"

    return
