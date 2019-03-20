# -*- coding: utf-8 -*-
#


def has_legend(axes):
    return axes.get_legend() is not None


def get_legend_text(obj):
    """Check if line is in legend.
    """
    leg = obj.axes.get_legend()
    if leg is None:
        return None

    keys = [l.get_label() for l in leg.legendHandles if l is not None]
    values = [l.get_text() for l in leg.texts]

    label = obj.get_label()
    d = dict(zip(keys, values))
    if label in d:
        return d[label]

    return None
