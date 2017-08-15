# -*- coding: utf-8 -*-
#
'''Script to convert Matplotlib generated figures into TikZ/PGFPlots figures.
'''
from __future__ import print_function

from matplotlib2tikz.__about__ import (
        __author__,
        __email__,
        __copyright__,
        __credits__,
        __license__,
        __version__,
        __maintainer__,
        __status__
        )

from matplotlib2tikz.save import get_tikz_code, save

try:
    import pipdate
except ImportError:
    pass
else:
    if pipdate.needs_checking(__name__):
        print(pipdate.check(__name__, __version__))
