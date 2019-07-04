from helpers import assert_equality


def plot():
    from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle, Wedge
    from matplotlib.collections import PatchCollection
    from matplotlib import pyplot as plt
    import numpy as np
    import matplotlib as mpl

    np.random.seed(123)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    N = 3
    x = np.random.rand(N)
    y = np.random.rand(N)
    radii = 0.1 * np.random.rand(N)
    patches = []
    for x1, y1, r in zip(x, y, radii):
        circle = Circle((x1, y1), r)
        patches.append(circle)

    rect = Rectangle(xy=[0.0, 0.25], width=1.0, height=0.5, angle=-45.0)
    patches.append(rect)

    x = np.random.rand(N)
    y = np.random.rand(N)
    radii = 0.1 * np.random.rand(N)
    theta1 = 360.0 * np.random.rand(N)
    theta2 = 360.0 * np.random.rand(N)
    for x1, y1, r, t1, t2 in zip(x, y, radii, theta1, theta2):
        wedge = Wedge((x1, y1), r, t1, t2)
        patches.append(wedge)

    # Some limiting conditions on Wedge
    patches += [
        Wedge((0.3, 0.7), 0.1, 0, 360),  # Full circle
        Wedge((0.7, 0.8), 0.2, 0, 360, width=0.05),  # Full ring
        Wedge((0.8, 0.3), 0.2, 0, 45),  # Full sector
        Wedge((0.8, 0.3), 0.2, 45, 90, width=0.10),  # Ring sector
    ]

    for _ in range(N):
        polygon = Polygon(np.random.rand(N, 2), True)
        patches.append(polygon)

    colors = 100 * np.random.rand(len(patches))
    p = PatchCollection(patches, cmap=mpl.cm.jet, alpha=0.4)
    p.set_array(np.array(colors))
    ax.add_collection(p)

    ellipse = Ellipse(xy=[1.0, 0.5], width=1.0, height=0.5, angle=45.0, alpha=0.4)
    ax.add_patch(ellipse)

    circle = Circle(xy=[0.0, 1.0], radius=0.5, color="r", alpha=0.4)
    ax.add_patch(circle)

    plt.colorbar(p)

    return fig


def test():
    assert_equality(plot, __file__[:-3] + "_reference.tex")
    return


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_latex(plot)
    # helpers.print_tree(plot())
