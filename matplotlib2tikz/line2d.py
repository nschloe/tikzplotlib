# -*- coding: utf-8 -*-
#
from __future__ import print_function

import six

from . import color as mycol
from . import path as mypath

def get_legend_label_(line):
    '''Check if line is in legend
    '''

    label = line.get_label()
    try:
        ax = line.axes
        leg = ax.get_legend()
        return label in [l.get_label() for l in leg.get_lines()]
    except AttributeError:
        return None

def draw_line2d(data, obj):
    '''Returns the PGFPlots code for an Line2D environment.
    '''
    content = []
    addplot_options = []

    # If line is of length 0, do nothing.  Otherwise, an empty \addplot table
    # will be created, which will be interpreted as an external data source
    # in either the file '' or '.tex'.  Instead, render nothing.
    # pylint: disable=len-as-condition
    if len(obj.get_xdata()) == 0:
        return data, []

    # get the linewidth (in pt)
    line_width = _mpl_linewidth2pgfp_linewidth(data, obj.get_linewidth())

    if line_width:
        addplot_options.append(line_width)

    # get line color
    color = obj.get_color()
    data, line_xcolor, _ = mycol.mpl_color2xcolor(data, color)
    addplot_options.append(line_xcolor)

    alpha = obj.get_alpha()
    if alpha is not None:
        addplot_options.append('opacity=%r' % alpha)

    show_line, linestyle = _mpl_linestyle2pgfp_linestyle(obj.get_linestyle())
    if show_line and linestyle:
        addplot_options.append(linestyle)

    marker_face_color = obj.get_markerfacecolor()
    marker_edge_color = obj.get_markeredgecolor()
    data, marker, extra_mark_options = \
        _mpl_marker2pgfp_marker(data, obj.get_marker(), marker_face_color)
    if marker:
        addplot_options.append('mark=' + marker)

        mark_size = obj.get_markersize()
        if mark_size:
            # setting half size because pgfplots counts the radius/half-width
            pgf_size = int(0.5 * mark_size)
            # make sure we didn't round off to zero by accident
            if pgf_size == 0 and mark_size != 0:
                pgf_size = 1
            addplot_options.append('mark size=%d' % pgf_size)

        mark_every = obj.get_markevery()
        if mark_every:
            addplot_options.append('mark repeat=%d' % mark_every)

        mark_options = ['solid']
        if extra_mark_options:
            mark_options.append(extra_mark_options)
        if marker_face_color is None or \
           (isinstance(marker_face_color, six.string_types) and
               marker_face_color == 'none'):
            mark_options.append('fill opacity=0')
        else:
            data, face_xcolor, _ = mycol.mpl_color2xcolor(
                    data,
                    marker_face_color
                    )
            if face_xcolor != line_xcolor:
                mark_options.append('fill=' + face_xcolor)

        face_and_edge_have_equal_color = \
            marker_edge_color == marker_face_color
        # Sometimes, the colors are given as arrays. Collapse them into a
        # single boolean.
        try:
            face_and_edge_have_equal_color = \
                all(face_and_edge_have_equal_color)
        except TypeError:
            pass

        if not face_and_edge_have_equal_color:
            data, draw_xcolor, _ = mycol.mpl_color2xcolor(
                    data,
                    marker_edge_color
                    )
            if draw_xcolor != line_xcolor:
                mark_options.append('draw=' + draw_xcolor)
        addplot_options.append('mark options={%s}' % ','.join(mark_options))

    if marker and not show_line:
        addplot_options.append('only marks')

    # Check if a line is not in a legend and forget it if so,
    # fixes bug #167:
    if not get_legend_label_(obj):
        addplot_options.append("forget plot")

    # process options
    content.append('\\addplot ')
    if addplot_options:
        options = ', '.join(addplot_options)
        content.append('[' + options + ']\n')

    content.append('table {%\n')

    # nschloe, Oct 2, 2015:
    #   The transform call yields warnings and it is unclear why. Perhaps
    #   the input data is not suitable? Anyhow, this should not happen.
    #   Comment out for now.
    # xdata, ydata = _transform_to_data_coordinates(obj, *obj.get_data())
    xdata, ydata = obj.get_data()

    try:
        has_mask = ydata.mask.any()
    except AttributeError:
        has_mask = 0

    if has_mask:
        # matplotlib jumps at masked images, while PGFPlots by default
        # interpolates. Hence, if we have a masked plot, make sure that
        # PGFPlots jumps as well.
        data['extra axis options'].add('unbounded coords=jump')
        for (x, y, is_masked) in zip(xdata, ydata, ydata.mask):
            if is_masked:
                content.append('%.15g nan\n' % x)
            else:
                content.append('%.15g %.15g\n' % (x, y))
    else:
        for (x, y) in zip(xdata, ydata):
            content.append('%.15g %.15g\n' % (x, y))
    content.append('};\n')

    return data, content


def draw_linecollection(data, obj):
    '''Returns Pgfplots code for a number of patch objects.
    '''
    content = []

    edgecolors = obj.get_edgecolors()
    linestyles = obj.get_linestyles()
    linewidths = obj.get_linewidths()
    paths = obj.get_paths()

    for i, path in enumerate(paths):
        if i < len(edgecolors):
            color = edgecolors[i]
        else:
            color = edgecolors[0]

        if i < len(linestyles):
            style = linestyles[i]
        else:
            style = linestyles[0]

        if i < len(linewidths):
            width = linewidths[i]
        else:
            width = linewidths[0]

        data, options = mypath.get_draw_options(data, color, None)

        width = _mpl_linewidth2pgfp_linewidth(data, width)
        if width:
            options.append(width)

        # linestyle is a string or dash tuple. Legal string values are
        # solid|dashed|dashdot|dotted.  The dash tuple is (offset, onoffseq)
        # where onoffseq is an even length tuple of on and off ink in points.
        #
        # solid: [(None, None), (None, None), ..., (None, None)]
        # dashed: (0, (6.0, 6.0))
        # dotted: (0, (1.0, 3.0))
        # dashdot: (0, (3.0, 5.0, 1.0, 5.0))
        if style[0] is not None:
            assert isinstance(style, tuple)
            if len(style[1]) == 2:
                linestyle = 'dash pattern=on %dpt off %dpt' % \
                            (int(style[1][0]), int(style[1][1]))
            else:
                assert len(style[1]) == 4
                linestyle = 'dash pattern=on %dpt off %dpt on %dpt off %dpt' \
                            % (int(style[1][0]), int(style[1][1]),
                               int(style[1][2]), int(style[1][3]))

            options.append(linestyle)

        # TODO what about masks?
        data, cont = mypath.draw_path(
                data, path,
                draw_options=options,
                simplify=False
                )

        content.append(cont)

    return data, content


TIKZ_LINEWIDTHS = {
        0.1: 'ultra thin',
        0.2: 'very thin',
        0.4: 'thin',
        0.6: 'semithick',
        0.8: 'thick',
        1.2: 'very thick',
        1.6: 'ultra thick'
        }


def _mpl_linewidth2pgfp_linewidth(data, line_width):
    if data['strict']:
        # Takes the matplotlib linewidths, and just translate them
        # into PGFPlots.
        try:
            return TIKZ_LINEWIDTHS[line_width]
        except KeyError:
            # explicit line width
            return 'line width=%spt' % line_width
    else:
        # The following is an alternative approach to line widths.
        # The default line width in matplotlib is 1.0pt, in PGFPlots 0.4pt
        # ('thin').
        # Match the two defaults, and scale for the rest.
        scaled_line_width = line_width / 1.0  # scale by default line width
        literals = {
            0.25: 'ultra thin',
            0.5: 'very thin',
            1.0: None,  # default, 'thin'
            1.5: 'semithick',
            2: 'thick',
            3: 'very thick',
            4: 'ultra thick',
            }

        try:
            out = literals[scaled_line_width]
        except KeyError:
            # explicit line width
            out = 'line width=%rpt' % (0.4 * line_width)

        return out


# for matplotlib markers, see: http://matplotlib.org/api/markers_api.html
_MP_MARKER2PGF_MARKER = {
        '.': '*',  # point
        'o': 'o',  # circle
        '+': '+',  # plus
        'x': 'x',  # x
        'None': None,
        ' ': None,
        '': None
        }

# the following markers are only available with PGF's plotmarks library
_MP_MARKER2PLOTMARKS = {
        'v': ('triangle', 'rotate=180'),  # triangle down
        '1': ('triangle', 'rotate=180'),
        '^': ('triangle', None),  # triangle up
        '2': ('triangle', None),
        '<': ('triangle', 'rotate=270'),  # triangle left
        '3': ('triangle', 'rotate=270'),
        '>': ('triangle', 'rotate=90'),  # triangle right
        '4': ('triangle', 'rotate=90'),
        's': ('square', None),
        'p': ('pentagon', None),
        '*': ('asterisk', None),
        'h': ('star', None),  # hexagon 1
        'H': ('star', None),  # hexagon 2
        'd': ('diamond', None),  # diamond
        'D': ('diamond', None),  # thin diamond
        '|': ('|', None),  # vertical line
        '_': ('-', None)  # horizontal line
        }


def _mpl_marker2pgfp_marker(data, mpl_marker, marker_face_color):
    '''Translates a marker style of matplotlib to the corresponding style
    in PGFPlots.
    '''
    # try default list
    try:
        pgfplots_marker = _MP_MARKER2PGF_MARKER[mpl_marker]
        if (marker_face_color is not None) and pgfplots_marker == 'o':
            pgfplots_marker = '*'
            data['tikz libs'].add('plotmarks')
        marker_options = None
        return (data, pgfplots_marker, marker_options)
    except KeyError:
        pass
    # try plotmarks list
    try:
        data['tikz libs'].add('plotmarks')
        pgfplots_marker, marker_options = _MP_MARKER2PLOTMARKS[mpl_marker]
        if marker_face_color is not None and \
           marker_face_color.lower() != 'none' and \
           pgfplots_marker not in ['|', '-']:
            pgfplots_marker += '*'
        return (data, pgfplots_marker, marker_options)
    except KeyError:
        pass

    # There's no equivalent for the pixel marker in Pgfplots.
    if mpl_marker == ',':
        print('Unsupported marker '','' (pixel).')

    return data, None, None


_MPLLINESTYLE_2_PGFPLOTSLINESTYLE = {
    '': None,
    'None': None,
    'none': None,  # happens when using plt.boxplot()
    '-': None,
    ':': 'dotted',
    '--': 'dashed',
    '-.': 'dash pattern=on 1pt off 3pt on 3pt off 3pt'
    }


def _mpl_linestyle2pgfp_linestyle(line_style):
    '''Translates a line style of matplotlib to the corresponding style
    in PGFPlots.
    '''
    show_line = (line_style != 'None')
    style = _MPLLINESTYLE_2_PGFPLOTSLINESTYLE[line_style]
    return show_line, style


# def _transform_to_data_coordinates(obj, xdata, ydata):
#     '''The coordinates might not be in data coordinates, but could be partly
#     in axes coordinates.  For example, the matplotlib command
#       axes.axvline(2)
#     will have the y coordinates set to 0 and 1, not to the limits. Therefore,
#     a two-stage transform has to be applied:
#       1. first transforming to display coordinates, then
#       2. from display to data.
#     In case of problems (non-invertible, or whatever), print a warning and
#     continue anyways.
#     '''
#     try:
#         import matplotlib.transforms
#         points = numpy.array(zip(xdata, ydata))
#         transform = matplotlib.transforms.composite_transform_factory(
#             obj.get_transform(),
#             obj.axes.transData.inverted()
#             )
#         points_data = transform.transform(points)
#         xdata, ydata = zip(*points_data)
#     except Exception as e:
#         print(xdata, ydata)
#         print(('Problem during transformation:\n' +
#                '   %s\n' +
#                'Continuing with original data.')
#               % e
#               )
#     return (xdata, ydata)
