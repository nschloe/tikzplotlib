import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import mpl_toolkits
from mpl_toolkits import mplot3d

# TODO: see which test cases the matlab2tikz guys used [!!!]
# TODO: find suitable test cases for remaining functions. [!!]
# TODO: implement remaining functions [!!]
# - simplify stair : plt.step
# -- looks like matlabs stairs plot and matplotlibs plt.step is implemented differently. The data representation is different.
# - there is still a missing code block in movePointsCloser. Maybe find suitable axes limits to get this code block to work
# TODO: make grid of plot types which are working and which not. 2D and 3D


STEP_DRAW_STYLES = ["steps-pre", "steps-post", "steps-mid"]


def cleanfigure(fig=None, targetResolution=600, scalePrecision=1.0):
    """Cleans figure as a preparation for tikz export.
    This will minimize the number of points required for the tikz figure.
    If the figure has subplots, it will recursively clean then up.

    Note that this function modifies the figure directly (impure function).

    :param fig: Matplotlib figure handle (Default value = None)
    :param targetResolution: target resolution of final figure in PPI.
        If a scalar integer is provided, it is assumed to be square in both axis.
        If a list or an np.array is provided, it is interpreted as [H, W].
        By default 600
    :type targetResolution: int, list or np.array, optional
    :param scalePrecision: scalar value indicating precision when scaling down.
        By default 1
    :type scalePrecision: float, optional
    Examples
    --------

        1. 2D lineplot
        ```python
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
                print("number of tikz lines saved", numLinesRaw - numLinesClean)
        ```

        2. 3D lineplot
        ```python
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

                cleanfigure.cleanfigure(fig)
                clean = get_tikz_code()

                # Use number of lines to test if it worked.
                numLinesRaw = raw.count("\n")
                numLinesClean = clean.count("\n")
                assert numLinesRaw - numLinesClean == 14
        ```
    """
    if fig is None:
        fig = plt.gcf()
    elif fig == "gcf":  # tikzplotlib syntax
        fig = plt.gcf()
    _recursive_cleanfigure(
        fig, targetResolution=targetResolution, scalePrecision=scalePrecision
    )


def _recursive_cleanfigure(obj, targetResolution=600, scalePrecision=1.0):
    """Recursively visit child objects and clean them up.

    :param obj: object
    :param targetResolution: target resolution of final figure in PPI.
        If a scalar integer is provided, it is assumed to be square in both axis.
        If a list or an np.array is provided, it is interpreted as [H, W].
        By default 600
    :type targetResolution: int, list or np.array, optional
    :param scalePrecision: scalar value indicating precision when scaling down.
        By default 1
    :type scalePrecision: float, optional
    """
    for child in obj.get_children():
        if isinstance(child, mpl.spines.Spine):
            pass
        if isinstance(child, mpl.axes.Axes):
            # Note: containers contain Patches but are not child objects.
            # This is a problem because a bar plot creates a Barcontainer.
            _clean_containers(child)
            _recursive_cleanfigure(
                child, targetResolution=targetResolution, scalePrecision=scalePrecision
            )
        elif isinstance(child, mpl_toolkits.mplot3d.axes3d.Axes3D):
            _clean_containers(child)
            _recursive_cleanfigure(
                child, targetResolution=targetResolution, scalePrecision=scalePrecision
            )
        elif isinstance(child, mpl.lines.Line2D):
            ax = child.axes
            fig = ax.figure
            _cleanline(
                fig,
                ax,
                linehandle=child,
                targetResolution=targetResolution,
                scalePrecision=scalePrecision,
            )
        elif isinstance(child, mplot3d.art3d.Line3D):
            ax = child.axes
            fig = ax.figure
            _cleanline(
                fig,
                ax,
                linehandle=child,
                targetResolution=targetResolution,
                scalePrecision=scalePrecision,
            )
        elif isinstance(child, mpl.image.AxesImage):
            pass
        elif isinstance(child, mpl.patches.Patch):
            pass
        elif isinstance(child, mpl.collections.PathCollection):
            import warnings

            warnings.warn(
                "Cleaning Path Collections (scatter plot) is not supported yet."
            )
        elif isinstance(child, mpl.collections.LineCollection):
            import warnings

            warnings.warn(
                "Cleaning Line Collections (scatter plot) is not supported yet."
            )
        elif isinstance(child, mplot3d.art3d.Line3DCollection):
            import warnings

            warnings.warn("Cleaning Line3DCollection is not supported yet.")
        elif isinstance(child, mplot3d.art3d.Poly3DCollection):
            import warnings

            warnings.warn("Cleaning Poly3DCollections is not supported yet.")
        else:
            pass


def _clean_containers(axes):
    """Containers are not children of axes. They need to be visited separately.

    :param axes: matplotlib axes object
    """
    for container in axes.containers:
        if isinstance(container, mpl.container.BarContainer):
            import warnings

            warnings.warn("Cleaning Bar Container (bar plot) is not supported yet.")


def _cleanline(fighandle, axhandle, linehandle, targetResolution, scalePrecision):
    """Clean a 2D Line plot figure.

    :param fighandle: matplotlib figure object
    :param axhandle: matplotlib axes object
    :param linehandle: matplotlib line object (2D or 3D)
    :param targetResolution: target resolution of final figure in PPI.
        If a scalar integer is provided, it is assumed to be square in both axis.
        If a list or an np.array is provided, it is interpreted as [H, W].
        By default 600
    :type targetResolution: int, list or np.array, optional
    :param scalePrecision: scalar value indicating precision when scaling down.
        By default 1
    :type scalePrecision: float, optional
    """
    if _isStep(linehandle):
        import warnings

        warnings.warn("step plot simplification not yet implemented.", Warning)
        # TODO: simplifyStairs not yet working
        # pruneOutsideBox(fighandle, axhandle, linehandle)
        # simplifyStairs(fighandle, axhandle, linehandle)
        # limitPrecision(fighandle, axhandle, linehandle, scalePrecision)
    else:
        _pruneOutsideBox(fighandle, axhandle, linehandle)
        _movePointscloser(fighandle, axhandle, linehandle)
        _simplifyLine(fighandle, axhandle, linehandle, targetResolution)
        _limitPrecision(fighandle, axhandle, linehandle, scalePrecision)


def _isStep(linehandle):
    """Check if plot is a step plot.

    :param linehandle: matplotlib line handle object
    :type linehandle: mpl.lines.Line2D or mpl_toolkits.mplot3d.art3d.Line3D
    """
    return linehandle._drawstyle in STEP_DRAW_STYLES


def _getVisualLimits(fighandle, axhandle):
    """Returns the visual representation of the axis limits,
    respecting possible log_scaling and projection into the image plane.

    :param fighandle: handle to matplotlib figure object
    :type fighandle: mpl.figure.Figure
    :param axhandle: handle to matplotlib axes object
    :type axhandle: mpl.axes.Axes or mpl_toolkits.mplot3d.axes3d.Axes3D
    """
    is3D = _axIs3D(axhandle)

    xLim = np.array(axhandle.get_xlim())
    yLim = np.array(axhandle.get_ylim())
    if is3D:
        zLim = np.array(axhandle.get_ylim())

    # Check for logarithmic scales
    isXlog = axhandle.get_xscale() == "log"
    if isXlog:
        xLim = np.log10(xLim)
    isYLog = axhandle.get_yscale() == "log"
    if isYLog:
        yLim = np.log10(yLim)
    if is3D:
        isZLog = axhandle.get_zscale() == "log"
        if isZLog:
            zLim = np.log10(zLim)

    if is3D:
        P = _getProjectionMatrix(axhandle)

        corners = _corners3D(xLim, yLim, zLim)

        # Add the canonical 4th dimension
        corners = np.concatenate([corners, np.ones((8, 1))], axis=1)
        cornersProjected = P @ corners.T

        xCorners = cornersProjected[0, :] / cornersProjected[3, :]
        yCorners = cornersProjected[1, :] / cornersProjected[3, :]

        xLim = np.array([np.min(xCorners), np.max(xCorners)])
        yLim = np.array([np.min(yCorners), np.max(yCorners)])

    return xLim, yLim


def _replaceDataWithNan(linehandle, id_replace):
    """Replaces data at id_replace with NaNs.

    :param data: array of x and y data with shape [N, 2]
    :type data: np.ndarray
    :param id_replace: array with indices to replace. Shape [K,]
    :type id_replace: np.array
    :param linehandle: matplotlib line handle object
    :type linehandle: object
    """
    if _elements(id_replace) == 0:
        return

    is3D = _lineIs3D(linehandle)

    if is3D:
        xData, yData, zData = linehandle.get_data_3d()
        zData = zData.copy()
    else:
        xData = linehandle.get_xdata().astype(np.float32)
        yData = linehandle.get_ydata().astype(np.float32)

    xData[id_replace] = np.NaN
    yData[id_replace] = np.NaN
    if is3D:
        zData = zData.copy()
        zData[id_replace] = np.NaN

    if is3D:
        # TODO: I don't understand why I need to set both to get tikz code reduction to work
        linehandle.set_data_3d(xData, yData, zData)
        linehandle.set_data(xData, yData)
    else:
        linehandle.set_xdata(xData)
        linehandle.set_ydata(yData)


def _removeData(linehandle, id_remove):
    """remove data at id_remove

    :param data: array of x and y data with shape [N, 2]
    :type data: np.ndarray
    :param id_remove: array of x and y data with shape [N, 2]
    :type id_remove: np.array
    :param linehandle: matplotlib linehandle object
    :type linehandle: object
    """
    if _elements(id_remove) == 0:
        return

    is3D = _lineIs3D(linehandle)
    if is3D:
        xData, yData, zData = linehandle.get_data_3d()
    else:
        xData = linehandle.get_xdata().astype(np.float32)
        yData = linehandle.get_ydata().astype(np.float32)

    xData = np.delete(xData, id_remove, axis=0)
    yData = np.delete(yData, id_remove, axis=0)
    if is3D:
        zData = np.delete(zData, id_remove, axis=0)

    if is3D:
        # TODO: I don't understand why I need to set both to get tikz code reduction to work
        linehandle.set_data_3d(xData, yData, zData)
        linehandle.set_data(xData, yData)
    else:
        linehandle.set_xdata(xData)
        linehandle.set_ydata(yData)


def _diff(x, *args, **kwargs):
    """modification of np.diff(x, *args, **kwargs).
    - If x is empty, return np.array([False])
    - else: return np.diff(x, *args, **kwargs)

    :param x: array to diff
    :type x: np.ndarray
    :param *args: additional arguments passed to `np.diff`
    :param **kwargs: additional keyword arguments passed to `np.diff`
    """
    if _isempty(x):
        return np.array([False])
    else:
        return np.diff(x, *args, **kwargs)


def _removeNaNs(linehandle):
    """Removes superflous NaNs in the data, i.e. those at the end/beginning of the data and consecutive ones.

    :param linehandle: matplotlib linehandle object
    """
    is3D = _lineIs3D(linehandle)
    if is3D:
        xData, yData, zData = linehandle.get_data_3d()
        data = np.stack([xData, yData, zData], axis=1)
    else:
        xData = linehandle.get_xdata().astype(np.float32)
        yData = linehandle.get_ydata().astype(np.float32)
        data = np.stack([xData, yData], axis=1)

    id_nan = np.any(np.isnan(data), axis=1)
    id_remove = np.argwhere(id_nan).reshape((-1,))
    if _isempty(id_remove):
        pass
    else:
        id_remove = id_remove[
            np.concatenate(
                [_diff(id_remove, axis=0) == 1, np.array([False]).reshape((-1,))]
            )
        ]

    id_first = np.argwhere(np.logical_not(id_nan))[0]
    id_last = np.argwhere(np.logical_not(id_nan))[-1]

    if _isempty(id_first):
        # remove entire data
        id_remove = np.arange(len(xData))
    else:
        id_remove = np.concatenate(
            [np.arange(0, id_first), id_remove, np.arange(id_last + 1, len(xData))]
        )
    data = np.delete(data, id_remove, axis=0)

    if is3D:
        # TODO: I don't understand why I need to set both to get tikz code reduction to work
        linehandle.set_data_3d(data[:, 0], data[:, 1], data[:, 2])
        linehandle.set_data(xData, yData)
    else:
        linehandle.set_xdata(data[:, 0])
        linehandle.set_ydata(data[:, 1])


def _isInBox(data, xLim, yLim):
    """Returns a mask that indicates, whether a data point is within the limits.

    :param data: data to check
    :type data: np.ndarray
    :param xLim: x axes limits
    :type xLim: list or np.array
    :param yLim: y axes limits
    :type xLim: list or np.array
    """
    maskX = np.logical_and(data[:, 0] > xLim[0], data[:, 0] < xLim[1])
    maskY = np.logical_and(data[:, 1] > yLim[0], data[:, 1] < yLim[1])
    mask = np.logical_and(maskX, maskY)
    return mask


def _lineIs3D(linehandle):
    """Check if given line object is a 3D plot.
    :param linehandle: matplotlib linehandle object
    :type linehandle: mpl.axes.Axes or mpl_toolkits.mplot3d.axes3d.Axes3D
    """
    return isinstance(linehandle, mpl_toolkits.mplot3d.art3d.Line3D)


def _axIs3D(axhandle):
    """Check if given axes handle object is a 3D plot.

    :param axhandle: matplotlib axes handle object
    :type axhandle: mpl.axes.Axes or mpl_toolkits.mplot3d.axes3d.Axes3D
    """
    return hasattr(axhandle, "get_zlim")


def _getVisualData(axhandle, linehandle):
    """Returns the visual representation of the data,
    respecting possible log_scaling and projection into the image plane.

    :param axhandle: handle for matplotlib axis object
    :type axhandle: object
    :param linehandle: handle for matplotlib line2D object
    :type linehandle: object
    """
    is3D = _lineIs3D(linehandle)
    if is3D:
        xData, yData, zData = linehandle.get_data_3d()
    else:
        xData = linehandle.get_xdata()
        yData = linehandle.get_ydata()

    isXlog = axhandle.get_xscale() == "log"
    if isXlog:
        xData = np.log10(xData)
    isYlog = axhandle.get_yscale() == "log"
    if isYlog:
        yData = np.log10(yData)
    if is3D:
        isZlog = axhandle.get_zscale() == "log"
        if isZlog:
            zData = np.log10(zData)

    if is3D:
        P = _getProjectionMatrix(axhandle)

        data = np.stack([xData, yData, zData, np.ones_like(zData)], axis=1)
        dataProjected = P @ data.T
        xData = dataProjected[0, :] / dataProjected[-1, :]
        yData = dataProjected[1, :] / dataProjected[-1, :]

    xData = np.reshape(xData, (-1,))
    yData = np.reshape(yData, (-1,))
    return xData, yData


def _elements(array):
    """check if array has elements.
    https://stackoverflow.com/questions/11295609/how-can-i-check-whether-the-numpy-array-is-empty-or-not

    :param array: array to check if it has any elements
    :type array: np.ndarray
    """
    return array.ndim and array.size


def _isempty(array):
    """proxy for matlab / octave isempty function

    :param array: array to check if it is empty
    :type array: np.ndarray
    """
    return _elements(array) == 0


def _pruneOutsideBox(fighandle, axhandle, linehandle):
    """Some sections of the line may sit outside of the visible box. Cut those off.

    This method is not pure because it updates the linehandle object's data.

    :param fighandle: matplotlib figure handle object
    :type fighandle: obj
    :param axhandle: matplotlib axes handle object
    :type axhandle: obj
    :param linehandle: matplotlib line2D handle object
    :type linehandle: obj
    """
    xData, yData = _getVisualData(axhandle, linehandle)

    data = np.stack([xData, yData], axis=1)

    if _elements(data) == 0:
        return

    hasLines = (linehandle.get_linestyle() is not None) and (
        linehandle.get_linewidth() > 0.0
    )

    xLim, yLim = _getVisualLimits(fighandle, axhandle)

    tol = 1.0e-10
    relaxedXLim = xLim + np.array([-tol, tol])
    relaxedYLim = yLim + np.array([-tol, tol])

    dataIsInBox = _isInBox(data, relaxedXLim, relaxedYLim)

    shouldPlot = dataIsInBox
    if hasLines:
        segvis = _segmentVisible(data, dataIsInBox, xLim, yLim)
        shouldPlot = np.logical_or(
            shouldPlot, np.concatenate([np.array([False]).reshape((-1,)), segvis])
        )
        shouldPlot = np.logical_or(
            shouldPlot, np.concatenate([segvis, np.array([False]).reshape((-1,))])
        )

    id_replace = np.array([[]])
    id_remove = np.array([[]])

    if not np.all(shouldPlot):
        id_remove = np.argwhere(np.logical_not(shouldPlot))

        # If there are consecutive data points to be removed, only replace
        # the first one by a NaN. Consecutive data points have
        # diff(id_remove)==1, so replace diff(id_remove)>1 by NaN and remove
        # the rest
        idx = np.diff(id_remove, axis=0) > 1
        idx = np.concatenate([np.array([True]).reshape((-1, 1)), idx], axis=0)

        id_replace = id_remove[idx]
        id_remove = id_remove[np.logical_not(idx)]
    _replaceDataWithNan(linehandle, id_replace)
    _removeData(linehandle, id_remove)
    _removeNaNs(linehandle)


def _movePointscloser(fighandle, axhandle, linehandle):
    """Move all points outside a box much larger than the visible one
    to the boundary of that box and make sure that lines in the visible
    box are preserved. This typically involves replacing one point by
    two new ones and a NaN.

    TODO: 3D simplification of frontal 2D projection. This requires the
    full transformation rather than the projection, as we have to calculate
    the inverse transformation to project back into 3D.

    :param fighandle: matplotlib figure handle object
    :type fighandle: obj
    :param axhandle: matplotlib axes handle object
    :type axhandle: obj
    :param linehandle: matplotlib line handle object
    :type linehandle: obj
    """
    is3D = _lineIs3D(linehandle)
    if is3D:
        return
    xData, yData = _getVisualData(axhandle, linehandle)
    xLim, yLim = _getVisualLimits(fighandle, axhandle)

    # Calculate the extension of the extended box
    xWidth = xLim[1] - xLim[0]
    yWidth = yLim[1] - yLim[0]

    # Don't choose the larger box too large to make sure that the values inside
    # it can still be treated by TeX.
    extendedFactor = 0.1
    largeXlim = xLim + extendedFactor * np.array([-xWidth, xWidth])
    largeYlim = yLim + extendedFactor * np.array([-yWidth, yWidth])

    data = np.stack([xData, yData], axis=1)
    dataIsInLargeBox = _isInBox(data, largeXlim, largeYlim)

    dataIsInLargeBox = np.logical_or(dataIsInLargeBox, np.any(np.isnan(data), axis=1))

    id_replace = np.argwhere(np.logical_not(dataIsInLargeBox))

    dataInsert = np.array([[]])
    if not _isempty(id_replace):
        # Get the indices of those points, that are the first point in a
        # segment. The last data point at size(data, 1) cannot be the first
        # point in a segment.
        id_first = id_replace[id_replace < (data.shape[0])]

        # Get the indices of those points, that are the second point in a
        # segment. Similarly the first data point cannot be the second data
        # point in a segment.
        id_second = id_replace[id_replace > 1]

        # Define the vectors of data points for the segments X1--X2
        X1_first = data[id_first, :]
        X2_first = data[id_first + 1, :]
        X1_second = data[id_second, :]
        X2_second = data[id_second - 1, :]

        newData_first = _moveToBox(X1_first, X2_first, largeXlim, largeYlim)
        newData_second = _moveToBox(X1_second, X2_second, largeXlim, largeYlim)

        isXlog = linehandle.get_xscale() == "log"
        if isXlog:
            newData_first[:, 0] = 10.0 ** newData_first[:, 0]
            newData_second[:, 0] = 10.0 ** newData_second[:, 0]

        isYlog = linehandle.get_yscale() == "log"
        if isYlog:
            newData_first[:, 1] = 10.0 ** newData_first[:, 1]
            newData_second[:, 1] = 10.0 ** newData_second[:, 1]

        isInfinite_first = np.any(np.logical_not(np.isfinite(newData_first)), axis=1)
        isInfinite_second = np.any(np.logical_not(np.isfinite(newData_second)), axis=1)

        #
        newData_first[isInfinite_first, :] = np.zeros((sum(isInfinite_first), 2)).fill(
            np.NaN
        )
        newData_second[isInfinite_second, :] = np.zeros(
            (sum(isInfinite_second), 2)
        ).fill(np.Nan)

        # rest of code
        #     % If a point is part of two segments, that cross the border, we need to
        #     % insert a NaN to prevent an additional line segment
        #     [trash, trash, id_conflict] = intersect(id_first (~isInfinite_first), ...
        #         id_second(~isInfinite_second));

        #     % Cut the data into length(id_replace)+1 segments.
        #     % Calculate the length of the segments
        #     length_segments = [id_replace(1);
        #         diff(id_replace);
        #         size(data, 1)-id_replace(end)];

        #     % Create an empty cell array for inserting NaNs and fill it at the
        #     % conflict sites
        #     dataInsert_NaN              = cell(length(length_segments),1);
        #     dataInsert_NaN(id_conflict) = mat2cell(NaN(length(id_conflict), 2),...
        #         ones(size(id_conflict)), 2);

        #     % Create a cell array for the moved points
        #     dataInsert_first  = mat2cell(newData_first,  ones(size(id_first)),  2);
        #     dataInsert_second = mat2cell(newData_second, ones(size(id_second)), 2);

        #     % Add an empty cell at the end of the last segment, as we do not
        #     % insert something *after* the data
        #     dataInsert_first  = [dataInsert_first;  cell(1)];
        #     dataInsert_second = [dataInsert_second; cell(1)];

        #     % If the first or the last point would have been replaced add an empty
        #     % cell at the beginning/end. This is because the last data point
        #     % cannot be the first data point of a line segment and vice versa.
        #     if(id_replace(end) == size(data, 1))
        #         dataInsert_first  = [dataInsert_first; cell(1)];
        #     end
        #     if(id_replace(1) == 1)
        #         dataInsert_second = [cell(1); dataInsert_second];
        #     end

        #     % Put the cells together, right points first, then the possible NaN
        #     % and then the left points
        #     dataInsert = cellfun(@(a,b,c) [a; b; c],...
        #                         dataInsert_second,...
        #                         dataInsert_NaN,...
        #                         dataInsert_first,...
        #                         'UniformOutput',false);
        # end

        # TODO: find a test case that enters this code block.
        raise NotImplementedError
    _insertData(fighandle, linehandle, id_replace, dataInsert)
    if _isempty(id_replace):
        return
    else:
        # TODO: implement this
        # numPointsInserted = cellfun(@(x) size(x,1), [cell(1);dataInsert(1:end-2)]);
        # id_remove = id_replace + cumsum(numPointsInserted);

        # % Remove the data point that should be replaced.
        # removeData(meta, handle, id_remove);

        # % Remove possible NaN duplications
        # removeNaNs(meta, handle);
        raise NotImplementedError


def _moveToBox(x, xRef, xLim, yLim):
    """Takes a box defined by xLim, yLim, a vector of points x and a vector of
    reference points xRef.
    Returns the vector of points xNew that sits on the line segment between
    x and xRef *and* on the box. If several such points exist, take the
    closest one to x.

    :param x:
    :type x: np.ndarray
    :param xRef:
    :type xRef:
    :param xLim:
    :type xLim: np.ndarray
    :param yLim:
    :type yLim: np.ndarray
    """
    # n = size(x, 1);

    # #% Find out with which border the line x---xRef intersects, and determine
    # #% the smallest parameter alpha such that x + alpha*(xRef-x)
    # #% sits on the boundary. Otherwise set Alpha to inf.
    # minAlpha = inf(n, 1);

    # #% Get the corner points
    # [bottomLeft, topLeft, bottomRight, topRight] = corners2D(xLim, yLim);

    # #% left boundary:
    # minAlpha = updateAlpha(x, xRef, bottomLeft, topLeft, minAlpha);

    # #% bottom boundary:
    # minAlpha = updateAlpha(x, xRef, bottomLeft, bottomRight, minAlpha);

    # #% right boundary:
    # minAlpha = updateAlpha(x, xRef, bottomRight, topRight, minAlpha);

    # #% top boundary:
    # minAlpha = updateAlpha(x, xRef, topLeft, topRight, minAlpha);

    # #% Create the new point
    # xNew = x + bsxfun(@times ,minAlpha, (xRef-x));
    raise NotImplementedError


def _insertData(fighandle, linehandle, id_insert, dataInsert):
    """Inserts the elements of the cell array dataInsert at position id_insert.

    :param fighandle: matplotlib figure handle object
    :type fighandle: obj
    :param linehandle: matplotlib line handle object
    :type linehandle: obj
    :param id_insert: array of indices where to insert. Shape [N, 2]
    :type id_insert: np.ndarray
    :param dataInsert: array of data to insert.  Shape [N, 2]
    :type dataInsert: np.ndarray
    """
    if _isempty(id_insert):
        return
    # TODO: actually implement rest of function
    raise NotImplementedError


def _simplifyLine(fighandle, axhandle, linehandle, target_resolution):
    """Reduce the number of data points in the line 'handle'.

    Applies a path-simplification algorithm if there are no markers or
    pixelization otherwise. Changes are visually negligible at the target
    resolution.

    The target resolution is either specificed as the number of PPI or as
    the [Width, Height] of the figure in pixels.
    A scalar value of INF or 0 disables path simplification.
    (default = 600)

    :param fighandle: matplotlib figure handle object
    :type fighandle: obj
    :param axhandle: matplotlib axes handle object
    :type axhandle: obj
    :param linehandle: matplotlib line handle object
    :type linehandle: obj
    :param target_resolution: target resolution of final figure in PPI.
        If a scalar integer is provided, it is assumed to be square in both axis.
        If a list or an np.array is provided, it is interpreted as [H, W]
    :type target_resolution: int, list of int or np.array
    """
    if type(target_resolution) not in [list, np.ndarray, np.array]:
        if np.isinf(target_resolution) or target_resolution == 0:
            return
    elif any(np.logical_or(np.isinf(target_resolution), target_resolution == 0)):
        return
    W, H = _getWidthHeightInPixels(fighandle, target_resolution)
    xData, yData = _getVisualData(axhandle, linehandle)
    # Only simplify if there are more than 2 points
    if np.size(xData) <= 2 or np.size(yData) <= 2:
        return

    xLim, yLim = _getVisualLimits(fighandle, axhandle)

    # Automatically guess a tol based on the area of the figure and
    # the area and resolution of the output
    xRange = xLim[1] - xLim[0]
    yRange = yLim[1] - yLim[0]

    # Conversion factors of data units into pixels
    xToPix = W / xRange
    yToPix = H / yRange

    id_remove = np.array([])
    # If the path has markers, perform pixelation instead of simplification
    hasMarkers = not linehandle.get_marker() == "None"
    hasLines = not linehandle.get_linestyle() == "None"
    if hasMarkers and not hasLines:
        # Pixelate data at the zoom multiplier
        mask = _pixelate(xData, yData, xToPix, yToPix)
        id_remove = np.argwhere(mask * 1 == 0)
    elif hasLines and not hasMarkers:
        # Get the width of a pixel
        xPixelWidth = 1 / xToPix
        yPixelWidth = 1 / yToPix
        tol = min(xPixelWidth, yPixelWidth)

        # Split up lines which are seperated by NaNs
        id_nan = np.logical_or(np.isnan(xData), np.isnan(yData))

        # If lines were separated by a NaN, diff(~id_nan) would give 1 for
        # the start of a line and -1 for the index after the end of
        # a line.

        id_diff = np.diff(
            1
            * np.concatenate(
                [np.array([False]), np.logical_not(id_nan), np.array([False])]
            ),
            axis=0,
        ).reshape((-1,))
        lineStart = np.argwhere(id_diff == 1)
        lineStart = lineStart.reshape((-1,))
        lineEnd = np.argwhere(id_diff == -1) - 1
        lineEnd = lineEnd.reshape((-1,))
        numLines = np.size(lineStart)

        # original_code : id_remove = cell(numLines, 1)
        id_remove = [np.array([], dtype=np.int32).reshape((-1,))] * numLines

        # Simplify the line segments
        for ii in np.arange(numLines):
            # Actual data that inherits the simplifications
            x = xData[lineStart[ii] : lineEnd[ii] + 1]
            y = yData[lineStart[ii] : lineEnd[ii] + 1]

            # Line simplification
            if np.size(x) > 2:
                mask = _opheimSimplify(x, y, tol)
                id_remove[ii] = np.argwhere(mask == 0).reshape((-1,)) + lineStart[ii]
        # Merge the indices of the line segments
        # original code : id_remove = cat(1, id_remove{:})
        id_remove = np.concatenate(id_remove)

    # remove the data points
    _removeData(linehandle, id_remove)


def _simplifyStairs(fighandle, axhandle, linehandle):
    """Simplify step plot (matlab's stairs plot).

    :param fighandle: matplotlib figure handle object
    :type fighandle: mpl.figure.Figure
    :param axhandle: matplotlib axes handle object
    :type axhandle: mpl.axes.Axes or mpl_toolkits.mplot3d.axes3d.Axes3D
    :param linehandle: matplotlib line handle object
    :type linehandle: mpl.lines.Line2D or mpl_toolkits.mplot3d.art3d.Line3D
    """
    # TODO: it looks like matlab changes the data to be plotted when using `stairs` command, whereas matplotlib stores the same data but displays it as a step.
    xData = linehandle.get_xdata()
    yData = linehandle.get_ydata()
    if _isempty(xData) or _isempty(yData):
        return

    xNoDiff = np.concatenate([np.array([False]).reshape((-1,)), _diff(xData) == 0])
    yNoDiff = np.concatenate([np.array([False]).reshape((-1,)), _diff(yData) == 0])

    xNoDiff[-1] = False
    yNoDiff[-1] = False

    xIsMonotone = np.concatenate(
        [
            np.array([True]).reshape((-1,)),
            _diff(np.sign(_diff(xData))) == 0,
            np.array([True]).reshape((-1,)),
        ]
    )
    yIsMonotone = np.concatenate(
        [
            np.array([True]).reshape((-1,)),
            _diff(np.sign(_diff(yData))) == 0,
            np.array([True]).reshape((-1,)),
        ]
    )
    xRemove = np.logical_and(xNoDiff, yIsMonotone)
    yRemove = np.logical_and(yNoDiff, xIsMonotone)

    id_remove = np.argwhere(xRemove or yRemove)
    _removeData(linehandle, id_remove)


def _pixelate(x, y, xToPix, yToPix):
    """Rough reduction of data points at a multiple of the target resolution.
    The resolution is lost only beyond the multiplier magnification.

    :param x: x coordinates of data points. Shape [N, ]
    :type x: np.ndarray
    :param y: y coordinates of data points. Shape [N, ]
    :type y: np.ndarray
    :param xToPix: scalar converting x measure to pixel measure in x direction
    :type xToPix: float
    :param yToPix: scalar converting x measure to pixel measure in y direction
    :type yToPix: float

    """
    mult = 2
    dataPixel = np.round(np.stack([x * xToPix * mult, y * yToPix * mult], axis=1))
    id_orig = np.argsort(dataPixel[:, 0])
    dataPixelSorted = dataPixel[id_orig, :]

    m = np.logical_or(
        np.diff(dataPixelSorted[:, 0]) != 0, np.diff(dataPixelSorted[:, 1]) != 0
    )
    mask_sorted = np.concatenate([np.array([True]).reshape((-1,)), m], axis=0)

    mask = np.ones((x.shape)) == 0
    mask[id_orig] = mask_sorted
    mask[0] = True
    mask[-1] = True

    isnan = np.logical_or(np.isnan(x), np.isnan(y))
    mask[isnan] = True
    return mask


def _getWidthHeightInPixels(fighandle, target_resolution):
    """Target resolution as ppi / dpi. Return width and height in pixels

    :param fighandle: matplotlib figure object handle
    :type fighandle: obj
    :param target_resolution: Target resolution in PPI/ DPI. If target_resolution is a scalar, calculate final pixels based on figure width and height.
    :type target_resolution: scalar or list or np.array

    """
    if np.isscalar(target_resolution):
        # in matplotlib, the figsize units are always in inches
        figWidthInches = fighandle.get_figwidth()
        figHeightInches = fighandle.get_figheight()
        W = figWidthInches * target_resolution
        H = figHeightInches * target_resolution
    else:
        W = target_resolution[0]
        H = target_resolution[1]
    return W, H


def _opheimSimplify(x, y, tol):
    """Opheim path simplification algorithm.

     Given a path of vertices V and a tolerance TOL, the algorithm:
       1. selects the first vertex as the KEY;
       2. finds the first vertex farther than TOL from the KEY and links
          the two vertices with a LINE;
       3. finds the last vertex from KEY which stays within TOL from the
          LINE and sets it to be the LAST vertex. Removes all points in
          between the KEY and the LAST vertex;
       4. sets the KEY to the LAST vertex and restarts from step 2.

     The Opheim algorithm can produce unexpected results if the path
     returns back on itself while remaining within TOL from the LINE.
     This behaviour can be seen in the following example:

       x   = [1,2,2,2,3];
       y   = [1,1,2,1,1];
       tol < 1

     The algorithm undesirably removes the second last point. See
     https://github.com/matlab2tikz/matlab2tikz/pull/585#issuecomment-89397577
     for additional details.

     To rectify this issues, step 3 is modified to find the LAST vertex as
     follows:
       3*. finds the last vertex from KEY which stays within TOL from the
           LINE, or the vertex that connected to its previous point forms
           a segment which spans an angle with LINE larger than 90
           degrees.

    :param x: x coordinates of path to simplify. Shape [N, ]
    :type x: np.ndarray
    :param y: y coordinates of path to simplify. Shape [N, ]
    :type y: np.ndarray
    :param tol: scalar float specifiying the tolerance for path simplification
    :type tol: float
    :returns: boolean array of shape [N, ] that masks out elements that need not be drawn
    :rtype: np.ndarray

    References
    ----------
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.95.5882&rep=rep1&type=pdf
    """
    mask = np.zeros_like(x) == 1
    mask[0] = True
    mask[-1] = True
    N = np.size(x)
    i = 0
    while i <= N - 2 - 1:
        j = i + 1
        v = np.array([x[j] - x[i], y[j] - y[i]])
        while j < N - 1 and np.linalg.norm(v) <= tol:
            j = j + 1
            v = np.array([x[j] - x[i], y[j] - y[i]])
        v = v / np.linalg.norm(v)

        # Unit normal to the line between point i and point j
        normal = np.array([v[1], -v[0]])

        # Find the last point which stays within TOL from the line
        # connecting i to j, or the last point within a direction change
        # of pi/2.
        # Starts from the j+1 points, since all previous points are within
        # TOL by construction.

        while j < N - 1:
            # Calculate the perpendicular distance from the i->j line
            v1 = np.array([x[j + 1] - x[i], y[j + 1] - y[i]])
            d = np.abs(np.dot(normal, v1))
            if d > tol:
                break

            # Calculate the angle between the line from the i->j and the
            # line from j -> j+1. If
            v2 = np.array([x[j + 1] - x[j], y[j + 1] - y[i]])
            anglecosine = np.dot(v, v2)
            if anglecosine <= 0:
                break
            j = j + 1
        i = j
        mask[i] = True
    return mask


def _updateAlpha(X1, X2, X3, X4, minAlpha):
    """Checks whether the segments X1--X2 and X3--X4 intersect.

    :param X1: [description]
    :type X1: [type]
    :param X2: [description]
    :type X2: [type]
    :param X3: [description]
    :type X3: [type]
    :param X4: [description]
    :type X4: [type]
    :param minAlpha: [description]
    :type minAlpha: [type]
    :returns: [description]
    :rtype: [type]
    """
    # TODO implement this
    raise NotImplementedError
    return minAlpha


def _limitPrecision(fighandle, axhandle, linehandle, alpha):
    """Limit the precision of the given data. If alpha is 0 or negative do nothing.

    :param fighandle: matplotlib figure handle object
    :type fighandle: obj
    :param axhandle: matplotlib axes handle object
    :type axhandle: obj
    :param linehandle: matplotlib line handle object
    :type linehandle: obj
    :param alpha: scalar value indicating precision when scaling down. By default 1
    :type alpha: float
    """
    if alpha <= 0:
        return

    is3D = _lineIs3D(linehandle)
    if is3D:
        xData, yData, zData = linehandle.get_data_3d()
    else:
        xData = linehandle.get_xdata().astype(np.float32)
        yData = linehandle.get_ydata().astype(np.float32)

    isXlog = axhandle.get_xscale() == "log"
    isYlog = axhandle.get_yscale() == "log"
    if is3D:
        isZlog = axhandle.get_zscale() == "log"

    # Put the data into a matrix and log bits into vector
    if is3D:
        data = np.stack([xData, yData, zData], axis=1)
        isLog = np.array([isXlog, isYlog, isZlog])
    else:
        data = np.stack([xData, yData], axis=1)
        isLog = np.array([isXlog, isYlog])

    # Only do something if the data is not empty
    if _isempty(data) or np.isinf(data).all():
        return

    # Scale to visual coordinates
    data[:, isLog] = np.log10(data[:, isLog])

    # Get the maximal value of the data, only considering finite values
    maxValue = max(np.abs(data[np.isfinite(data)]))

    # The least significant bit is proportional to the numerical precision
    # of the largest number. Scale it with a user defined value alpha
    leastSignificantBit = np.finfo(maxValue).eps * alpha

    data = np.round(data / leastSignificantBit) * leastSignificantBit
    data[:, isLog] = 10.0 ** data[:, isLog]

    if is3D:
        # TODO: I don't understand why I need to set both to get tikz code reduction to work
        linehandle.set_data_3d(data[:, 0], data[:, 1], data[:, 2])
        linehandle.set_data(data[:, 0], data[:, 1])
    else:
        linehandle.set_xdata(data[:, 0])
        linehandle.set_ydata(data[:, 1])


def _pruneOutsideText(fighandle, axhandle, linehandle):
    """

    :param fighandle:
    :param axhandle:
    :param linehandle:
    """
    # TODO implement this
    raise NotImplementedError


def _segmentVisible(data, dataIsInBox, xLim, yLim):
    """Given a bounding box {x,y}Lim, determine whether the line between all
    pairs of subsequent data points [data(idx,:)<-->data(idx+1,:)] is visible.
    There are two possible cases:
    1: One of the data points is within the limits
    2: The line segments between the datapoints crosses the bounding box

    :param data: array of data points. Shape [N, 2]
    :type data: np.ndarray
    :param dataIsInBox: boolen mask that specifies if data point lies within visual box
    :type dataIxInBox: np.ndarray
    :param xLim: x axes limits
    :type xLim: list, np.array
    :param yLim: y axes limits
    :type yLim: list, np.array
    """
    n = np.shape(data)[0]
    mask = np.zeros((n - 1, n)) == 1

    # Only check if there is more than 1 point
    if n > 1:
        # Define the vectors of data points for the segments X1--X2
        idx = np.arange(n - 1)
        X1 = data[idx, :]
        X2 = data[idx + 1, :]

        # One of the neighbors is inside the box and the other is finite
        thisVisible = np.logical_and(dataIsInBox[idx], np.all(np.isfinite(X2), 1))
        nextVisible = np.logical_and(dataIsInBox[idx + 1], np.all(np.isfinite(X1), 1))

        bottomLeft, topLeft, bottomRight, topRight = _corners2D(xLim, yLim)

        left = _segmentsIntersect(X1, X2, bottomLeft, topLeft)
        right = _segmentsIntersect(X1, X2, bottomRight, topRight)
        bottom = _segmentsIntersect(X1, X2, bottomLeft, bottomRight)
        top = _segmentsIntersect(X1, X2, topLeft, topRight)

        # Check the result
        mask1 = np.logical_or(thisVisible, nextVisible)
        mask2 = np.logical_or(left, right)
        mask3 = np.logical_or(top, bottom)

        mask = np.logical_or(mask1, mask2)
        mask = np.logical_or(mask3, mask)

    return mask


def _corners2D(xLim, yLim):
    """Determine the corners of the axes as defined by xLim and yLim

    :param xLim: x limits interval. Shape [2, ]
    :type xLim: np.array
    :param yLim: y limits interval. Shape [2, ]
    :type yLim: np.array
    """

    bottomLeft = np.array([xLim[0], yLim[0]])
    topLeft = np.array([xLim[0], yLim[1]])
    bottomRight = np.array([xLim[1], yLim[0]])
    topRight = np.array([xLim[1], yLim[1]])
    return bottomLeft, topLeft, bottomRight, topRight


def _corners3D(xLim, yLim, zLim):
    """Determine the corners of the 3D axes as defined by xLim, yLim and zLim.

    :param xLim: x-axis limits
    :type xLim: list or np.array
    :param yLim: y-axis limits
    :type yLim: list or np.array
    :param zLim: z-axis limits
    :type zLim: list or np.array
    """

    # Lower square of the cube
    lowerBottomLeft = np.array([xLim[0], yLim[0], zLim[0]])
    lowerTopLeft = np.array([xLim[0], yLim[1], zLim[0]])
    lowerBottomRight = np.array([xLim[1], yLim[0], zLim[0]])
    lowerTopRight = np.array([xLim[1], yLim[1], zLim[0]])

    # Upper square of the cube
    upperBottomLeft = np.array([xLim[0], yLim[0], zLim[1]])
    upperTopLeft = np.array([xLim[0], yLim[1], zLim[1]])
    upperBottomRight = np.array([xLim[1], yLim[0], zLim[1]])
    upperTopRight = np.array([xLim[1], yLim[1], zLim[1]])

    corners = np.array(
        [
            lowerBottomLeft,
            lowerTopLeft,
            lowerBottomRight,
            lowerTopRight,
            upperBottomLeft,
            upperTopLeft,
            upperBottomRight,
            upperTopRight,
        ]
    )
    return corners


def _getProjectionMatrix(axhandle):
    """Get Projection matrix that projects 3D points into 2D image plane.

    :param axhandle: matplotlib axes handle object
    :type axhandle: obj
    """
    # TODO: write test
    az = np.deg2rad(axhandle.azim)
    el = np.deg2rad(axhandle.elev)
    rotationZ = np.array(
        [
            [np.cos(-az), -np.sin(-az), 0, 0],
            [np.sin(-az), np.cos(-az), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    rotationX = np.array(
        [
            [1, 0, 0, 0],
            [0, np.sin(el), np.cos(el), 0],
            [0, -np.cos(el), np.sin(el), 0],
            [0, 0, 0, 1],
        ]
    )
    xLim = axhandle.get_xlim3d()
    yLim = axhandle.get_ylim3d()
    zLim = axhandle.get_zlim3d()

    aspectRatio = np.array([xLim[1] - xLim[0], yLim[1] - xLim[0], zLim[1] - zLim[0]])
    aspectRatio /= aspectRatio[-1]
    scaleMatrix = np.diag(np.concatenate([aspectRatio, np.array([1.0])]))

    P = rotationX @ rotationZ @ scaleMatrix
    return P


def _isValidTargetResolution(val):
    """Check if given target resolution value is valid.

    :param val: target resolution value
    :type val: int, list or np.array
    """
    # TODO: implement this
    raise NotImplementedError


def _isValidAxis(val):
    """Check if given axes object is a valid axes object.

    :param val: axes object
    :type val: object
    """
    # TODO: implement this
    raise NotImplementedError


def _normalizeAxis(fighandle, axhandle):
    """Normalize Axis.

    :param fighandle: matplotlib figure handle object
    :param axhandle: matplotlib axes handle object
    """
    # TODO: implement this
    raise NotImplementedError


def _segmentsIntersect(X1, X2, X3, X4):
    """Checks whether the segments X1--X2 and X3--X4 intersect.

    :param X1: X1
    :type X1: np.ndarray
    :param X2: X2
    :type X2: np.ndarray
    :param X3: X3
    :type X3: np.ndarray
    :param X4: X4
    :type X4: np.ndarray
    """
    Lambda = _crossLines(X1, X2, X3, X4)

    # Check whether lambda is in bound
    mask1 = np.logical_and(0.0 < Lambda[:, 0], Lambda[:, 0] < 1.0)
    mask2 = np.logical_and(0.0 < Lambda[:, 1], Lambda[:, 1] < 1.0)
    mask = np.logical_and(mask1, mask2)
    return mask


def _crossLines(X1, X2, X3, X4):
    """Checks whether the segments X1--X2 and X3--X4 intersect.
    See https://en.wikipedia.org/wiki/Line-line_intersection for reference.
    Given four points X_k=(x_k,y_k), k in {1,2,3,4}, and the two lines defined by those,

        L1(lambda) = X1 + lambda (X2 - X1)
        L2(lambda) = X3 + lambda (X4 - X3)

    returns the lambda for which they intersect (and Inf if they are parallel).
    Technically, one needs to solve the 2x2 equation system

        x1 + lambda1 (x2-x1)  =  x3 + lambda2 (x4-x3)
        y1 + lambda1 (y2-y1)  =  y3 + lambda2 (y4-y3)

    for lambda1 and lambda2.

    Now X1 is a vector of all data points X1 and X2 is a vector of all
    consecutive data points X2
    n is the number of segments (not points in the plot!)

    :param X1: X1
    :type X1: np.ndarray
    :param X2: X2
    :type X2: np.ndarray
    :param X3: X3
    :type X3: np.ndarray
    :param X4: X4
    :type X4: np.ndarray
    """
    n = X2.shape[0]
    Lambda = np.zeros((n, 2))
    detA = -(X2[:, 0] - X1[:, 0]) * (X4[1] - X3[1]) + (X2[:, 1] - X1[:, 1]) * (
        X4[0] - X3[0]
    )

    id_detA = detA != 0

    if id_detA.any():
        rhs = -X1.reshape((-1, 2)) + X3.reshape(
            (-1, 2)
        )  # NOTE: watch out for broadcasting
        Rotate = np.array([[0, -1], [1, 0]])
        Lambda[id_detA, 0] = (rhs[id_detA, :] @ Rotate @ (X4 - X3).T) / detA[id_detA]
        Lambda[id_detA, 1] = (
            np.sum(
                -(X2[id_detA, :] - X1[id_detA, :]) @ Rotate * rhs[id_detA, :], axis=1
            )
            / detA[id_detA]
        )
    return Lambda
