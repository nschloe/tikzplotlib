from matplotlib import pyplot as plt
import numpy as np


def getVisualLimits(fighandle, axhandle):
    """Returns the visual representation of the axis limits (Respecting
        possible log_scaling and projection into the image plane)
    
    Parameters
    ----------
    fighandle : obj
        handle to matplotlib figure object
    axhandle : obj
        hande to matplotlib axes object
    
    Returns
    -------
    np.array
        xLim as array of shape [2, ]
    np.array
        yLim as array of shape [2, ]        
    """
    # TODO: implement 3D functionality
    is3D = False

    xLim = np.array(axhandle.get_xlim())
    yLim = np.array(axhandle.get_ylim())
    if is3D:
        zLim = axhandle.get_ylim()

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

    return xLim, yLim


def replaceDataWithNaN(data, id_replace):
    """Replaces data at id_replace with NaNs
    
    Parameters
    ----------
    data : np.ndarray
        array of x and y data with shape [N, 2]
    id_replace : np.array
        array with indices to replace. Shape [K,]
    
    Returns
    -------
    np.ndarray
        data with replace values
    """
    if elements(id_replace) == 0:
        return data

    # TODO: add 3D compatibility
    is3D = False
    data = data.astype(np.float32)
    xData, yData = np.split(data, 2, 1)
    xData[id_replace] = np.NaN
    yData[id_replace] = np.NaN
    return np.concatenate([xData, yData], axis=1)


def removeData(data, id_remove):
    """remove data at id_remove
    
    Parameters
    ----------
    data : np.ndarray
        array of x and y data with shape [N, 2]
    id_remove : np.array
        array of x and y data with shape [N, 2]
    
    Returns
    -------
    np.ndarray
        new data array
    """
    if elements(id_remove) == 0:
        return data

    # TODO: add 3D compatibility
    is3D = False
    xData, yData = np.split(data, 2, 1)
    xData = np.delete(xData, id_remove, axis=0)
    yData = np.delete(yData, id_remove, axis=0)
    return np.concatenate([xData, yData], axis=1)


def removeNaNs(data):
    """Removes superflous NaNs in the data, i.e. those at the end/beginning of the data and consequtive ones.
    
    Parameters
    ----------
    data : np.ndarray
        array of x and y data with shape [N, 2]
    
    Returns
    -------
    np.ndarray
        new data array
    """
    # TODO: implement 3D functionality
    xData, yData = np.split(data, 2, 1)
    id_nan = np.any(np.isnan(data), axis=1)
    id_remove = np.argwhere(id_nan).reshape((-1,))
    id_remove = id_remove[
        np.concatenate(
            [np.array([True,]).reshape((-1,)), np.diff(id_remove, axis=0) == 1]
        )
    ]

    id_first = np.argwhere(np.logical_not(id_nan))[0]
    id_last = np.argwhere(np.logical_not(id_nan))[-1]

    if elements(id_first) == 0:
        id_remove = np.arange(len(xData))
    else:
        id_remove = np.concatenate(
            [np.arange(1, id_first - 1), id_remove, np.arange(id_last + 1, len(xData))]
        )
    xData = np.delete(xData, id_remove, axis=0)
    yData = np.delete(yData, id_remove, axis=0)
    return np.concatenate([xData, yData], axis=1)

    return data


def isInBox(data, xLim, yLim):
    """Returns a mask that indicates, whether a data point is within the limits
    
    Parameters
    ----------
    data : np.ndarray
        N x 2 array of data points. data[:, 0] are x coordinates, data[:, 1] are y coordinates
    xLim : np.array
        array with x limits. Shape [2, ]
    yLim : np.array
        array with y limits. Shape [2, ]
    """
    maskX = np.logical_and(data[:, 0] > xLim[0], data[:, 0] < xLim[1])
    maskY = np.logical_and(data[:, 1] > yLim[0], data[:, 1] < yLim[1])
    mask = maskX & maskY
    return mask


def getVisualData(axhandle, linehandle):
    """Returns the visual representation of the data (Respecting possible log_scaling and projection into the image plane)
    
    Parameters
    ----------
    axhandle : obj
        handle for matplotlib axis object
    linehandle : obj
        handle for matplotlib line2D object
    
    Returns
    -------
    np.ndarray
        xData with shape [N, 1]
    np.ndarray
        yData with shape [N, 1]
    """
    is3D = False

    xData = linehandle.get_xdata()
    yData = linehandle.get_ydata()
    if is3D:
        zData = linehandle.get_zdata()

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

    xData = np.reshape(xData, (-1,))
    yData = np.reshape(yData, (-1,))
    return xData, yData


def elements(array):
    """check if array has elements. 
    https://stackoverflow.com/questions/11295609/how-can-i-check-whether-the-numpy-array-is-empty-or-not
    """
    return array.ndim and array.size


def pruneOutsideBox(fighandle, axhandle, linehandle):
    """Some sections of the line may sit outside of the visible box. Cut those off.

    This method is not pure because it updates the linehandle object's data.
    
    Parameters
    ----------
    fighandle : obj
        matplotlib figure handle object
    axhandle : obj
        matplotlib axes handle object
    linehandle : obj
        matplotlib line2D handle object
    
    Returns
    -------
    """
    xData, yData = getVisualData(axhandle, linehandle)

    data = np.stack([xData, yData], axis=1)

    if elements(data) == 0:
        return

    hasLines = (linehandle.get_linestyle() is not None) and (
        linehandle.get_linewidth() > 0.0
    )

    xLim, yLim = getVisualLimits(fighandle, axhandle)

    tol = 1.0e-10
    relaxedXLim = xLim + np.array([-tol, tol])
    relaxedYLim = yLim + np.array([-tol, tol])

    dataIsInBox = isInBox(data, relaxedXLim, relaxedYLim)

    shouldPlot = dataIsInBox
    if hasLines:
        pass
        # TODO: adapt this snippet from matlab2tikz
        # segvis = segmentVisible(data, dataIsInBox, xLim, yLim)
        # shouldPlot = shouldPlot | [false; segvis] | [segvis; false];

    if not np.all(shouldPlot):
        id_remove = np.argwhere(np.logical_not(shouldPlot))

        # If there are consecutive data points to be removed, only replace
        # the first one by a NaN. Consecutive data points have
        # diff(id_remove)==1, so replace diff(id_remove)>1 by NaN and remove
        # the rest
        idx = np.diff(id_remove, axis=0) > 1
        idx = np.concatenate([np.array([True,]).reshape((-1, 1)), idx], axis=0)

        id_replace = id_remove[idx]
        id_remove = id_remove[np.logical_not(idx)]
    data = replaceDataWithNaN(data, id_replace)
    data = removeData(data, id_remove)
    data = removeNaNs(data)
    linehandle.set_xdata(data[:, 0])
    linehandle.set_ydata(data[:, 1])
