# -*- coding: utf-8 -*-
#
import matplotlib as mpl
import numpy

from . import color
from .axes import _mpl_cmap2pgf_cmap


def draw_path(data, path, draw_options=None, simplify=None):
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
        #
        # if code == mpl.path.Path.STOP: pass
        if code == mpl.path.Path.MOVETO:
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
            #
            # Cannot draw quadratic Bezier curves as the beginning of of a path
            assert prev is not None
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
        else:
            assert code == mpl.path.Path.CLOSEPOLY
            nodes.append('--cycle')

        # Store the previous point for quadratic Beziers.
        prev = vert[0:2]

    do = '[{}]'.format(', '.join(draw_options)) if draw_options else ''
    path_command = '\\path {} {};\n\n'.format(do, '\n'.join(nodes))

    return data, path_command


def draw_pathcollection(data, obj):
    '''Returns PGFPlots code for a number of patch objects.
    '''
    content = []

    # gather data
    assert obj.get_offsets() is not None
    labels = ['x' + 21*' ', 'y' + 21*' ']
    dd = obj.get_offsets()

    draw_options = ['only marks']
    table_options = []
    if obj.get_array() is not None:
        draw_options.append('scatter')
        dd = numpy.column_stack([dd, obj.get_array()])
        labels.append('colordata' + 13*' ')
        draw_options.append('scatter src=explicit')
        table_options.extend(['x=x', 'y=y', 'meta=colordata'])
        ec = None
        fc = None
    else:
        # gather the draw options
        ec = obj.get_edgecolors()
        fc = obj.get_facecolors()
        try:
            ec = ec[0]
        except (TypeError, IndexError):
            ec = None
        try:
            fc = fc[0]
        except (TypeError, IndexError):
            fc = None

    # TODO Use linewidths
    # linewidths = obj.get_linewidths()
    data, extra_draw_options = get_draw_options(data, ec, fc)
    draw_options.extend(extra_draw_options)

    if obj.get_cmap():
        mycolormap, is_custom_cmap = _mpl_cmap2pgf_cmap(
                obj.get_cmap()
                )
        if is_custom_cmap:
            draw_options.append('colormap=' + mycolormap)
        else:
            draw_options.append('colormap/' + mycolormap)

    if len(obj.get_sizes()) == len(dd):
        # See Pgfplots manual, chapter 4.25.
        # In Pgfplots, \mark size specifies raddi, in matplotlib circle areas.
        radii = numpy.sqrt(obj.get_sizes() / numpy.pi)
        dd = numpy.column_stack([dd, radii])
        labels.append('sizedata' + 14*' ')
        draw_options.extend([
            'visualization depends on='
            '{\\thisrow{sizedata} \\as\\perpointmarksize}',
            'scatter/@pre marker code/.append style='
            '{/tikz/mark size=\\perpointmarksize}',
            ])

    do = ' [{}]'.format(', '.join(draw_options)) if draw_options else ''
    content.append('\\addplot{}\n'.format(do))

    to = ' [{}]'.format(', '.join(table_options)) if table_options else ''
    content.append('table{}{{%\n'.format(to))

    content.append((' '.join(labels)).strip() + '\n')
    fmt = (' '.join(dd.shape[1] * ['%+.15e'])) + '\n'
    for d in dd:
        content.append(fmt % tuple(d))
    content.append('};\n')

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
