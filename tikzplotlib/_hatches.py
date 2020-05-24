r"""
    Map matplotlib hatches to tikz patterns

    For matplotlib hatches, see:
    https://matplotlib.org/3.1.1/gallery/shapes_and_collections/hatch_demo.html

    For patterns in tikzpgf:
    Ch 26 Pattern Lbrary in the manual
    Requires \usetikzlibrary{patterns}
"""

# These methods exist, and might be relevant (in the future?):
# matplotlib.backend_bases.GraphicsContextBase.set/get_hatch_color
# matplotlib.backend_bases.GraphicsContextBase.set/get_hatch_linewidth
# hatch_density is mentioned in mpl API Changes in 2.0.1


import warnings

BAD_MP_HATCH = ["o", "O"]  # Bad hatch/pattern correspondance
UNUSED_PGF_PATTERN = ["dots"]
_MP_HATCH2PGF_PATTERN = {
    "-": "horizontal lines",
    "|": "vertical lines",
    "/": "north east lines",
    "\\": "north west lines",
    "+": "grid",
    "x": "crosshatch",
    ".": "crosshatch dots",
    "*": "fivepointed stars",
    "o": "sixpointed stars",
    "O": "bricks",
}


def add_custom_pattern(mpl_hatch, pattern_name, pattern_definition=None):
    """
        The patterns of tikzpgf are quite simple, and cannot be customized but for the
        color. A solution is to expose a function like this one to allow the user to
        populate _MP_HATCH2PGF_PATTERN with custom (hatch, pattern) pairs. mpl does no
        validation of the hatch string, it just ignores it if it does not recognize it,
        so it is possible to have <any> string be a mpl_hatch.

        If the pattern definition is passed, it could be added at the start of the code
        in a similar fashion to
        > data["custom colors"] = {}
        in get_tikz_code(). tikzplotlib pattern definitions would mend the bad
        correspondence between the mpl hatches and tikz patterns, with custom patterns
        for the mpl hatches 'o' and 'O'

        Want some opinions on this before I implement it..

        From https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.patches.Patch.html:
        > Letters can be combined, in which case all the specified hatchings are done.
        > If same letter repeats, it increases the density of hatching of that pattern.
        To achieve something like this, custom patterns must be created
        https://tex.stackexchange.com/questions/29359/pgfplots-how-to-fill-the-area-
        under-a-curve-with-oblique-lines-hatching-as-a/29367#29367
    """


def __validate_hatch(hatch):
    """ Warn about the shortcomings of patterns """
    if len(hatch) > 1:
        warnings.warn(
            f"tikzplotlib: Hatch '{hatch}' cannot be rendered. "
            + "Only single character hatches are supported, e.g., "
            + r"{'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}. "
            + f"Hatch '{hatch[0]}' will be used."
        )
        hatch = hatch[0]

    if hatch in BAD_MP_HATCH:
        warnings.warn(
            f"tikzplotlib: The hatches {BAD_MP_HATCH} do not have good PGF"
            + " counterparts."
        )
    return hatch


def _mpl_hatch2pgfp_pattern(data, hatch, color_name, color_rgba):
    r"""
        Translates a hatch from matplotlib to the corresponding patten in PGFPlots.

        Input:
            hatch - str, like {'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}
            color_name - str, xcolor or custom color name
            color_rgba - np.array, the rgba value of the color
        Output:
            draw_options - list, empty or with a post action string
    """
    hatch = __validate_hatch(hatch)
    try:
        pgfplots_pattern = _MP_HATCH2PGF_PATTERN[hatch]
    except KeyError:
        warnings.warn("tikzplotlib: The hatch", hatch, "is ignored.")
        return data, []

    data["tikz libs"].add("patterns")

    pattern_options = [f"pattern={pgfplots_pattern}"]
    if color_name != "black":
        # PGFPlots render patterns in 'pattern color' (default: black)
        pattern_options += [f"pattern color={color_name}"]
    if color_rgba[3] != 1:
        ff = data["float format"]
        # PGFPlots render patterns according to opacity fill.
        # This change is within the scope of the postaction
        pattern_options.append(f"fill opacity={color_rgba[3]:{ff}}")

    # Add pattern as postaction to allow color fill and pattern together
    # https://tex.stackexchange.com/questions/24964/
    # how-to-combine-fill-and-pattern-in-a-pgfplot-bar-plot
    postaction = f"postaction={{{', '.join(pattern_options)}}}"

    return data, [postaction]
