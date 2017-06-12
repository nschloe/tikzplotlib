# -*- coding: utf-8 -*-
#
import matplotlib as mpl

from . import path as mypath


def draw_patch(data, obj):
    '''Return the PGFPlots code for patches.
    '''
    # Gather the draw options.
    data, draw_options = mypath.get_draw_options(
            data,
            obj.get_edgecolor(),
            obj.get_facecolor()
            )

    if isinstance(obj, mpl.patches.Rectangle):
        # rectangle specialization
        return _draw_rectangle(data, obj, draw_options)
    elif isinstance(obj, mpl.patches.Ellipse):
        # ellipse specialization
        return _draw_ellipse(data, obj, draw_options)

    # regular patch
    return mypath.draw_path(
        data, obj.get_path(), draw_options=draw_options
        )


def draw_patchcollection(data, obj):
    '''Returns PGFPlots code for a number of patch objects.
    '''
    content = []
    # Gather the draw options.
    try:
        edge_color = obj.get_edgecolor()[0]
    except IndexError:
        edge_color = None

    try:
        face_color = obj.get_facecolor()[0]
    except IndexError:
        face_color = None

    data, draw_options = mypath.get_draw_options(
            data, edge_color, face_color
            )
    for path in obj.get_paths():
        data, cont = mypath.draw_path(
            data, path, draw_options=draw_options
            )
        content.append(cont)
    return data, content


def _draw_rectangle(data, obj, draw_options):
    '''Return the PGFPlots code for rectangles.
    '''

    # Objects with labels are plot objects (from bar charts, etc).
    # Even those without labels explicitly set have a label of
    # "_nolegend_".  Everything else should be skipped because
    # they likely correspong to axis/legend objects which are
    # handled by PGFPlots
    label = obj.get_label()
    if label == '':
        return data, []

    # get real label, bar charts by default only give rectangles
    # labels of "_nolegend_"
    # See
    # <http://stackoverflow.com/questions/35881290/how-to-get-the-label-on-bar-plot-stacked-bar-plot-in-matplotlib>
    handles, labels = obj.axes.get_legend_handles_labels()
    labelsFound = [
        label for h, label in zip(handles, labels) if obj in h.get_children()
        ]
    if len(labelsFound) == 1:
        label = labelsFound[0]

    legend = ''
    if label != '_nolegend_' and label not in data['rectangle_legends']:
        data['rectangle_legends'].add(label)
        legend = (
            '\\addlegendimage{ybar,ybar legend,%s};\n'
            ) % (','.join(draw_options))

    left_lower_x = obj.get_x()
    left_lower_y = obj.get_y()
    cont = ('%s\\draw[%s] (axis cs:%.15g,%.15g) '
            'rectangle (axis cs:%.15g,%.15g);\n'
            ) % (legend,
                 ','.join(draw_options),
                 left_lower_x,
                 left_lower_y,
                 left_lower_x + obj.get_width(),
                 left_lower_y + obj.get_height()
                 )
    return data, cont


def _draw_ellipse(data, obj, draw_options):
    '''Return the PGFPlots code for ellipses.
    '''
    if isinstance(obj, mpl.patches.Circle):
        # circle specialization
        return _draw_circle(data, obj, draw_options)
    x, y = obj.center
    cont = '\\draw[%s] (axis cs:%.15g,%.15g) ellipse (%.15g and %.15g);\n' % \
        (','.join(draw_options),
         x, y,
         0.5 * obj.width, 0.5 * obj.height
         )
    return data, cont


def _draw_circle(data, obj, draw_options):
    '''Return the PGFPlots code for circles.
    '''
    x, y = obj.center
    cont = '\\draw[%s] (axis cs:%.15g,%.15g) circle (%.15g);\n' % \
        (','.join(draw_options),
         x, y,
         obj.get_radius()
         )
    return data, cont
