def plot():
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
    import numpy as np

    x, y = np.meshgrid(np.linspace(0, 1), np.linspace(0, 1))
    z = x**2 - y**2

    fig = plt.figure()
    plt.pcolormesh(x, y, z, cmap=cm.viridis, shading="gouraud")
    # plt.colorbar()

    return fig


def test():
    from .helpers import assert_equality

    # test relative data path
    assert_equality(
        plot,
        __file__[:-3] + "_reference.tex",
        # tex_relative_path_to_data="data/files"
    )
