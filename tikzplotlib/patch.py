import matplotlib as mpl

from . import path as mypath


def draw_patch(data, obj):
    """Return the PGFPlots code for patches.
    """
    # Gather the draw options.
    data, draw_options = mypath.get_draw_options(
        data,
        obj,
        obj.get_edgecolor(),
        obj.get_facecolor(),
        obj.get_linestyle(),
        obj.get_linewidth(),
    )

    if isinstance(obj, mpl.patches.Rectangle):
        # rectangle specialization
        return _draw_rectangle(data, obj, draw_options)
    elif isinstance(obj, mpl.patches.Ellipse):
        # ellipse specialization
        return _draw_ellipse(data, obj, draw_options)

    # regular patch
    data, path_command, _, _ = mypath.draw_path(
        data, obj.get_path(), draw_options=draw_options
    )
    return data, path_command


def draw_patchcollection(data, obj):
    """Returns PGFPlots code for a number of patch objects.
    """
    content = []
    # Gather the draw options.
    try:
        ec = obj.get_edgecolor()[0]
    except IndexError:
        ec = None

    try:
        fc = obj.get_facecolor()[0]
    except IndexError:
        fc = None

    try:
        ls = obj.get_linestyle()[0]
    except IndexError:
        ls = None

    try:
        w = obj.get_linewidth()[0]
    except IndexError:
        w = None

    data, draw_options = mypath.get_draw_options(data, obj, ec, fc, ls, w)

    paths = obj.get_paths()
    for path in paths:
        data, cont, draw_options, is_area = mypath.draw_path(
            data, path, draw_options=draw_options
        )
        content.append(cont)

    if _is_in_legend(obj):
        # Unfortunately, patch legend entries need \addlegendimage in Pgfplots.
        tpe = "area legend" if is_area else "line legend"
        do = ", ".join([tpe] + draw_options) if draw_options else ""
        content += [
            "\\addlegendimage{{{}}}\n".format(do),
            "\\addlegendentry{{{}}}\n\n".format(obj.get_label()),
        ]
    else:
        content.append("\n")

    return data, content


def _is_in_legend(obj):
    label = obj.get_label()
    leg = obj.axes.get_legend()
    if leg is None:
        return False
    return label in [txt.get_text() for txt in leg.get_texts()]


def _draw_rectangle(data, obj, draw_options):
    """Return the PGFPlots code for rectangles.
    """
    # Objects with labels are plot objects (from bar charts, etc).  Even those without
    # labels explicitly set have a label of "_nolegend_".  Everything else should be
    # skipped because they likely correspong to axis/legend objects which are handled by
    # PGFPlots
    label = obj.get_label()
    if label == "":
        return data, []

    # Get actual label, bar charts by default only give rectangles labels of
    # "_nolegend_". See <https://stackoverflow.com/q/35881290/353337>.
    handles, labels = obj.axes.get_legend_handles_labels()
    labelsFound = [
        label for h, label in zip(handles, labels) if obj in h.get_children()
    ]
    if len(labelsFound) == 1:
        label = labelsFound[0]

    left_lower_x = obj.get_x()
    left_lower_y = obj.get_y()
    ff = data["float format"]
    cont = (
        "\\draw[{}] (axis cs:" + ff + "," + ff + ") "
        "rectangle (axis cs:" + ff + "," + ff + ");\n"
    ).format(
        ",".join(draw_options),
        left_lower_x,
        left_lower_y,
        left_lower_x + obj.get_width(),
        left_lower_y + obj.get_height(),
    )

    if label != "_nolegend_" and label not in data["rectangle_legends"]:
        data["rectangle_legends"].add(label)
        cont += "\\addlegendimage{{ybar,ybar legend,{}}};\n".format(
            ",".join(draw_options)
        )
        cont += "\\addlegendentry{{{}}}\n\n".format(label)
    return data, cont


def _draw_ellipse(data, obj, draw_options):
    """Return the PGFPlots code for ellipses.
    """
    if isinstance(obj, mpl.patches.Circle):
        # circle specialization
        return _draw_circle(data, obj, draw_options)
    x, y = obj.center
    ff = data["float format"]

    if obj.angle != 0:
        fmt = "rotate around={{" + ff + ":(axis cs:" + ff + "," + ff + ")}}"
        draw_options.append(fmt.format(obj.angle, x, y))

    cont = (
        "\\draw[{}] (axis cs:"
        + ff
        + ","
        + ff
        + ") ellipse ("
        + ff
        + " and "
        + ff
        + ");\n"
    ).format(",".join(draw_options), x, y, 0.5 * obj.width, 0.5 * obj.height)
    return data, cont


def _draw_circle(data, obj, draw_options):
    """Return the PGFPlots code for circles.
    """
    x, y = obj.center
    ff = data["float format"]
    cont = ("\\draw[{}] (axis cs:" + ff + "," + ff + ") circle (" + ff + ");\n").format(
        ",".join(draw_options), x, y, obj.get_radius()
    )
    return data, cont
