#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Insert proper documentation
"""

# ==============================================================================
# imported modules
import matplotlib as mpl
import numpy
import types
# ==============================================================================
# meta info
__author__     = "Nico Schlömer"
__copyright__  = "Copyright (c) 2010, Nico Schlömer <nico.schloemer@gmail.com>"
__credits__    = ["Nico Schlömer"]
__license__    = "GNU Lesser General Public License (LGPL), Version 3"
__version__    = "0.1.0_pre"
__maintainer__ = "Nico Schlömer"
__email__      = "nico.schloeme@gmail.com"
__status__     = "Development"
# ==============================================================================
# global variables
FWIDTH        = None
FHEIGHT       = None
REL_DATA_PATH = None
PGFPLOTS_LIBS = None
OUTPUT_DIR    = None
IMG_NUMBER    = -1
# ==============================================================================
def print_tree( obj, indent = "" ):
    """
    Recursively prints the tree structure of the matplotlib object.
    """
    print indent, type(obj)
    for child in obj.get_children():
        print_tree( child, indent + "   " )
    return
# ==============================================================================
def matplotlib2tikz( filepath,
                     figurewidth = None,
                     figureheight = None,
                     tex_relative_path_to_data = None ):

    from os import path

    global FWIDTH    
    FWIDTH        = figurewidth
    global FHEIGHT
    FHEIGHT       = figureheight
    global REL_DATA_PATH
    REL_DATA_PATH = tex_relative_path_to_data
    global PGFPLOTS_LIBS
    PGFPLOTS_LIBS = []
    global OUTPUT_DIR
    OUTPUT_DIR    = path.dirname(filepath)

    # open file
    file_handle = open( filepath, "w" )

    # write the contents
    file_handle.write( "\\begin{tikzpicture}\n\n" )
    handle_children( file_handle, mpl.pyplot.gcf() )
    file_handle.write( "\\end{tikzpicture}" )

    # close file
    file_handle.close()
    
    # print message about necessary pgfplot libs to command line
    print_pgfplot_libs_message()
    return
# ==============================================================================
def draw_axes( file_handle, obj ):
    """
    Returns the Pgfplots code for an axis environment.
    """

    # Are we dealing with an axis that hosts a colorbar?
    # Skip then.
    # TODO instead of testing here, rather blacklist the colorbar axis
    #      plots as soon as they have been found, e.g., by
    #      find_associated_colorbar()
    if extract_colorbar(obj):
        return

    # instantiation
    nsubplots = 1
    subplot_index = 0
    issubplot = False

    if isinstance( obj, mpl.axes.Subplot ):
        geom = obj.get_geometry()
        nsubplots = geom[0]*geom[1]
        if nsubplots > 1:
            issubplot = True
            subplot_index = geom[2]
            if subplot_index == 1:
                file_handle.write( "\\begin{groupplot}[group style=" \
                                   "{group size=%.d by %.d}]\n" % \
                                   (geom[1],geom[0]) )
                PGFPLOTS_LIBS.append( "groupplots" )

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
    axis_options.append(     "xmin=" + str(xlim[0])
                         + ", xmax=" + str(xlim[1]) )
    ylim = sorted( list( obj.get_ylim() ) )
    axis_options.append(     "ymin=" + str(ylim[0])
                         + ", ymax=" + str(ylim[1]) )
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
            print "aspect was not a number!"

    global FWIDTH
    global FHEIGHT
    if FWIDTH or FHEIGHT:
        axis_options.append( "scale only axis" )

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
    axis_options += get_ticks( 'x', obj.get_xticks(), obj.get_xticklabels() )
    axis_options += get_ticks( 'y', obj.get_yticks(), obj.get_yticklabels() )
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
    colorbar = find_associated_colorbar( obj )
    if colorbar != None:
        clim = colorbar.get_clim()
        axis_options.append( "colorbar=true" )
        mycolormap = mpl_cmap2pgf_cmap( colorbar.get_cmap() )
        axis_options.append( "colormap=" + mycolormap )
        axis_options.append( 'point meta min=' + str(clim[0]) )
        axis_options.append( 'point meta max=' + str(clim[1]) )
        colorbar_styles = []
        cbar_yticks = colorbar.ax.get_yticks()
        colorbar_styles.append( "ytick={%s}" % \
                                ",".join(["%s" % el for el in cbar_yticks])
                              )
        axis_options.append( "colorbar style={%s}" % \
                             ",".join(colorbar_styles)
                           )
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # actually print the thing
    if issubplot:
        file_handle.write( "\\nextgroupplot" )
    else:
        file_handle.write( "\\begin{axis}" )

    if axis_options:
        options = ",\n".join( axis_options )
        file_handle.write( "[\n" + options + "\n]\n" )

    # TODO Use get_lines()?
    handle_children( file_handle, obj )

    if not issubplot:
        file_handle.write( "\\end{axis}\n\n" )
    elif issubplot  and  nsubplots == subplot_index:
        file_handle.write( "\\end{groupplot}\n\n" )

    return
# ==============================================================================
def get_ticks( xy, ticks, ticklabels ):
    """
    Gets a {'x','y'}, a number of ticks and ticks labels, and returns the
    necessary axis options for the given configuration.
    """
    pgfplots_ticks = []
    pgfplots_ticklabels = []
    is_label_necessary = False
    for (k, tick) in enumerate(ticks):
        pgfplots_ticks.append( tick )
        # store the label anyway
        label = ticklabels[k].get_text()
        pgfplots_ticklabels.append( label )
        # Check if the label is necessary.
        # If *one* of the labels is, then all of them must
        # appear in the TikZ plot.
        is_label_necessary  =  label!=str(tick)

    axis_options = []

    if pgfplots_ticks:
        axis_options.append( "%stick={%s}" % \
                             ( xy,
                               ",".join(["%s" % el for el in pgfplots_ticks]) )
                           )
    else:
        axis_options.append( "%stick=\\empty" % xy )

    if is_label_necessary:
        axis_options.append( "%sticklabels={%s}" % \
                             ( xy, ",".join( pgfplots_ticklabels ) )
                           )
    return axis_options
# ==============================================================================
def mpl_cmap2pgf_cmap( cmap ):
    """
    Converts a color map as given in matplotlib to a color map as represented
    in Pgfplots.
    """
    if isinstance( cmap, mpl.colors.LinearSegmentedColormap ):
        if cmap.is_gray():
            return 'blackwhite'
        else:
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
                    red_comp = linear_interpolation( x,
                                                     ( red[k_red-1][0],
                                                       red[k_red]  [0]  ),
                                                     ( red[k_red-1][2],
                                                       red[k_red]  [1]  )
                                                   )
    
                if ( green[k_green][0]==x ):
                    green_comp = green[k_green][1]
                    k_green    = k_green+1
                else:
                    green_comp = linear_interpolation( x,
                                                       ( green[k_green-1][0],
                                                         green[k_green]  [0]  ),
                                                       ( green[k_green-1][2],
                                                         green[k_green]  [1]  )
                                                     )
    
                if ( blue[k_blue][0]==x ):
                    blue_comp = blue[k_blue][1]
                    k_blue    = k_blue+1
                else:
                    blue_comp = linear_interpolation( x,
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
            X = scale_to_int( X )

            color_changes = []
            for (k, x) in enumerate(X):
                color_changes.append( "rgb(%d%s)=(%.3f,%.3f,%.3f)" % \
                                      ( ( x, unit ) + colors[k] )
                                    )
          
            return "{mymap}{[1%s] %s }" % \
                   ( unit, "; ".join( color_changes ) )

    else :
        print "Don't know how to handle color map. Using 'blackwhite'."
        return 'blackwhite'
# ==============================================================================
def scale_to_int( X ):
    """
    Scales the array X such that i contains only integers.
    """
    X = X / gcd_array( X )
    return [int(entry) for entry in X]
# ==============================================================================
def gcd_array( X ):
    """
    Return the largest real value h such that all elements in x are integer
    multiples of h.
    """
    greatest_common_divisor = 0.0
    for x in X:
        greatest_common_divisor = gcd( greatest_common_divisor, x )

    return greatest_common_divisor
# ==============================================================================
def gcd( a, b ):
    """
    Euclidean algorithm for calculating the GCD of two numbers a, b.
    This algoritm also works for real numbers:
      Find the greatest number h such that a and b are integer multiples of h.
    """
    while a > 1.0e-10:
            a, b = b % a, a
    return b
# ==============================================================================
def linear_interpolation( x, X, Y ):
    """
    Given two data points [X,Y], linearly interpolate those at x.
    """
    return ( Y[1]*(x-X[0]) + Y[0]*(X[1]-x) ) / ( X[1]-X[0] )
# ==============================================================================
def draw_line2d( file_handle, obj ):
    """
    Returns the Pgfplots code for an Line2D environment.
    """

    addplot_options = []

    # get line color
    color = obj.get_color()
    xcolor = mpl_color2xcolor(color)
    if xcolor:
        addplot_options.append( xcolor )

    linestyle = mpl_linestyle2pgfp_linestyle( obj.get_linestyle() )
    if linestyle:
        addplot_options.append( linestyle )

    marker_face_color = obj.get_markerfacecolor()
    marker, extra_mark_options = mpl_marker2pgfp_marker( obj.get_marker(),
                                                         marker_face_color )
    if marker:
        addplot_options.append( "mark=" + marker )

        mark_options = []
        if extra_mark_options:
            mark_options.append( extra_mark_options )
        if marker_face_color:
            col = mpl_color2xcolor( marker_face_color )
            mark_options.append( "fill=" + col )
        if mark_options:
            addplot_options.append( "mark options={%s}" % \
                                    ",".join(mark_options)
                                  )

    if marker and not linestyle:
        addplot_options.append( "only marks" )

    # process options
    file_handle.write( "\\addplot " )
    if addplot_options:
        options = ", ".join( addplot_options )
        file_handle.write( "[" + options + "]\n" )

    # print the hard numerical data
    xdata, ydata = obj.get_data()
    file_handle.write(  "coordinates {\n" )
    for (k, x) in enumerate(xdata):
        file_handle.write( "(%.15g,%.15g) " % (x, ydata[k]) )
    file_handle.write( "\n};\n" )

    return
# ==============================================================================
def mpl_marker2pgfp_marker( mpl_marker, is_marker_face_color ):
    """
    Translates a marker style of matplotlib to the corresponding style
    in Pgfplots.
    """
    marker_options = None

    # for matplotlib markers, see
    # http://matplotlib.sourceforge.net/api/artist_api.html#matplotlib.lines.Line2D.set_marker
    if mpl_marker == '.': # point
        pgfplots_marker = '*'
    elif mpl_marker == 'o': # circle
        if is_marker_face_color:
            pgfplots_marker = '*'
        else:
            pgfplots_marker = 'o' # only with plotmarks
    elif mpl_marker == '+': # plus
        pgfplots_marker = '+'
    elif mpl_marker == 'x': # x
        pgfplots_marker = 'x'
    elif mpl_marker in [ 'None', ' ', '' ] : # nothing
        pgfplots_marker = None
    else:  # the following markers are only available with PGF's
           # plotmarks library
        print 'Make sure to load \\usetikzlibrary{plotmarks} in the preamble.'
        if mpl_marker in ['v','1']: # triangle down
            marker_options = 'rotate=180'
            if is_marker_face_color:
                pgfplots_marker = 'triangle*'
            else:
                pgfplots_marker = 'triangle'
        elif mpl_marker in ['^','2']: # triangle up
            if is_marker_face_color:
                pgfplots_marker = 'triangle*'
            else:
                pgfplots_marker = 'triangle'
        elif mpl_marker in ['<','3']: # triangle left
            marker_opions = 'rotate=270'
            if is_marker_face_color:
                pgfplots_marker = 'triangle*'
            else:
                pgfplots_marker = 'triangle'
        elif mpl_marker in ['>','4']: # triangle right
            marker_opions = 'rotate=90'
            if is_marker_face_color:
                pgfplots_marker = 'triangle*'
            else:
                pgfplots_marker = 'triangle'
        elif mpl_marker == 's': # square
            if is_marker_face_color:
                pgfplots_marker = 'square*'
            else:
                pgfplots_marker = 'square'
        elif mpl_marker == 'p': # pentagon
            if is_marker_face_color:
                pgfplots_marker = 'pentagon*'
            else:
                pgfplots_marker = 'pentagon'
        elif mpl_marker == '*': # star
            pgfplots_marker = 'asterisk'
        elif mpl_marker in ['h','H']: # hexagon 1, hexagon 2
            if is_marker_face_color:
                pgfplots_marker = 'star*'
            else:
                pgfplots_marker = 'star'
        elif mpl_marker in ['D','d']: # diamond, thin diamond
            if is_marker_face_color:
                pgfplots_marker = 'diamond*'
            else:
                pgfplots_marker = 'diamond'
        elif mpl_marker == '|': # vertical line
            pgfplots_marker = '|'
        elif mpl_marker == '_': # horizontal line
            pgfplots_marker = '_'
        elif mpl_marker in [',']: # pixel
            print 'Unsupported marker \"' + mpl_marker + '\".'
            pgfplots_marker = None
        else:
            print 'Unknown marker \"' + mpl_marker + '\".'
            pgfplots_marker = None

    return ( pgfplots_marker, marker_options )
# ==============================================================================
def mpl_linestyle2pgfp_linestyle( line_style ):
    """
    Translates a line style of matplotlib to the corresponding style
    in Pgfplots.
    """
    if (line_style == '-' or line_style == 'None'):
        return None
    elif line_style == ':':
        return 'dotted'
    elif line_style == '--':
        return 'dashed'
    else:
        print '%Unknown line style \"' + str(line_style) + '\".'
        return None
# ==============================================================================
def draw_image( file_handle, obj ):
    """
    Returns the Pgfplots code for an image environment.
    """
    from os import path
    
    global IMG_NUMBER
    IMG_NUMBER = IMG_NUMBER+1

    global OUTPUT_DIR
    filename = path.join( OUTPUT_DIR,
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
    elif len(dims) == 3: # RGB information
        if dims[2] == 4: # RGB+alpha information at each point
            import Image
            # convert to PIL image (after upside-down flip)
            image = Image.fromarray( numpy.flipud(img_array), 'RGBA' )
            image.save( filename )

    # write the corresponding information to the TikZ file
    extent = obj.get_extent()

    # the format specification will only accept tuples, not lists
    if isinstance(extent, list): # convert to () list
        extent = tuple(extent)

    if REL_DATA_PATH:
        rel_filepath = path.join( REL_DATA_PATH,  path.basename(filename) )
    else:
        rel_filepath = path.basename(filename)

    # Explicitly use \pgfimage as includegrapics command, as the default
    # \includegraphics fails unexpectedly in some cases
    file_handle.write( "\\addplot graphics [ includegraphics cmd=\pgfimage,"
                                             "xmin=%.15g, xmax=%.15g, "
                                             "ymin=%.15g, ymax=%.15g] {%s};\n" % \
                       ( extent + (rel_filepath,) )
                      )

    handle_children( file_handle, obj )

    return
# ==============================================================================
def draw_polygon( file_handle, obj ):
    """
    Return the Pgfplots code for polygons.
    """
    # TODO do nothing for polygons?!
    handle_children( file_handle, obj )
    return
# ==============================================================================
def find_associated_colorbar( obj ):
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
def is_colorbar( obj ):
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
def extract_colorbar( obj ):
    """
    Search for color bars as subobjects of obj, and return the first found.
    If none is found, return None.
    """
    colorbars = mpl.pyplot.findobj( obj, is_colorbar )

    if not colorbars:
        return None
    if not equivalent( colorbars ):
        print "More than one color bar found. Use first one."

    return colorbars[0]
# ==============================================================================
def equivalent( array ):
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
def draw_polycollection( file_handle, obj ):
    print "matplotlib2tikz: Don't know how to draw a PolyCollection."
    return
# ==============================================================================
def draw_patchcollection( file_handle, obj ):
    print "matplotlib2tikz: Don't know how to draw a PatchCollection."

    edgecolors = obj.get_edgecolors()
    print edgecolors

    edgecolor = obj.get_edgecolor()
    print edgecolor

    facecolors = obj.get_facecolors()
    print facecolors

    linewidths = obj.get_linewidths()
    print linewidths

    paths = obj.get_paths()
    print len(paths)

    for path in paths:
        draw_path( file_handle, path )

    return
# ==============================================================================
def draw_path( file_handle, path ):

    nodes = []
    for vert,code in path.iter_segments():
        # TODO respect the path code,
        #      <http://matplotlib.sourceforge.net/api/path_api.html#matplotlib.path.Path>
        if len(vert)==2:
            nodes.append( '(axis cs:%s,%s)' % ( str(vert[0]), str(vert[1]) ) )
        elif len(vert)==6:
            # This is actually a Bezier curve, but can't deal with this yet.
            nodes.append( '(axis cs:%s,%s)' % ( str(vert[0]), str(vert[1]) ) )
            nodes.append( '(axis cs:%s,%s)' % ( str(vert[2]), str(vert[3]) ) )
            nodes.append( '(axis cs:%s,%s)' % ( str(vert[4]), str(vert[5]) ) )
        else:
            sys.exit( "Strange." )

    file_handle.write('\\path [fill] %s;\n\n' % "--".join( nodes ) )

    return
# ==============================================================================
def mpl_color2xcolor( color ):
    """
    Translates a matplotlib color specification into a proper LaTeX
    xcolor.
    """
    if type(color) == types.TupleType:
        if len(color) != 3:
            print "Unknown color \"", color ,"\". Giving up."
            return None
        if color == (0, 0, 0):
            return 'black'
        elif color == (1, 0, 0):
            return 'red'
        elif color == (0, 1, 0):
            return 'green'
        elif color == (0, 0, 1):
            return 'blue'
        else:
            print "Unknown color tuple \"", color ,"\". Giving up."
            return None

    try: # is the color a gray-scale value?
        alpha = float(color)
        if alpha == 0.0:
            return 'black'
        elif alpha == 0.5:
            return 'gray'
        elif alpha == 0.75:
            return 'lightgray'
        elif alpha == 1.0:
            return None
        else:
            return color
    except ValueError:
        pass
    except TypeError:
        print 
        print color.length

    if color == 'r':
        return 'red'
    elif color == 'g' or color == 'green':
        return 'green'
    elif color == 'b':
        return 'blue'
    elif color == 'k':
        return None
    else:
        print '%Unknown color \"' + color + '\".'
        return None # default
# ==============================================================================
def handle_children( file_handle, obj ):

    for child in obj.get_children():
        if ( isinstance( child, mpl.axes.Axes ) ):
            draw_axes( file_handle, child )
        elif ( isinstance( child, mpl.lines.Line2D ) ):
            draw_line2d( file_handle, child )
        elif ( isinstance( child, mpl.image.AxesImage ) ):
            draw_image( file_handle, child )
        elif ( isinstance( child, mpl.patches.Polygon ) ):
            draw_polygon( file_handle, child )
        elif ( isinstance( child, mpl.collections.PolyCollection ) ):
            draw_polycollection( file_handle, child )
        elif ( isinstance( child, mpl.collections.PatchCollection ) ):
            draw_patchcollection( file_handle, child )
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

    return
# ==============================================================================
def print_pgfplot_libs_message():
    """
    Prints message to screen indicating the use of Pgfplots and its libraries.
    """
    clean_pgfplots_libs = list( set(PGFPLOTS_LIBS) )
    libs = ",".join( clean_pgfplots_libs )
    
    print "========================================================="
    print "Please add the following line to your LaTeX preamble:\n"
    print "\usepackage{pgfplots}"
    if clean_pgfplots_libs:
        print "\usepgfplotslibrary{" + libs + "}"
    print "========================================================="

    return
# ==============================================================================
