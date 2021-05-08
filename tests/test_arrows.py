import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


# https://matplotlib.org/examples/pylab_examples/fancyarrow_demo.html
def plot():
    styles = mpatches.ArrowStyle.get_styles()

    ncol = 2
    nrow = (len(styles) + 1) // ncol
    figheight = nrow + 0.5
    fig1 = plt.figure(1, (4.0 * ncol / 1.5, figheight / 1.5))
    fontsize = 0.2 * 70

    ax = fig1.add_axes([0, 0, 1, 1], frameon=False, aspect=1.0)

    ax.set_xlim(0, 4 * ncol)
    ax.set_ylim(0, figheight)

    def to_texstring(s):
        s = s.replace("<", r"$<$")
        s = s.replace(">", r"$>$")
        s = s.replace("|", r"$|$")
        return s

    for i, (stylename, styleclass) in enumerate(sorted(styles.items())):
        x = 3.2 + (i // nrow) * 4
        y = figheight - 0.7 - i % nrow  # /figheight
        p = mpatches.Circle((x, y), 0.2)
        ax.add_patch(p)

        ax.annotate(
            to_texstring(stylename),
            (x, y),
            (x - 1.2, y),
            # xycoords="figure fraction", textcoords="figure fraction",
            ha="right",
            va="center",
            size=fontsize,
            arrowprops=dict(
                arrowstyle=stylename,
                patchB=p,
                shrinkA=5,
                shrinkB=5,
                fc="k",
                ec="k",
                connectionstyle="arc3,rad=-0.05",
            ),
            bbox=dict(boxstyle="square", fc="w"),
        )

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    return plt.gcf()


# if __name__ == "__main__":
#     import helpers
#
#     # fig = plot()
#     # helpers.print_tree(fig)
#     # plt.show()
#
#     plot()
#     import tikzplotlib
#     code = tikzplotlib.get_tikz_code(include_disclaimer=False, standalone=True)
#     plt.close()
#     helpers._does_compile(code)

if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_tex(plot)
    # helpers.print_tree(plot())
