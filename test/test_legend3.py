import matplotlib.pyplot as plt


def plot():
    # mpl.style.use("seaborn-colorblind")
    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot(111)
    ax.fill_between([1, 2], [2, 2], [3, 3], color="red", alpha=0.2, label="roh")
    ax.fill_between([1, 2], [4, 4], [5, 5], color="blue", alpha=0.2, label="kal")
    ax.plot([1, 2], [2, 5], "k", label="ref")
    ax.grid()
    plt.legend()
    return fig


if __name__ == "__main__":
    import helpers

    helpers.compare_mpl_latex(plot)
    # helpers.print_tree(plot())
