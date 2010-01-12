#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

from pylab import *

# =============================================================================
def matplotlib2tikz():
	handle_children( gcf() )
	return
# =============================================================================
def draw_axes( obj ):

        axis_options = []

        # get axes title
        title = obj.get_title()
        if len(title) != 0 :
            axis_options.append( "title=" + title )

        # get axes titles
        xlabel = obj.get_xlabel()
        if len(xlabel) != 0 :
	    axis_options.append( "xlabel=" + xlabel )
        ylabel = obj.get_ylabel()
        if len(ylabel) != 0 :
            axis_options.append( "ylabel=" + ylabel )

	# axes limits
	xlim = obj.get_xlim()
        axis_options.append(     "xmin=" + repr(xlim[0])
                             + ", xmax=" + repr(xlim[1]) )
        ylim = obj.get_ylim()
        axis_options.append(     "ymin=" + repr(ylim[0])
                             + ", ymax=" + repr(ylim[1]) )

	# actually print the thing
	print "\\begin{axes}",
        if len(axis_options)!=0:
		options = ",\n".join( axis_options )
		print "[\n", options, "\n]\n",      

        # TODO Use get_lines()?
        handle_children( obj )

	print "\\end{axes}"
 
	return
# =============================================================================
def draw_line2d( obj ):
        addplot_options = []

        marker = obj.get_marker()
        if marker!="None":
		print "%TODO Implement markers."

        # get line color
        color = obj.get_color()
        addplot_options.append( mpl_color2xcolor(color) )

        linestyle = mpl_linestyle2pgfp_linestyle( obj.get_linestyle() )
        if linestyle:
		addplot_options.append( linestyle )

        # process options
	print "\\addplot",
        if  len(addplot_options) != 0:
		options = ", ".join( addplot_options )
		print "[", options, "]\n",

        # print the hard numerical data
	xdata, ydata = obj.get_data()
        print "coordinates {"
        for k in range(len(xdata)):
		print "(", xdata[k], ",", ydata[k], ") ",
        print "\n};"

        return
# =============================================================================
# Translates a line style of matplotlib to the corresponding style
# in Pgfplots.
def mpl_linestyle2pgfp_linestyle( ls ):
	translator = { '-': None,
                       ':': "dotted"
		     }
        return translator[ ls ]
# =============================================================================
# Translates a matplotlib color specification into a proper LaTeX
# xcolor.
def mpl_color2xcolor( color ):
	translator = { "r": "red",
                       "g": "green",
                       "b": "blue",
		     }
        return translator[ color ]
# =============================================================================
def handle_children( obj ):
	for child in obj.get_children():
                if (isinstance( child, matplotlib.axes.Axes ) ):
			draw_axes( child )
		elif (isinstance( child, matplotlib.lines.Line2D ) ):
			draw_line2d( child )
		elif (   isinstance( child, matplotlib.axis.XAxis )
		      or isinstance( child, matplotlib.axis.YAxis )
                      or isinstance( child, matplotlib.spines.Spine )
		      or isinstance( child, matplotlib.patches.Rectangle )
		      or isinstance( child, matplotlib.text.Text )
                     ):
			pass
                else:
			print "Don't know how to handle object ", type(child), "."
	return
# =============================================================================
def plot_tree( obj, indent ):
        print indent, type(obj)
	for child in obj.get_children():
		plot_tree( child, indent + "   " )
	return
# =============================================================================