import matplotlib as mpl
from matplotlib.patches import ArrowStyle

from . import _color


def draw_text(data, obj):
    """Paints text on the graph.
    """
    content = []
    properties = []
    style = []
    ff = data["float format"]
    if isinstance(obj, mpl.text.Annotation):
        pos = _annotation(obj, data, content)
    else:
        pos = obj.get_position()

    if isinstance(pos, str):
        tikz_pos = pos
    else:
        # from .util import transform_to_data_coordinates
        # pos = transform_to_data_coordinates(obj, *pos)

        if obj.axes:
            # If the coordinates are relative to an axis, use `axis cs`.
            tikz_pos = f"(axis cs:{pos[0]:{ff}},{pos[1]:{ff}})"
        else:
            # relative to the entire figure, it's a getting a littler harder. See
            # <http://tex.stackexchange.com/a/274902/13262> for a solution to the
            # problem:
            tikz_pos = (
                f"({{$(current bounding box.south west)!{pos[0]:{ff}}!"
                "(current bounding box.south east)$}"
                "|-"
                f"{{$(current bounding box.south west)!{pos[1]:{ff}}!"
                "(current bounding box.north west)$})"
            )

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
    if scaling != 1.0:
        properties.append(f"scale={scaling:{ff}}")

    if bbox is not None:
        _bbox(bbox, data, properties, scaling)

    ha = obj.get_ha()
    va = obj.get_va()
    anchor = _transform_positioning(ha, va)
    if anchor is not None:
        properties.append(anchor)
    data, col, _ = _color.mpl_color2xcolor(data, converter.to_rgb(obj.get_color()))
    properties.append(f"text={col}")
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

    if "\n" in text:
        # http://tex.stackexchange.com/a/124114/13262
        properties.append(f"align={ha}")
        # Manipulating the text here is actually against mpl2tikz's policy not
        # to do that. On the other hand, newlines should translate into
        # newlines.
        # We might want to remove this here in the future.
        text = text.replace("\n ", "\\\\")

    content.append(
        "\\draw {pos} node[\n  {props}\n]{{{text}}};\n".format(
            pos=tikz_pos, props=",\n  ".join(properties), text=" ".join(style + [text])
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


def _parse_annotation_coords(ff, coords, xy):
    """ Convert a coordinate name and xy into a tikz coordinate string """
    # todo: add support for all the missing ones
    if coords == "data":
        x, y = xy
        return f"(axis cs:{x:{ff}},{y:{ff}})"
    elif coords == "figure points":
        raise NotImplementedError
    elif coords == "figure pixels":
        raise NotImplementedError
    elif coords == "figure fraction":
        raise NotImplementedError
    elif coords == "axes points":
        raise NotImplementedError
    elif coords == "axes pixels":
        raise NotImplementedError
    elif coords == "axes fraction":
        raise NotImplementedError
    elif coords == "data":
        raise NotImplementedError
    elif coords == "polar":
        raise NotImplementedError
    else:
        # unknown
        raise NotImplementedError


def _get_arrow_style(obj, data):
    # get a style string from a FancyArrowPatch
    arrow_translate = {
        ArrowStyle._style_list["-"]: ["-"],
        ArrowStyle._style_list["->"]: ["->"],
        ArrowStyle._style_list["<-"]: ["<-"],
        ArrowStyle._style_list["<->"]: ["<->"],
        ArrowStyle._style_list["|-|"]: ["|-|"],
        ArrowStyle._style_list["-|>"]: ["-latex"],
        ArrowStyle._style_list["<|-"]: ["latex-"],
        ArrowStyle._style_list["<|-|>"]: ["latex-latex"],
        ArrowStyle._style_list["]-["]: ["|-|"],
        ArrowStyle._style_list["-["]: ["-|"],
        ArrowStyle._style_list["]-"]: ["|-"],
        ArrowStyle._style_list["fancy"]: ["-latex", "very thick"],
        ArrowStyle._style_list["simple"]: ["-latex", "very thick"],
        ArrowStyle._style_list["wedge"]: ["-latex", "very thick"],
    }
    style_cls = type(obj.get_arrowstyle())
    try:
        style = arrow_translate[style_cls]
    except KeyError:
        raise NotImplementedError(f"Unknown arrow style {style_cls}")
    else:
        data, col, _ = _color.mpl_color2xcolor(data, obj.get_ec())
        return style + ["draw=" + col]


def _annotation(obj, data, content):
    ann_xy = obj.xy
    ann_xycoords = obj.xycoords
    ann_xytext = obj.xyann
    ann_textcoords = obj.anncoords

    ff = data["float format"]

    try:
        xy_pos = _parse_annotation_coords(ff, ann_xycoords, ann_xy)
    except NotImplementedError:
        # Anything else except for explicit positioning is not supported yet
        return obj.get_position()

    # special cases only for text_coords
    if ann_textcoords == "offset points":
        x, y = ann_xytext
        unit = "pt"
        text_pos = f"{xy_pos} ++({x:{ff}}{unit},{y:{ff}}{unit})"
    # elif ann_textcoords == "offset pixels":
    #     x, y = ann_xytext
    #     unit = "px"
    #     text_pos = f"{xy_pos} ++({x:{ff}}{unit},{y:{ff}}{unit})"
    else:
        try:
            text_pos = _parse_annotation_coords(ff, ann_xycoords, ann_xytext)
        except NotImplementedError:
            # Anything else except for explicit positioning is not supported yet
            return obj.get_position()

    if obj.arrow_patch:
        style = ",".join(_get_arrow_style(obj.arrow_patch, data))
        the_arrow = ("\\draw[{}] {} -- {};\n").format(style, text_pos, xy_pos)
        content.append(the_arrow)
    return text_pos


def _bbox(bbox, data, properties, scaling):
    bbox_style = bbox.get_boxstyle()
    if bbox.get_fill():
        data, fc, _ = _color.mpl_color2xcolor(data, bbox.get_facecolor())
        if fc:
            properties.append(f"fill={fc}")
    data, ec, _ = _color.mpl_color2xcolor(data, bbox.get_edgecolor())
    if ec:
        properties.append(f"draw={ec}")
    # XXX: This is ugly, too
    ff = data["float format"]
    line_width = bbox.get_lw() * 0.4
    properties.append(f"line width={line_width:{ff}}pt")
    inner_sep = bbox_style.pad * data["font size"]
    properties.append(f"inner sep={inner_sep:{ff}}pt")
    if bbox.get_alpha():
        properties.append("fill opacity={}".format(bbox.get_alpha()))
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
