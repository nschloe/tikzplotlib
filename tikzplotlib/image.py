import matplotlib as mpl
import numpy
import PIL

from . import files


def draw_image(data, obj):
    """Returns the PGFPlots code for an image environment.
    """
    content = []

    filename, rel_filepath = files.new_filename(data, "img", ".png")

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
            origin=obj.origin,
        )
    else:
        # RGB (+alpha) information at each point
        assert len(dims) == 3 and dims[2] in [3, 4]
        # convert to PIL image
        if obj.origin == "lower":
            img_array = numpy.flipud(img_array)

        # Convert mpl image to PIL
        image = PIL.Image.fromarray(numpy.uint8(img_array * 255))

        # If the input image is PIL:
        # image = PIL.Image.fromarray(img_array)

        image.save(filename, origin=obj.origin)

    # write the corresponding information to the TikZ file
    extent = obj.get_extent()

    # the format specification will only accept tuples
    if not isinstance(extent, tuple):
        extent = tuple(extent)

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
