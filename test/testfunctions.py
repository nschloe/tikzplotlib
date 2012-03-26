#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==============================================================================
#
# Copyright (C) 2010--2012 Nico Schlömer
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
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as pp
# =============================================================================
def basic_sin():
        t = np.arange( 0.0, 2.0, 0.01 )
        s = np.sin( 2*np.pi*t )
        pp.plot( t, s, ':' )

        pp.xlabel('time(s) _ % $ \\')
        pp.ylabel('Voltage (mV)')
        pp.title('Easier than easy $\\frac{1}{2}$')
        pp.grid( True )

        return 'Simple $\sin$ plot with some labels'
# =============================================================================
def subplots():
        def f(t):
            s1 = np.cos(2*np.pi*t)
            e1 = np.exp(-t)
            return np.multiply(s1,e1)

        t1 = np.arange(0.0, 5.0, 0.1)
        t2 = np.arange(0.0, 5.0, 0.02)
        t3 = np.arange(0.0, 2.0, 0.01)

        pp.subplot(211)
        pp.plot(t1, f(t1), 'bo', t2, f(t2), 'k--', markerfacecolor='green')
        pp.grid(True)
        pp.title('A tale of 2 subplots')
        pp.ylabel('Damped oscillation')

        pp.subplot(212)
        pp.plot(t3, np.cos(2*np.pi*t3), 'r.')
        pp.grid(True)
        pp.xlabel('time (s)')
        pp.ylabel('Undamped')

        return 'Two subplots on top of each other'
# =============================================================================
def image_plot():
    from matplotlib import rcParams
    try:
        import Image
    except ImportError, exc:
        raise SystemExit('PIL must be installed to run this example')

    lena = Image.open('lena.png')
    dpi = rcParams['figure.dpi']
    figsize = lena.size[0]/dpi, lena.size[1]/dpi

    pp.figure( figsize=figsize )
    ax = pp.axes([0,0,1,1], frameon=False)
    ax.set_axis_off()
    im = pp.imshow(lena, origin='lower')
    # Set the current color map to HSV.
    pp.hsv()
    pp.colorbar()

    return 'An \\texttt{imshow} plot'
# =============================================================================
def noise():
    from numpy.random import randn

    # Make plot with vertical (default) colorbar
    fig = pp.figure()
    ax = fig.add_subplot(111)

    data = np.clip(randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation='nearest')
    ax.set_title('Gaussian noise with vertical colorbar')

    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
    cbar.ax.set_yticklabels(['< -1', '0', '> 1'])# vertically oriented colorbar

    # Make plot with horizontal colorbar
    fig = pp.figure()
    ax = fig.add_subplot(111)

    data = np.clip(np.random.randn(250, 250), -1, 1)

    cax = ax.imshow(data, interpolation='nearest')
    ax.set_title('Gaussian noise with horizontal colorbar')

    cbar = fig.colorbar(cax, ticks=[-1, 0, 1], orientation='horizontal')
    cbar.ax.set_xticklabels(['Low', 'Medium', 'High'])# horizontal colorbar

    return 'Noise with a color bar'
# =============================================================================
def circle_patch():
    from matplotlib.patches import Circle

    fig = pp.figure()
    ax = fig.add_subplot(111)

    ax.add_patch( Circle((0,0), 1) )

    return 'A circle patch'
# =============================================================================
def patches():

    from matplotlib.patches import Circle, Wedge, Polygon
    from matplotlib.collections import PatchCollection

    fig = pp.figure()
    ax = fig.add_subplot(111)

    resolution = 50 # the number of vertices
    N = 3
    x       = np.random.rand(N)
    y       = np.random.rand(N)
    radii   = 0.1*np.random.rand(N)
    patches = []
    for x1,y1,r in zip(x, y, radii):
        circle = Circle((x1,y1), r)
        patches.append(circle)

    x       = np.random.rand(N)
    y       = np.random.rand(N)
    radii   = 0.1*np.random.rand(N)
    theta1  = 360.0*np.random.rand(N)
    theta2  = 360.0*np.random.rand(N)
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
        polygon = Polygon(np.random.rand(N,2), True)
        patches.append(polygon)

    colors = 100*np.random.rand(len(patches))
    p = PatchCollection( patches,
                         cmap = mpl.cm.jet,
                         alpha=0.4
                       )
    p.set_array( np.array(colors) )
    ax.add_collection(p)
    pp.colorbar(p)

    return 'Some patches and a color bar'
# =============================================================================
def legends():
    x = np.ma.arange(0, 2*np.pi, 0.02)
    y = np.ma.sin(x)
    y1 = np.sin(2*x)
    y2 = np.sin(3*x)
    ym1 = np.ma.masked_where(y1 > 0.5, y1)
    ym2 = np.ma.masked_where(y2 < -0.5, y2)

    lines = pp.plot(x, y, 'r', x, ym1, 'g', x, ym2, 'bo')
    pp.setp(lines[0], linewidth = 4)
    pp.setp(lines[1], linewidth = 2)
    pp.setp(lines[2], markersize = 10)

    pp.legend( ( 'No mask', 'Masked if > 0.5', 'Masked if < -0.5') ,
               loc = 'upper right'
             )

    pp.title('Masked line demo')

    return 'Plot with legends'
# =============================================================================
def annotate():
    fig = pp.figure( 1, figsize=(8,5) )
    ax = fig.add_subplot( 111,
                          autoscale_on = False,
                          xlim=(-1,5),
                          ylim=(-4,3)
                        )

    t = np.arange( 0.0, 5.0, 0.01 )
    s = np.cos( 2*np.pi*t )
    line, = ax.plot( t, s, color='blue' )
    ann1 = ax.annotate( 'text',
                        xy = (4., 1.),
                        xycoords = 'data',
                        xytext = (4.5, 1.5),
                        textcoords='data',
                        arrowprops = dict(arrowstyle='->',ec='r')
                      )

    ann2 = ax.annotate( 'arrowstyle',
                        xy = (0, 1),
                        xycoords = 'data',
                        xytext = (-50, 30),
                        textcoords = 'offset points',
                        arrowprops = dict(arrowstyle='->')
                      )

    return 'Annotations'
# =============================================================================
def legends2():
    t1 = np.arange(0.0, 2.0, 0.1)
    t2 = np.arange(0.0, 2.0, 0.01)

    # note that plot returns a list of lines.  The 'l1, = plot' usage
    # extracts the first element of the list inot l1 using tuple
    # unpacking.  So l1 is a Line2D instance, not a sequence of lines
    l1,    = pp.plot(t2, np.exp(-t2))
    l2, l3 = pp.plot(t2, np.sin(2*np.pi*t2), '--go', t1, np.log(1+t1), '.')
    l4,    = pp.plot(t2, np.exp(-t2)*np.sin(2*np.pi*t2), 'rs-.')

    pp.legend( (l2, l4), ('oscillatory', 'damped'), 'upper right', shadow=True)
    pp.xlabel('time')
    pp.ylabel('volts')
    pp.title('Damped oscillation')

    return 'Another legend plot'
# =============================================================================
def logplot():
    a = [ pow(10,i) for i in range(10) ]
    fig = pp.figure()
    ax = fig.add_subplot(1,1,1)

    line, = ax.semilogy(a, color='blue', lw=2)
    return 'Log scaled plot'
# =============================================================================
def loglogplot():

    x = np.logspace( 0, 6, num=5 )
    pp.loglog( x, x**2 )

    return 'Loglog plot with large ticks dimensions'
# ==============================================================================
def text_overlay():
    xxx = np.linspace(0,5)
    yyy = xxx**2

    pp.text(1, 5, 'test1', size=50, rotation=30.,
         ha='center', va='bottom', color='r', style='italic',
         bbox = dict(boxstyle='round, pad=0.2',
                     ec=(1., 0.5, 0.5),
                     fc=(1., 0.8, 0.8),
                     ls='dashdot'
                     )
         )

    pp.text(3, 6, 'test2', size=50, rotation=-30.,
         ha='center', va='center', color='b', weight='bold',
         bbox = dict(boxstyle='square',
                     ec=(1., 0.5, 0.5),
                     fc=(1., 0.8, 0.8),
                     )
         )
    pp.plot(xxx,yyy,label='graph')
    pp.legend()

    return 'Regular plot with overlay text'
# ==============================================================================
def subplot4x4():
    an = np.linspace(0,2*np.pi,100)

    pp.subplot(221)
    pp.plot( 3*np.cos(an), 3*np.sin(an) )
    pp.title('not equal, looks like ellipse',fontsize=10)

    pp.subplot(222)
    pp.plot( 3*np.cos(an), 3*np.sin(an) )
    pp.axis('equal')
    pp.title('equal, looks like circle',fontsize=10)

    pp.subplot(223)
    pp.plot( 3*np.cos(an), 3*np.sin(an) )
    pp.axis('equal')
    pp.axis([-3,3,-3,3])
    pp.title('looks like circle, even after changing limits',fontsize=10)

    pp.subplot(224)
    pp.plot( 3*np.cos(an), 3*np.sin(an) )
    pp.axis('equal')
    pp.axis([-3,3,-3,3])
    pp.plot([0,4],[0,4])
    pp.title('still equal after adding line',fontsize=10)

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
def contourf_with_logscale():
    import matplotlib.pyplot as plt
    import matplotlib.ticker as tkr
    #from matplotlib import colors, ticker
    from matplotlib.mlab import bivariate_normal

    N = 100
    x = np.linspace(-3.0, 3.0, N)
    y = np.linspace(-2.0, 2.0, N)

    X, Y = np.meshgrid(x, y)

    # A low hump with a spike coming out of the top right.
    # Needs to have z/colour axis on a log scale so we see both hump and spike.
    # linear scale only shows the spike.
    z = bivariate_normal(X, Y, 0.1, 0.2, 1.0, 1.0) \
      + 0.1 * bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)

    # Put in some negative values (lower left corner) to cause trouble with logs:
    z[:5, :5] = -1

    # The following is not strictly essential, but it will eliminate
    # a warning.  Comment it out to see the warning.
    z = np.ma.masked_where( z<=0, z )

    # Automatic selection of levels works; setting the
    # log locator tells contourf to use a log scale:
    cs = plt.contourf( X, Y, z,
                       locator = tkr.LogLocator()
                     )

    # Alternatively, you can manually set the levels
    # and the norm:
    #lev_exp = np.arange(np.floor(np.log10(z.min())-1),
    #                       np.ceil(np.log10(z.max())+1))
    #levs = np.power(10, lev_exp)
    #cs = plt.contourf(X, Y, z, levs, norm=colors.LogNorm())

    #The 'extend' kwarg does not work yet with a log scale.

    cbar = plt.colorbar()

    return 'contourf with logscale'
# ==============================================================================
if __name__ == 'main':
    patches()
    show()
# ==============================================================================
