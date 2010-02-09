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
        pylab.show()
# =============================================================================