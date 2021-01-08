import matplotlib.pyplot as plt
from helpers import assert_equality
from matplotlib.collections import PolyCollection


def plot():
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1)

    col = PolyCollection(
        [], facecolors="none", edgecolors="red", linestyle="--", linewidth=1.2
    )
    col.set_zorder(1)
    axis.add_collection(col)
    axis.set_xlim(0.5, 2.5)
    axis.set_ylim(0.5, 2.5)
    axis.collections[0].set_verts([[[1, 1], [1, 2], [2, 2], [2, 1]]])
    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_tex(plot)
    # helpers.print_tree(plot())
