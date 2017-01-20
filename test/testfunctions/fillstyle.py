# -*- coding: utf-8 -*-
#
desc = 'fillstyle "none"'
# phash = '015752594e6d3ebc'
phash = 'a103fa59ee613e94'


def plot():
    from matplotlib import pyplot as plt
    import numpy as np
    fig = plt.figure()

    N = 10
    t = np.linspace(0, 1, N)
    x = np.arange(N)
    plt.plot(t, x, '-o', fillstyle='none')
    plt.tight_layout()
    return fig
