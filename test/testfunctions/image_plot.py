# -*- coding: utf-8 -*-
#
desc = 'An \\texttt{imshow} plot'
phash = '7558d3b30f634b06'


def plot():
    from matplotlib import rcParams
    from matplotlib import pyplot as pp
    import os
    try:
        from PIL import Image
    except ImportError:
        raise RuntimeError('PIL must be installed to run this example')

    this_dir = os.path.dirname(os.path.realpath(__file__))
    lena = Image.open(os.path.join(this_dir, 'lena.png'))
    dpi = rcParams['figure.dpi']
    figsize = lena.size[0]/dpi, lena.size[1]/dpi
    fig = pp.figure(figsize=figsize)
    ax = pp.axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()
    pp.imshow(lena, origin='lower')
    # Set the current color map to HSV.
    pp.hsv()
    pp.colorbar()
    return fig
