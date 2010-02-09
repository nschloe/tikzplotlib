#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

from pylab import *

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