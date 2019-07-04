from PIL import Image

from . import files


def draw_quadmesh(data, obj):
    """Returns the PGFPlots code for an graphics environment holding a
       rendering of the object.
    """
    content = []

    # Generate file name for current object
    filename, rel_filepath = files.new_filename(data, "img", ".png")

    # Get the dpi for rendering and store the original dpi of the figure
    dpi = data["dpi"]
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
        "RGBA", ren.get_canvas_width_height(), ren.buffer_rgba(), "raw", "RGBA", 0, 1
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
        int(round(cbox.extents[3] - cbox.extents[1])),
    )
    cropped = image.crop(box)
    cropped.save(filename)

    # Restore the original dpi of the figure
    obj.figure.set_dpi(fig_dpi)

    # write the corresponding information to the TikZ file
    extent = obj.axes.get_xlim() + obj.axes.get_ylim()

    # Explicitly use \pgfimage as includegrapics command, as the default
    # \includegraphics fails unexpectedly in some cases
    ff = data["float format"]
    content.append(
        (
            "\\addplot graphics [includegraphics cmd=\\pgfimage,"
            "xmin=" + ff + ", xmax=" + ff + ", "
            "ymin=" + ff + ", ymax=" + ff + "] {{{}}};\n"
        ).format(*(extent + (rel_filepath,)))
    )

    return data, content
