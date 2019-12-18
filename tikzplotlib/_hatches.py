import warnings

# From https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.patches.Patch.html:
# > Letters can be combined, in which case all the specified hatchings are done.
# > If same letter repeats, it increases the density of hatching of that pattern.
# To achieve something like this, custom patterns must be created
# https://tex.stackexchange.com/questions/29359/pgfplots-how-to-fill-the-area-under-a-curve-with-oblique-lines-hatching-as-a/29367#29367

# These methods exist, and might be relevant:
# matplotlib.backend_bases.GraphicsContextBase.set/get_hatch_color
# matplotlib.backend_bases.GraphicsContextBase.set/get_hatch_linewidth
# hatch_density is mentioned in mpl API Changes in 2.0.1

# for matplotlib hatches, see:
# https://matplotlib.org/3.1.1/gallery/shapes_and_collections/hatch_demo.html

# hatches in tikzpgf: Ch 26 Pattern Lbrary with \usetikzlibrary{patterns}

BAD_MP_HATCH = ["o", "O"]  # Bad hatch/pattern correspondance
UNUSED_PGF_HATCH = ["dots"]
_MP_HATCH2PGF_HATCH = {
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


def add_custom_pattern(mpl_hatch, pattern_name, pattern_definition):
    pass


def __validate_mpl_hatch(mpl_hatch):
    if len(mpl_hatch) > 1:
        warnings.warn(
            f"tikzplotlib: Hatch '{mpl_hatch}' cannot be rendered. "
            + "Only single character hatches are supported, e.g., "
            + r"{'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}. "
            + f"Hatch '{mpl_hatch[0]}' will be used."
        )
        mpl_hatch = mpl_hatch[0]

    if mpl_hatch in BAD_MP_HATCH:
        warnings.warn(
            f"tikzplotlib: The hatches {BAD_MP_HATCH} do not have good PGF"
            + " counterparts."
        )
    return mpl_hatch


def _mpl_hatch2pgfp_hatch(data, mpl_hatch, color_name, color_rgba):
    """
        Translates a hatch style of matplotlib to the corresponding style
        in PGFPlots.
    """
    data["tikz libs"].add("patterns")

    mpl_hatch = __validate_mpl_hatch(mpl_hatch)
    try:
        pgfplots_hatch = _MP_HATCH2PGF_HATCH.get(mpl_hatch)
    except KeyError:
        warnings.warn("tikzplotlib: The hatch", mpl_hatch, "cannot be handled.")
        return data, []
    else:
        pattern_options = [f"pattern={pgfplots_hatch}"]
        if color_name != "black":
            # PGFPlots render patterns in 'pattern color' (default: black)
            pattern_options += [f"pattern color={color_name}"]
        if color_rgba[3] != 1:
            ff = data["float format"]
            # PGFPlots render patterns according to opacity fill.
            pattern_options.append(("fill opacity=" + ff).format(color_rgba[3]))

    # Add pattern as postaction to allow fill and pattern
    # https://tex.stackexchange.com/questions/24964/
    # how-to-combine-fill-and-pattern-in-a-pgfplot-bar-plot
    hatch_postaction = f"postaction={{{', '.join(pattern_options)}}}"

    return data, [hatch_postaction]


if __name__ == "__main__":
    import warnings
    import matplotlib.pyplot as plt
    import matplotlib

    fig, ax = plt.subplots()

    ax.bar(range(1, 5), range(1, 5), color="red", edgecolor="black", hatch="O")

    for c in ax.get_children():
        try:
            hatch = c.get_hatch()
        except AttributeError as error:
            pass
        else:
            if hatch is not None:
                print(c, hatch)
        try:
            color = c.get_hatch_color()
        except AttributeError as error:
            pass
        else:
            if color is not None:
                print(c, color)
        try:
            lw = c.get_hatch_linewidth()
        except AttributeError as error:
            pass
        else:
            if lw is not None:
                print(c, lw)

    plt.show()
