#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==============================================================================
#
# Copyright (C) 2010 Nico Schlömer
#
# This file is part of matplotlib2tikz.
#
# matplotlib2tikz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# matplotlib2tikz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# ==============================================================================
from pylab import *
import numpy
# =============================================================================
def basic_sin():
        t = arange( 0.0, 2.0, 0.01 )
        s = sin( 2*pi*t )
        plot( t, s, ":" )

        xlabel("time(s)")
        ylabel("Voltage (mV)")
        title("Easier than easy $\\frac{1}{2}$")
        grid( True )

        return "Simple $\sin$ plot with some labels"
# =============================================================================
def subplots():
        def f(t):
            s1 = numpy.cos(2*numpy.pi*t)
            e1 = numpy.exp(-t)
            return numpy.multiply(s1,e1)

        t1 = numpy.arange(0.0, 5.0, 0.1)
        t2 = numpy.arange(0.0, 5.0, 0.02)
        t3 = numpy.arange(0.0, 2.0, 0.01)

        subplot(211)
        l = plot(t1, f(t1), 'bo', t2, f(t2), 'k--', markerfacecolor='green')
        grid(True)
        title('A tale of 2 subplots')
        ylabel('Damped oscillation')

        subplot(212)
        plot(t3, numpy.cos(2*numpy.pi*t3), 'r.')
        grid(True)
        xlabel('time (s)')
        ylabel('Undamped')

        return "Two subplots on top of each other"
# =============================================================================
def image_plot():
    try:
        import Image
    except ImportError, exc:
        raise SystemExit("PIL must be installed to run this example")

    lena = Image.open('lena.png')
    dpi = rcParams['figure.dpi']
    figsize = lena.size[0]/dpi, lena.size[1]/dpi

    figure(figsize=figsize)
    ax = axes([0,0,1,1], frameon=False)
    ax.set_axis_off()
    im = imshow(lena, origin='lower')

    colorbar()

    return "An \\texttt{imshow} plot"
# =============================================================================
def noise():
    import matplotlib.pyplot as plt
    import numpy as np

    from numpy.random import randn

    # Make plot with vertical (default) colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)

    data = np.clip(randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation='nearest')
    ax.set_title('Gaussian noise with vertical colorbar')

    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
    cbar.ax.set_yticklabels(['< -1', '0', '> 1'])# vertically oriented colorbar

    # Make plot with horizontal colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)

    data = np.clip(randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation='nearest')
    ax.set_title('Gaussian noise with horizontal colorbar')

    cbar = fig.colorbar(cax, ticks=[-1, 0, 1], orientation='horizontal')
    cbar.ax.set_xticklabels(['Low', 'Medium', 'High'])# horizontal colorbar

    return "Noise with a color bar"
# =============================================================================
def patches():

    from matplotlib.patches import Circle, Wedge, Polygon
    from matplotlib.collections import PatchCollection

    fig=figure()
    ax=fig.add_subplot(111)

    resolution = 50 # the number of vertices
    N = 3
    x       = rand(N)
    y       = rand(N)
    radii   = 0.1*rand(N)
    patches = []
    for x1,y1,r in zip(x, y, radii):
        circle = Circle((x1,y1), r)
        patches.append(circle)

    x       = rand(N)
    y       = rand(N)
    radii   = 0.1*rand(N)
    theta1  = 360.0*rand(N)
    theta2  = 360.0*rand(N)
    for x1,y1,r,t1,t2 in zip(x, y, radii, theta1, theta2):
        wedge = Wedge((x1,y1), r, t1, t2)
        patches.append(wedge)

    # Some limiting conditions on Wedge
    patches += [
        Wedge((.3,.7), .1, 0, 360),             # Full circle
        Wedge((.7,.8), .2, 0, 360, width=0.05), # Full ring
        Wedge((.8,.3), .2, 0, 45),              # Full sector
        Wedge((.8,.3), .2, 45, 90, width=0.10), # Ring sector
    ]

    for i in range(N):
        polygon = Polygon(rand(N,2), True)
        patches.append(polygon)

    colors = 100*rand(len(patches))
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
    p.set_array(array(colors))
    ax.add_collection(p)
    colorbar(p)

    return "Some patches and a color bar"
# =============================================================================
def legends():
    x = ma.arange(0, 2*pi, 0.02)
    y = ma.sin(x)
    y1 = sin(2*x)
    y2 = sin(3*x)
    ym1 = ma.masked_where(y1 > 0.5, y1)
    ym2 = ma.masked_where(y2 < -0.5, y2)

    lines = plot(x, y, 'r', x, ym1, 'g', x, ym2, 'bo')
    setp(lines[0], linewidth = 4)
    setp(lines[1], linewidth = 2)
    setp(lines[2], markersize = 10)

    legend( ('No mask', 'Masked if > 0.5', 'Masked if < -0.5') ,
            loc = 'upper right')

    title('Masked line demo')

    return "Plot with legends"
# =============================================================================
def annotate():
    fig = figure(1,figsize=(8,5))
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1,5), ylim=(-4,3))

    t = np.arange(0.0, 5.0, 0.01)
    s = np.cos(2*np.pi*t)
    line, = ax.plot(t, s, color='blue')
    ann1 = ax.annotate('text', xy=(4., 1.),  xycoords='data',
                xytext=(4.5, 1.5), textcoords='data',
                arrowprops=dict(arrowstyle="->",ec="r"))

    ann2 = ax.annotate('arrowstyle', xy=(0, 1),  xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                arrowprops=dict(arrowstyle="->"))

    return "Annotations"
# =============================================================================
def legends2():
    t1 = arange(0.0, 2.0, 0.1)
    t2 = arange(0.0, 2.0, 0.01)

    # note that plot returns a list of lines.  The "l1, = plot" usage
    # extracts the first element of the list inot l1 using tuple
    # unpacking.  So l1 is a Line2D instance, not a sequence of lines
    l1,    = plot(t2, exp(-t2))
    l2, l3 = plot(t2, sin(2*pi*t2), '--go', t1, log(1+t1), '.')
    l4,    = plot(t2, exp(-t2)*sin(2*pi*t2), 'rs-.')

    legend( (l2, l4), ('oscillatory', 'damped'), 'upper right', shadow=True)
    xlabel('time')
    ylabel('volts')
    title('Damped oscillation')

    return "Another legend plot"
# =============================================================================
def logplot():
    a = [ pow(10,i) for i in range(10) ]
    fig = figure()
    ax = fig.add_subplot(1,1,1)

    line, = ax.semilogy(a, color='blue', lw=2)
    return "Log scaled plot"
# =============================================================================
def loglogplot():

    x = logspace( 0, 6, num=5 )
    loglog( x, x**2 )

    return "Loglog plot with large ticks dimensions"
# ==============================================================================
def text_overlay():
    xxx = linspace(0,5)
    yyy = xxx**2

    text(1, 5, "test1", size=50, rotation=30.,
         ha="center", va="bottom", color="r", style="italic",
         bbox = dict(boxstyle="round, pad=0.2",
                     ec=(1., 0.5, 0.5),
                     fc=(1., 0.8, 0.8),
                     ls="dashdot"
                     )
         )

    text(3, 6, "test2", size=50, rotation=-30.,
         ha="center", va="center", color="b", weight='bold',
         bbox = dict(boxstyle="square",
                     ec=(1., 0.5, 0.5),
                     fc=(1., 0.8, 0.8),
                     )
         )
    plot(xxx,yyy,label="graph")
    legend()

    return "Regular plot with overlay text"
# ==============================================================================
def subplot4x4():
    an = linspace(0,2*pi,100)

    subplot(221)
    plot( 3*cos(an), 3*sin(an) )
    title('not equal, looks like ellipse',fontsize=10)

    subplot(222)
    plot( 3*cos(an), 3*sin(an) )
    axis('equal')
    title('equal, looks like circle',fontsize=10)

    subplot(223)
    plot( 3*cos(an), 3*sin(an) )
    axis('equal')
    axis([-3,3,-3,3])
    title('looks like circle, even after changing limits',fontsize=10)

    subplot(224)
    plot( 3*cos(an), 3*sin(an) )
    axis('equal')
    axis([-3,3,-3,3])
    plot([0,4],[0,4])
    title('still equal after adding line',fontsize=10)

    return '4x4 subplots'
# ==============================================================================
def histogram():
    import matplotlib.pyplot as plt

    # Make plot with vertical (default) colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.hist(10+2*np.random.randn(1000), label='men')
    ax.hist(12+3*np.random.randn(1000), label='women', alpha=0.5)
    ax.legend()
    return 'Histogram'
# ==============================================================================
if __name__ == 'main':
    patches()
    show()
# ==============================================================================

