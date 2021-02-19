from PIL import Image

from ._image import prepare_image_addplot, prepare_image_storage


def draw_quadmesh(data, obj):
    """Returns the PGFPlots code for an graphics environment holding a
    rendering of the object.
    """
    content = []

    filepath_or_handle, rel_filepath_or_handle = prepare_image_storage(data)

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
    cropped.save(filepath_or_handle, format="PNG")

    # Restore the original dpi of the figure
    obj.figure.set_dpi(fig_dpi)

    # write the corresponding information to the TikZ file
    extent = obj.axes.get_xlim() + obj.axes.get_ylim()

    content.append(prepare_image_addplot(data, rel_filepath_or_handle, extent))

    return data, content
