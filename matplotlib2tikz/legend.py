# -*- coding: utf-8 -*-
#
import warnings

import numpy

from . import color as mycol


def draw_legend(data, obj):
    '''Adds legend code.
    '''
    texts = []
    children_alignment = []
    for text in obj.texts:
        texts.append('%s' % text.get_text())
        children_alignment.append('%s' % text.get_horizontalalignment())

    cont = 'legend entries={{%s}}' % '},{'.join(texts)
    data['extra axis options'].add(cont)

    # Get the location.
    # http://matplotlib.org/api/legend_api.html
    pad = 0.03
    # pylint: disable=protected-access
    loc = obj._loc
    if loc == 0:
        # best
        # Create a renderer
        from matplotlib.backends import backend_agg
        renderer = backend_agg.RendererAgg(width=obj.figure.get_figwidth(),
                                           height=obj.figure.get_figheight(),
                                           dpi=obj.figure.dpi)

        # Rectangles of the legend and of the axes
        # Lower left and upper right points
        # pylint: disable=protected-access
        x0_legend, x1_legend = \
            obj._legend_box.get_window_extent(renderer).get_points()
        x0_axes, x1_axes = obj.axes.get_window_extent(renderer).get_points()
        dimension_legend = x1_legend - x0_legend
        dimension_axes = x1_axes - x0_axes

        # To determine the actual position of the legend, check which corner
        # (or center) of the legend is closest to the corresponding corner
        # (or center) of the axes box.
        # 1. Key points of the legend
        lower_left_legend = x0_legend
        lower_right_legend = numpy.array([x1_legend[0], x0_legend[1]],
                                         dtype=numpy.float_)
        upper_left_legend = numpy.array([x0_legend[0], x1_legend[1]],
                                        dtype=numpy.float_)
        upper_right_legend = x1_legend
        center_legend = x0_legend + dimension_legend / 2.
        center_left_legend = numpy.array(
            [x0_legend[0], x0_legend[1] + dimension_legend[1] / 2.],
            dtype=numpy.float_)
        center_right_legend = numpy.array(
            [x1_legend[0], x0_legend[1] + dimension_legend[1] / 2.],
            dtype=numpy.float_)
        lower_center_legend = numpy.array(
            [x0_legend[0] + dimension_legend[0] / 2., x0_legend[1]],
            dtype=numpy.float_)
        upper_center_legend = numpy.array(
            [x0_legend[0] + dimension_legend[0] / 2., x1_legend[1]],
            dtype=numpy.float_)

        # 2. Key points of the axes
        lower_left_axes = x0_axes
        lower_right_axes = numpy.array([x1_axes[0], x0_axes[1]],
                                       dtype=numpy.float_)
        upper_left_axes = numpy.array([x0_axes[0], x1_axes[1]],
                                      dtype=numpy.float_)
        upper_right_axes = x1_axes
        center_axes = x0_axes + dimension_axes / 2.
        center_left_axes = numpy.array(
            [x0_axes[0], x0_axes[1] + dimension_axes[1] / 2.],
            dtype=numpy.float_)
        center_right_axes = numpy.array(
            [x1_axes[0], x0_axes[1] + dimension_axes[1] / 2.],
            dtype=numpy.float_)
        lower_center_axes = numpy.array(
            [x0_axes[0] + dimension_axes[0] / 2., x0_axes[1]],
            dtype=numpy.float_)
        upper_center_axes = numpy.array(
            [x0_axes[0] + dimension_axes[0] / 2., x1_axes[1]],
            dtype=numpy.float_)

        # 3. Compute the distances between comparable points.
        distances = {
            1: upper_right_axes - upper_right_legend,  # upper right
            2: upper_left_axes - upper_left_legend,  # upper left
            3: lower_left_axes - lower_left_legend,  # lower left
            4: lower_right_axes - lower_right_legend,  # lower right
            # 5:, Not Implemented  # right
            6: center_left_axes - center_left_legend,  # center left
            7: center_right_axes - center_right_legend,  # center right
            8: lower_center_axes - lower_center_legend,  # lower center
            9: upper_center_axes - upper_center_legend,  # upper center
            10: center_axes - center_legend  # center
        }
        for k, v in distances.items():
            distances[k] = numpy.linalg.norm(v, ord=2)

        # 4. Take the shortest distance between key points as the final
        # location
        loc = min(distances, key=distances.get)

    if loc == 1:
        # upper right
        position = None
        anchor = None
    elif loc == 2:
        # upper left
        position = [pad, 1.0 - pad]
        anchor = 'north west'
    elif loc == 3:
        # lower left
        position = [pad, pad]
        anchor = 'south west'
    elif loc == 4:
        # lower right
        position = [1.0 - pad, pad]
        anchor = 'south east'
    elif loc == 5:
        # right
        position = [1.0 - pad, 0.5]
        anchor = 'east'
    elif loc == 6:
        # center left
        position = [3 * pad, 0.5]
        anchor = 'west'
    elif loc == 7:
        # center right
        position = [1.0 - 3 * pad, 0.5]
        anchor = 'east'
    elif loc == 8:
        # lower center
        position = [0.5, 3 * pad]
        anchor = 'south'
    elif loc == 9:
        # upper center
        position = [0.5, 1.0 - 3 * pad]
        anchor = 'north'
    else:
        assert loc == 10
        # center
        position = [0.5, 0.5]
        anchor = 'center'

    legend_style = []
    if position:
        legend_style.append('at={(%.15g,%.15g)}' % (position[0], position[1]))
    if anchor:
        legend_style.append('anchor=%s' % anchor)

    # Get the edgecolor of the box
    if obj.get_frame_on():
        edgecolor = obj.get_frame().get_edgecolor()
        data, frame_xcolor, _ = mycol.mpl_color2xcolor(data, edgecolor)
        if frame_xcolor != 'black':  # black is default
            legend_style.append('draw=%s' % frame_xcolor)
    else:
        legend_style.append('draw=none')

    # Get the facecolor of the box
    facecolor = obj.get_frame().get_facecolor()
    data, fill_xcolor, _ = mycol.mpl_color2xcolor(data, facecolor)
    if fill_xcolor != 'white':  # white is default
        legend_style.append('fill=%s' % fill_xcolor)

    # Get the horizontal alignment
    try:
        alignment = children_alignment[0]
    except IndexError:
        alignment = None

    for child_alignment in children_alignment:
        if alignment != child_alignment:
            warnings.warn(
                'Varying horizontal alignments in the legend. Using default.'
                )
            alignment = None
            break

    if alignment:
        data['extra axis options'].add(
            'legend cell align={{{}}}'.format(alignment)
            )

    if obj._ncol != 1:
        data['extra axis options'].add(
            'legend columns={}'.format(obj._ncol)
            )

    # Write styles to data
    if legend_style:
        style = 'legend style={%s}' % ', '.join(legend_style)
        data['extra axis options'].add(style)

    return data
