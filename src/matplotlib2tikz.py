#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pylab import *

# =============================================================================
# Recursively prints the tree structure of the matplotlib object
def print_tree( obj, indent = "" ):
    print indent, type(obj)
    for child in obj.get_children():
        print_tree( child, indent + "   " )
    return
# =============================================================================
def matplotlib2tikz( filepath, figurewidth=None, figureheight=None, tex_relative_path_to_data=None ):
    from os import path
    
    global fwidth
    fwidth = figurewidth
    global fheight
    fheight = figureheight
    global rel_data_path
    rel_data_path = tex_relative_path_to_data
    
    global pgfplots_libs
    pgfplots_libs = []
    
    global output_dir
    output_dir = path.dirname(filepath)

    # open file
    file_handle = open( filepath, "w" )

    # write the contents
    file_handle.write( "\\begin{tikzpicture}\n\n" )
    handle_children( file_handle, gcf() )
    file_handle.write( "\\end{tikzpicture}" )

    # close file
    file_handle.close()
    
    # print message about necessary pgfplot libs to command line
    print_pgfplot_libs_message()
    return
# =============================================================================
def draw_axes( file_handle, obj ):
    # Are we dealing with an axis that hosts a colorbar?
    # Skip then.
    # TODO instead of testing here, rather blacklist the colorbar axis
    #      plots as soon as they have been found, e.g., by find_associated_colorbar()
    if extract_colorbar(obj)!=None:
        return

    # instantiation
    nsubplots = 0
    subplot_index = 0
    issubplot = False

    if isinstance( obj, matplotlib.axes.Subplot ):
        issubplot = True
        geom = obj.get_geometry()
        nsubplots = geom[0]*geom[1]
        subplot_index = geom[2]
        if subplot_index==1:
            file_handle.write( "\\begin{groupplot}[group style={group size=%.d by %.d}]\n" % (geom[1],geom[0]) )
            pgfplots_libs.append( "groupplots" )

    axis_options = []

    if fwidth or fheight:
        axis_options.append( "scale only axis" )
    if fwidth:
        axis_options.append( "width="+fwidth )
    if fheight:
        axis_options.append( "height="+fheight )

    # get axes title
    title = obj.get_title()
    if len(title) != 0 :
        axis_options.append( "title={" + title + "}" )

    # get axes titles
    xlabel = obj.get_xlabel()
    if len(xlabel) != 0 :
        axis_options.append( "xlabel={" + xlabel + "}" )
    ylabel = obj.get_ylabel()
    if len(ylabel) != 0 :
        axis_options.append( "ylabel={" + ylabel + "}" )
        
    # get x ticks
    xticks = obj.get_xticks()
    xticklabels = obj.get_xticklabels()    
    pgfplots_xtick = []
    pgfplots_xticklabel = []
    for i in range(0, len(xticks)):
        pgfplots_xtick.append( xticks[i] )
        if len( xticklabels[i].get_text() ) != 0:
            pgfplots_xticklabel.append( xticklabels[i] )
            
    if len(pgfplots_xtick)==0:
        axis_options.append( "xtick=\\empty" )
    else:
        axis_options.append( "xtick={" +  ",".join(["%s" % el for el in pgfplots_xtick]) + "}" )
        
    if len(pgfplots_xticklabel)!=0:
        axis_options.append( "xticklabel={" + ",".join(pgfplots_xticklabel) + "}" )
        
        
    # get y ticks
    yticks = obj.get_yticks()
    yticklabels = obj.get_yticklabels()    
    pgfplots_ytick = []
    pgfplots_yticklabel = []
    for i in range(0, len(yticks)):
        pgfplots_ytick.append( yticks[i] )
        if len( yticklabels[i].get_text() ) != 0:
            pgfplots_yticklabel.append( yticklabels[i] )
            
    if len(pgfplots_ytick)==0:
        axis_options.append( "ytick=\\empty" )
    else:
        axis_options.append( "ytick={" +  ",".join(["%s" % el for el in pgfplots_ytick]) + "}" )
        
    if len(pgfplots_yticklabel)!=0:
        axis_options.append( "yticklabel={" + ",".join(pgfplots_yticklabel) + "}" )


    # axes limits
    xlim = obj.get_xlim()
    axis_options.append(     "xmin=" + repr(xlim[0])
                         + ", xmax=" + repr(xlim[1]) )
    ylim = obj.get_ylim()
    axis_options.append(     "ymin=" + repr(ylim[0])
                         + ", ymax=" + repr(ylim[1]) )

    # find color bar
    colorbar = find_associated_colorbar( obj )
    if colorbar!=None:
        clim = colorbar.get_clim()
        axis_options.append( "colorbar=true" )
        mycolormap = matplotlibColormap2pgfplotsColormap( colorbar.get_cmap() )
        axis_options.append( "colormap/" + mycolormap )
        axis_options.append( 'point meta min=' + repr(clim[0]) )
        axis_options.append( 'point meta max=' + repr(clim[1]) )

    # actually print the thing
    if issubplot:
        file_handle.write( "\\nextgroupplot" )
    else:
        file_handle.write( "\\begin{axis}" )

    if len(axis_options)!=0:
        options = ",\n".join( axis_options )
        file_handle.write( "[\n" + options + "\n]\n" )

    # TODO Use get_lines()?
    handle_children( file_handle, obj )

    if not issubplot:
        file_handle.write( "\\end{axis}\n\n" )
    elif issubplot and nsubplots==subplot_index:
        file_handle.write( "\\end{groupplot}\n\n" )

    return
# =============================================================================
# Converts a color map as given in matplotlib to a color map as represented
# in Pgfplots.
def matplotlibColormap2pgfplotsColormap( cmap ):
    if isinstance( cmap, matplotlib.colors.LinearSegmentedColormap ):
        if cmap.is_gray():
            return 'blackwhite'
        else:
            segdata = cmap._segmentdata
            red    = segdata['red']
            green  = segdata['green']
            blue   = segdata['blue']
            print red
            print green
            print blue
            # loop over the data, stop at each spot where the linear
            # interpolations is interrupted, and set a color mark there
            # set initial color
            k_red   = 0
            k_green = 0
            k_blue  = 0
            x = 0.0
            color_changes = []
            while True:
                # find next x
                x = min( red[k_red][0], green[k_green][0], blue[k_blue][0] )
    
                if ( red[k_red][0]==x ):
                    red_part = red[k_red][1]
                    k_red    = k_red+1
                else:
                    red_part = linear_interpolation( x, (red[k_red-1][0],red[k_red][0]), (red[k_red-1][2],red[k_red][1]) )
    
                if ( green[k_green][0]==x ):
                    green_part = green[k_green][1]
                    k_green    = k_green+1
                else:
                    green_part = linear_interpolation( x, (green[k_green-1][0],green[k_green][0]), (green[k_green-1][2],green[k_green][1]) )
                    #print green_part
    
                if ( blue[k_blue][0]==x ):
                    blue_part = blue[k_blue][1]
                    k_blue    = k_blue+1
                else:
                    blue_part = linear_interpolation( x, (blue[k_blue-1][0],blue[k_blue][0]), (blue[k_blue-1][2],blue[k_blue][1]) )
    
                #print k
                color_changes.append( "rgb(%.3fcm)=(%.3f,%.3f,%.3f)" % ( x, red_part,green_part,blue_part ) )
    
                if x>=1.0: break
    
            return "{mymap}{" + "; ".join( color_changes ) + "}"
    else :
        print "Don't know how to handle color map. Using 'blackwhite'."
        return 'blackwhite'
# =============================================================================
def linear_interpolation( x, X, Y ):
    xRet = ( Y[1]*(x-X[0]) + Y[0]*(X[1]-x) ) / ( X[1]-X[0] )
    return xRet
# =============================================================================
def draw_line2d( file_handle, obj ):
    addplot_options = []

    marker = obj.get_marker()
    if marker!="None":
        print "%TODO Implement markers."

    # get line color
    color = obj.get_color()
    xcolor = mpl_color2xcolor(color)
    if xcolor:
        addplot_options.append( xcolor )

    linestyle = mpl_linestyle2pgfp_linestyle( obj.get_linestyle() )
    if linestyle:
        addplot_options.append( linestyle )

    # process options
    file_handle.write( "\\addplot " )
    if addplot_options:
        options = ", ".join( addplot_options )
        file_handle.write( "[" + options + "]\n" )

    # print the hard numerical data
    xdata, ydata = obj.get_data()
    file_handle.write(  "coordinates {\n" )
    for k in range(len(xdata)):
        file_handle.write( "(%.15g,%.15g) " % (xdata[k], ydata[k]) )
    file_handle.write( "\n};\n" )

    return
# =============================================================================
# Translates a line style of matplotlib to the corresponding style
# in Pgfplots.
def mpl_linestyle2pgfp_linestyle( ls ):
    if (ls=='-' or ls=='None'):
        return None
    elif ls==':':
        return 'dotted'
    else:
        print '%Unknown line style \"' + ls + '\".'
        return None
# =============================================================================
def draw_image( file_handle, obj ):
    from os import path
    
    global img_number
    try:
       img_number = img_number+1
    except NameError, e:
       img_number = 0

    filename = path.join( output_dir, 
                          "img" + repr(img_number) + ".png" )

    # store the image as in a file
    img_array = obj.get_array()
    dims = img_array.shape
    if len(dims)==2: # the values are given as one real number: look at cmap
        clims = obj.get_clim()
        imsave( fname = filename,
                arr   = img_array ,
                cmap  = obj.get_cmap(),
                vmin  = clims[0],
                vmax  = clims[1] )
    elif len(dims)==3: # RGB information
        if dims[2]==4: # RGB+alpha information at each point
            import Image
            # convert to PIL image (after upside-down flip)
            im = Image.fromarray( flipud(img_array), 'RGBA' )
            im.save( filename )

    # write the corresponding information to the TikZ file
    extent = obj.get_extent()
    rel_filepath = path.join( rel_data_path,  path.basename(filename) )
    file_handle.write( ("\\addplot graphics [xmin=%.15g, xmax=%.15g, ymin=%.15g, ymax=%.15g] {" + rel_filepath + "};\n")
                        % extent )

    handle_children( file_handle, obj )

    return
# =============================================================================
def draw_polygon( file_handle, obj ):
    # TODO do nothing for polygons?!
    handle_children( file_handle, obj )
    return
# =============================================================================
# Rather poor way of telling whether an axis has a colorbar associated:
# Check the next axis environment, and see if it is de facto a color bar;
# if yes, return the color bar object.
def find_associated_colorbar( obj ):
      for child in obj.get_children():
              try:
                      cbar = child.colorbar
              except AttributeError:
                      continue
              if not cbar == None: # really necessary?
                      # if fetch was successful, cbar contains
                      # ( reference to colorbar, reference to axis containing colorbar )
                      return cbar[0]
      return None
# =============================================================================
# TODO This function contains crude logic.
def is_colorbar( obj ):
    if isinstance( obj, matplotlib.cm.ScalarMappable ):
        arr = obj.get_array()
        dims = arr.shape
        if len(dims)==1:
            return True # o rly?
        else:
            return False
    else:
        return False
# =============================================================================
def extract_colorbar( obj ):
    colorbars = findobj( obj, is_colorbar )
    if len(colorbars)==0:
        return None
    if not equivalent( colorbars ):
        print "More than one color bar found. Use first one."
    return colorbars[0]
# =============================================================================
# checks if the vectors consists of all the same objects
def equivalent( array ):
    if len(array)==0:
        return False
    else:
        for elem in array:
            if elem!=array[0]:
                return False

    return True
# =============================================================================
def draw_polycollection( file_handle, obj ):
    print "matplotlib2tikz: Don't know how to draw a PolyCollection."
    return
# =============================================================================
# Translates a matplotlib color specification into a proper LaTeX
# xcolor.
def mpl_color2xcolor( color ):
    try: # is the color a gray-scale value?
        alpha = float(color)
        if alpha==0.0:
            return 'black'
        elif alpha==0.5:
            return 'gray'
        elif alpha==0.75:
            return 'lightgray'
        elif alpha==1.0:
            return None
        else:
            return color
    except ValueError:
      pass

    if color=='r':
        return 'red'
    elif color=='g':
        return 'green'
    elif color=='b':
        return 'blue'
    elif color=='k':
        return None
    else:
        print '%Unknown color \"' + color + '\".'
        return None # default
# =============================================================================
def handle_children( file_handle, obj ):
    for child in obj.get_children():
        if ( isinstance( child, matplotlib.axes.Axes ) ):
            draw_axes( file_handle, child )
        elif ( isinstance( child, matplotlib.lines.Line2D ) ):
            draw_line2d( file_handle, child )
        elif ( isinstance( child, matplotlib.image.AxesImage ) ):
            draw_image( file_handle, child )
        elif ( isinstance( child, matplotlib.patches.Polygon ) ):
            draw_polygon( file_handle, child )
        elif ( isinstance( child, matplotlib.collections.PolyCollection ) ):
            draw_polycollection( file_handle, child )
        elif (   isinstance( child, matplotlib.axis.XAxis )
              or isinstance( child, matplotlib.axis.YAxis )
              or isinstance( child, matplotlib.spines.Spine )
              or isinstance( child, matplotlib.patches.Rectangle )
              or isinstance( child, matplotlib.text.Text )
             ):
            pass
        else:
            print "matplotlib2tikz: Don't know how to handle object ", type(child), "."
    return
# =============================================================================
def print_pgfplot_libs_message():
    # remove duplicates
    clean_pgfplots_libs = list(set(pgfplots_libs) ) 
    libs = ",".join( clean_pgfplots_libs )
    
    print "========================================================="
    print "Please add the following line to your LaTeX preamble:\n"
    print "\usepackage{pgfplots}"
    if len(clean_pgfplots_libs)!=0:
        print "\usepgfplotslibrary{" + libs + "}"
    print "========================================================="

    return
# =============================================================================
