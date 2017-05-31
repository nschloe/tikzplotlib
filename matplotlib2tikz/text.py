# -*- coding: utf-8 -*-
#
import matplotlib as mpl

from . import color


def draw_text(data, obj):
    '''Paints text on the graph.
    '''
    content = []
    properties = []
    style = []
    if isinstance(obj, mpl.text.Annotation):
        ann_xy = obj.xy
        ann_xycoords = obj.xycoords
        ann_xytext = obj.xyann
        ann_textcoords = obj.anncoords
        if ann_xycoords != 'data' or ann_textcoords != 'data':
            print('Warning: Anything else except for explicit positioning '
                  'is not supported for annotations yet :(')
            return data, content
        else:  # Create a basic tikz arrow
            arrow_style = []
            if obj.arrowprops is not None:
                if obj.arrowprops['arrowstyle'] is not None:
                    if obj.arrowprops['arrowstyle'] in ['-', '->',
                                                        '<-', '<->']:
                        arrow_style.append(obj.arrowprops['arrowstyle'])
                        data, col, _ = color.mpl_color2xcolor(
                            data,
                            obj.arrow_patch.get_ec()
                            )
                        arrow_style.append(col)

            arrow_proto = '\\draw[%s] (axis cs:%.15g,%.15g) ' \
                          '-- (axis cs:%.15g,%.15g);\n'
            the_arrow = arrow_proto % (','.join(arrow_style),
                                       ann_xytext[0], ann_xytext[1],
                                       ann_xy[0], ann_xy[1]
                                       )
            content.append(the_arrow)

    # 1: coordinates
    # 2: properties (shapes, rotation, etc)
    # 3: text style
    # 4: the text
    #                   -------1--------2---3--4--
    pos = obj.get_position()
    text = obj.get_text()
    size = obj.get_size()
    bbox = obj.get_bbox_patch()
    converter = mpl.colors.ColorConverter()
    # without the factor 0.5, the fonts are too big most of the time.
    # TODO fix this
    scaling = 0.5 * size / data['font size']
    if scaling != 1.0:
        properties.append('scale=%.15g' % scaling)

    if bbox is not None:
        bbox_style = bbox.get_boxstyle()
        if bbox.get_fill():
            data, fc, _ = color.mpl_color2xcolor(data, bbox.get_facecolor())
            if fc:
                properties.append('fill=%s' % fc)
        data, ec, _ = color.mpl_color2xcolor(data, bbox.get_edgecolor())
        if ec:
            properties.append('draw=%s' % ec)
        # XXX: This is ugly, too
        properties.append('line width=%.15gpt' % (bbox.get_lw() * 0.4))
        properties.append('inner sep=%.15gpt'
                          % (bbox_style.pad * data['font size'])
                          )
        # Rounded boxes
        if isinstance(bbox_style, mpl.patches.BoxStyle.Round):
            properties.append('rounded corners')
        elif isinstance(bbox_style, mpl.patches.BoxStyle.RArrow):
            data['tikz libs'].add('shapes.arrows')
            properties.append('single arrow')
        elif isinstance(bbox_style, mpl.patches.BoxStyle.LArrow):
            data['tikz libs'].add('shapes.arrows')
            properties.append('single arrow')
            properties.append('shape border rotate=180')
        elif isinstance(bbox_style, mpl.patches.BoxStyle.DArrow):
            data['tikz libs'].add('shapes.arrows')
            properties.append('double arrow')
        elif isinstance(bbox_style, mpl.patches.BoxStyle.Circle):
            properties.append('circle')
        elif isinstance(bbox_style, mpl.patches.BoxStyle.Roundtooth):
            properties.append('decorate')
            properties.append(
                'decoration={snake,amplitude=0.5,segment length=3}'
                )
        elif isinstance(bbox_style, mpl.patches.BoxStyle.Sawtooth):
            properties.append('decorate')
            properties.append(
                'decoration={zigzag,amplitude=0.5,segment length=3}'
                )
        else:
            # TODO Round4
            assert isinstance(bbox_style, mpl.patches.BoxStyle.Square)

        # Line style
        if bbox.get_ls() == 'dotted':
            properties.append('dotted')
        elif bbox.get_ls() == 'dashed':
            properties.append('dashed')
        # TODO Check if there is there any way to extract the dashdot
        # pattern from matplotlib instead of hardcoding
        # an approximation?
        elif bbox.get_ls() == 'dashdot':
            properties.append(('dash pattern=on %.3gpt off %.3gpt on '
                               '%.3gpt off %.3gpt'
                               ) % (1.0 / scaling, 3.0 / scaling,
                                    6.0 / scaling, 3.0 / scaling)
                              )
        else:
            assert bbox.get_ls() == 'solid'

    ha = obj.get_ha()
    va = obj.get_va()
    anchor = _transform_positioning(ha, va)
    if anchor is not None:
        properties.append(anchor)
    data, col, _ = color.mpl_color2xcolor(
            data,
            converter.to_rgb(obj.get_color())
            )
    properties.append('text=%s' % col)
    properties.append('rotate=%.1f' % obj.get_rotation())

    if obj.get_style() == 'italic':
        style.append('\\itshape')
    else:
        assert obj.get_style() == 'normal'

    # From matplotlib/font_manager.py:
    # weight_dict = {
    #     'ultralight' : 100,
    #     'light'      : 200,
    #     'normal'     : 400,
    #     'regular'    : 400,
    #     'book'       : 400,
    #     'medium'     : 500,
    #     'roman'      : 500,
    #     'semibold'   : 600,
    #     'demibold'   : 600,
    #     'demi'       : 600,
    #     'bold'       : 700,
    #     'heavy'      : 800,
    #     'extra bold' : 800,
    #     'black'      : 900}
    if obj.get_weight() > 550:
        style.append('\\bfseries')

    if obj.axes:
        # If the coordinates are relative to an axis, use `axis cs`.
        tikz_pos = '(axis cs:%.15g,%.15g)' % pos
    else:
        # relative to the entire figure, it's a getting a littler harder. See
        # <http://tex.stackexchange.com/a/274902/13262> for a solution to the
        # problem:
        tikz_pos = (
            '({$(current bounding box.south west)!%.15g!'
            '(current bounding box.south east)$}'
            '|-'
            '{$(current bounding box.south west)!%0.15g!'
            '(current bounding box.north west)$})'
            ) % pos

    if '\n' in text:
        # http://tex.stackexchange.com/a/124114/13262
        properties.append('align=%s' % ha)
        # Manipulating the text here is actually against mpl2tikz's policy not
        # to do that. On the other hand, newlines should translate into
        # newlines.
        # We might want to remove this here in the future.
        text = text.replace('\n ', '\\\\')

    content.append(
            '\\node at %s[\n  %s\n]{%s %s};\n' %
            (tikz_pos, ',\n  '.join(properties), ' '.join(style), text)
            )
    return data, content


def _transform_positioning(ha, va):
    '''Converts matplotlib positioning to pgf node positioning.
    Not quite accurate but the results are equivalent more or less.'''
    if ha == 'center' and va == 'center':
        return None

    ha_mpl_to_tikz = {
            'right': 'east',
            'left': 'west',
            'center': ''
            }
    va_mpl_to_tikz = {
            'top': 'north',
            'bottom': 'south',
            'center': '',
            'baseline': 'base'
            }
    return (
        'anchor=%s %s' % (va_mpl_to_tikz[va], ha_mpl_to_tikz[ha])
        ).strip()
