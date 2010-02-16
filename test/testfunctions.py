# -*- coding: utf-8 -*-

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
        grid(True)

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

        return "An \\texttt{imshow} plot"
# =============================================================================
def subplot_plot():
        def f(t):
            s1 = cos(2*pi*t)
            e1 = exp(-t)
            return multiply(s1,e1)

        t1 = arange(0.0, 5.0, 0.1)
        t2 = arange(0.0, 5.0, 0.02)
        t3 = arange(0.0, 2.0, 0.01)

        subplot(211)
        l = plot(t1, f(t1), 'bo', t2, f(t2), 'k--', markerfacecolor='green')
        grid(True)
        title('A tale of 2 subplots')
        ylabel('Damped oscillation')

        subplot(212)
        plot(t3, cos(2*pi*t3), 'r.')
        grid(True)
        xlabel('time (s)')
        ylabel('Undamped')

        return "Two subplot on top of each other"
# =============================================================================