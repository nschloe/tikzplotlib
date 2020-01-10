import matplotlib as mpl

from . import _path as mypath
from ._text import _get_arrow_style


def draw_patch(data, obj):
    """Return the PGFPlots code for patches.
    """
    if isinstance(obj, mpl.patches.FancyArrowPatch):
        data, draw_options = mypath.get_draw_options(
            data,
            obj,
            obj.get_edgecolor(),
            # get_fillcolor for the arrow refers to the head, not the path
            None,
            obj.get_linestyle(),
            obj.get_linewidth(),
            obj.get_hatch(),
        )
        return _draw_fancy_arrow(data, obj, draw_options)

    # Gather the draw options.
    data, draw_options = mypath.get_draw_options(
        data,
        obj,
        obj.get_edgecolor(),
        obj.get_facecolor(),
        obj.get_linestyle(),
        obj.get_linewidth(),
        obj.get_hatch(),
    )

    if isinstance(obj, mpl.patches.Rectangle):
        # rectangle specialization
        return _draw_rectangle(data, obj, draw_options)
    elif isinstance(obj, mpl.patches.Ellipse):
        # ellipse specialization
        return _draw_ellipse(data, obj, draw_options)
    else:
        # regular patch
        return _draw_polygon(data, obj, draw_options)


def _is_in_legend(obj):
    label = obj.get_label()
    leg = obj.axes.get_legend()
    if leg is None:
        return False
    return label in [txt.get_text() for txt in leg.get_texts()]


def _patch_legend(obj, draw_options, legend_type):
    """ Decorator for handling legend of mpl.Patch """
    legend = ""
    if _is_in_legend(obj):
        # Unfortunately, patch legend entries need \addlegendimage in Pgfplots.
        do = ", ".join([legend_type] + draw_options) if draw_options else ""
        legend += "\\addlegendimage{{{}}}\n\\addlegendentry{{{}}}\n\n".format(
            do, obj.get_label()
        )

    return legend


def draw_patchcollection(data, obj):
    """Returns PGFPlots code for a number of patch objects.
    """
    content = []

    # recompute the face colors
    obj.update_scalarmappable()

    def ensure_list(x):
        return [None] if len(x) == 0 else x

    ecs = ensure_list(obj.get_edgecolor())
    fcs = ensure_list(obj.get_facecolor())
    lss = ensure_list(obj.get_linestyle())
    ws = ensure_list(obj.get_linewidth())

    paths = obj.get_paths()
    for i, path in enumerate(paths):
        # Gather the draw options.
        ec = ecs[i % len(ecs)]
        fc = fcs[i % len(fcs)]
        ls = lss[i % len(lss)]
        w = ws[i % len(ws)]

        data, draw_options = mypath.get_draw_options(data, obj, ec, fc, ls, w)
        data, cont, draw_options, is_area = mypath.draw_path(
            data, path, draw_options=draw_options
        )
        content.append(cont)

    legend_type = "area legend" if is_area else "line legend"
    legend = _patch_legend(obj, draw_options, legend_type) or "\n"
    content.append(legend)

    return data, content


def _draw_polygon(data, obj, draw_options):
    data, content, _, is_area = mypath.draw_path(
        data, obj.get_path(), draw_options=draw_options
    )
    legend_type = "area legend" if is_area else "line legend"
    content += _patch_legend(obj, draw_options, legend_type)

    return data, content


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

    content = (
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

    content += _patch_legend(obj, draw_options, "area legend")

    return data, content


def _draw_circle(data, obj, draw_options):
    """Return the PGFPlots code for circles.
    """
    x, y = obj.center
    ff = data["float format"]
    content = (
        "\\draw[{}] (axis cs:" + ff + "," + ff + ") circle (" + ff + ");\n"
    ).format(",".join(draw_options), x, y, obj.get_radius())
    content += _patch_legend(obj, draw_options, "area legend")

    return data, content


def _draw_fancy_arrow(data, obj, draw_options):
    style = _get_arrow_style(obj, data)
    ff = data["float format"]
    if obj._posA_posB is not None:
        posA, posB = obj._posA_posB
        content = "\\draw[{{}}] (axis cs:{ff},{ff}) -- (axis cs:{ff},{ff});\n".format(
            ff=ff
        ).format(",".join(style), *posA, *posB)
    else:
        data, content, _, _ = mypath.draw_path(
            data, obj._path_original, draw_options=draw_options + style
        )
    content += _patch_legend(obj, draw_options, "line legend")
    return data, content
