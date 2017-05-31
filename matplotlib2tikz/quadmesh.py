# -*- coding: utf-8 -*-
#
import os

from PIL import Image


def draw_quadmesh(data, obj):
    '''Returns the PGFPlots code for an graphics environment holding a
       rendering of the object.
    '''
    content = []

    # Generate file name for current object
    if 'img number' not in data.keys():
        data['img number'] = 0

    filename = os.path.join(
            data['output dir'],
            '%s_img%03d.png' % (data['base name'], data['img number'])
            )
    data['img number'] = data['img number'] + 1

    # Get the dpi for rendering and store the original dpi of the figure
    dpi = data['dpi']
    fig_dpi = obj.figure.get_dpi()
    obj.figure.set_dpi(dpi)

    # Render the object and save as png file
    from matplotlib.backends.backend_agg import RendererAgg
    cbox = obj.get_clip_box()
    width = int(round(cbox.extents[2]))
    height = int(round(cbox.extents[3]))
    ren = RendererAgg(width, height, dpi)
    obj.draw(ren)

    # Generate a image from the render buffer
    image = Image.frombuffer(
            'RGBA',
            ren.get_canvas_width_height(),
            ren.buffer_rgba(),
            'raw', 'RGBA', 0, 1
            )
    # Crop the image to the actual content (removing the the regions otherwise
    # used for axes, etc.)
    # 'image.crop' expects the crop box to specify the left, upper, right, and
    # lower pixel. 'cbox.extents' gives the left, lower, right, and upper
    # pixel.
    box = (
        int(round(cbox.extents[0])),
        0,
        int(round(cbox.extents[2])),
        int(round(cbox.extents[3] - cbox.extents[1]))
        )
    cropped = image.crop(box)
    cropped.save(filename)

    # Restore the original dpi of the figure
    obj.figure.set_dpi(fig_dpi)

    # write the corresponding information to the TikZ file
    extent = obj.axes.get_xlim() + obj.axes.get_ylim()

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
