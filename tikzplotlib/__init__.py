"""Script to convert Matplotlib generated figures into TikZ/PGFPlots figures.
"""
from .__about__ import (
    __copyright__,
    __version__,
)
from ._cleanfigure import clean_figure
from ._save import Flavors, get_tikz_code, save

__all__ = [
    "__author__",
    "__email__",
    "__copyright__",
    "__license__",
    "__version__",
    "__status__",
    "get_tikz_code",
    "save",
    "clean_figure",
    "Flavors",
]
