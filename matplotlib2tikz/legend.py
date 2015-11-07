# -*- coding: utf-8 -*-
#


def draw_legend(data, obj):
    '''Adds legend code to the EXTRA_AXIS_OPTIONS.
    '''
    texts = []
    for text in obj.texts:
        texts.append('%s' % text.get_text())

    cont = 'legend entries={{%s}}' % '},{'.join(texts)
    data['extra axis options'].add(cont)

    # Get the location.
    # http://matplotlib.org/api/legend_api.html
    pad = 0.03
    if obj._loc == 1:
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
    elif obj._loc == 10:
        # center
        position = [0.5, 0.5]
        anchor = 'center'  # does this work?
    else:
        position = None
        anchor = None
        warnings.warn('Unknown legend location ''%r''. Using default.'
                      % obj._loc)

    legend_style = []
    if position:
        legend_style.append('at={(%.15g,%.15g)}' % (position[0], position[1]))
    if anchor:
        legend_style.append('anchor=%s' % anchor)

    if legend_style:
        style = 'legend style={%s}' % ', '.join(legend_style)
        data['extra axis options'].add(style)

    return data
