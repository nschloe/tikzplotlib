"""Custom collection test

This tests plots a subclass of Collection, which contains enough information
as a base class to be rendered.
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from helpers import assert_equality


class TransformedEllipseCollection(matplotlib.collections.Collection):
    """
    A gutted version of matplotlib.collections.EllipseCollection that lets us
    pass the transformation matrix directly.

    This is useful for plotting cholesky factors of covariance matrices.
    """

    def __init__(self, matrices, **kwargs):
        super().__init__(**kwargs)
        self.set_transform(matplotlib.transforms.IdentityTransform())
        self._transforms = np.zeros(matrices.shape[:-2] + (3, 3))
        self._transforms[..., :2, :2] = matrices
        self._transforms[..., 2, 2] = 1
        self._paths = [matplotlib.path.Path.unit_circle()]

    def _set_transforms(self):
        """Calculate transforms immediately before drawing."""
        m = self.axes.transData.get_affine().get_matrix().copy()
        m[:2, 2:] = 0
        self.set_transform(matplotlib.transforms.Affine2D(m))

    @matplotlib.artist.allow_rasterization
    def draw(self, renderer):
        self._set_transforms()
        super().draw(renderer)


def rot(theta):
    """ Get a stack of rotation matrices """
    return np.stack(
        [
            np.stack([np.cos(theta), -np.sin(theta)], axis=-1),
            np.stack([np.sin(theta), np.cos(theta)], axis=-1),
        ],
        axis=-2,
    )


def plot():
    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)

    theta = np.linspace(0, 2 * np.pi, 12, endpoint=False)
    mats = rot(theta) @ np.diag([0.1, 0.2])
    x = np.cos(theta)
    y = np.sin(theta)

    c = TransformedEllipseCollection(
        mats,
        offsets=np.stack((x, y), axis=-1),
        edgecolor="tab:red",
        alpha=0.5,
        facecolor="tab:blue",
        transOffset=ax.transData,
    )
    ax.add_collection(c)
    ax.set(xlim=[-1.5, 1.5], ylim=[-1.5, 1.5])

    return fig


def test():
    assert_equality(plot, "test_custom_collection_reference.tex")
    return
