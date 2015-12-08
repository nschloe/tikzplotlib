# -*- coding: utf-8 -*-
#
from . import color

import matplotlib as mpl


def draw_path(obj, data, path, draw_options=None, simplify=None):
    '''Adds code for drawing an ordinary path in PGFPlots (TikZ).
    '''
    # For some reasons, matplotlib sometimes adds void paths which consist of
    # only one point and have 0 fill opacity. To not let those clutter the
    # output TeX file, bail out here.
    if len(path.vertices) == 2 and \
            all(path.vertices[0] == path.vertices[1]) and \
            'fill opacity=0' in draw_options:
        return data, ''

    nodes = []
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
        if code == mpl.path.Path.STOP:
            pass
        elif code == mpl.path.Path.MOVETO:
            nodes.append('(axis cs:%.15g,%.15g)' % tuple(vert))
        elif code == mpl.path.Path.LINETO:
            nodes.append('--(axis cs:%.15g,%.15g)' % tuple(vert))
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
            if prev is None:
                raise RuntimeError('Cannot draw quadratic Bezier curves '
                                   'as the beginning of of a path.')
            Q1 = 1. / 3. * prev + 2. / 3. * vert[0:2]
            Q2 = 2. / 3. * vert[0:2] + 1. / 3. * vert[2:4]
            Q3 = vert[2:4]
            nodes.append(('.. controls (axis cs:%.15g,%.15g) ' +
                          'and (axis cs:%.15g,%.15g) ' +
                          '.. (axis cs:%.15g,%.15g)')
                         % (Q1[0], Q1[1], Q2[0], Q2[1], Q3[0], Q3[1])
                         )
        elif code == mpl.path.Path.CURVE4:
            # Cubic Bezier curves.
            nodes.append(('.. controls (axis cs:%.15g,%.15g) ' +
                          'and (axis cs:%.15g,%.15g) ' +
                          '.. (axis cs:%.15g,%.15g)')
                         % tuple(vert)
                         )
        elif code == mpl.path.Path.CLOSEPOLY:
            nodes.append('--cycle')
        else:
            raise RuntimeError('Unknown path code %d. Abort.' % code)
        # Store the previous point for quadratic Beziers.
        prev = vert[0:2]

    nodes_string = '\n'.join(nodes)
    if draw_options:
        path_command = '\\path [%s] %s;\n\n' % \
                       (', '.join(draw_options), nodes_string)
    else:
        path_command = '\\path %s;\n\n' % nodes_string

    return data, path_command


def draw_pathcollection(data, obj):
    '''Returns PGFPlots code for a number of patch objects.
    '''
    content = []
    # TODO Use those properties
    # linewidths = obj.get_linewidths()
    # gather the draw options
    ec = obj.get_edgecolors()
    fc = obj.get_facecolors()
    # TODO always use [0]?
    try:
        ec = ec[0]
    except (TypeError, IndexError):
        ec = None
    try:
        fc = fc[0]
    except (TypeError, IndexError):
        fc = None
    data, draw_options = get_draw_options(data, ec, fc)
    draw_options.extend(['mark=*', 'only marks'])

    if obj.get_offsets() is not None:
        a = '\n'.join([' '.join(map(str, line)) for line in obj.get_offsets()])
        if draw_options:
            content.append('\\addplot [%s] table {%%\n%s\n};\n' %
                           (', '.join(draw_options), a))
        else:
            content.append('\\addplot table {%%\n%s\n};\n' % a)
    elif obj.get_paths():
        # Not sure if we need this here at all.
        for path in obj.get_paths():
            data, cont = _draw_path(
                obj, data, path, draw_options=draw_options
                )
            content.append(cont)
    else:
        raise RuntimeError('Pathcollection without offsets and paths.')
    return data, content


def get_draw_options(data, ec, fc):
    '''Get the draw options for a given (patch) object.
    '''
    draw_options = []

    if ec is not None:
        data, col, ec_rgba = color.mpl_color2xcolor(data, ec)
        if ec_rgba[3] != 0.0:
            # Don't draw if it's invisible anyways.
            draw_options.append('draw=%s' % col)

    if fc is not None:
        data, col, fc_rgba = color.mpl_color2xcolor(data, fc)
        if fc_rgba[3] != 0.0:
            # Don't draw if it's invisible anyways.
            draw_options.append('fill=%s' % col)

    # handle transparency
    if ec is not None and fc is not None and \
       ec_rgba[3] != 1.0 and ec_rgba[3] == fc_rgba[3]:
        draw_options.append('opacity=%.15g' % ec[3])
    else:
        if ec is not None and ec_rgba[3] != 1.0:
            draw_options.append('draw opacity=%.15g' % ec_rgba[3])
        if fc is not None and fc_rgba[3] != 1.0:
            draw_options.append('fill opacity=%.15g' % fc_rgba[3])
    # TODO Use those properties
    # linewidths = obj.get_linewidths()
    return data, draw_options
