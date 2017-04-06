# -*- coding: utf-8 -*-
#
'''Script to convert Matplotlib generated figures into TikZ/PGFPlots figures.
'''

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

import pipdated
if pipdated.needs_checking('matplotlib2tikz'):
    msg = pipdated.check('matplotlib2tikz', __version__)
    if msg:
        print(msg)
