# -*- coding: utf-8 -*-
#
from . import axes
from . import legend
from . import line2d
from . import image as img
from . import path
from . import patch
from . import text as mytext

import os
import matplotlib as mpl
from matplotlib2tikz import __version__


def save(filepath,
         figure='gcf',
         encoding=None,
         figurewidth=None,
         figureheight=None,
         textsize=10.0,
         tex_relative_path_to_data=None,
         strict=False,
         draw_rectangles=False,
         wrap=True,
         extra=None,
         show_info=True
         ):
    '''Main function. Here, the recursion into the image starts and the
    contents are picked up. The actual file gets written in this routine.

    :param figure: either a Figure object or 'gcf' (default).

    :param filepath: The file to which the TikZ output will be written.
    :type filepath: str

    :param encoding: Which encoding to use for the file.

    :param figurewidth: If not ``None``, this will be used as figure width
                        within the TikZ/PGFPlots output. If ``figureheight``
                        is not given, ``matplotlib2tikz`` will try to preserve
                        the original width/height ratio.
                        Note that ``figurewidth`` can be a string literal,
                        such as ``'\\figurewidth'``.
    :type figurewidth: str

    :param figureheight: If not ``None``, this will be used as figure height
                         within the TikZ/PGFPlots output. If ``figurewidth`` is
                         not given, ``matplotlib2tikz`` will try to preserve
                         the original width/height ratio.  Note that
                         ``figurewidth`` can be a string literal, such as
                         ``'\\figureheight'``.
    :type figureheight: str

    :param textsize: The text size (in pt) that the target latex document is
                     using.  Default is 10.0.
    :type textsize: float

    :param tex_relative_path_to_data: In some cases, the TikZ file will have to
                                      refer to another file, e.g., a PNG for
                                      image plots. When ``\\input`` into a
                                      regular LaTeX document, the additional
                                      file is looked for in a folder relative
                                      to the LaTeX file, not the TikZ file.
                                      This arguments optionally sets the
                                      relative path from the LaTeX file to the
                                      data.
    :type tex_relative_path_to_data: str

    :param strict: Whether or not to strictly stick to matplotlib's appearance.
                   This influences, for example, whether tick marks are set
                   exactly as in the matplotlib plot, or if TikZ/PGFPlots
                   can decide where to put the ticks.
    :type strict: bool

    :param draw_rectangles: Whether or not to draw Rectangle objects.
                            You normally don't want that as legend, axes, and
                            other entities which are natively taken care of by
                            PGFPlots are represented as rectangles in
                            matplotlib. Some plot types (such as bar plots)
                            cannot otherwise be represented though.
                            Don't expect working or clean output when using
                            this option.
    :type draw_rectangles: bool

    :param wrap: Whether ``'\\begin{tikzpicture}'`` and
                 ``'\\end{tikzpicture}'`` will be written. One might need to
                 provide custom arguments to the environment (eg. scale= etc.).
                 Default is ``True``.
    :type wrap: bool

    :param extra: Extra axis options to be passed (as a set) to pgfplots.
                  Default is ``None``.
    :type extra: a set of strings for the pfgplots axes.

    :returns: None


    The following optional attributes of matplotlib's objects are recognized
    and handled:

     - axes.Axes._matplotlib2tikz_anchors
       This attribute can be set to a list of ((x,y), anchor_name) tuples.
       Invisible nodes at the respective location will be created which  can be
       referenced from outside the axis environment.
    '''
    # not as default value because gcf() would be evaluated at import time
    if figure == 'gcf':
        figure = mpl.pyplot.gcf()
    data = {}
    data['fwidth'] = figurewidth
    data['fheight'] = figureheight
    data['rel data path'] = tex_relative_path_to_data
    data['output dir'] = os.path.dirname(filepath)
    data['strict'] = strict
    data['draw rectangles'] = draw_rectangles
    data['tikz libs'] = set()
    data['pgfplots libs'] = set()
    data['font size'] = textsize
    data['custom colors'] = {}
    if extra:
        data['extra axis options'] = extra.copy()
    else:
        data['extra axis options'] = set()

    # open file
    import codecs
    file_handle = codecs.open(filepath, 'w', encoding)

    if show_info:
        print('file encoding: {0}'.format(file_handle.encoding))

    # gather the file content
    data, content = _recurse(data, figure)

    disclaimer = 'This file was created by matplotlib2tikz v%s.' % __version__

    if show_info:
        disclaimer += \
            '\nThe lastest updates can be retrieved from\n\n' \
            + 'https://github.com/nschloe/matplotlib2tikz\n\n' \
            + 'where you can also submit bug reports and leave' \
            + 'comments.\n'

    # write disclaimer to the file header
    file_handle.write(_tex_comment(disclaimer))

    # write the contents
    if wrap:
        file_handle.write('\\begin{tikzpicture}\n\n')

    coldefs = _get_color_definitions(data)
    if coldefs:
        file_handle.write('\n'.join(coldefs))
        file_handle.write('\n\n')

    try:
        file_handle.write(''.join(content))
    except UnicodeEncodeError:
        # We're probably using Python 2, so use proper unicode treatment
        file_handle.write(unicode(''.join(content)).encode('utf-8'))

    if wrap:
        file_handle.write('\\end{tikzpicture}')

    # close file
    file_handle.close()

    # print message about necessary pgfplot libs to command line
    if show_info:
        _print_pgfplot_libs_message(data)
    return


def _tex_comment(comment):
    '''Prepends each line in string with the LaTeX comment key, '%'.
    '''
    return '% ' + str.replace(comment, '\n', '\n% ') + '\n'


def _get_color_definitions(data):
    '''Returns the list of custom color definitions for the TikZ file.
    '''
    definitions = []
    for name, rgb in data['custom colors'].items():
        definitions.append('\\definecolor{%s}{rgb}{%.15g,%.15g,%.15g}'
                           % (name, rgb[0], rgb[1], rgb[2])
                           )
    return definitions


def _print_pgfplot_libs_message(data):
    '''Prints message to screen indicating the use of PGFPlots and its
    libraries.'''
    pgfplotslibs = ','.join(list(data['pgfplots libs']))
    tikzlibs = ','.join(list(data['tikz libs']))

    print('=========================================================')
    print('Please add the following lines to your LaTeX preamble:\n')
    print('\\usepackage[utf8]{inputenc}')
    print('\\usepackage{fontspec}')
    print('\\usepackage{pgfplots}')
    if tikzlibs:
        print('\\usetikzlibrary{' + tikzlibs + '}')
    if pgfplotslibs:
        print('\\usepgfplotslibrary{' + pgfplotslibs + '}')
    print('=========================================================')
    return


def _recurse(data, obj):
    '''Iterates over all children of the current object, gathers the contents
    contributing to the resulting PGFPlots file, and returns those.
    '''
    content = []
    for child in obj.get_children():
        if isinstance(child, mpl.axes.Axes):
            ax = axes.Axes(data, child)
            if not ax.is_colorbar:
                # Run through the children objects, gather the content.
                data, children_content = _recurse(data, child)
                # add extra axis options from children
                if data['extra axis options']:
                    ax.axis_options.extend(data['extra axis options'])
                # populate content
                content.extend(ax.get_begin_code())
                content.extend(children_content)
                content.extend(ax.get_end_code())
        elif isinstance(child, mpl.lines.Line2D):
            data, cont = line2d.draw_line2d(data, child)
            content.extend(cont)
        elif isinstance(child, mpl.image.AxesImage):
            data, cont = img.draw_image(data, child)
            content.extend(cont)
            # # Really necessary?
            # data, children_content = _recurse(data, child)
            # content.extend(children_content)
        elif isinstance(child, mpl.patches.Patch):
            data, cont = patch.draw_patch(data, child)
            content.extend(cont)
        elif isinstance(child, mpl.collections.PatchCollection):
            data, cont = patch.draw_patchcollection(data, child)
            content.extend(cont)
        elif isinstance(child, mpl.collections.PathCollection):
            data, cont = path.draw_pathcollection(data, child)
            content.extend(cont)
        elif isinstance(child, mpl.legend.Legend):
            data = legend.draw_legend(data, child)
        elif isinstance(child, mpl.axis.XAxis) or \
                isinstance(child, mpl.axis.YAxis) or \
                isinstance(child, mpl.spines.Spine) or \
                isinstance(child, mpl.text.Text) or \
                isinstance(child, mpl.collections.QuadMesh):
            pass
        else:
            print('matplotlib2tikz: Don''t know how to handle object ''%s''.' %
                  type(child))
    # XXX: This is ugly
    if isinstance(obj, mpl.axes.Subplot) or isinstance(obj, mpl.figure.Figure):
        for text in obj.texts:
            data, cont = mytext.draw_text(data, text)
            content.extend(cont)
    return data, content
