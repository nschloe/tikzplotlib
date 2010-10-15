# -*- coding: utf-8 -*-
# ==============================================================================
#
# Copyright (C) 2010 Nico Schl"omer
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
"""Script to convert Matplotlib generated figures into TikZ/Pgfplots figures.
"""
# ==============================================================================
# imported modules
import matplotlib as mpl
import numpy
import types
import os
import sys
from itertools import izip
# ==============================================================================
# meta info
__author__     = 'Nico Schl"omer'
__copyright__  = 'Copyright (c) 2010, Nico Schl"omer <nico.schloemer@gmail.com>'
__credits__    = []
__license__    = 'GNU Lesser General Public License (LGPL), Version 3'
__version__    = '0.1.0'
__maintainer__ = 'Nico Schl"omer'
__email__      = 'nico.schloemer@gmail.com'
__status__     = 'Development'
# ==============================================================================
# global variables
FWIDTH        = None
FHEIGHT       = None
REL_DATA_PATH = None
PGFPLOTS_LIBS = set()
TIKZ_LIBS     = set()
OUTPUT_DIR    = None
IMG_NUMBER    = -1
CUSTOM_COLORS = {}
EXTRA_AXIS_OPTIONS = set()
STRICT        = False
# ==============================================================================
def save( filepath,
          figurewidth = None,
          figureheight = None,
          tex_relative_path_to_data = None,
          strict = False,
          wrap = True,
          extra = None):
    """Main function. Here, the recursion into the image starts and the contents
    are picked up. The actual file gets written in this routine.

    :param filepath: The file to which the TikZ output will be written.
    :type filepath: str.

    :param figurewidth: If not ``None``, this will be used as figure width
                        within the TikZ/Pgfplot output. If ``figureheight``
                        is not given, ``matplotlib2tikz`` will try to preserve
                        the original width/height ratio.
                        Note that ``figurewidth`` can be a string literal,
                        such as ``'\\figurewidth'``.
    :type figurewidth: str.

    :param figureheight: If not ``None``, this will be used as figure height
                         within the TikZ/Pgfplot output. If ``figurewidth`` is
                         not given, ``matplotlib2tikz`` will try to preserve the
                         original width/height ratio.
                         Note that ``figurewidth`` can be a string literal,
                         such as ``'\\figureheight'``.
    :type figureheight: str.

    :param tex_relative_path_to_data: In some cases, the TikZ file will have to
                                      refer to another file, e.g., a PNG for
                                      image plots. When ``\\input`` into a
                                      regular LaTeX document, the additional
                                      file is looked for in a folder relative
                                      to the LaTeX file, not the TikZ file.
                                      This arguments optionally sets the
                                      relative path from the LaTeX file to the
                                      data.
    :type tex_relative_path_to_data: str.

    :param strict: Whether or not to strictly stick to matplotlib's appearance.
                   This influences, for example, whether tick marks are set
                   exactly as in the matplotlib plot, or if TikZ/Pgfplots
                   can decide where to put the ticks.
    :type strict: bool.

    :param wrap: Whether ``'\\begin{tikzpicture}'`` and ``'\\end{tikzpicture}'``
                 will be written. One might need to provide custom arguments to
                 the environment (eg. scale= etc.). Default is ``True``
    :type wrap: bool.

    :param extra: Extra axis options to be passed (as a dict) to pgfplots. Default
                  is ``None``.
    :type extra: dict.

    :returns: None.
    """
    global FWIDTH    
    FWIDTH        = figurewidth
    global FHEIGHT
    FHEIGHT       = figureheight
    global REL_DATA_PATH
    REL_DATA_PATH = tex_relative_path_to_data
    global OUTPUT_DIR
    OUTPUT_DIR    = os.path.dirname(filepath)
    global STRICT
    STRICT = strict
    global TIKZ_LIBS

    if extra is not None:
        for key,val in extra.items():
            EXTRA_AXIS_OPTIONS.add("%s=%s"%(key,val))

    # open file
    file_handle = open( filepath, "w" )

    # gather the file content
    content = _handle_children( mpl.pyplot.gcf() )

    # write the contents
    if wrap:
        file_handle.write( "\\begin{tikzpicture}\n\n" )

    coldefs = _get_color_definitions()
    if coldefs:
        file_handle.write( "\n".join( _get_color_definitions() ) )
        file_handle.write( "\n\n" )

    file_handle.write( ''.join(content) )
    if wrap:
        file_handle.write( "\\end{tikzpicture}" )

    # close file
    file_handle.close()
    
    # print message about necessary pgfplot libs to command line
    _print_pgfplot_libs_message()
    return
# ==============================================================================
def _print_tree( obj, indent = "" ):
    """
    Recursively prints the tree structure of the matplotlib object.
    """
    print indent, type(obj)
    for child in obj.get_children():
        _print_tree( child, indent + "   " )
    return
# ==============================================================================
def _get_color_definitions():
    """
    Returns the list of custom color definitions for the TikZ file.
    """
    definitions = []
    for rgb in CUSTOM_COLORS:
        definitions.append( "\\definecolor{%s}{rgb}{%g,%g,%g}" % \
                            ( (CUSTOM_COLORS[rgb],) + rgb )
                          )
    return definitions
# ==============================================================================
def _draw_axes( obj ):
    """
    Returns the Pgfplots code for an axis environment.
    """
    global PGFPLOTS_LIBS

    content = []

    # Are we dealing with an axis that hosts a colorbar?
    # Skip then.
    # TODO instead of testing here, rather blacklist the colorbar axis
    #      plots as soon as they have been found, e.g., by
    #      _find_associated_colorbar()
    if _extract_colorbar(obj):
        return

    # instantiation
    nsubplots = 1
    subplot_index = 0
    is_subplot = False

    if isinstance( obj, mpl.axes.Subplot ):
        geom = obj.get_geometry()
        nsubplots = geom[0]*geom[1]
        if nsubplots > 1:
            is_subplot = True
            subplot_index = geom[2]
            if subplot_index == 1:
                content.append( "\\begin{groupplot}[group style=" \
                                "{group size=%.d by %.d}]\n" % (geom[1],geom[0])
                              )
                PGFPLOTS_LIBS.add( "groupplots" )

    axis_options = []

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get plot title
    title = obj.get_title()
    if title:
        axis_options.append( "title={" + title + "}" )
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get axes titles
    xlabel = obj.get_xlabel()
    if xlabel:
        axis_options.append( "xlabel={" + xlabel + "}" )
    ylabel = obj.get_ylabel()
    if ylabel:
        axis_options.append( "ylabel={" + ylabel + "}" )
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Axes limits.
    # Sort the limits so make sure that the smaller of the two is actually
    # *min.
    xlim = sorted( list( obj.get_xlim() ) )
    axis_options.append(     "xmin=%e" % xlim[0]
                         + ", xmax=%e" % xlim[1] )
    ylim = sorted( list( obj.get_ylim() ) )
    axis_options.append(     "ymin=%e" % ylim[0]
                         + ", ymax=%e" % ylim[1] )
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # axes scaling
    xscale = obj.get_xscale()
    yscale = obj.get_yscale()
    if xscale == 'log'  and  yscale == 'log':
        env = 'loglogaxis'
    elif xscale == 'log':
        env = 'semilogxaxis'
    elif yscale == 'log':
        env = 'semilogyaxis'
    else:
        env = 'axis'
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # aspect ratio, plot width/height
    aspect = obj.get_aspect()
    if aspect == "auto"  or  aspect == "normal":
        aspect_num = None # just take the given width/height values
    elif aspect == "equal":
        aspect_num = 1.0
    else:
        try:
            aspect_num = float(aspect)
        except ValueError:
            print "Aspect ratio not a number?!"

    global FWIDTH
    global FHEIGHT
    if FWIDTH and FHEIGHT: # width and height overwrite aspect ratio
        axis_options.append( "width="+FWIDTH )
        axis_options.append( "height="+FHEIGHT )
    elif FWIDTH: # only FWIDTH given. calculate height by the aspect ratio
        axis_options.append( "width="+FWIDTH )
        if aspect_num:
            alpha = aspect_num * (ylim[1]-ylim[0])/(xlim[1]-xlim[0])
            if alpha != 1.0:
                # Concatenate the literals, as FWIDTH could as well be
                # a LaTeX length variable such as \figurewidth.
                FHEIGHT = str(alpha) + "*" + FWIDTH
            else:
                FHEIGHT = FWIDTH
            axis_options.append( "height="+FHEIGHT )
    elif FHEIGHT: # only FHEIGHT given. calculate width by the aspect ratio
        axis_options.append( "height="+FHEIGHT )
        if aspect_num:
            alpha = aspect_num * (ylim[1]-ylim[0])/(xlim[1]-xlim[0])
            if alpha != 1.0:
                # Concatenate the literals, as FHEIGHT could as well be
                # a LaTeX length variable such as \figureheight.
                FWIDTH = str(1.0/alpha) + "*" + FHEIGHT
            else:
                FWIDTH = FHEIGHT
            axis_options.append( "width="+FWIDTH )
    else:
        if aspect_num:
            print "Non-automatic aspect ratio demanded, but neither height " \
                  "nor width of the plot are given. Discard aspect ratio."
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # get ticks
    axis_options.extend( _get_ticks( 'x', obj.get_xticks(),
                                         obj.get_xticklabels() ) )
    axis_options.extend( _get_ticks( 'y', obj.get_yticks(),
                                         obj.get_yticklabels() ) )
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Don't use get_{x,y}gridlines for gridlines; see discussion on
    # <http://sourceforge.net/mailarchive/forum.php?thread_name=AANLkTima87pQkZmJhU2oNb8uxD2dfeV-Pa-uXWAFc2-v%40mail.gmail.com&forum_name=matplotlib-users>
    # Coordinate of the lines are entirely meaningless, but styles (colors,...
    # are respected.
    if obj.xaxis._gridOnMajor:
        axis_options.append( "xmajorgrids" )
    elif obj.xaxis._gridOnMinor:
        axis_options.append( "xminorgrids" )

    if obj.yaxis._gridOnMajor:
        axis_options.append( "ymajorgrids" )
    elif obj.yaxis._gridOnMinor:
        axis_options.append( "yminorgrids" )
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # find color bar
    colorbar = _find_associated_colorbar( obj )
    if colorbar:
        colorbar_styles = []

        orientation = colorbar.orientation
        limits = colorbar.get_clim()
        if orientation == 'horizontal':
            axis_options.append( "colorbar horizontal" )

            colorbar_ticks = colorbar.ax.get_xticks()
            axis_limits = colorbar.ax.get_xlim()

            # In matplotlib, the colorbar color limits are determined by
            # get_clim(), and the tick positions are as usual with respect to
            # {x,y}lim. In Pgfplots, however, they are mixed together.
            # Hence, scale the tick positions just like {x,y}lim are scaled
            # to clim.
            colorbar_ticks = (colorbar_ticks - axis_limits[0]) \
                             / (axis_limits[1] - axis_limits[0]) \
                             * (limits[1] - limits[0]) \
                             + limits[0]

            # Getting the labels via get_* might not actually be suitable:
            # they might not reflect the current state.
            # http://sourceforge.net/mailarchive/message.php?msg_name=AANLkTikdNFwSAhMIlLjnd4Ai8-XIdJYGmrwq6PrHkbgi%40mail.gmail.com
            colorbar_ticklabels = colorbar.ax.get_xticklabels()
            colorbar_styles.extend( _get_ticks( 'x', colorbar_ticks,
                                                    colorbar_ticklabels ) )

        elif orientation == 'vertical':
            axis_options.append( "colorbar" )
            colorbar_ticks = colorbar.ax.get_yticks()
            axis_limits = colorbar.ax.get_ylim()

            # In matplotlib, the colorbar color limits are determined by
            # get_clim(), and the tick positions are as usual with respect to
            # {x,y}lim. In Pgfplots, however, they are mixed together.
            # Hence, scale the tick positions just like {x,y}lim are scaled
            # to clim.
            colorbar_ticks = (colorbar_ticks - axis_limits[0]) \
                             / (axis_limits[1] - axis_limits[0]) \
                             * (limits[1] - limits[0]) \
                             + limits[0]

            # Getting the labels via get_* might not actually be suitable:
            # they might not reflect the current state.
            # http://sourceforge.net/mailarchive/message.php?msg_name=AANLkTikdNFwSAhMIlLjnd4Ai8-XIdJYGmrwq6PrHkbgi%40mail.gmail.com
            colorbar_ticklabels = colorbar.ax.get_yticklabels()
            colorbar_styles.extend( _get_ticks( 'y', colorbar_ticks,
                                                    colorbar_ticklabels ) )
        else:
            sys.exit( "Unknown color bar orientation \"%s\". Abort." % \
                      orientation )


        mycolormap, is_custom_cmap = _mpl_cmap2pgf_cmap( colorbar.get_cmap() )
        if is_custom_cmap:
            axis_options.append( "colormap=" + mycolormap )
        else:
            axis_options.append( "colormap/" + mycolormap )

        axis_options.append( 'point meta min=%e' % limits[0] )
        axis_options.append( 'point meta max=%e' % limits[1] )

        if colorbar_styles:
            axis_options.append( "colorbar style={%s}" % ",".join(colorbar_styles) )
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # actually print the thing
    if is_subplot:
        content.append( "\\nextgroupplot" )
    else:
        content.append( "\\begin{%s}" % env )

    # Run through the children objects, gather the content, and give them the
    # opportunity to contributethe EXTRA_AXIS_OPTIONS.
    children_content = _handle_children( obj )

    axis_options.extend( EXTRA_AXIS_OPTIONS )
    if axis_options:
        options = ",\n".join( axis_options )
        content.append( "[\n" + options + "\n]\n" )

    content.extend( children_content )

    if not is_subplot:
        content.append( "\\end{%s}\n\n" % env )
    elif is_subplot  and  nsubplots == subplot_index:
        content.append( "\\end{groupplot}\n\n" )
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    return content
# ==============================================================================
def _get_ticks( xy, ticks, ticklabels ):
    """
    Gets a {'x','y'}, a number of ticks and ticks labels, and returns the
    necessary axis options for the given configuration.
    """
    axis_options = []
    pgfplots_ticks = []
    pgfplots_ticklabels = []
    is_label_necessary = False
    for (tick, ticklabel) in izip(ticks, ticklabels):
        pgfplots_ticks.append( tick )
        # store the label anyway
        label = ticklabel.get_text()
        pgfplots_ticklabels.append( label )
        # Check if the label is necessary.
        # If *one* of the labels is, then all of them must
        # appear in the TikZ plot.
        is_label_necessary  =  (label and label != str(tick))
        # TODO This seems not quite to be the test whether labels are necessary.

    # Leave the ticks to Pgfplots if not in STRICT mode and if there are no
    # explicit labels.
    if STRICT or is_label_necessary:
        if pgfplots_ticks:
            axis_options.append( "%stick={%s}" % \
                                ( xy,
                                  ",".join(["%e" % el for el in pgfplots_ticks]) )
                              )
        else:
            axis_options.append( "%stick=\\empty" % xy )

        if is_label_necessary:
            axis_options.append( "%sticklabels={%s}" % \
                                ( xy, ",".join( pgfplots_ticklabels ) )
                              )
    return axis_options
# ==============================================================================
def _mpl_cmap2pgf_cmap( cmap ):
    """
    Converts a color map as given in matplotlib to a color map as represented
    in Pgfplots.
    """
    if not isinstance( cmap, mpl.colors.LinearSegmentedColormap ):
        print "Don't know how to handle color map. Using 'blackwhite'."
        is_custom_colormap = False
        return ('blackwhite', is_custom_colormap)

    if cmap.is_gray():
        is_custom_colormap = False
        return ('blackwhite', is_custom_colormap)


    segdata = cmap._segmentdata
    red    = segdata['red']
    green  = segdata['green']
    blue   = segdata['blue']

    # loop over the data, stop at each spot where the linear
    # interpolations is interrupted, and set a color mark there
    # set initial color
    k_red   = 0
    k_green = 0
    k_blue  = 0
    x = 0.0
    colors = []
    X = numpy.array([])
    while True:
        # find next x
        x = min( red[k_red][0], green[k_green][0], blue[k_blue][0] )

        if ( red[k_red][0]==x ):
            red_comp = red[k_red][1]
            k_red    = k_red+1
        else:
            red_comp = _linear_interpolation( x,
                                             ( red[k_red-1][0], red[k_red][0] ),
                                             ( red[k_red-1][2], red[k_red][1] )
                                            )

        if ( green[k_green][0]==x ):
            green_comp = green[k_green][1]
            k_green    = k_green+1
        else:
            green_comp = _linear_interpolation( x,
                                                ( green[k_green-1][0],
                                                  green[k_green]  [0]  ),
                                                ( green[k_green-1][2],
                                                  green[k_green]  [1]  )
                                              )

        if ( blue[k_blue][0]==x ):
            blue_comp = blue[k_blue][1]
            k_blue    = k_blue+1
        else:
            blue_comp = _linear_interpolation( x,
                                              ( blue[k_blue-1][0],
                                                blue[k_blue]  [0]  ),
                                              ( blue[k_blue-1][2],
                                                blue[k_blue]  [1]  )
                                            )

        X = numpy.append( X, x )
        colors.append( (red_comp, green_comp, blue_comp) )

        if x >= 1.0:
            break

    # The Pgfplots color map has an actual physical scale, like
    # (0cm,10cm), and the points where the colors change is also given
    # in those units. As of now (2010-05-06) it is crucial for Pgfplots
    # that the difference between two successive points is an integer
    # multiple of a given unity (parameter to the colormap; e.g., 1cm).
    # At the same time, TeX suffers from significant round-off errors,
    # so make sure that this unit is not too small such that the round-
    # off errors don't play much of a role. A unit of 1pt, e.g., does
    # most often not work
    unit = 'pt'

    # Scale to integer
    X = _scale_to_int( X )

    color_changes = []
    for (k, x) in enumerate(X):
        color_changes.append( "rgb(%d%s)=(%.3f,%.3f,%.3f)" % \
                              ( ( x, unit ) + colors[k] )
                            )

    colormap_string = "{mymap}{[1%s] %s }" % \
                      ( unit, "; ".join( color_changes ) )
    is_custom_colormap = True
    return ( colormap_string, is_custom_colormap )
# ==============================================================================
def _scale_to_int( X ):
    """
    Scales the array X such that i contains only integers.
    """
    X = X / _gcd_array( X )
    return [int(entry) for entry in X]
# ==============================================================================
def _gcd_array( X ):
    """
    Return the largest real value h such that all elements in x are integer
    multiples of h.
    """
    greatest_common_divisor = 0.0
    for x in X:
        greatest_common_divisor = _gcd( greatest_common_divisor, x )

    return greatest_common_divisor
# ==============================================================================
def _gcd( a, b ):
    """
    Euclidean algorithm for calculating the GCD of two numbers a, b.
    This algoritm also works for real numbers:
      Find the greatest number h such that a and b are integer multiples of h.
    """
    # Keep the tolerance somewhat significantly about machine precision,
    # as otherwise round-off errors will be accounted for, returning 1.0e-10
    # instead of 1 for the values
    #   [ 1.0, 2.0000000001, 3.0, 4.0 ].
    while a > 1.0e-5:
        a, b = b % a, a
    return b
# ==============================================================================
def _linear_interpolation( x, X, Y ):
    """
    Given two data points [X,Y], linearly interpolate those at x.
    """
    return ( Y[1]*(x-X[0]) + Y[0]*(X[1]-x) ) / ( X[1]-X[0] )
# ==============================================================================
TIKZ_LINEWIDTHS = { 0.1: 'ultra thin',
                    0.2: 'very thin',
                    0.4: 'thin',
                    0.6: 'semithick',
                    0.8: 'thick',
                    1.2: 'very thick',
                    1.6: 'ultra thick' }
# ------------------------------------------------------------------------------
def _draw_line2d( obj ):
    """
    Returns the Pgfplots code for an Line2D environment.
    """
    content = []

    addplot_options = []

    # --------------------------------------------------------------------------
    # get the linewidth (in pt)
    line_width = obj.get_linewidth()

    if STRICT:
        # Takes the matplotlib linewidths, and just translate them
        # into Pgfplots.
        try:
            addplot_options.append( TIKZ_LINEWIDTHS[ line_width ] )
        except KeyError:
            # explicit line width
            addplot_options.append( "line width=%spt" % line_width )
    else:
        # The following is an alternative approach to line widths.
        # The default line width in matplotlib is 1.0pt, in Pgfplots 0.4pt
        # ("thin").
        # Match the two defaults, and scale for the rest.
        scaled_line_width = line_width / 1.0  # scale by default line width
        if scaled_line_width == 0.25:
            addplot_options.append( "ultra thin" )
        elif scaled_line_width == 0.5:
            addplot_options.append( "very thin" )
        elif scaled_line_width == 1.0:
            pass # Pgfplots default line width, "thin"
        elif scaled_line_width == 1.5:
            addplot_options.append( "semithick" )
        elif scaled_line_width == 2:
            addplot_options.append( "thick" )
        elif scaled_line_width == 3:
            addplot_options.append( "very thick" )
        elif scaled_line_width == 4:
            addplot_options.append( "ultra thick" )
        else:
            # explicit line width
            addplot_options.append( "line width=%spt" % 0.4*line_width )
    # --------------------------------------------------------------------------
    # get line color
    color = obj.get_color()
    xcolor = _mpl_color2xcolor(color)
    if xcolor:
        addplot_options.append( xcolor )

    linestyle = _mpl_linestyle2pgfp_linestyle( obj.get_linestyle() )
    if linestyle:
        addplot_options.append( linestyle )

    marker_face_color = obj.get_markerfacecolor()
    marker_edge_color = obj.get_markeredgecolor()
    marker, extra_mark_options = _mpl_marker2pgfp_marker( obj.get_marker(),
                                                         marker_face_color )
    if marker:
        addplot_options.append( "mark=" + marker )

        mark_options = []
        if extra_mark_options:
            mark_options.append( extra_mark_options )
        if marker_face_color:
            col = _mpl_color2xcolor( marker_face_color )
            mark_options.append( "fill=" + col )
        if marker_edge_color  and  marker_edge_color != marker_face_color:
            col = _mpl_color2xcolor( marker_edge_color )
            mark_options.append( "draw=" + col )
        if mark_options:
            addplot_options.append( "mark options={%s}" % \
                                    ",".join(mark_options)
                                  )

    if marker and not linestyle:
        addplot_options.append( "only marks" )

    # process options
    content.append( "\\addplot " )
    if addplot_options:
        options = ", ".join( addplot_options )
        content.append( "[" + options + "]\n" )

    content.append( "coordinates {\n" )

    # print the hard numerical data
    xdata, ydata = obj.get_data()
    try:
        has_mask = ydata.mask.any()
    except AttributeError:
        has_mask = 0
    if has_mask:
        # matplotlib jumps at masked images, while Pgfplots by default
        # interpolates. Hence, if we have a masked plot, make sure that Pgfplots
        # jump as well.
        EXTRA_AXIS_OPTIONS.add( 'unbounded coords=jump' )
        for (x, y, is_masked) in izip(xdata, ydata, ydata.mask):
            if is_masked:
                content.append( "(%e,nan) " % x )
            else:
                content.append( "(%e,%e) " % (x, y) )
    else:
        for (x, y) in izip(xdata, ydata):
            content.append( "(%e,%e) " % (x, y) )
    content.append( "\n};\n" )

    return content
# ==============================================================================
# for matplotlib markers, see
# http://matplotlib.sourceforge.net/api/artist_api.html#matplotlib.lines.Line2D.set_marker
MP_MARKER2PGF_MARKER = { '.'   : '*', # point
                         'o'   : 'o', # circle
                         '+'   : '+', # plus
                         'x'   : 'x', # x
                         'None': None,
                         ' '   : None,
                         ''    : None
                       }
# the following markers are only available with PGF's plotmarks library
MP_MARKER2PLOTMARKS = { 'v' : ('triangle', 'rotate=180'), # triangle down
                        '1' : ('triangle', 'rotate=180'), 
                        '^' : ('triangle', None), # triangle up
                        '2' : ('triangle', None),
                        '<' : ('triangle', 'rotate=270'), # triangle left
                        '3' : ('triangle', 'rotate=270'),
                        '>' : ('triangle', 'rotate=90'), # triangle right
                        '4' : ('triangle', 'rotate=90'),
                        's' : ('square', None),
                        'p' : ('pentagon', None),
                        '*' : ('asterisk', None),
                        'h' : ('star', None), # hexagon 1
                        'H' : ('star', None), # hexagon 2
                        'd' : ('diamond', None), # diamond
                        'D' : ('diamond', None), # thin diamond
                        '|' : ('|', None), # vertical line
                        '_' : ('_', None)  # horizontal line
                      }
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def _mpl_marker2pgfp_marker( mpl_marker, is_marker_face_color ):
    """
    Translates a marker style of matplotlib to the corresponding style
    in Pgfplots.
    """
    # try default list
    try:
        pgfplots_marker = MP_MARKER2PGF_MARKER[ mpl_marker ]
        if is_marker_face_color and pgfplots_marker == 'o':
            pgfplots_marker = '*'
            PGFPLOTS_LIBS.add( 'plotmarks' )
        marker_options = None
        return ( pgfplots_marker, marker_options )
    except KeyError:
        pass

    # try plotmarks list    
    try:
        PGFPLOTS_LIBS.add( 'plotmarks' )
        pgfplots_marker, marker_options = MP_MARKER2PLOTMARKS[ mpl_marker ]
        if is_marker_face_color and not pgfplots_marker in ['|', '_']:
            pgfplots_marker += '*'
        return ( pgfplots_marker, marker_options )
    except KeyError:
        pass

    if mpl_marker == ',': # pixel
        print 'Unsupported marker \"' + mpl_marker + '\".'
    else:
        print 'Unknown marker \"' + mpl_marker + '\".'

    return ( None, None )
# ==============================================================================
MPLLINESTYLE_2_PGFPLOTSLINESTYLE = { '-'   : None,
                                     'None': None,
                                     ':'   : 'dotted',
                                     '--'  : 'dashed',
                                     '-.'  : 'dash pattern=on 1pt off 3pt ' \
                                             'on 3pt off 3pt'
                                   }
# ------------------------------------------------------------------------------
def _mpl_linestyle2pgfp_linestyle( line_style ):
    """
    Translates a line style of matplotlib to the corresponding style
    in Pgfplots.
    """
    try:
        return MPLLINESTYLE_2_PGFPLOTSLINESTYLE[ line_style ]
    except KeyError:
        print 'Unknown line style \"' + str(line_style) + '\".'
        return None
# ==============================================================================
def _draw_image( obj ):
    """
    Returns the Pgfplots code for an image environment.
    """
    content = []

    global IMG_NUMBER
    IMG_NUMBER = IMG_NUMBER+1

    filename = os.path.join( OUTPUT_DIR,
                             "img" + str(IMG_NUMBER) + ".png" )

    # store the image as in a file
    img_array = obj.get_array()

    dims = img_array.shape
    if len(dims)==2: # the values are given as one real number: look at cmap
        clims = obj.get_clim()
        mpl.pyplot.imsave( fname = filename,
                           arr   = img_array ,
                           cmap  = obj.get_cmap(),
                           vmin  = clims[0],
                           vmax  = clims[1] )
    elif len(dims) == 3 and dims[2] in [3, 4]:
        # RGB (+alpha) information at each point
        import Image
        # convert to PIL image (after upside-down flip)
        image = Image.fromarray( numpy.flipud(img_array) )
        image.save( filename )
    else:
        sys.exit( 'Unable to store image array.' )

    # write the corresponding information to the TikZ file
    extent = obj.get_extent()

    # the format specification will only accept tuples, not lists
    if isinstance(extent, list): # convert to () list
        extent = tuple(extent)

    if REL_DATA_PATH:
        rel_filepath = os.path.join( REL_DATA_PATH, os.path.basename(filename) )
    else:
        rel_filepath = os.path.basename(filename)

    # Explicitly use \pgfimage as includegrapics command, as the default
    # \includegraphics fails unexpectedly in some cases
    content.append(  "\\addplot graphics [includegraphics cmd=\pgfimage," \
                                          "xmin=%e, xmax=%e, " \
                                          "ymin=%e, ymax=%e] {%s};\n" % \
                                          ( extent + (rel_filepath,) )
                  )

    content.extend( _handle_children( obj ) )

    return content
# ==============================================================================
def _draw_polygon( obj ):
    """
    Return the Pgfplots code for polygons.
    """
    # TODO do nothing for polygons?!
    content = []
    content.extend( _handle_children( obj ) )
    return
# ==============================================================================
def _find_associated_colorbar( obj ):
    """
    Rather poor way of telling whether an axis has a colorbar associated:
    Check the next axis environment, and see if it is de facto a color bar;
    if yes, return the color bar object.
    """
    for child in obj.get_children():
        try:
            cbar = child.colorbar
        except AttributeError:
            continue
        if not cbar == None: # really necessary?
            # if fetch was successful, cbar contains
            # ( reference to colorbar,
            #   reference to axis containing colorbar )
            return cbar[0]
    return None
# ==============================================================================
def _is_colorbar( obj ):
    """
    Returns 'True' if 'obj' is a  color bar, and 'False' otherwise.
    """
    # TODO Are the colorbars exactly the l.collections.PolyCollection's?
    if isinstance( obj, mpl.collections.PolyCollection ):
        arr = obj.get_array()
        dims = arr.shape
        if len(dims) == 1:
            return True # o rly?
        else:
            return False
    else:
        return False
# ==============================================================================
def _extract_colorbar( obj ):
    """
    Search for color bars as subobjects of obj, and return the first found.
    If none is found, return None.
    """
    colorbars = mpl.pyplot.findobj( obj, _is_colorbar )

    if not colorbars:
        return None
    if not _equivalent( colorbars ):
        print "More than one color bar found. Use first one."

    return colorbars[0]
# ==============================================================================
def _equivalent( array ):
    """
    Checks if the vectors consists of all the same objects.
    """
    if not array:
        return False
    else:
        for elem in array:
            if elem != array[0]:
                return False

    return True
# ==============================================================================
def _draw_polycollection( obj ):
    """
    Returns Pgfplots code for a number of polygons.
    Currently empty.
    """
    print "matplotlib2tikz: Don't know how to draw a PolyCollection."
    return None
# ==============================================================================
def _draw_patchcollection( obj ):
    """
    Returns Pgfplots code for a number of patch objects.
    """

    content = []

    # TODO Use those properties
    #edgecolors = obj.get_edgecolors()
    #edgecolor = obj.get_edgecolor()
    #facecolors = obj.get_facecolors()
    #linewidths = obj.get_linewidths()

    paths = obj.get_paths()
    for path in paths:
        content.append( _draw_path( path ) )

    return content
# ==============================================================================
def _draw_path( path ):
    """
    Adds code for drawing an ordinary path in Pgfplots (TikZ).
    """

    nodes = []
    for vert, code in path.iter_segments():
        # TODO respect the path code,
        #      <http://matplotlib.sourceforge.net/api/path_api.html#matplotlib.path.Path>
        if len(vert) == 2:
            nodes.append( '(axis cs:%s,%s)' % ( str(vert[0]), str(vert[1]) ) )
        elif len(vert) == 6:
            # This is actually a Bezier curve, but can't deal with this yet.
            nodes.append( '(axis cs:%s,%s)' % ( str(vert[0]), str(vert[1]) ) )
            nodes.append( '(axis cs:%s,%s)' % ( str(vert[2]), str(vert[3]) ) )
            nodes.append( '(axis cs:%s,%s)' % ( str(vert[4]), str(vert[5]) ) )
        else:
            sys.exit( "Strange." )

    return '\\path [fill] %s;\n\n' % "--".join( nodes )
# ==============================================================================
MPLCOLOR_2_XCOLOR = { # RGB values:
                      (1,    0,    0   ): 'red',
                      (0,    1,    0   ): 'green',
                      (0,    0,    1   ): 'blue',
                      (0.75, 0.5,  0.25): 'brown',
                      (0.75, 1,    0   ): 'lime',
                      (1,    0.5,  0   ): 'orange',
                      (1,    0.75, 0.75): 'pink',
                      (0.75, 0,    0.25): 'purple',
                      (0,    0.5,  0.5 ): 'teal',
                      (0.5,  0,    0.5 ): 'violet',
                      # gray values:
                      '0.0' : 'red',
                      '0.5' : 'gray',
                      '0.75': 'lightgray',
                      '1.0' : None,
                      # literals:
                      'b'    : 'blue',
                      'blue' : 'blue',
                      'g'    : 'green',
                      'green': 'green',
                      'r'    : 'red',
                      'red'  : 'red',
                      'c'    : 'cyan',
                      'm'    : 'magenta',
                      'y'    : 'yellow',
                      'k'    : 'black',
                      'w'    : 'white'
                    }
# ------------------------------------------------------------------------------
def _mpl_color2xcolor( color ):
    """
    Translates a matplotlib color specification into a proper LaTeX
    xcolor.
    """
    try:
        return MPLCOLOR_2_XCOLOR[ color ]
    except KeyError:
        if isinstance( color, types.TupleType ) and len(color)==3:
            # add a custom color
            return _add_rgbcolor_definition( color )
        else:
            print "Unknown color \"" + color  + "\". Giving up."
            return None
# ==============================================================================
def _add_rgbcolor_definition( rgb_color_tuple ):
    """
    Takes an RGB color tuple, adds it to the list of colors that will need to be
    defined in the TikZ file, and returned the label with which the color can
    be used.
    """
    if rgb_color_tuple not in CUSTOM_COLORS:
        CUSTOM_COLORS[ rgb_color_tuple ] = 'color' + str(len(CUSTOM_COLORS))

    return CUSTOM_COLORS[ rgb_color_tuple ]
# ==============================================================================
def _draw_legend( obj ):
    """
    Adds legend code to the EXTRA_AXIS_OPTIONS.
    """
    texts = []
    for text in obj.texts:
        texts.append( "%s" % text.get_text() )

    EXTRA_AXIS_OPTIONS.add( 'legend entries={%s}' % ",".join( texts )  )

    return
# ==============================================================================
def _draw_text( obj ):  
    """
    Paints text on the graph
    """
    content = []
    properties = []
    style = []
    # 1: coordinates in axis system
    # 2: properties (shapes, rotation, etc)
    # 3: text style
    # 4: the text
    #                   ------ 1 -------2---3--4--
    proto = "\\node at (axis cs:%e,%e)[%s]{%s %s};\n"
    pos = obj.get_position()
    text = obj.get_text()
    bbox = obj.get_bbox_patch()
    bbox_style = bbox.get_boxstyle()
    converter = mpl.colors.ColorConverter()
    if bbox.get_fill():
        properties.append("fill=%s"%_mpl_color2xcolor(bbox.get_facecolor()))
    # Rounded boxes
    if( isinstance(bbox_style, mpl.patches.BoxStyle.Round) ):
        properties.append("rounded corners")
    elif( isinstance(bbox_style, mpl.patches.BoxStyle.RArrow) ):
        TIKZ_LIBS.add("shapes.arrows")
        properties.append("single arrow")
    elif( isinstance(bbox_style, mpl.patches.BoxStyle.LArrow) ):
        TIKZ_LIBS.add("shapes.arrows")
        properties.append("single arrow")
        properties.append("shape border rotate=180")
    # Sawtooth, Roundtooth or Round4 not supported atm
    # Round4 should be easy with "rounded rectangle"
    # directive though.
    else:
        pass # Rectangle
    # Line style
    if(bbox.get_ls() == "dotted"):
        properties.append("dotted")
    elif(bbox.get_ls() == "dashed"):
        properties.append("dashed")
    # TODO: Fix this
    elif(bbox.get_ls() == "dashdot"):
        pass
    else:
        pass # solid

    ha = obj.get_ha()
    va = obj.get_va()
    anchor = _transform_positioning(ha,va)
    if anchor is not None:
        properties.append(anchor)
    properties.append("draw=%s"%_mpl_color2xcolor(bbox.get_edgecolor()))
    properties.append("text=%s"%_mpl_color2xcolor( converter.to_rgb(obj.get_color()) ))
    properties.append("rotate=%.1f"%obj.get_rotation())
    properties.append("line width=%g"%(bbox.get_lw()*0.4)) # XXX: Ugly as hell
    if obj.get_style() <> "normal":
        style.append("\\itshape")
    content.append(proto%(pos[0],pos[1],",".join(properties)," ".join(style),text))
    return content

def _transform_positioning(ha, va):
    """
    Converts matplotlib positioning to pgf node positioning.
    Not quite accurate but the results are equivalent more or less
    """
    if (ha == "center" and va == "center"):
        return None
    else:
        ha_mpl_to_tikz = {'right':'east',
                          'left':'west',
                          'center':''}
        va_mpl_to_tikz = {'top':'north',
                          'bottom':'south',
                          'center':'',
                          'baseline':'base'}
        return "anchor=%s %s"%(va_mpl_to_tikz[va],ha_mpl_to_tikz[ha])


# ==============================================================================
def _handle_children( obj ):
    """
    Iterates over all children of the current object, gathers the contents
    contributing to the resulting Pgfplots file, and returns those.
    """

    content = []
    for child in obj.get_children():
        if ( isinstance( child, mpl.axes.Axes ) ):
            try:
                content.extend( _draw_axes( child ) )
            except TypeError: # _draw_axes() probably returned None
                pass
        elif ( isinstance( child, mpl.lines.Line2D ) ):
            content.extend( _draw_line2d( child ) )
        elif ( isinstance( child, mpl.image.AxesImage ) ):
            content.extend( _draw_image( child ) )
        elif ( isinstance( child, mpl.patches.Polygon ) ):
            content.extend( _draw_polygon( child ) )
        elif ( isinstance( child, mpl.collections.PolyCollection ) ):
            content.extend( _draw_polycollection( child ) )
        elif ( isinstance( child, mpl.collections.PatchCollection ) ):
            content.extend( _draw_patchcollection( child ) )
        elif ( isinstance( child, mpl.legend.Legend ) ):
            _draw_legend( child )
        elif (   isinstance( child, mpl.axis.XAxis )
              or isinstance( child, mpl.axis.YAxis )
              or isinstance( child, mpl.spines.Spine )
              or isinstance( child, mpl.patches.Rectangle )
              or isinstance( child, mpl.text.Text )
             ):
            pass
        else:
            print "matplotlib2tikz: Don't know how to handle object \"%s\"." % \
                  type(child)

    # XXX: This is ugly
    if isinstance(obj, mpl.axes.Subplot) or isinstance(obj,mpl.figure.Figure):
        for text in obj.texts:
            content.extend(_draw_text(text))

    return content
# ==============================================================================
def _print_pgfplot_libs_message():
    """
    Prints message to screen indicating the use of Pgfplots and its libraries.
    """
    pgfplotslibs = ",".join( list( PGFPLOTS_LIBS ) )
    tikzlibs = ",".join( list( TIKZ_LIBS ) )

    print "========================================================="
    print "Please add the following line to your LaTeX preamble:\n"
    print "\usepackage{pgfplots}"
    if tikzlibs:
        print "\usetikzlibrary{"+ tikzlibs +"}"
    if pgfplotslibs:
        print "\usepgfplotslibrary{" + pgfplotslibs + "}"
    print "========================================================="

    return
# ==============================================================================
