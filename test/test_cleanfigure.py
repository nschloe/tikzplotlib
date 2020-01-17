import numpy as np
import pytest
from matplotlib import pyplot as plt

from tikzplotlib import cleanfigure

RC_PARAMS = {"figure.figsize": [5, 5], "figure.dpi": 220, "pgf.rcfonts": False}


def test_pruneOutsideBox():
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
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(x, y)
        ax.set_ylim([20, 80])
        ax.set_xlim([20, 80])
        cleanfigure.pruneOutsideBox(fig, ax, l)
        assert l.get_xdata().shape == (14,)


def test_replaceDataWithNaN():
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
    data = np.stack([np.linspace(1, 100, 20)] * 2, axis=1)

    newdata = cleanfigure.replaceDataWithNaN(data, id_replace)
    assert newdata.shape == data.shape
    assert np.any(np.isnan(newdata))


def test_removeData():
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
    id_remove = np.array([1, 2, 3, 17, 18, 19])
    data = np.stack([np.linspace(1, 100, 20)] * 2, axis=1)

    newdata = cleanfigure.removeData(data, id_remove)
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
    data = np.stack([np.linspace(1, 100, 20)] * 2, axis=1)
    newdata = cleanfigure.replaceDataWithNaN(data, id_replace)
    newdata = cleanfigure.removeData(newdata, id_remove)
    newdata = cleanfigure.removeNaNs(newdata)
    assert not np.any(np.isnan(newdata))
    assert newdata.shape == (12, 2)


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
    mask = cleanfigure.isInBox(data, relaxedXLim, relaxedYLim)
    assert int(np.sum(mask)) == 12


def test_getVisualLimits():
    """
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
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(x, y)
        ax.set_xlim([20, 80])
        ax.set_ylim([20, 80])
        xLim, yLim = cleanfigure.getVisualLimits(fig, ax)
        assert np.allclose(xLim, np.array([20, 80]))
        assert np.allclose(yLim, np.array([20, 80]))


def test_interactiveManipulation():
    """Create a plot, then remove some data, and see if the graph is updated
    """
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)
    id_remove = np.arange(0, 10)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(x, y)
        xData, yData = cleanfigure.getVisualData(ax, l)
        data = np.stack([xData, yData], axis=1)
        data = cleanfigure.removeData(data, id_remove)
        l.set_xdata(data[:, 0])
        l.set_ydata(data[:, 1])
        plt.show()


def test_movePointsCloser():
    """
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
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(x, y)
        ax.set_ylim([20, 80])
        ax.set_xlim([20, 80])
        cleanfigure.pruneOutsideBox(fig, ax, l)
        cleanfigure.movePointscloser(fig, ax, l)
        assert l.get_xdata().shape == (14,)


def test_simplifyLine():
    """
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
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(x, y)
        ax.set_ylim([20, 80])
        ax.set_xlim([20, 80])
        cleanfigure.pruneOutsideBox(fig, ax, l)
        cleanfigure.movePointscloser(fig, ax, l)
        cleanfigure.simplifyLine(fig, ax, l, 600)
        assert l.get_xdata().shape == (2,)
        assert l.get_ydata().shape == (2,)


def test_limitPrecision():
    """
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
    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        (l,) = ax.plot(x, y)
        ax.set_ylim([20, 80])
        ax.set_xlim([20, 80])
        cleanfigure.pruneOutsideBox(fig, ax, l)
        cleanfigure.movePointscloser(fig, ax, l)
        cleanfigure.simplifyLine(fig, ax, l, 600)
        cleanfigure.limitPrecision(fig, ax, l, 1)
        assert l.get_xdata().shape == (2,)
        assert l.get_ydata().shape == (2,)


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
    mask = cleanfigure.opheimSimplify(x, y, tol)
    assert mask.shape == (12,)
    assert np.allclose(mask * 1, np.array([1,] + [0,] * 10 + [1,]))


# TODO: test for getVisualData


def test_cleanfigure():
    """test high-level usage for simple example.
    Test is successfull if generated tikz code saves correct amount of lines
    """
    from tikzplotlib import get_tikz_code

    x = np.linspace(1, 100, 20)
    y = np.linspace(1, 100, 20)

    with plt.rc_context(rc=RC_PARAMS):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        ax.plot(x, y)
        ax.set_ylim([20, 80])
        ax.set_xlim([20, 80])
        raw = get_tikz_code()

        cleanfigure.cleanfigure(fig, ax)
        clean = get_tikz_code()

        # Use number of lines to test if it worked.
        # the baseline (raw) should have 20 points
        # the clean version (clean) should have 2 points
        # the difference in line numbers should therefore be 2
        numLinesRaw = raw.count("\n")
        numLinesClean = clean.count("\n")
        assert numLinesRaw - numLinesClean == 18


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
    dataIsInBox = np.array([0,] * 4 + [1,] * 12 + [0,] * 4) == 1
    xLim = np.array([20, 80])
    yLim = np.array([20, 80])
    mask = cleanfigure.segmentVisible(data, dataIsInBox, xLim, yLim)
    assert np.allclose(mask * 1, np.array([0,] * 3 + [1,] * 13 + [0,] * 3))


def test_crossLines():
    """test against matplotlib2tikz implementation
    """
    y = np.linspace(1, 100, 20)
    x = y.copy()
    data = np.stack([x, y], axis=1)
    X1 = data[:-1, :]
    X2 = data[1:, :]
    X3 = np.array([80, 20])
    X4 = np.array([80, 80])
    Lambda = cleanfigure.crossLines(X1, X2, X3, X4)

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
    """test against matplotlib2tikz implementation
    """
    y = np.linspace(1, 100, 20)
    x = y.copy()
    data = np.stack([x, y], axis=1)
    X1 = data[:-1, :]
    X2 = data[1:, :]
    X3 = np.array([80, 20])
    X4 = np.array([80, 80])
    mask = cleanfigure.segmentsIntersect(X1, X2, X3, X4)
    assert np.allclose(mask * 1, np.zeros_like(mask))

