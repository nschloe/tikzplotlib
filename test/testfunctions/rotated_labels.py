# -*- coding: utf-8 -*-

desc = 'Rotated labels'
phash = 'a91fa2a3713dcc0b'


def plot():
    from matplotlib import pyplot as plt

    x = [1, 2, 3, 4]
    y = [1, 4, 9, 6]

    fig = plt.figure()

    plt.subplot(611)
    plt.plot(x, y, 'ro')
    plt.xticks(x, rotation='horizontal')

    plt.subplot(612)
    plt.plot(x, y, 'ro')
    plt.xticks(x, rotation='vertical')

    ax = plt.subplot(613)
    ax.plot(x, y, 'ro')
    plt.xticks(y, rotation=-25)

    ax = plt.subplot(614)
    ax.plot(x, y, 'ro')
    plt.yticks(y, rotation=-25)

    ax = plt.subplot(615)
    ax.plot(x, y, 'ro')

    for idx, label in enumerate(ax.get_xticklabels()):
        label.set_rotation(45 if idx % 2 == 0 else 0)

    ax = plt.subplot(616)
    ax.plot(x, y, 'ro')

    for idx, label in enumerate(ax.get_yticklabels()):
        label.set_rotation(90 if idx % 2 == 0 else 0)

    return fig
