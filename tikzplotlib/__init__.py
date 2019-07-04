"""Script to convert Matplotlib generated figures into TikZ/PGFPlots figures.
"""
from tikzplotlib.__about__ import (
    __author__,
    __copyright__,
    __email__,
    __license__,
    __status__,
    __version__,
)
from tikzplotlib.save import get_tikz_code, save

__all__ = [
    "__author__",
    "__email__",
    "__copyright__",
    "__license__",
    "__version__",
    "__status__",
    "get_tikz_code",
    "save",
]
