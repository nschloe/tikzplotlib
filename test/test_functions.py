# -*- coding: utf-8 -*-
import pylab
import numpy

# =============================================================================
def simple_sin():
        t = numpy.arange(0.0, 2.0, 0.01)
        s = numpy.sin(2*numpy.pi*t)

        pylab.plot(t, s, linewidth=1.0)

        pylab.xlabel('time (s)')
        pylab.ylabel('voltage (mV)')
        pylab.title('About as simple as it gets, folks')
        pylab.grid(True)
# =============================================================================
def subplots():
        def f(t):
            s1 = numpy.cos(2*numpy.pi*t)
            e1 = numpy.exp(-t)
            return numpy.multiply(s1,e1)

        t1 = numpy.arange(0.0, 5.0, 0.1)
        t2 = numpy.arange(0.0, 5.0, 0.02)
        t3 = numpy.arange(0.0, 2.0, 0.01)

        pylab.subplot(211)
        l = pylab.plot(t1, f(t1), 'bo', t2, f(t2), 'k--', markerfacecolor='green')
        pylab.grid(True)
        pylab.title('A tale of 2 subplots')
        pylab.ylabel('Damped oscillation')

        pylab.subplot(212)
        pylab.plot(t3, numpy.cos(2*numpy.pi*t3), 'r.')
        pylab.grid(True)
        pylab.xlabel('time (s)')
        pylab.ylabel('Undamped')
# =============================================================================