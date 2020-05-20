import numpy as np
from matplotlib import pyplot as plt

import pytest
from tikzplotlib import clean_figure, get_tikz_code

RC_PARAMS = {"figure.figsize": [5, 5], "figure.dpi": 220, "pgf.rcfonts": False}


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

            clean_figure(fig)
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
                clean_figure(fig)
        plt.close("all")

    def test_scatter(self):
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)
        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.scatter(x, y)
            ax.set_ylim([20, 80])
            ax.set_xlim([20, 80])
            raw = get_tikz_code()

            clean_figure()
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
                clean_figure(fig)
        plt.close("all")

    def test_hist(self):
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)
        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.hist(x, y)
            ax.set_ylim([20, 80])
            ax.set_xlim([20, 80])
            with pytest.warns(Warning):
                clean_figure(fig)
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

            clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            numLinesRaw = raw.count("\n")
            numLinesClean = clean.count("\n")

            assert numLinesRaw - numLinesClean == 14
        plt.close("all")

    def test_scatter3d(self):
        theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
        z = np.linspace(-2, 2, 100)
        r = z ** 2 + 1
        x = r * np.sin(theta)
        y = r * np.cos(theta)

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            ax.scatter(x, y, z)
            ax.set_xlim([-2, 2])
            ax.set_ylim([-2, 2])
            ax.set_zlim([-2, 2])
            ax.view_init(30, 30)
            raw = get_tikz_code(fig)

            clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            numLinesRaw = raw.count("\n")
            numLinesClean = clean.count("\n")

            assert numLinesRaw - numLinesClean == 14
        plt.close("all")

    def test_wireframe3D(self):
        from mpl_toolkits.mplot3d import axes3d

        # Grab some test data.
        X, Y, Z = axes3d.get_test_data(0.05)

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")

            # Plot a basic wireframe.
            ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
            with pytest.warns(Warning):
                clean_figure(fig)
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
                clean_figure(fig)
        plt.close("all")

    def test_trisurface3D(self):
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
                clean_figure(fig)
        plt.close("all")

    def test_contour3D(self):
        from mpl_toolkits.mplot3d import axes3d
        from matplotlib import cm

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            X, Y, Z = axes3d.get_test_data(0.05)
            cset = ax.contour(X, Y, Z, cmap=cm.coolwarm)
            ax.clabel(cset, fontsize=9, inline=1)
            with pytest.warns(Warning):
                clean_figure(fig)
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
                clean_figure(fig)
        plt.close("all")

    def test_bar3D(self):
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
                clean_figure(fig)
        plt.close("all")

    def test_quiver3D(self):
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
                clean_figure(fig)
        plt.close("all")

    def test_2D_in_3D(self):
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
        plt.close("all")


class Test_lineplot_markers:
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

            clean_figure(fig)
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

            clean_figure(fig)
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

            clean_figure(fig)
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

            clean_figure(fig)
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

            clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            numLinesRaw = raw.count("\n")
            numLinesClean = clean.count("\n")
            assert numLinesRaw - numLinesClean == 36
        plt.close("all")


def test_memory():
    plt.plot(np.arange(100000))
    clean_figure()
    plt.close("all")
