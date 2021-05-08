import matplotlib as mpl
import numpy as np


def mpl_color2xcolor(data, matplotlib_color):
    """Translates a matplotlib color specification into a proper LaTeX xcolor."""
    # Convert it to RGBA.
    my_col = np.array(mpl.colors.ColorConverter().to_rgba(matplotlib_color))

    # If the alpha channel is exactly 0, then the color is really 'none'
    # regardless of the RGB channels.
    if my_col[-1] == 0.0:
        return data, "none", my_col

    xcol = None
    # RGB values (as taken from xcolor.dtx):
    available_colors = {
        # List white first such that for gray values, the combination
        # white!<x>!black is preferred over, e.g., gray!<y>!black. Note that
        # the order of the dictionary is respected from Python 3.6 on.
        "white": np.array([1, 1, 1]),
        "lightgray": np.array([0.75, 0.75, 0.75]),
        "gray": np.array([0.5, 0.5, 0.5]),
        "darkgray": np.array([0.25, 0.25, 0.25]),
        "black": np.array([0, 0, 0]),
        #
        "red": np.array([1, 0, 0]),
        "green": np.array([0, 1, 0]),
        "blue": np.array([0, 0, 1]),
        "brown": np.array([0.75, 0.5, 0.25]),
        "lime": np.array([0.75, 1, 0]),
        "orange": np.array([1, 0.5, 0]),
        "pink": np.array([1, 0.75, 0.75]),
        "purple": np.array([0.75, 0, 0.25]),
        "teal": np.array([0, 0.5, 0.5]),
        "violet": np.array([0.5, 0, 0.5]),
        # The colors cyan, magenta, yellow, and olive are also
        # predefined by xcolor, but their RGB approximation of the
        # native CMYK values is not very good. Don't use them here.
    }

    available_colors.update(data["custom colors"])

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
        if name == "black":
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
            ff = data["float format"]
            xcol = name + f"!{alpha*100:{ff}}!black"
            return data, xcol, my_col

    # Lookup failed, add it to the custom list.
    xcol = "color" + str(len(data["custom colors"]))
    data["custom colors"][xcol] = my_col[:3]

    return data, xcol, my_col
