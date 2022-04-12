import matplotlib as mpl
import numpy as np
import webcolors

# RGB values (as taken from xcolor.dtx):
builtin_colors = {
    "white": [1, 1, 1],
    "lightgray": [0.75, 0.75, 0.75],
    "gray": [0.5, 0.5, 0.5],
    "darkgray": [0.25, 0.25, 0.25],
    "black": [0, 0, 0],
    #
    "red": [1, 0, 0],
    "green": [0, 1, 0],
    "blue": [0, 0, 1],
    "brown": [0.75, 0.5, 0.25],
    "lime": [0.75, 1, 0],
    "orange": [1, 0.5, 0],
    "pink": [1, 0.75, 0.75],
    "purple": [0.75, 0, 0.25],
    "teal": [0, 0.5, 0.5],
    "violet": [0.5, 0, 0.5],
    # The colors cyan, magenta, yellow, and olive are also
    # predefined by xcolor, but their RGB approximation of the
    # native CMYK values is not very good. Don't use them here.
}


def _get_closest_colour_name(rgb):
    match = None
    mindiff = 1.0e15
    for h, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r = int(h[1:3], 16)
        g = int(h[3:5], 16)
        b = int(h[5:7], 16)

        diff = (rgb[0] - r) ** 2 + (rgb[1] - g) ** 2 + (rgb[2] - b) ** 2
        if diff < mindiff:
            match = name
            mindiff = diff

        if mindiff == 0:
            break

    return match, mindiff


def mpl_color2xcolor(data, matplotlib_color):
    """Translates a matplotlib color specification into a proper LaTeX xcolor."""
    # Convert it to RGBA.
    my_col = np.array(mpl.colors.ColorConverter().to_rgba(matplotlib_color))

    # If the alpha channel is exactly 0, then the color is really 'none'
    # regardless of the RGB channels.
    if my_col[-1] == 0.0:
        return data, "none", my_col

    # Check if it exactly matches any of the colors already available.
    # This case is actually treated below (alpha==1), but that loop
    # may pick up combinations with black before finding the exact
    # match. Hence, first check all colors.
    for name, rgb in builtin_colors.items():
        if all(my_col[:3] == rgb):
            return data, name, my_col

    # Don't handle gray colors separately. They can be specified in xcolor as
    #
    #  {gray}{0.6901960784313725}
    #
    # but this float representation hides the fact that this is actually an
    # RGB255 integer value, 176.

    # convert to RGB255
    rgb255 = np.array(my_col[:3] * 255, dtype=int)

    name, diff = _get_closest_colour_name(rgb255)
    if diff > 0:
        if np.all(my_col[0] == my_col[:3]):
            name = f"{name}{rgb255[0]}"
        else:
            name = f"{name}{rgb255[0]}{rgb255[1]}{rgb255[2]}"
    data["custom colors"][name] = ("RGB", ",".join([str(val) for val in rgb255]))

    return data, name, my_col


def _mpl_cmap2pgf_cmap(cmap, data):
    """Converts a color map as given in matplotlib to a color map as
    represented in PGFPlots.
    """
    if isinstance(cmap, mpl.colors.LinearSegmentedColormap):
        return _handle_linear_segmented_color_map(cmap, data)

    assert isinstance(
        cmap, mpl.colors.ListedColormap
    ), "Only LinearSegmentedColormap and ListedColormap are supported"
    return _handle_listed_color_map(cmap, data)


def _handle_linear_segmented_color_map(cmap, data):
    assert isinstance(cmap, mpl.colors.LinearSegmentedColormap)

    if cmap.is_gray():
        is_custom_colormap = False
        return ("blackwhite", is_custom_colormap)

    # For an explanation of what _segmentdata contains, see
    # http://matplotlib.org/mpl_examples/pylab_examples/custom_cmap.py
    # A key sentence:
    # If there are discontinuities, then it is a little more complicated.  Label the 3
    # elements in each row in the cdict entry for a given color as (x, y0, y1).  Then
    # for values of x between x[i] and x[i+1] the color value is interpolated between
    # y1[i] and y0[i+1].
    segdata = cmap._segmentdata
    red = segdata["red"]
    green = segdata["green"]
    blue = segdata["blue"]

    # Loop over the data, stop at each spot where the linear interpolations is
    # interrupted, and set a color mark there.
    #
    # Set initial color.
    k_red = 0
    k_green = 0
    k_blue = 0
    colors = []
    X = []
    while True:
        # find next x
        x = min(red[k_red][0], green[k_green][0], blue[k_blue][0])

        if red[k_red][0] == x:
            red_comp = red[k_red][1]
            k_red += 1
        else:
            red_comp = _linear_interpolation(
                x,
                (red[k_red - 1][0], red[k_red][0]),
                (red[k_red - 1][2], red[k_red][1]),
            )

        if green[k_green][0] == x:
            green_comp = green[k_green][1]
            k_green += 1
        else:
            green_comp = _linear_interpolation(
                x,
                (green[k_green - 1][0], green[k_green][0]),
                (green[k_green - 1][2], green[k_green][1]),
            )

        if blue[k_blue][0] == x:
            blue_comp = blue[k_blue][1]
            k_blue += 1
        else:
            blue_comp = _linear_interpolation(
                x,
                (blue[k_blue - 1][0], blue[k_blue][0]),
                (blue[k_blue - 1][2], blue[k_blue][1]),
            )

        X.append(x)
        colors.append((red_comp, green_comp, blue_comp))

        if x >= 1.0:
            break

    # The PGFPlots color map has an actual physical scale, like (0cm,10cm), and the
    # points where the colors change is also given in those units. As of now
    # (2010-05-06) it is crucial for PGFPlots that the difference between two successive
    # points is an integer multiple of a given unity (parameter to the colormap; e.g.,
    # 1cm).  At the same time, TeX suffers from significant round-off errors, so make
    # sure that this unit is not too small such that the round- off errors don't play
    # much of a role. A unit of 1pt, e.g., does most often not work.
    unit = "pt"

    # Scale to integer (too high integers will firstly be slow and secondly may produce
    # dimension errors or memory errors in latex)
    # 0-1000 is the internal granularity of PGFplots.
    # 16300 was the maximum value for pgfplots<=1.13
    X = _scale_to_int(np.array(X), 1000)

    color_changes = []
    ff = data["float format"]
    for k, x in enumerate(X):
        color_changes.append(
            f"rgb({x}{unit})="
            f"({colors[k][0]:{ff}},{colors[k][1]:{ff}},{colors[k][2]:{ff}})"
        )

    colormap_string = "{{mymap}}{{[1{}]\n  {}\n}}".format(
        unit, ";\n  ".join(color_changes)
    )
    is_custom_colormap = True
    return (colormap_string, is_custom_colormap)


def _handle_listed_color_map(cmap, data):
    assert isinstance(cmap, mpl.colors.ListedColormap)

    # check for predefined colormaps in both matplotlib and pgfplots
    from matplotlib import pyplot as plt

    cm_translate = {
        # All the rest are LinearSegmentedColorMaps. :/
        # 'autumn': 'autumn',
        # 'cool': 'cool',
        # 'copper': 'copper',
        # 'gray': 'blackwhite',
        # 'hot': 'hot2',
        # 'hsv': 'hsv',
        # 'jet': 'jet',
        # 'spring': 'spring',
        # 'summer': 'summer',
        "viridis": "viridis",
        # 'winter': 'winter',
    }
    for mpl_cm, pgf_cm in cm_translate.items():
        if cmap.colors == plt.get_cmap(mpl_cm).colors:
            is_custom_colormap = False
            return (pgf_cm, is_custom_colormap)

    unit = "pt"
    ff = data["float format"]
    if cmap.N is None or cmap.N == len(cmap.colors):
        colors = [
            f"rgb({k}{unit})=({rgb[0]:{ff}},{rgb[1]:{ff}},{rgb[2]:{ff}})"
            for k, rgb in enumerate(cmap.colors)
        ]
    else:
        reps = int(float(cmap.N) / len(cmap.colors) - 0.5) + 1
        repeated_cols = reps * cmap.colors
        colors = [
            f"rgb({k}{unit})=({rgb[0]:{ff}},{rgb[1]:{ff}},{rgb[2]:{ff}})"
            for k, rgb in enumerate(repeated_cols[: cmap.N])
        ]
    colormap_string = "{{mymap}}{{[1{}]\n {}\n}}".format(unit, ";\n  ".join(colors))
    is_custom_colormap = True
    return (colormap_string, is_custom_colormap)


def _linear_interpolation(x, X, Y):
    """Given two data points [X,Y], linearly interpolate those at x."""
    return (Y[1] * (x - X[0]) + Y[0] * (X[1] - x)) / (X[1] - X[0])


def _scale_to_int(X, max_val):
    """Scales the array X such that it contains only integers."""
    # if max_val is None:
    #     X = X / _gcd_array(X)
    X = X / max(1 / max_val, _gcd_array(X))
    return [int(entry) for entry in X]


def _gcd_array(X):
    """
    Return the largest real value h such that all elements in x are integer
    multiples of h.
    """
    greatest_common_divisor = 0.0
    for x in X:
        greatest_common_divisor = _gcd(greatest_common_divisor, x)

    return greatest_common_divisor


def _gcd(a, b):
    """Euclidean algorithm for calculating the GCD of two numbers a, b.
    This algorithm also works for real numbers:
    Find the greatest number h such that a and b are integer multiples of h.
    """
    # Keep the tolerance somewhat significantly above machine precision as otherwise
    # round-off errors will be accounted for, returning 1.0e-10 instead of 1.0 for the
    # values
    #   [1.0, 2.0000000001, 3.0, 4.0].
    while a > 1.0e-5:
        a, b = b % a, a
    return b
