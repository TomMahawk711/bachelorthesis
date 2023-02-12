from data_processing import process, get_config
from plotting_aux import create_bar_plot, create_heatmap, create_scatter_plot


def create_stream_plots(parameters):
    benchmark_name = "stream"
    folder_name = "i7-3770"
    grouping_metric = parameters.thread_counts
    energies_plot_data, times_plot_data, copy_plot_data, scale_plot_data, add_plot_data, triad_plot_data = \
        process(parameters, benchmark_name, folder_name, grouping_metric, "foo")

    x = grouping_metric
    mean_power = [e / t for e, t in zip(energies_plot_data, times_plot_data)]


def create_monte_carlo_plots(parameters):
    benchmark_name = "monte_carlo"
    folder_name = "i7-3770"
    grouping_metric = parameters.limits
    energies_plot_data, times_plot_data = process(parameters, benchmark_name, folder_name, grouping_metric, "AVX")

    x = parameters.limits
    mean_power = [e / t for e, t in zip(energies_plot_data, times_plot_data)]


def create_vectorization_heatmaps(parameters):
    benchmark_name = "vector-operations"
    folder_name = "R7-5800X"
    grouping_metric = parameters.limits
    x_labels = parameters.limits
    y_labels = parameters.instruction_sets
    y_labels.remove("SSE2")

    sse_energies, sse_times = process(parameters, benchmark_name, folder_name, grouping_metric, "SSE")
    avx_energies, avx_times = process(parameters, benchmark_name, folder_name, grouping_metric, "AVX")

    energies_data = [sse_energies, avx_energies]
    times_data = [sse_times, avx_times]


    # _create_heatmap(energies_data, x_labels, y_labels, "adolf")
    create_heatmap(times_data, x_labels, y_labels, "eva")


def create_vectorization_scatter_plots(parameters):
    benchmark_name = "vector-operations"
    folder_name = "R7-5800X"
    grouping_metric = parameters.limits

    sse_energies, sse_times = process(parameters, benchmark_name, folder_name, grouping_metric, "SSE")
    avx_energies, avx_times = process(parameters, benchmark_name, folder_name, grouping_metric, "AVX")

    energies_data = [(grouping_metric, sse_energies), (grouping_metric, avx_energies)]
    times_data = [(grouping_metric, sse_times), (grouping_metric, avx_times)]

    relative_energies = [1-(e1/e2) for e1,e2 in zip(sse_energies, avx_energies)]

    create_scatter_plot(energies_data, "frequencies [MHz]", "consumed energy [Joules]", "energy comparison of instruction sets",
                        ["SSE", "AVX"])
    create_scatter_plot(times_data, "frequencies [MHz]", "time [s]", "time comparison of instruction sets", ["SSE", "AVX"])
    create_bar_plot(grouping_metric, relative_energies, "frequencies [MHz]", "relative energy difference",
                     "relative energy difference SSE/AVX")



if __name__ == "__main__":

    create_vectorization_scatter_plots(get_config("R7-5800X"))

    # create_monte_carlo_plots(get_config("i7-3770"))
