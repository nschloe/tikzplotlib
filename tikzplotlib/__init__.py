"""Script to convert Matplotlib generated figures into TikZ/PGFPlots figures.
"""
from .__about__ import (
    __author__,
    __copyright__,
    __email__,
    __license__,
    __status__,
    __version__,
)
from ._save import get_tikz_code, save
from ._cleanfigure import clean_figure

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
]
