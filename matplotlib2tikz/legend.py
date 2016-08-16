# -*- coding: utf-8 -*-
#
import warnings
from . import color as mycol


def draw_legend(data, obj):
    '''Adds legend code.
    '''
    texts = []
    childrenAlignment = []
    for text in obj.texts:
        texts.append('%s' % text.get_text())
        childrenAlignment.append('%s' % text.get_horizontalalignment())

    cont = 'legend entries={{%s}}' % '},{'.join(texts)
    data['extra axis options'].add(cont)

    # Get the location.
    # http://matplotlib.org/api/legend_api.html
    pad = 0.03
    if obj._loc == 0:
        # best
        print('Legend location "best" not yet implemented, choosing "upper',
              'right" instead.')
        position = None
        anchor = None
    elif obj._loc == 1:
        # upper right
        position = None
        anchor = None
    elif obj._loc == 2:
        # upper left
        position = [pad, 1.0 - pad]
        anchor = 'north west'
    elif obj._loc == 3:
        # lower left
        position = [pad, pad]
        anchor = 'south west'
    elif obj._loc == 4:
        # lower right
        position = [1.0 - pad, pad]
        anchor = 'south east'
    elif obj._loc == 5:
        # right
        position = [1.0 - pad, 0.5]
        anchor = 'west'
    elif obj._loc == 6:
        # center left
        position = [3 * pad, 0.5]
        anchor = 'east'
    elif obj._loc == 7:
        # center right
        position = [1.0 - 3 * pad, 0.5]
        anchor = 'west'
    elif obj._loc == 8:
        # lower center
        position = [0.5, 3 * pad]
        anchor = 'south'
    elif obj._loc == 9:
        # upper center
        position = [0.5, 1.0 - 3 * pad]
        anchor = 'north'
    else:
        assert obj._loc == 10
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
    if len(childrenAlignment) > 0:
        alignment = childrenAlignment[0]
    else:
        alignment = None

    for childAlignment in childrenAlignment:
        if alignment != childAlignment:
            warnings.warn(
                'Varying horizontal alignments in the legend. Using default.'
                )
            alignment = None
            break

    # Write styles to data
    if legend_style:
        style = 'legend style={%s}' % ', '.join(legend_style)
        data['extra axis options'].add(style)

    if childAlignment:
        cellAlign = 'legend cell align={%s}' % alignment
        data['extra axis options'].add(cellAlign)

    return data
