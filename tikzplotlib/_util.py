import matplotlib.transforms
import numpy


def has_legend(axes):
    return axes.get_legend() is not None


def get_legend_text(obj):
    """Check if line is in legend.
    """
    leg = obj.axes.get_legend()
    if leg is None:
        return None

    keys = [h.get_label() for h in leg.legendHandles if h is not None]
    values = [t.get_text() for t in leg.texts]

    label = obj.get_label()
    d = dict(zip(keys, values))
    if label in d:
        return d[label]

    return None


def transform_to_data_coordinates(obj, xdata, ydata):
    """The coordinates might not be in data coordinates, but could be sometimes in axes
    coordinates. For example, the matplotlib command
      axes.axvline(2)
    will have the y coordinates set to 0 and 1, not to the limits. Therefore, a
    two-stage transform has to be applied:
      1. first transforming to display coordinates, then
      2. from display to data.
    """
    if obj.axes is not None and obj.get_transform() != obj.axes.transData:
        points = numpy.array([xdata, ydata]).T
        transform = matplotlib.transforms.composite_transform_factory(
            obj.get_transform(), obj.axes.transData.inverted()
        )
        return transform.transform(points).T
    return xdata, ydata
