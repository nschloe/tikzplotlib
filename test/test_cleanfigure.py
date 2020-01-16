import pytest
from tikzplotlib import cleanfigure
import numpy as np
from matplotlib import pyplot as plt

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
        plt.show()


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

