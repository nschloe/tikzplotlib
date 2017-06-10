# -*- coding: utf-8 -*-
#
import os

import matplotlib as mpl
import numpy
import PIL


def draw_image(data, obj):
    '''Returns the PGFPlots code for an image environment.
    '''
    content = []

    if 'img number' not in data.keys():
        data['img number'] = 0

    # Make sure not to overwrite anything.
    file_exists = True
    while file_exists:
        data['img number'] = data['img number'] + 1
        filename = os.path.join(
            data['output dir'],
            data['base name'] + str(data['img number']) + '.png'
        )
        file_exists = os.path.isfile(filename)

    # store the image as in a file
    img_array = obj.get_array()

    dims = img_array.shape
    if len(dims) == 2:  # the values are given as one real number: look at cmap
        clims = obj.get_clim()
        mpl.pyplot.imsave(
                fname=filename,
                arr=img_array,
                cmap=obj.get_cmap(),
                vmin=clims[0],
                vmax=clims[1],
                origin=obj.origin
                )
    else:
        # RGB (+alpha) information at each point
        assert len(dims) == 3 and dims[2] in [3, 4]
        # convert to PIL image
        if obj.origin == "lower":
            img_array = numpy.flipud(img_array)
        image = PIL.Image.fromarray(img_array)
        image.save(filename, origin=obj.origin)

    # write the corresponding information to the TikZ file
    extent = obj.get_extent()

    # the format specification will only accept tuples
    if not isinstance(extent, tuple):
        extent = tuple(extent)

    rel_filepath = os.path.basename(filename)
    if data['rel data path']:
        rel_filepath = os.path.join(data['rel data path'], rel_filepath)

    # Explicitly use \pgfimage as includegrapics command, as the default
    # \includegraphics fails unexpectedly in some cases
    content.append(
            '\\addplot graphics [includegraphics cmd=\\pgfimage,'
            'xmin=%.15g, xmax=%.15g, '
            'ymin=%.15g, ymax=%.15g] {%s};\n'
            % (extent + (rel_filepath,))
            )

    return data, content
