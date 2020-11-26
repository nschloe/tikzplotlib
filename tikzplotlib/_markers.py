# for matplotlib markers, see https://matplotlib.org/api/markers_api.html
_MP_MARKER2PGF_MARKER = {
    ".": "*",  # point
    # ",": # pixel
    "o": "o",  # circle
    "+": "+",  # plus
    "P": "+",  # actually plus filled
    "x": "x",  # x
    "X": "x",  # actually x filled
    "None": None,
    " ": None,
    "": None,
}

# the following markers are only available with PGF's plotmarks library
# See
# <https://mirror.clientvps.com/CTAN/graphics/pgf/contrib/pgfplots/doc/pgfplots.pdf>,
# chapter 4.7, page 183 ff.
_MP_MARKER2PLOTMARKS = {
    "v": ("triangle", ["rotate=180"]),  # triangle down
    "^": ("triangle", []),  # triangle up
    "<": ("triangle", ["rotate=270"]),  # triangle left
    ">": ("triangle", ["rotate=90"]),  # triangle right
    "1": ("Mercedes star flipped", []),
    "2": ("Mercedes star", []),
    "3": ("Mercedes star", ["rotate=90"]),
    "4": ("Mercedes star", ["rotate=270"]),
    "s": ("square", []),
    "p": ("pentagon", []),
    "*": ("asterisk", []),
    "h": ("star", []),  # hexagon 1
    "H": ("star", []),  # hexagon 2
    "d": ("diamond", []),  # diamond
    "D": ("diamond", []),  # thin diamond
    "|": ("|", []),  # vertical line
    "_": ("-", []),  # horizontal line
}


def _mpl_marker2pgfp_marker(data, mpl_marker, marker_face_color):
    """Translates a marker style of matplotlib to the corresponding style
    in PGFPlots.
    """
    # try default list
    try:
        pgfplots_marker = _MP_MARKER2PGF_MARKER[mpl_marker]
    except KeyError:
        pass
    else:
        if (marker_face_color is not None) and pgfplots_marker == "o":
            pgfplots_marker = "*"
            data["tikz libs"].add("plotmarks")
        marker_options = []
        return data, pgfplots_marker, marker_options

    # try plotmarks list
    try:
        data["tikz libs"].add("plotmarks")
        pgfplots_marker, marker_options = _MP_MARKER2PLOTMARKS[mpl_marker]
    except KeyError:
        # There's no equivalent for the pixel marker (,) in Pgfplots.
        pass
    else:
        if (
            marker_face_color is not None
            and (
                not isinstance(marker_face_color, str)
                or marker_face_color.lower() != "none"
            )
            and pgfplots_marker not in ["|", "-", "asterisk", "star"]
        ):
            pgfplots_marker += "*"
        return data, pgfplots_marker, marker_options

    return data, None, []
