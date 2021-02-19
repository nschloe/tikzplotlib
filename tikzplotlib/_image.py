from base64 import encodebytes
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import PIL

from . import _files


def prepare_image_storage(data):
    """Prepares a storage location for an image."""
    if data["embed_images"]:
        handle = BytesIO()
        return handle, handle
    else:
        filepath, rel_filepath = _files.new_filepath(data, "img", ".png")
        return filepath, rel_filepath


def prepare_image_addplot(data, rel_filepath_or_handle, extent):
    """Returns an \\addplot command for an image, previously prepared with `prepare_image_storage`."""
    if not isinstance(rel_filepath_or_handle, BytesIO):
        # Explicitly use \pgfimage as includegrapics command, as the default
        # \includegraphics fails unexpectedly in some cases
        image_embedding_command = "\\pgfimage"
        image_embedding_parameter = rel_filepath_or_handle
    else:
        image_embedding_command = "\\pgfimageembedded"
        image_embedding_parameter = (
            "\n" + encodebytes(rel_filepath_or_handle.getbuffer()).decode()
        )

    # the format specification will only accept tuples
    if not isinstance(extent, tuple):
        extent = tuple(extent)

    ff = data["float format"]
    return (
        f"\\addplot graphics [includegraphics cmd={image_embedding_command},"
        f"xmin={extent[0]:{ff}}, xmax={extent[1]:{ff}}, "
        f"ymin={extent[2]:{ff}}, ymax={extent[3]:{ff}}] {{{image_embedding_parameter}}};\n"
    )


def draw_image(data, obj):
    """Returns the PGFPlots code for an image environment."""
    content = []

    filepath_or_handle, rel_filepath_or_handle = prepare_image_storage(data)

    # store the image as in a file
    img_array = obj.get_array()

    dims = img_array.shape
    if len(dims) == 2:  # the values are given as one real number: look at cmap
        clims = obj.get_clim()
        plt.imsave(
            fname=filepath_or_handle,
            arr=img_array,
            cmap=obj.get_cmap(),
            vmin=clims[0],
            vmax=clims[1],
            origin=obj.origin,
        )
    else:
        # RGB (+alpha) information at each point
        assert len(dims) == 3 and dims[2] in [3, 4]
        # convert to PIL image
        if obj.origin == "lower":
            img_array = np.flipud(img_array)

        # Convert mpl image to PIL
        if img_array.dtype != np.uint8:
            img_array = np.uint8(img_array * 255)
        image = PIL.Image.fromarray(img_array)

        # If the input image is PIL:
        # image = PIL.Image.fromarray(img_array)

        image.save(filepath_or_handle, origin=obj.origin, format="PNG")

    # write the corresponding information to the TikZ file
    extent = obj.get_extent()

    content.append(prepare_image_addplot(data, rel_filepath_or_handle, extent))

    return data, content
