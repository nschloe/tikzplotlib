# -*- coding: utf-8 -*-
#
from . import color
from . import path as mypath

import matplotlib as mpl


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
    else:
        # regular patch
        return mypath.draw_path(
            obj, data, obj.get_path(), draw_options=draw_options
            )


def draw_patchcollection(data, obj):
    '''Returns PGFPlots code for a number of patch objects.
    '''
    content = []
    # Gather the draw options.
    data, draw_options = mypath.get_draw_options(
            data, obj.get_edgecolor()[0], obj.get_facecolor()[0]
            )
    for path in obj.get_paths():
        data, cont = mypath.draw_path(
            obj, data, path, draw_options=draw_options
            )
        content.append(cont)
    return data, content


def _draw_rectangle(data, obj, draw_options):
    '''Return the PGFPlots code for rectangles.
    '''
    if not data['draw rectangles']:
        return data, []

    left_lower_x = obj.get_x()
    left_lower_y = obj.get_y()
    cont = ('\draw[%s] (axis cs:%.15g,%.15g) '
            'rectangle (axis cs:%.15g,%.15g);\n'
            ) % (','.join(draw_options),
                 left_lower_x,
                 left_lower_y,
                 left_lower_x + obj.get_width(),
                 left_lower_y + obj.get_height()
                 )
    return data, cont


def _draw_ellipse(data, obj, draw_options):
    '''Return the PGFPlots code for ellipses.
    '''
    if (isinstance(obj, mpl.patches.Circle)):
        # circle specialization
        return _draw_circle(data, obj, draw_options)
    x, y = obj.center
    cont = '\draw[%s] (axis cs:%.15g,%.15g) ellipse (%.15g and %.15g);\n' % \
        (','.join(draw_options),
         x, y,
         0.5 * obj.width, 0.5 * obj.height
         )
    return data, cont


def _draw_circle(data, obj, draw_options):
    '''Return the PGFPlots code for circles.
    '''
    x, y = obj.center
    cont = '\draw[%s] (axis cs:%.15g,%.15g) circle (%.15g);\n' % \
        (','.join(draw_options),
         x, y,
         obj.get_radius()
         )
    return data, cont
