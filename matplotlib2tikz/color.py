# -*- coding: utf-8 -*-
#
import matplotlib as mpl
import numpy


def mpl_color2xcolor(data, matplotlib_color):
    '''Translates a matplotlib color specification into a proper LaTeX xcolor.
    '''
    # Convert it to RGBA.
    my_col = numpy.array(mpl.colors.ColorConverter().to_rgba(matplotlib_color))

    xcol = None

    # RGB values (as taken from xcolor.dtx):
    available_colors = {
        'red':  numpy.array([1, 0, 0]),
        'green': numpy.array([0, 1, 0]),
        'blue': numpy.array([0, 0, 1]),
        'brown': numpy.array([0.75, 0.5, 0.25]),
        'lime': numpy.array([0.75, 1, 0]),
        'orange': numpy.array([1, 0.5, 0]),
        'pink': numpy.array([1, 0.75, 0.75]),
        'purple': numpy.array([0.75, 0, 0.25]),
        'teal': numpy.array([0, 0.5, 0.5]),
        'violet': numpy.array([0.5, 0, 0.5]),
        'black': numpy.array([0, 0, 0]),
        'darkgray': numpy.array([0.25, 0.25, 0.25]),
        'gray': numpy.array([0.5, 0.5, 0.5]),
        'lightgray': numpy.array([0.75, 0.75, 0.75]),
        'white': numpy.array([1, 1, 1])
        # The colors cyan, magenta, yellow, and olive are also
        # predefined by xcolor, but their RGB approximation of the
        # native CMYK values is not very good. Don't use them here.
        }

    available_colors.update(data['custom colors'])

    # Check if it exactly matches any of the colors already available.
    # This case is actually treated below (alpha==1), but that loop
    # may pick up combinations with black before finding the exact
    # match. Hence, first check all colors.
    for name, rgb in available_colors.items():
        if all(my_col[:3] == rgb):
            xcol = name
            return data, xcol, my_col

    # Check if my_col is a multiple of a predefined color and 'black'.
    for name, rgb in available_colors.items():
        if name == 'black':
            continue

        if rgb[0] != 0.0:
            alpha = my_col[0] / rgb[0]
        elif rgb[1] != 0.0:
            alpha = my_col[1] / rgb[1]
        else:
            assert rgb[2] != 0.0
            alpha = my_col[2] / rgb[2]

        # The cases 0.0 (my_col == black) and 1.0 (my_col == rgb) are
        # already accounted for by checking in available_colors above.
        if all(my_col[:3] == alpha * rgb) and 0.0 < alpha < 1.0:
            xcol = name + ('!%r!black' % (alpha * 100))
            return data, xcol, my_col

    # Lookup failed, add it to the custom list.
    xcol = 'color' + str(len(data['custom colors']))
    data['custom colors'][xcol] = my_col[:3]
    return data, xcol, my_col
