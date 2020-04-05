import matplotlib as mpl
import numpy
from matplotlib.backends.backend_pgf import (
    common_texification as mpl_common_texification,
)

from . import _color


def _common_texification(string):
    # Work around <https://github.com/matplotlib/matplotlib/issues/15493>
    return mpl_common_texification(string).replace("&", "\\&")


class Axes:
    def __init__(self, data, obj):  # noqa: C901
        """Returns the PGFPlots code for an axis environment.
        """
        self.content = []

        # Are we dealing with an axis that hosts a colorbar? Skip then, those are
        # treated implicitily by the associated axis.
        self.is_colorbar = _is_colorbar_heuristic(obj)
        if self.is_colorbar:
            return

        # instantiation
        self.nsubplots = 1
        self.subplot_index = 0
        self.is_subplot = False

        if isinstance(obj, mpl.axes.Subplot):
            self._subplot(obj, data)

        self.axis_options = []

        # check if axes need to be displayed at all
        if not obj.axison:
            self.axis_options.append("hide x axis")
            self.axis_options.append("hide y axis")

        # get plot title
        title = obj.get_title()
        data["current axis title"] = title
        if title:
            title = _common_texification(title)
            self.axis_options.append(f"title={{{title}}}")

        # get axes titles
        xlabel = obj.get_xlabel()
        if xlabel:
            xlabel = _common_texification(xlabel)
            self.axis_options.append(f"xlabel={{{xlabel}}}")
            xrotation = obj.xaxis.get_label().get_rotation()
            if xrotation != 0:
                self.axis_options.append(f"xlabel style={{rotate={xrotation - 90}}}")
        ylabel = obj.get_ylabel()
        if ylabel:
            ylabel = _common_texification(ylabel)
            self.axis_options.append(f"ylabel={{{ylabel}}}")
            yrotation = obj.yaxis.get_label().get_rotation()
            if yrotation != 90:
                self.axis_options.append(f"ylabel style={{rotate={yrotation - 90}}}")

        # Axes limits.
        ff = data["float format"]
        xlim = list(obj.get_xlim())
        xlim0, xlim1 = sorted(xlim)
        ylim = list(obj.get_ylim())
        ylim0, ylim1 = sorted(ylim)
        # Sort the limits so make sure that the smaller of the two is actually *min.
        self.axis_options.append(f"xmin={xlim0:{ff}}, xmax={xlim1:{ff}}")
        self.axis_options.append(f"ymin={ylim0:{ff}}, ymax={ylim1:{ff}}")
        # When the axis is inverted add additional option
        if xlim != sorted(xlim):
            self.axis_options.append("x dir=reverse")
        if ylim != sorted(ylim):
            self.axis_options.append("y dir=reverse")

        # axes scaling
        if obj.get_xscale() == "log":
            self.axis_options.append("xmode=log")
            self.axis_options.append(
                "log basis x={{{}}}".format(_try_f2i(obj.xaxis._scale.base))
            )
        if obj.get_yscale() == "log":
            self.axis_options.append("ymode=log")
            self.axis_options.append(
                "log basis y={{{}}}".format(_try_f2i(obj.yaxis._scale.base))
            )

        # Possible values for get_axisbelow():
        #   True (zorder = 0.5):   Ticks and gridlines are below all Artists.
        #   'line' (zorder = 1.5): Ticks and gridlines are above patches (e.g.
        #                          rectangles) but still below lines / markers.
        #   False (zorder = 2.5):  Ticks and gridlines are above patches and lines /
        #                          markers.
        if not obj.get_axisbelow():
            self.axis_options.append("axis on top")

        # aspect ratio, plot width/height
        aspect = obj.get_aspect()
        if aspect in ["auto", "normal"]:
            aspect_num = None  # just take the given width/height values
        elif aspect == "equal":
            aspect_num = 1.0
        else:
            aspect_num = float(aspect)

        self._set_axis_dimensions(data, aspect_num, xlim, ylim)

        # axis positions
        xaxis_pos = obj.get_xaxis().label_position
        if xaxis_pos == "top":
            # default: "bottom"
            self.axis_options.append("axis x line=top")

        yaxis_pos = obj.get_yaxis().label_position
        if yaxis_pos == "right":
            # default: "left"
            self.axis_options.append("axis y line=right")

        self._ticks(data, obj)

        self._grid(obj, data)

        # axis line styles
        # Assume that the bottom edge color is the color of the entire box.
        axcol = obj.spines["bottom"].get_edgecolor()
        data, col, _ = _color.mpl_color2xcolor(data, axcol)
        if col != "black":
            self.axis_options.append(f"axis line style={{{col}}}")

        # background color
        bgcolor = obj.get_facecolor()

        data, col, _ = _color.mpl_color2xcolor(data, bgcolor)
        if col != "white":
            self.axis_options.append(f"axis background/.style={{fill={col}}}")

        # find color bar
        colorbar = _find_associated_colorbar(obj)
        if colorbar:
            self._colorbar(colorbar, data)

        if self.is_subplot:
            self.content.append("\n\\nextgroupplot")
        else:
            self.content.append(data["flavor"].start("axis"))

    def get_begin_code(self):
        content = self.content
        if self.axis_options:
            # Put axis_options in a deterministic order to avoid diff churn.
            self.axis_options.sort()
            content.append("[\n" + ",\n".join(self.axis_options) + "\n]\n")
        return content

    def get_end_code(self, data):
        if not self.is_subplot:
            return data["flavor"].end("axis") + "\n\n"
        elif self.is_subplot and self.nsubplots == self.subplot_index:
            data["is_in_groupplot_env"] = False
            return data["flavor"].end("groupplot") + "\n\n"

        return ""

    def _set_axis_dimensions(self, data, aspect_num, xlim, ylim):
        if data["axis width"] and data["axis height"]:
            # width and height overwrite aspect ratio
            self.axis_options.append("width=" + data["axis width"])
            self.axis_options.append("height=" + data["axis height"])
        elif data["axis width"]:
            # only data["axis width"] given. calculate height by the aspect ratio
            self.axis_options.append("width=" + data["axis width"])
            if aspect_num:
                alpha = aspect_num * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
                if alpha == 1.0:
                    data["axis height"] = data["axis width"]
                else:
                    # Concatenate the literals, as data["axis width"] could as well
                    # be a LaTeX length variable such as \figurewidth.
                    data["axis height"] = str(alpha) + "*" + data["axis width"]
                self.axis_options.append("height=" + data["axis height"])
        elif data["axis height"]:
            # only data["axis height"] given. calculate width by the aspect ratio
            self.axis_options.append("height=" + data["axis height"])
            if aspect_num:
                alpha = aspect_num * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
                if alpha == 1.0:
                    data["axis width"] = data["axis height"]
                else:
                    # Concatenate the literals, as data["axis height"] could as
                    # well be a LaTeX length variable such as \figureheight.
                    data["axis width"] = str(1.0 / alpha) + "*" + data["axis height"]
                self.axis_options.append("width=" + data["axis width"])
        else:
            # TODO keep an eye on https://tex.stackexchange.com/q/480058/13262
            pass

    def _ticks(self, data, obj):
        # get ticks
        self.axis_options.extend(
            _get_ticks(data, "x", obj.get_xticks(), obj.get_xticklabels())
        )
        self.axis_options.extend(
            _get_ticks(data, "y", obj.get_yticks(), obj.get_yticklabels())
        )
        self.axis_options.extend(
            _get_ticks(
                data,
                "minor x",
                obj.get_xticks(minor=True),
                obj.get_xticklabels(minor=True),
            )
        )
        self.axis_options.extend(
            _get_ticks(
                data,
                "minor y",
                obj.get_yticks(minor=True),
                obj.get_yticklabels(minor=True),
            )
        )

        try:
            l0 = obj.get_xticklines()[0]
        except IndexError:
            pass
        else:
            c0 = l0.get_color()
            data, xtickcolor, _ = _color.mpl_color2xcolor(data, c0)
            self.axis_options.append(f"xtick style={{color={xtickcolor}}}")

        try:
            l0 = obj.get_yticklines()[0]
        except IndexError:
            pass
        else:
            c0 = l0.get_color()
            data, ytickcolor, _ = _color.mpl_color2xcolor(data, c0)
            self.axis_options.append(f"ytick style={{color={ytickcolor}}}")

        # Find tick direction
        # For new matplotlib versions, we could replace the direction getter by
        # `get_ticks_direction()`, see
        # <https://github.com/matplotlib/matplotlib/pull/5290>.  Unfortunately, _tickdir
        # doesn't seem to be quite accurate. See
        # <https://github.com/matplotlib/matplotlib/issues/5311>.  For now, just take
        # the first tick direction of each of the axes.
        x_tick_dirs = [tick._tickdir for tick in obj.xaxis.get_major_ticks()]
        y_tick_dirs = [tick._tickdir for tick in obj.yaxis.get_major_ticks()]
        if x_tick_dirs or y_tick_dirs:
            if x_tick_dirs and y_tick_dirs:
                direction = x_tick_dirs[0] if x_tick_dirs[0] == y_tick_dirs[0] else None
            elif x_tick_dirs:
                direction = x_tick_dirs[0]
            else:
                # y_tick_dirs must be present
                direction = y_tick_dirs[0]

            if direction:
                if direction == "in":
                    # 'tick align=inside' is the PGFPlots default
                    pass
                elif direction == "out":
                    self.axis_options.append("tick align=outside")
                else:
                    assert direction == "inout"
                    self.axis_options.append("tick align=center")

        # Set each rotation for every label
        x_tick_rotation_and_horizontal_alignment = self._get_label_rotation_and_horizontal_alignment(
            obj, data, "x"
        )
        if x_tick_rotation_and_horizontal_alignment:
            self.axis_options.append(x_tick_rotation_and_horizontal_alignment)

        y_tick_rotation_and_horizontal_alignment = self._get_label_rotation_and_horizontal_alignment(
            obj, data, "y"
        )
        if y_tick_rotation_and_horizontal_alignment:
            self.axis_options.append(y_tick_rotation_and_horizontal_alignment)

        # Set tick position
        x_tick_position_string, x_tick_position = _get_tick_position(obj, "x")
        y_tick_position_string, y_tick_position = _get_tick_position(obj, "y")

        if x_tick_position == y_tick_position and x_tick_position is not None:
            self.axis_options.append(f"tick pos={x_tick_position}")
        else:
            self.axis_options.append(x_tick_position_string)
            self.axis_options.append(y_tick_position_string)

    def _grid(self, obj, data):
        # Don't use get_{x,y}gridlines for gridlines; see discussion on
        # <http://sourceforge.net/p/matplotlib/mailman/message/25169234/> Coordinate of
        # the lines are entirely meaningless, but styles (colors,...) are respected.
        if obj.xaxis._gridOnMajor:
            self.axis_options.append("xmajorgrids")
        if obj.xaxis._gridOnMinor:
            self.axis_options.append("xminorgrids")

        xlines = obj.get_xgridlines()
        if xlines:
            xgridcolor = xlines[0].get_color()
            data, col, _ = _color.mpl_color2xcolor(data, xgridcolor)
            if col != "black":
                self.axis_options.append(f"x grid style={{{col}}}")

        if obj.yaxis._gridOnMajor:
            self.axis_options.append("ymajorgrids")
        if obj.yaxis._gridOnMinor:
            self.axis_options.append("yminorgrids")

        ylines = obj.get_ygridlines()
        if ylines:
            ygridcolor = ylines[0].get_color()
            data, col, _ = _color.mpl_color2xcolor(data, ygridcolor)
            if col != "black":
                self.axis_options.append(f"y grid style={{{col}}}")

    def _colorbar(self, colorbar, data):
        colorbar_styles = []

        orientation = colorbar.orientation
        limits = colorbar.mappable.get_clim()
        if orientation == "horizontal":
            self.axis_options.append("colorbar horizontal")

            colorbar_ticks = colorbar.ax.get_xticks()
            colorbar_ticks_minor = colorbar.ax.get_xticks(minor=True)
            axis_limits = colorbar.ax.get_xlim()

            # In matplotlib, the colorbar color limits are determined by get_clim(), and
            # the tick positions are as usual with respect to {x,y}lim. In PGFPlots,
            # however, they are mixed together.  Hence, scale the tick positions just
            # like {x,y}lim are scaled to clim.
            colorbar_ticks = (colorbar_ticks - axis_limits[0]) / (
                axis_limits[1] - axis_limits[0]
            ) * (limits[1] - limits[0]) + limits[0]
            colorbar_ticks_minor = (colorbar_ticks_minor - axis_limits[0]) / (
                axis_limits[1] - axis_limits[0]
            ) * (limits[1] - limits[0]) + limits[0]
            # Getting the labels via get_* might not actually be suitable:
            # they might not reflect the current state.
            colorbar_ticklabels = colorbar.ax.get_xticklabels()
            colorbar_ticklabels_minor = colorbar.ax.get_xticklabels(minor=True)

            colorbar_styles.extend(
                _get_ticks(data, "x", colorbar_ticks, colorbar_ticklabels)
            )
            colorbar_styles.extend(
                _get_ticks(
                    data, "minor x", colorbar_ticks_minor, colorbar_ticklabels_minor
                )
            )

        else:
            assert orientation == "vertical"

            self.axis_options.append("colorbar")
            colorbar_ticks = colorbar.ax.get_yticks()
            colorbar_ticks_minor = colorbar.ax.get_yticks(minor=True)
            axis_limits = colorbar.ax.get_ylim()

            # In matplotlib, the colorbar color limits are determined by get_clim(), and
            # the tick positions are as usual with respect to {x,y}lim. In PGFPlots,
            # however, they are mixed together.  Hence, scale the tick positions just
            # like {x,y}lim are scaled to clim.
            colorbar_ticks = (colorbar_ticks - axis_limits[0]) / (
                axis_limits[1] - axis_limits[0]
            ) * (limits[1] - limits[0]) + limits[0]
            colorbar_ticks_minor = (colorbar_ticks_minor - axis_limits[0]) / (
                axis_limits[1] - axis_limits[0]
            ) * (limits[1] - limits[0]) + limits[0]

            # Getting the labels via get_* might not actually be suitable:
            # they might not reflect the current state.
            colorbar_ticklabels = colorbar.ax.get_yticklabels()
            colorbar_ylabel = colorbar.ax.get_ylabel()
            colorbar_ticklabels_minor = colorbar.ax.get_yticklabels(minor=True)
            colorbar_styles.extend(
                _get_ticks(data, "y", colorbar_ticks, colorbar_ticklabels)
            )
            colorbar_styles.extend(
                _get_ticks(
                    data, "minor y", colorbar_ticks_minor, colorbar_ticklabels_minor
                )
            )
            colorbar_styles.append("ylabel={" + colorbar_ylabel + "}")

        mycolormap, is_custom_cmap = _mpl_cmap2pgf_cmap(
            colorbar.mappable.get_cmap(), data
        )
        if is_custom_cmap:
            self.axis_options.append("colormap=" + mycolormap)
        else:
            self.axis_options.append("colormap/" + mycolormap)

        ff = data["float format"]
        self.axis_options.append(f"point meta min={limits[0]:{ff}}")
        self.axis_options.append(f"point meta max={limits[1]:{ff}}")

        if colorbar_styles:
            self.axis_options.append(
                "colorbar style={{{}}}".format(",".join(colorbar_styles))
            )

    def _subplot(self, obj, data):
        # https://github.com/matplotlib/matplotlib/issues/7225#issuecomment-252173667
        geom = obj.get_subplotspec().get_topmost_subplotspec().get_geometry()

        self.nsubplots = geom[0] * geom[1]
        if self.nsubplots > 1:
            # Is this an axis-colorbar pair? No need for groupplot then.
            is_groupplot = self.nsubplots != 2 or not _find_associated_colorbar(obj)

            if is_groupplot:
                self.is_subplot = True
                # subplotspec geometry positioning is 0-based
                self.subplot_index = geom[2] + 1
                if "is_in_groupplot_env" not in data or not data["is_in_groupplot_env"]:
                    group_style = [f"group size={geom[1]} by {geom[0]}"]
                    group_style.extend(data["extra groupstyle options [base]"])
                    options = ["group style={{{}}}".format(", ".join(group_style))]
                    self.content.append(
                        data["flavor"].start("groupplot") + f"[{', '.join(options)}]"
                    )
                    data["is_in_groupplot_env"] = True
                    data["pgfplots libs"].add("groupplots")

    def _get_label_rotation_and_horizontal_alignment(self, obj, data, x_or_y):
        tick_label_text_width = None
        tick_label_text_width_identifier = f"{x_or_y} tick label text width"
        if tick_label_text_width_identifier in self.axis_options:
            self.axis_options.remove(tick_label_text_width_identifier)

        label_style = ""

        major_tick_labels = (
            obj.xaxis.get_majorticklabels()
            if x_or_y == "x"
            else obj.yaxis.get_majorticklabels()
        )

        if not major_tick_labels:
            return None

        tick_labels_rotation = [label.get_rotation() for label in major_tick_labels]
        tick_labels_rotation_same_value = len(set(tick_labels_rotation)) == 1

        tick_labels_horizontal_alignment = [
            label.get_horizontalalignment() for label in major_tick_labels
        ]
        tick_labels_horizontal_alignment_same_value = (
            len(set(tick_labels_horizontal_alignment)) == 1
        )

        if (
            tick_labels_rotation_same_value
            and tick_labels_horizontal_alignment_same_value
        ):
            values = []

            if any(tick_labels_rotation) != 0:
                values.append(f"rotate={tick_labels_rotation[0]}")

            # Horizontal alignment will be ignored if no 'x/y tick label text width' has
            # been passed in the 'extra' parameter
            if tick_label_text_width:
                values.append(f"align={tick_labels_horizontal_alignment[0]}")
                values.append(f"text width={tick_label_text_width}")

            if values:
                label_style = "{}ticklabel style = {{{}}}".format(
                    x_or_y, ",".join(values)
                )
        else:
            values = []

            if tick_labels_rotation_same_value:
                values.append("rotate={tick_labels_rotation[0]}")
            else:
                values.append(
                    "rotate={{{},0}}[\\ticknum]".format(
                        ",".join(str(x) for x in tick_labels_rotation)
                    )
                )

            # Ignore horizontal alignment if no '{x,y} tick label text width' has been
            # passed in the 'extra' parameter
            if tick_label_text_width:
                if tick_labels_horizontal_alignment_same_value:
                    values.append(f"align={tick_labels_horizontal_alignment[0]}")
                    values.append(f"text width={tick_label_text_width}")
                else:
                    for idx, x in enumerate(tick_labels_horizontal_alignment):
                        label_style += f"{x_or_y}_tick_label_ha_{idx}/.initial = {x}"

                    values.append(
                        f"align=\\pgfkeysvalueof{{/pgfplots/{x_or_y}_tick_label_ha_\\ticknum}}"
                    )
                    values.append(f"text width={tick_label_text_width}")

            label_style = (
                "every {} tick label/.style = {{\n"
                "{}\n"
                "}}".format(x_or_y, ",\n".join(values))
            )

        return label_style


def _get_tick_position(obj, axes_obj):
    major_ticks = obj.xaxis.majorTicks if axes_obj == "x" else obj.yaxis.majorTicks

    major_ticks_bottom = [tick.tick1line.get_visible() for tick in major_ticks]
    major_ticks_top = [tick.tick2line.get_visible() for tick in major_ticks]

    major_ticks_bottom_show_all = False
    if len(set(major_ticks_bottom)) == 1 and major_ticks_bottom[0] is True:
        major_ticks_bottom_show_all = True

    major_ticks_top_show_all = False
    if len(set(major_ticks_top)) == 1 and major_ticks_top[0] is True:
        major_ticks_top_show_all = True

    major_ticks_position = None
    if not major_ticks_bottom_show_all and not major_ticks_top_show_all:
        position_string = f"{axes_obj}majorticks=false"
    elif major_ticks_bottom_show_all and major_ticks_top_show_all:
        major_ticks_position = "both"
    elif major_ticks_bottom_show_all:
        major_ticks_position = "left"
    elif major_ticks_top_show_all:
        major_ticks_position = "right"

    if major_ticks_position:
        position_string = f"{axes_obj}tick pos={major_ticks_position}"

    return position_string, major_ticks_position


def _get_ticks(data, xy, ticks, ticklabels):
    """Gets a {'x','y'}, a number of ticks and ticks labels, and returns the
    necessary axis options for the given configuration.
    """
    axis_options = []
    pgfplots_ticks = []
    pgfplots_ticklabels = []
    is_label_required = False
    for tick, ticklabel in zip(ticks, ticklabels):
        # store the label anyway
        label = ticklabel.get_text()
        if "," in label:
            label = "{" + label + "}"
        if ticklabel.get_visible():
            label = _common_texification(label)
            pgfplots_ticklabels.append(label)
        else:
            is_label_required = True
        # Check if the label is necessary. If one of the labels is, then all of them
        # must appear in the TikZ plot.
        if label:
            try:
                label_float = float(label.replace("\N{MINUS SIGN}", "-"))
                is_label_required = is_label_required or (label and label_float != tick)
            except ValueError:
                is_label_required = True
    # note: ticks may be present even if labels are not, keep them for grid lines
    for tick in ticks:
        pgfplots_ticks.append(tick)

    # if the labels are all missing, then we need to output an empty set of labels
    if len(ticklabels) == 0 and len(ticks) != 0:
        axis_options.append(f"{xy}ticklabels={{}}")
        # remove the multiplier too
        axis_options.append(f"scaled {xy} ticks=" + r"manual:{}{\pgfmathparse{#1}}")

    # Leave the ticks to PGFPlots if not in STRICT mode and if there are no explicit
    # labels.
    if data["strict"] or is_label_required:
        if pgfplots_ticks:
            ff = data["float format"]
            axis_options.append(
                "{}tick={{{}}}".format(
                    xy, ",".join([f"{el:{ff}}" for el in pgfplots_ticks])
                )
            )
        else:
            val = "{}" if "minor" in xy else "\\empty"
            axis_options.append(f"{xy}tick={val}")

        if is_label_required:
            axis_options.append(
                "{}ticklabels={{{}}}".format(xy, ",".join(pgfplots_ticklabels))
            )
    return axis_options


def _is_colorbar_heuristic(obj):
    """Find out if the object is in fact a color bar.
    """
    # TODO come up with something more accurate here
    # Might help:
    # TODO Are the colorbars exactly the l.collections.PolyCollection's?
    try:
        aspect = float(obj.get_aspect())
    except ValueError:
        # e.g., aspect == 'equal'
        return False

    # Assume that something is a colorbar if and only if the ratio is above 5.0
    # and there are no ticks on the corresponding axis. This isn't always true,
    # though: The ratio of a color can be freely adjusted by the aspect
    # keyword, e.g.,
    #
    #    plt.colorbar(im, aspect=5)
    #
    limit_ratio = 5.0

    return (aspect >= limit_ratio and len(obj.get_xticks()) == 0) or (
        aspect <= 1.0 / limit_ratio and len(obj.get_yticks()) == 0
    )


def _mpl_cmap2pgf_cmap(cmap, data):
    """Converts a color map as given in matplotlib to a color map as
    represented in PGFPlots.
    """
    if isinstance(cmap, mpl.colors.LinearSegmentedColormap):
        return _handle_linear_segmented_color_map(cmap, data)

    assert isinstance(
        cmap, mpl.colors.ListedColormap
    ), "Only LinearSegmentedColormap and ListedColormap are supported"
    return _handle_listed_color_map(cmap, data)


def _handle_linear_segmented_color_map(cmap, data):
    assert isinstance(cmap, mpl.colors.LinearSegmentedColormap)

    if cmap.is_gray():
        is_custom_colormap = False
        return ("blackwhite", is_custom_colormap)

    # For an explanation of what _segmentdata contains, see
    # http://matplotlib.org/mpl_examples/pylab_examples/custom_cmap.py
    # A key sentence:
    # If there are discontinuities, then it is a little more complicated.  Label the 3
    # elements in each row in the cdict entry for a given color as (x, y0, y1).  Then
    # for values of x between x[i] and x[i+1] the color value is interpolated between
    # y1[i] and y0[i+1].
    segdata = cmap._segmentdata
    red = segdata["red"]
    green = segdata["green"]
    blue = segdata["blue"]

    # Loop over the data, stop at each spot where the linear interpolations is
    # interrupted, and set a color mark there.
    #
    # Set initial color.
    k_red = 0
    k_green = 0
    k_blue = 0
    x = 0.0
    colors = []
    X = []
    while True:
        # find next x
        x = min(red[k_red][0], green[k_green][0], blue[k_blue][0])

        if red[k_red][0] == x:
            red_comp = red[k_red][1]
            k_red += 1
        else:
            red_comp = _linear_interpolation(
                x,
                (red[k_red - 1][0], red[k_red][0]),
                (red[k_red - 1][2], red[k_red][1]),
            )

        if green[k_green][0] == x:
            green_comp = green[k_green][1]
            k_green += 1
        else:
            green_comp = _linear_interpolation(
                x,
                (green[k_green - 1][0], green[k_green][0]),
                (green[k_green - 1][2], green[k_green][1]),
            )

        if blue[k_blue][0] == x:
            blue_comp = blue[k_blue][1]
            k_blue += 1
        else:
            blue_comp = _linear_interpolation(
                x,
                (blue[k_blue - 1][0], blue[k_blue][0]),
                (blue[k_blue - 1][2], blue[k_blue][1]),
            )

        X.append(x)
        colors.append((red_comp, green_comp, blue_comp))

        if x >= 1.0:
            break

    # The PGFPlots color map has an actual physical scale, like (0cm,10cm), and the
    # points where the colors change is also given in those units. As of now
    # (2010-05-06) it is crucial for PGFPlots that the difference between two successive
    # points is an integer multiple of a given unity (parameter to the colormap; e.g.,
    # 1cm).  At the same time, TeX suffers from significant round-off errors, so make
    # sure that this unit is not too small such that the round- off errors don't play
    # much of a role. A unit of 1pt, e.g., does most often not work.
    unit = "pt"

    # Scale to integer (too high integers will firstly be slow and secondly may produce
    # dimension errors or memory errors in latex)
    # 0-1000 is the internal granularity of PGFplots.
    # 16300 was the maximum value for pgfplots<=1.13
    X = _scale_to_int(numpy.array(X), 1000)

    color_changes = []
    ff = data["float format"]
    for k, x in enumerate(X):
        color_changes.append(
            f"rgb({x}{unit})="
            f"({colors[k][0]:{ff}},{colors[k][1]:{ff}},{colors[k][2]:{ff}})"
        )

    colormap_string = "{{mymap}}{{[1{}]\n  {}\n}}".format(
        unit, ";\n  ".join(color_changes)
    )
    is_custom_colormap = True
    return (colormap_string, is_custom_colormap)


def _handle_listed_color_map(cmap, data):
    assert isinstance(cmap, mpl.colors.ListedColormap)

    # check for predefined colormaps in both matplotlib and pgfplots
    from matplotlib import pyplot as plt

    cm_translate = {
        # All the rest are LinearSegmentedColorMaps. :/
        # 'autumn': 'autumn',
        # 'cool': 'cool',
        # 'copper': 'copper',
        # 'gray': 'blackwhite',
        # 'hot': 'hot2',
        # 'hsv': 'hsv',
        # 'jet': 'jet',
        # 'spring': 'spring',
        # 'summer': 'summer',
        "viridis": "viridis",
        # 'winter': 'winter',
    }
    for mpl_cm, pgf_cm in cm_translate.items():
        if cmap.colors == plt.get_cmap(mpl_cm).colors:
            is_custom_colormap = False
            return (pgf_cm, is_custom_colormap)

    unit = "pt"
    ff = data["float format"]
    if cmap.N is None or cmap.N == len(cmap.colors):
        colors = [
            f"rgb({k}{unit})=({rgb[0]:{ff}},{rgb[1]:{ff}},{rgb[2]:{ff}})"
            for k, rgb in enumerate(cmap.colors)
        ]
    else:
        reps = int(float(cmap.N) / len(cmap.colors) - 0.5) + 1
        repeated_cols = reps * cmap.colors
        colors = [
            "rgb({k}{unit})=({rgb[0]:{ff}},{rgb[1]:{ff}},{rgb[2]:{ff}})"
            for k, rgb in enumerate(repeated_cols[: cmap.N])
        ]
    colormap_string = "{{mymap}}{{[1{}]\n {}\n}}".format(unit, ";\n  ".join(colors))
    is_custom_colormap = True
    return (colormap_string, is_custom_colormap)


def _scale_to_int(X, max_val):
    """Scales the array X such that it contains only integers.
    """
    # if max_val is None:
    #     X = X / _gcd_array(X)
    X = X / max(1 / max_val, _gcd_array(X))
    return [int(entry) for entry in X]


def _gcd_array(X):
    """
    Return the largest real value h such that all elements in x are integer
    multiples of h.
    """
    greatest_common_divisor = 0.0
    for x in X:
        greatest_common_divisor = _gcd(greatest_common_divisor, x)

    return greatest_common_divisor


def _gcd(a, b):
    """Euclidean algorithm for calculating the GCD of two numbers a, b.
    This algoritm also works for real numbers:
    Find the greatest number h such that a and b are integer multiples of h.
    """
    # Keep the tolerance somewhat significantly above machine precision as otherwise
    # round-off errors will be accounted for, returning 1.0e-10 instead of 1.0 for the
    # values
    #   [1.0, 2.0000000001, 3.0, 4.0].
    while a > 1.0e-5:
        a, b = b % a, a
    return b


def _linear_interpolation(x, X, Y):
    """Given two data points [X,Y], linearly interpolate those at x.
    """
    return (Y[1] * (x - X[0]) + Y[0] * (X[1] - x)) / (X[1] - X[0])


def _find_associated_colorbar(obj):
    """A rather poor way of telling whether an axis has a colorbar associated: Check the
    next axis environment, and see if it is de facto a color bar; if yes, return the
    color bar object.
    """
    for child in obj.get_children():
        try:
            cbar = child.colorbar
        except AttributeError:
            continue
        if cbar is not None:  # really necessary?
            # if fetch was successful, cbar contains
            # (reference to colorbar, reference to axis containing colorbar)
            return cbar
    return None


def _try_f2i(x):
    """If possible, convert float to int without rounding.
    Used for log base: if not used, base for log scale can be "10.0" (and then
    printed as such  by pgfplots).
    """
    return int(x) if int(x) == x else x
