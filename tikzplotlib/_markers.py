# for matplotlib markers, see: http://matplotlib.org/api/markers_api.html
_MP_MARKER2PGF_MARKER = {
    ".": "*",  # point
    "o": "o",  # circle
    "+": "+",  # plus
    "x": "x",  # x
    "None": None,
    " ": None,
    "": None,
}

# the following markers are only available with PGF's plotmarks library
_MP_MARKER2PLOTMARKS = {
    "v": ("triangle", ["rotate=180"]),  # triangle down
    "1": ("triangle", ["rotate=180"]),
    "^": ("triangle", []),  # triangle up
    "2": ("triangle", []),
    "<": ("triangle", ["rotate=270"]),  # triangle left
    "3": ("triangle", ["rotate=270"]),
    ">": ("triangle", ["rotate=90"]),  # triangle right
    "4": ("triangle", ["rotate=90"]),
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
