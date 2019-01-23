def is_in_legend(obj):
    """Check if obj is in legend
    """
    label = obj.get_label()
    try:
        ax = obj.axes
        leg = ax.get_legend()
        return label in [l.get_label() for l in leg.legendHandles]
    except AttributeError:
        return False
