# -*- coding: utf-8 -*-
#
import helpers


def plot():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(17, 6))
    ax.plot(np.array([1, 2, 3, 4, 5]), label='Test 1')
    ax.plot(np.array([5, 4, 3, 2, 1]), label='Test 2')
    ax.legend(ncol=2, loc='upper center')
    return fig


def test():
    phash = helpers.Phash(plot())
    assert phash.phash == 'a3267e19cad99998', phash.get_details()
    return


if __name__ == '__main__':
    helpers.compare_with_latex(plot())
