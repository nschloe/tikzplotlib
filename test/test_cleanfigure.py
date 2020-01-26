import numpy as np
import pytest
from matplotlib import pyplot as plt

from tikzplotlib import get_tikz_code
from tikzplotlib import _cleanfigure as cleanfigure

RC_PARAMS = {"figure.figsize": [5, 5], "figure.dpi": 220, "pgf.rcfonts": False}


def test_clean_figure():
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(x, y)
        ax.set_ylim([20, 80])
        ax.set_xlim([20, 80])
        cleanfigure.clean_figure(fig)
    plt.close("all")


def test_pruneOutsideBox():
    """test against matlab2tikz implementation

    octave code to generate baseline results.
    Note that octave has indexing 1...N, whereas python has indexing 0...N-1.
    ```octave
        x = linspace(1, 100, 20);
        y1 = linspace(1, 100, 20);

        figure
        plot(x, y1)
        xlim([20, 80])
        ylim([20, 80])
        cleanfigure;
    ```
    """
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(x, y)
        ax.set_ylim([20, 80])
        ax.set_xlim([20, 80])
        axhandle = ax
        linehandle = l
        fighandle = fig
        xData, yData = cleanfigure._get_visual_data(axhandle, linehandle)
        visual_data = cleanfigure._stack_data_2D(xData, yData)
        data = cleanfigure._get_data(linehandle)
        xLim, yLim = cleanfigure._get_visual_limits(fighandle, axhandle)
        is3D = cleanfigure._lineIs3D(linehandle)
        hasLines = cleanfigure._line_has_lines(linehandle)

        data = cleanfigure._prune_outside_box(
            xLim, yLim, data, visual_data, is3D, hasLines
        )
        assert data.shape == (14, 2)



def test_replaceDataWithNaN():
    """test against matlab2tikz implementation.

    octave code to generate baseline results.
    Note that octave has indexing 1...N, whereas python has indexing 0...N-1.
    ```octave
        x = linspace(1, 100, 20);
        y1 = linspace(1, 100, 20);

        figure
        plot(x, y1)
        xlim([20, 80])
        ylim([20, 80])
        cleanfigure;
    ```
    """
    id_replace = np.array([0, 16])
    xData = np.linspace(1, 100, 20)
    yData = xData.copy()
    data = np.stack([xData, yData], axis=1)

    newdata = cleanfigure._replace_data_with_NaN(data, id_replace, False)
        assert newdata.shape == data.shape
        assert np.any(np.isnan(newdata))


def test_removeData():
    """test against matlab2tikz implementation.

    octave code to generate baseline results.
    Note that octave has indexing 1...N, whereas python has indexing 0...N-1.
    ```octave
        x = linspace(1, 100, 20);
        y1 = linspace(1, 100, 20);

        figure
        plot(x, y1)
        xlim([20, 80])
        ylim([20, 80])
        cleanfigure;
    ```
    """
    id_remove = np.array([1, 2, 3, 17, 18, 19])
    xData = np.linspace(1, 100, 20)
    yData = xData.copy()
    data = np.stack([xData, yData], axis=1)

    newdata = cleanfigure._remove_data(data, id_remove, False)
    assert newdata.shape == (14, 2)


def test_removeNaNs():
    """test against matlab2tikz implementation

    octave code to generate baseline results. Note that octave has indexing 1...N, whereas python has indexing 0...N-1.
    ```octave
        x = linspace(1, 100, 20);
        y1 = linspace(1, 100, 20);

        figure
        plot(x, y1)
        xlim([20, 80])
        ylim([20, 80])
        cleanfigure;
    ```
    """
    id_replace = np.array([0, 16])
    id_remove = np.array([1, 2, 3, 17, 18, 19])
    xData = np.linspace(1, 100, 20)
    yData = xData.copy()

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(xData, yData)
        cleanfigure._replace_data_with_NaN(l, id_replace)
        cleanfigure._remove_data(l, id_remove)
        cleanfigure._remove_NaNs(l)
        newdata = np.stack(l.get_data(), axis=1)
        assert not np.any(np.isnan(newdata))
        assert newdata.shape == (12, 2)
    plt.close("all")


def test_isInBox():
    """octave code to generate baseline results

        ```octave
            x = 1:10;
            y = 1:10;
            data = [x', y'];
            xlim = [3, 7];
            ylim = [3, 7];
            mask = isInBox(data, xlim, ylim)
        ```
    """
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)
    data = np.stack([x, y], axis=1)
    xLim = np.array([20, 80])
    yLim = np.array([20, 80])
    tol = 1.0e-10
    relaxedXLim = xLim + np.array([-tol, tol])
    relaxedYLim = yLim + np.array([-tol, tol])
    mask = cleanfigure._isInBox(data, relaxedXLim, relaxedYLim)
    assert int(np.sum(mask)) == 12


def test_getVisualLimits():
    """octave code
        ```octave
            addpath ("../matlab2tikz/src")

            x = linspace(1, 100, 20);
            y1 = linspace(1, 100, 20);

            figure
            plot(x, y1)
            xlim([20, 80])
            ylim([20, 80])
            set(gcf,'Units','Inches');
            set(gcf,'Position',[2.5 2.5 5 5])
            cleanfigure;
        ```
    """
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(x, y)
        ax.set_xlim([20, 80])
        ax.set_ylim([20, 80])
        xLim, yLim = cleanfigure._get_visual_limits(fig, ax)
        assert np.allclose(xLim, np.array([20, 80]))
        assert np.allclose(yLim, np.array([20, 80]))
    plt.close("all")


def test_movePointsCloser():
    """octave code
        ```octave
            addpath ("../matlab2tikz/src")

            x = linspace(1, 100, 20);
            y1 = linspace(1, 100, 20);

            figure
            plot(x, y1)
            xlim([20, 80])
            ylim([20, 80])
            set(gcf,'Units','Inches');
            set(gcf,'Position',[2.5 2.5 5 5])
            cleanfigure;
        ```
    """
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(x, y)
        ax.set_ylim([20, 80])
        ax.set_xlim([20, 80])
        cleanfigure._prune_outside_box(fig, ax, l)
        cleanfigure._move_points_closer(fig, ax, l)
        assert l.get_xdata().shape == (14,)
    plt.close("all")


def test_simplifyLine():
    """octave code
        ```octave
            addpath ("../matlab2tikz/src")

            x = linspace(1, 100, 20);
            y1 = linspace(1, 100, 20);

            figure
            plot(x, y1)
            xlim([20, 80])
            ylim([20, 80])
            set(gcf,'Units','Inches');
            set(gcf,'Position',[2.5 2.5 5 5])
            cleanfigure;
        ```
    """
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(x, y)
        ax.set_ylim([20, 80])
        ax.set_xlim([20, 80])
        cleanfigure._prune_outside_box(fig, ax, l)
        cleanfigure._move_points_closer(fig, ax, l)
        cleanfigure._simplify_line(fig, ax, l, 600)
        assert l.get_xdata().shape == (2,)
        assert l.get_ydata().shape == (2,)
    plt.close("all")


def test_limitPrecision():
    """octave code
        ```octave
            addpath ("../matlab2tikz/src")

            x = linspace(1, 100, 20);
            y1 = linspace(1, 100, 20);

            figure
            plot(x, y1)
            xlim([20, 80])
            ylim([20, 80])
            set(gcf,'Units','Inches');
            set(gcf,'Position',[2.5 2.5 5 5])
            cleanfigure;
        ```
    """
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(x, y)
        ax.set_ylim([20, 80])
        ax.set_xlim([20, 80])
        cleanfigure._prune_outside_box(fig, ax, l)
        cleanfigure._move_points_closer(fig, ax, l)
        cleanfigure._simplify_line(fig, ax, l, 600)
        cleanfigure._limit_precision(fig, ax, l, 1)
        assert l.get_xdata().shape == (2,)
        assert l.get_ydata().shape == (2,)
    plt.close("all")


def test_opheimSimplify():
    """test path simplification

        octave code
        ```octave
            addpath ("../matlab2tikz/src")

            x = linspace(1, 100, 20);
            y1 = linspace(1, 100, 20);

            figure
            plot(x, y1)
            xlim([20, 80])
            ylim([20, 80])
            set(gcf,'Units','Inches');
            set(gcf,'Position',[2.5 2.5 5 5])
            cleanfigure;
        ```
    """
    x = np.array(
        [
            21.842106,
            27.052631,
            32.263157,
            37.473682,
            42.68421,
            47.894737,
            53.105263,
            58.31579,
            63.526318,
            68.73684,
            73.947365,
            79.1579,
        ]
    )
    y = x.copy()
    tol = 0.02
    mask = cleanfigure._opheim_simplify(x, y, tol)
    assert mask.shape == (12,)
    assert np.allclose(mask * 1, np.array([1] + [0] * 10 + [1]))


@pytest.mark.parametrize(
    "function, result", [("plot", False), ("step", True)],
)
def test_is_step(function, result):
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        if function == "plot":
            (l,) = ax.plot(x, y)
        elif function == "step":
            (l,) = ax.step(x, y)
        assert cleanfigure._isStep(l) == result
    plt.close("all")


class Test_plottypes:
    """Testing plot types found here https://matplotlib.org/3.1.1/tutorials/introductory/sample_plots.html"""

    def test_plot(self):
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.plot(x, y)
            ax.set_ylim([20, 80])
            ax.set_xlim([20, 80])
            raw = get_tikz_code()

            cleanfigure.clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            numLinesRaw = raw.count("\n")
            numLinesClean = clean.count("\n")
            assert numLinesRaw - numLinesClean == 18
        plt.close("all")

    def test_step(self):
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.step(x, y)
            ax.set_ylim([20, 80])
            ax.set_xlim([20, 80])
            with pytest.warns(Warning):
                cleanfigure.clean_figure(fig)
        plt.close("all")

    def test_scatter(self):
        # TODO: scatter plots are represented through axes.collections. Currently, this is simply ignored and nothing is done.
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)
        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.scatter(x, y)
            ax.set_ylim([20, 80])
            ax.set_xlim([20, 80])
            raw = get_tikz_code()

            cleanfigure.clean_figure()
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            numLinesRaw = raw.count("\n")
            numLinesClean = clean.count("\n")
            assert numLinesRaw - numLinesClean == 6
        plt.close("all")

    def test_bar(self):
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)
        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.bar(x, y)
            ax.set_ylim([20, 80])
            ax.set_xlim([20, 80])
            with pytest.warns(Warning):
                cleanfigure.clean_figure(fig)
        plt.close("all")

    def test_hist(self):
        """creates same test case as bar"""
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)
        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.hist(x, y)
            ax.set_ylim([20, 80])
            ax.set_xlim([20, 80])
            with pytest.warns(Warning):
                cleanfigure.clean_figure(fig)
        plt.close("all")

    def test_plot3d(self):
        theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
        z = np.linspace(-2, 2, 100)
        r = z ** 2 + 1
        x = r * np.sin(theta)
        y = r * np.cos(theta)

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            ax.plot(x, y, z)
            ax.set_xlim([-2, 2])
            ax.set_ylim([-2, 2])
            ax.set_zlim([-2, 2])
            ax.view_init(30, 30)
            raw = get_tikz_code(fig)

            cleanfigure.clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            numLinesRaw = raw.count("\n")
            numLinesClean = clean.count("\n")
            assert numLinesRaw - numLinesClean == 14
        plt.close("all")

    def test_scatter3d(self):
        x, y = np.meshgrid(np.linspace(1, 100, 20), np.linspace(1, 100, 20))
        z = np.abs(x - 50) + np.abs(y - 50)

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            ax.scatter(x, y, z)
            ax.set_xlim([20, 80])
            ax.set_ylim([20, 80])
            ax.set_zlim([0, 80])
            with pytest.warns(Warning):
                cleanfigure.clean_figure(fig)
        plt.close("all")

    def test_wireframe3D(self):
        """ """
        from mpl_toolkits.mplot3d import axes3d

        # Grab some test data.
        X, Y, Z = axes3d.get_test_data(0.05)

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")

            # Plot a basic wireframe.
            ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
            with pytest.warns(Warning):
                cleanfigure.clean_figure(fig)
        plt.close("all")

    def test_surface3D(self):
        from matplotlib import cm
        from matplotlib.ticker import LinearLocator, FormatStrFormatter

        # Make data.
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.gca(projection="3d")

            # Plot the surface.
            surf = ax.plot_surface(
                X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False
            )

            # Customize the z axis.
            ax.set_zlim(-1.01, 1.01)
            ax.zaxis.set_major_locator(LinearLocator(10))
            ax.zaxis.set_major_formatter(FormatStrFormatter("%.02f"))

            # Add a color bar which maps values to colors.
            fig.colorbar(surf, shrink=0.5, aspect=5)

            with pytest.warns(Warning):
                cleanfigure.clean_figure(fig)
        plt.close("all")

    def test_trisurface3D(self):
        """:param Self:
        """
        import matplotlib.pyplot as plt
        import numpy as np

        n_radii = 8
        n_angles = 36
        # Make radii and angles spaces (radius r=0 omitted to eliminate duplication).
        radii = np.linspace(0.125, 1.0, n_radii)
        angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)

        # Repeat all angles for each radius.
        angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)

        # Convert polar (radii, angles) coords to cartesian (x, y) coords.
        # (0, 0) is manually added at this stage,  so there will be no duplicate
        # points in the (x, y) plane.
        x = np.append(0, (radii * np.cos(angles)).flatten())
        y = np.append(0, (radii * np.sin(angles)).flatten())

        # Compute z to make the pringle surface.
        z = np.sin(-x * y)

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.gca(projection="3d")

            ax.plot_trisurf(x, y, z, linewidth=0.2, antialiased=True)
            with pytest.warns(Warning):
                cleanfigure.clean_figure(fig)
        plt.close("all")

    def test_contour3D(self):
        from mpl_toolkits.mplot3d import axes3d
        import matplotlib.pyplot as plt
        from matplotlib import cm

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            X, Y, Z = axes3d.get_test_data(0.05)
            cset = ax.contour(X, Y, Z, cmap=cm.coolwarm)
            ax.clabel(cset, fontsize=9, inline=1)
            with pytest.warns(Warning):
                cleanfigure.clean_figure(fig)
        plt.close("all")

    def test_polygon3D(self):
        from matplotlib.collections import PolyCollection
        from matplotlib import colors as mcolors

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.gca(projection="3d")

            def cc(arg):
                """

                :param arg:

                """
                return mcolors.to_rgba(arg, alpha=0.6)

            xs = np.arange(0, 10, 0.4)
            verts = []
            zs = [0.0, 1.0, 2.0, 3.0]
            for z in zs:
                ys = np.random.rand(len(xs))
                ys[0], ys[-1] = 0, 0
                verts.append(list(zip(xs, ys)))

            poly = PolyCollection(
                verts, facecolors=[cc("r"), cc("g"), cc("b"), cc("y")]
            )
            poly.set_alpha(0.7)
            ax.add_collection3d(poly, zs=zs, zdir="y")

            ax.set_xlabel("X")
            ax.set_xlim3d(0, 10)
            ax.set_ylabel("Y")
            ax.set_ylim3d(-1, 4)
            ax.set_zlabel("Z")
            ax.set_zlim3d(0, 1)
            with pytest.warns(Warning):
                cleanfigure.clean_figure(fig)
        plt.close("all")

    def test_bar3D(self):
        import matplotlib.pyplot as plt
        import numpy as np

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            for c, z in zip(["r", "g", "b", "y"], [30, 20, 10, 0]):
                xs = np.arange(20)
                ys = np.random.rand(20)

                # You can provide either a single color or an array. To demonstrate this,
                # the first bar of each set will be colored cyan.
                cs = [c] * len(xs)
                cs[0] = "c"
                ax.bar(xs, ys, zs=z, zdir="y", color=cs, alpha=0.8)

            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            with pytest.warns(Warning):
                cleanfigure.clean_figure(fig)
        plt.close("all")

    def test_quiver3D(self):
        import matplotlib.pyplot as plt
        import numpy as np

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.gca(projection="3d")

            # Make the grid
            x, y, z = np.meshgrid(
                np.arange(-0.8, 1, 0.2),
                np.arange(-0.8, 1, 0.2),
                np.arange(-0.8, 1, 0.8),
            )

            # Make the direction data for the arrows
            u = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
            v = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
            w = (
                np.sqrt(2.0 / 3.0)
                * np.cos(np.pi * x)
                * np.cos(np.pi * y)
                * np.sin(np.pi * z)
            )

            ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True)
            with pytest.warns(Warning):
                cleanfigure.clean_figure(fig)
        plt.close("all")

    def test_2D_in_3D(self):
        import numpy as np
        import matplotlib.pyplot as plt

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.gca(projection="3d")

            # Plot a sin curve using the x and y axes.
            x = np.linspace(0, 1, 100)
            y = np.sin(x * 2 * np.pi) / 2 + 0.5
            ax.plot(x, y, zs=0, zdir="z", label="curve in (x,y)")

            # Plot scatterplot data (20 2D points per colour) on the x and z axes.
            colors = ("r", "g", "b", "k")
            x = np.random.sample(20 * len(colors))
            y = np.random.sample(20 * len(colors))
            c_list = []
            for c in colors:
                c_list += [c] * 20
            # By using zdir='y', the y value of these points is fixed to the zs value 0
            # and the (x,y) points are plotted on the x and z axes.
            ax.scatter(x, y, zs=0, zdir="y", c=c_list, label="points in (x,z)")

            # Make legend, set axes limits and labels
            ax.legend()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_zlim(0, 1)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")

            # Customize the view angle so it's easier to see that the scatter points lie
            # on the plane y=0
            ax.view_init(elev=20.0, azim=-35)
            with pytest.warns(Warning):
                cleanfigure.clean_figure(fig)
        plt.close("all")


class Test_lineplot:
    def test_line_no_markers(self):
        """test high-level usage for simple example.
        Test is successfull if generated tikz code saves correct amount of lines
        """
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.plot(x, y, linestyle="-", marker="None")
            ax.set_ylim([20, 80])
            ax.set_xlim([20, 80])
            raw = get_tikz_code()

            cleanfigure.clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            numLinesRaw = raw.count("\n")
            numLinesClean = clean.count("\n")
            assert numLinesRaw - numLinesClean == 18
        plt.close("all")

    def test_no_line_markers(self):
        """test high-level usage for simple example.
        Test is successfull if generated tikz code saves correct amount of lines
        """
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.plot(x, y, linestyle="None", marker="*")
            ax.set_ylim([20, 80])
            ax.set_xlim([20, 80])
            raw = get_tikz_code()

            cleanfigure.clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            numLinesRaw = raw.count("\n")
            numLinesClean = clean.count("\n")
            assert numLinesRaw - numLinesClean == 6
        plt.close("all")

    def test_line_markers(self):
        """test high-level usage for simple example.
        Test is successfull if generated tikz code saves correct amount of lines
        """
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.plot(x, y, linestyle="-", marker="*")
            ax.set_ylim([20, 80])
            ax.set_xlim([20, 80])
            raw = get_tikz_code()

            cleanfigure.clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            numLinesRaw = raw.count("\n")
            numLinesClean = clean.count("\n")
            assert numLinesRaw - numLinesClean == 6
        plt.close("all")

    def test_sine(self):
        x = np.linspace(1, 2 * np.pi, 100)
        y = np.sin(8 * x)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.plot(x, y, linestyle="-", marker="*")
            ax.set_xlim([0.5 * np.pi, 1.5 * np.pi])
            ax.set_ylim([-1, 1])
            raw = get_tikz_code()

            cleanfigure.clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            numLinesRaw = raw.count("\n")
            numLinesClean = clean.count("\n")
            assert numLinesRaw - numLinesClean == 39
        plt.close("all")


class Test_subplots:
    def test_subplot(self):
        """octave code
        ```octave
            addpath ("../matlab2tikz/src")

            x = linspace(1, 100, 20);
            y1 = linspace(1, 100, 20);

            figure
            subplot(2, 2, 1)
            plot(x, y1, "-")
            subplot(2, 2, 2)
            plot(x, y1, "-")
            subplot(2, 2, 3)
            plot(x, y1, "-")
            subplot(2, 2, 4)
            plot(x, y1, "-")
            xlim([20, 80])
            ylim([20, 80])
            set(gcf,'Units','Inches');
            set(gcf,'Position',[2.5 2.5 5 5])
            cleanfigure;
        ```
        """

        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, axes = plt.subplots(2, 2, figsize=(5, 5))
            plotstyles = [("-", "o"), ("-", "None"), ("None", "o"), ("--", "x")]
            for ax, style in zip(axes.ravel(), plotstyles):
                ax.plot(x, y, linestyle=style[0], marker=style[1])
                ax.set_ylim([20, 80])
                ax.set_xlim([20, 80])
            raw = get_tikz_code()

            cleanfigure.clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            numLinesRaw = raw.count("\n")
            numLinesClean = clean.count("\n")
            assert numLinesRaw - numLinesClean == 36
        plt.close("all")


def test_segmentVisible():
    """test against matlab2tikz implementation

    octave code to generate baseline results. Note that octave has indexing 1...N, whereas python has indexing 0...N-1.
    ```octave
        x = linspace(1, 100, 20);
        y1 = linspace(1, 100, 20);

        figure
        plot(x, y1)
        xlim([20, 80])
        ylim([20, 80])
        cleanfigure;
    ```
    """

    y = np.linspace(1, 100, 20)
    x = y.copy()
    data = np.stack([x, y], axis=1)
    dataIsInBox = np.array([0] * 4 + [1] * 12 + [0] * 4) == 1
    xLim = np.array([20, 80])
    yLim = np.array([20, 80])
    mask = cleanfigure._segment_visible(data, dataIsInBox, xLim, yLim)
    assert np.allclose(mask * 1, np.array([0] * 3 + [1] * 13 + [0] * 3))


def test_crossLines():
    """test against matplotlib2tikz implementation"""
    y = np.linspace(1, 100, 20)
    x = y.copy()
    data = np.stack([x, y], axis=1)
    X1 = data[:-1, :]
    X2 = data[1:, :]
    X3 = np.array([80, 20])
    X4 = np.array([80, 80])
    Lambda = cleanfigure._cross_lines(X1, X2, X3, X4)

    expected_result = np.array(
        [
            [15.16162, 1.00000],
            [14.16162, 1.00000],
            [13.16162, 1.00000],
            [12.16162, 1.00000],
            [11.16162, 1.00000],
            [10.16162, 1.00000],
            [9.16162, 1.00000],
            [8.16162, 1.00000],
            [7.16162, 1.00000],
            [6.16162, 1.00000],
            [5.16162, 1.00000],
            [4.16162, 1.00000],
            [3.16162, 1.00000],
            [2.16162, 1.00000],
            [1.16162, 1.00000],
            [0.16162, 1.00000],
            [-0.83838, 1.00000],
            [-1.83838, 1.00000],
            [-2.83838, 1.00000],
        ]
    )
    assert np.allclose(Lambda, expected_result, rtol=1.0e-4)


def test_segmentsIntersect():
    """test against matplotlib2tikz implementation"""
    y = np.linspace(1, 100, 20)
    x = y.copy()
    data = np.stack([x, y], axis=1)
    X1 = data[:-1, :]
    X2 = data[1:, :]
    X3 = np.array([80, 20])
    X4 = np.array([80, 80])
    mask = cleanfigure._segments_intersect(X1, X2, X3, X4)
    assert np.allclose(mask * 1, np.zeros_like(mask))


def test_pixelate():
    xToPix = 49.952
    yToPix = 49.952
    xData = np.array(
        [
            21.842,
            27.053,
            32.263,
            37.474,
            42.684,
            47.895,
            53.105,
            58.316,
            63.526,
            68.737,
            73.947,
            79.158,
        ]
    )
    yData = xData.copy()
    mask = cleanfigure._pixelate(xData, yData, xToPix, yToPix)
    assert mask.shape == (12,)
    assert np.all(mask)


def test_corners3D():
    xlim = ylim = zlim = np.array([-5, 5])
    corners = cleanfigure._corners3D(xlim, ylim, zlim)

    assert corners.shape == (8, 3)
    assert np.sum(corners) == 0


def test_corners2D():
    xLim = np.array([20, 80])
    yLim = np.array([20, 80])
    corners = cleanfigure._corners2D(xLim, yLim)

    import itertools

    expected_output = tuple(np.array(t) for t in itertools.product([20, 80], [20, 80]))
    assert np.allclose(corners, expected_output)


def test_getHeightWidthInPixels():
    with plt.rc_context(rc=RC_PARAMS):
        fig, axes = plt.subplots(1, 1, figsize=(5, 5))
        w, h = cleanfigure._get_width_height_in_pixels(fig, [600, 400])
        assert w == 600 and h == 400
        w, h = cleanfigure._get_width_height_in_pixels(fig, 600)
        assert w == h
        plt.close("all")


def test_memory():
    import matplotlib.pyplot as plt
    import numpy as np
    import tikzplotlib

    plt.plot(np.arange(100000))
    tikzplotlib.clean_figure()
    plt.close("all")
