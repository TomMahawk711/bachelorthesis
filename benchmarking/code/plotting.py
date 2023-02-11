import matplotlib.pyplot as plt
import numpy as np

from data_processing import process, get_config


def create_stream_plots(parameters):
    benchmark_name = "stream"
    folder_name = "i7-3770"
    grouping_metric = parameters.thread_counts
    energies_plot_data, times_plot_data, copy_plot_data, scale_plot_data, add_plot_data, triad_plot_data = \
        process(parameters, benchmark_name, folder_name, grouping_metric, "foo")

    x = grouping_metric
    mean_power = [e / t for e, t in zip(energies_plot_data, times_plot_data)]



    _create_scatter_plot()


def create_monte_carlo_plots(parameters):
    folder_name = parameters.limit_type + "_" + parameters.start_time
    folder_name = "i7-3770"
    grouping_metric = parameters.limits
    energies_plot_data, times_plot_data = process(parameters, "monte-carlo", folder_name, grouping_metric, "AVX")

    x = parameters.limits
    mean_power = [e / t for e, t in zip(energies_plot_data, times_plot_data)]

    grid_x_size = 2
    grid_y_size = 2

    _create_scatter_plot(grid_x_size, grid_y_size, 1, "frequency/time", "frequency", "time [s]", x, times_plot_data)
    # _create_scatter_plot(grid_x_size, grid_y_size, 2, "frequency/energy", "frequency", "energy [J]", x, energies_plot_data)
    # _create_scatter_plot(grid_x_size, grid_y_size, 3, "frequency/power", "frequency", "power [W]", x, mean_power)
    # _create_scatter_plot(grid_x_size, grid_y_size, 4, "execution time/energy", "time [s]", "energy [J]", times_plot_data, energies_plot_data)

    plt.tight_layout()
    plt.grid()
    plt.savefig("test_plots.png")
    plt.show()


def create_vectorization_heatmaps(parameters):
    benchmark_name = "vector-operations"
    folder_name = "R7-5800X"
    grouping_metric = parameters.limits
    x_labels = parameters.limits
    y_labels = parameters.instruction_sets
    y_labels.remove("SSE2")

    SSE_energies, SSE_times = process(parameters, benchmark_name, folder_name, grouping_metric, "SSE")
    # SSE2_energies, SSE2_times = process(parameters, benchmark_name, folder_name, grouping_metric, "SSE2")
    AVX_energies, AVX_times = process(parameters, benchmark_name, folder_name, grouping_metric, "AVX")

    energies_data = [SSE_energies, AVX_energies]
    times_data = [SSE_times, AVX_times]


    # _create_heatmap(energies_data, x_labels, y_labels, "adolf")
    _create_heatmap(times_data, x_labels, y_labels, "eva")


def create_vectorization_scatter_plots(parameters):
    benchmark_name = "vector-operations"
    folder_name = "i7-3770"
    grouping_metric = parameters.limits

    SSE_energies, SSE_times = process(parameters, benchmark_name, folder_name, grouping_metric, "SSE")
    # energies, times = process(parameters, benchmark_name, folder_name, grouping_metric, "")
    AVX_energies, AVX_times = process(parameters, benchmark_name, folder_name, grouping_metric, "AVX")

    energies_data = [(grouping_metric, SSE_energies), (grouping_metric, AVX_energies)]
    times_data = [(grouping_metric, SSE_times), (grouping_metric, AVX_times)]

    relative_energies = [1-(e1/e2) for e1,e2 in zip(SSE_energies, AVX_energies)]

    _create_scatter_plot(energies_data, "frequencies [MHz]", "consumed energy [Joules]", "comparison of instruction sets")
    _create_scatter_plot(times_data, "frequencies [MHz]", "time [s]", "comparison of instruction sets")
    _create_bar_plot(grouping_metric, relative_energies, "frequencies [MHz]", "relative energy difference", "relative energy difference SSE/AVX")


def _create_heatmap(data, x_labels, y_labels, title):
    fig, ax = plt.subplots()
    image = ax.imshow(data, cmap="copper")
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


def _create_scatter_plot(data, x_label, y_label, title):
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    for x_list, y_list in data:
        plt.scatter(x_list, y_list, marker="x")

    plt.show()


def _create_bar_plot(x, y, x_label, y_label, title):
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.bar(x,y, width=200, tick_label=x)
    plt.show()


if __name__ == "__main__":

    create_vectorization_scatter_plots(get_config("i7-3770"))

    # create_monte_carlo_plots(get_config("i7-3770"))
