import matplotlib.pyplot as plt
import numpy as np


def create_heatmap(data, x_labels, y_labels, title):
    fig, ax = plt.subplots()
    ax.imshow(data, cmap="copper")
    ax.set_xticks(np.arange(len(x_labels)), labels=x_labels)
    ax.set_yticks(np.arange(len(y_labels)), labels=y_labels)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    data = np.array(data)
    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            ax.text(j, i, round(data[i, j], 2), ha="center", va="center", color="w", fontsize="large")

    ax.set_title(title)
    fig.tight_layout()
    plt.show()


# TODO: fix xticks
def create_scatter_plot(data, x_label, y_label, title, legend, loc, x_scale='linear', x_ticks="", bbox="", x_rotation=""):
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if x_scale == 'log':
        plt.xscale('log')
    scatters = list()

    if x_scale == 'symlog':
        plt.xscale('symlog')
    scatters = list()

    if x_ticks != "":
        if x_rotation == 45:
            plt.xticks(x_ticks, rotation=45)
        else:
            plt.xticks(x_ticks)


    for x_list, y_list in data:
        scatters.append(plt.scatter(x_list, y_list, marker="x"))

    plt.grid()

    if bbox == "":
        plt.legend(scatters, legend, scatterpoints=1, loc=loc, ncol=1, fontsize=8)
    else:
        plt.legend(scatters, legend, scatterpoints=1, loc=loc, ncol=1, fontsize=8, bbox_to_anchor=bbox)

    plt.show()


def create_bar_plot(x, y, x_label, y_label, title):
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.bar(x, y, width=200, tick_label=x)
    plt.show()

