# -*- coding: utf-8 -*-
#
import helpers
from matplotlib import rcParams
from matplotlib import pyplot as pp
import pytest
import os

try:
    from PIL import Image
except ImportError:
    raise RuntimeError('PIL must be installed to run this example')

#the picture 'lena.png' with origin='lower' is flipped upside-down. So it has to be upside-down in the pdf-file as well.

def plot1(): #test for monochrome picture

    this_dir = os.path.dirname(os.path.realpath(__file__))
    lena = Image.open(os.path.join(this_dir, 'lena.png'))
    lena = lena.convert('L')
    dpi = rcParams['figure.dpi']
    figsize = lena.size[0]/dpi, lena.size[1]/dpi
    fig = pp.figure(figsize=figsize)
    ax = pp.axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()
    pp.imshow(lena, cmap='viridis', origin='lower')
    # Set the current color map to HSV.
    pp.hsv()
    pp.colorbar()
    return fig

def plot2(): #test for rgb picture

    this_dir = os.path.dirname(os.path.realpath(__file__))
    lena = Image.open(os.path.join(this_dir, 'lena.png'))
    dpi = rcParams['figure.dpi']
    figsize = lena.size[0] / dpi, lena.size[1] / dpi
    fig = pp.figure(figsize=figsize)
    ax = pp.axes([0, 0, 1, 1], frameon=False)
    ax.set_axis_off()
    pp.imshow(lena, cmap='viridis', origin='lower')
    # Set the current color map to HSV.
    pp.hsv()
    pp.colorbar()
    return fig

@pytest.mark.parametrize(
    'plot, phash', [
        (plot1, '455361ec211d72fb'),
        (plot2, '7558d3b30f634b06'),
    ]
    )

def test(plot, phash):
    helpers.assert_phash(plot(), phash)
    return

