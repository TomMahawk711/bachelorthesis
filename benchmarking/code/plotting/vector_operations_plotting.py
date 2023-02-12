from data_processing import process, get_config
from plotting_templates import create_bar_plot, create_heatmap, create_scatter_plot


def _create_vectorization_heatmaps():
    folder_name = "R7-5800X"
    parameters = get_config(folder_name)
    benchmark_name = "vector-operations"
    grouping_metric = parameters.limits

    x_labels = parameters.limits
    y_labels = parameters.instruction_sets
    y_labels.remove("SSE2")

    sse_energies, sse_times = process(parameters, benchmark_name, folder_name, grouping_metric, "SSE")
    avx_energies, avx_times = process(parameters, benchmark_name, folder_name, grouping_metric, "AVX")

    energies_data = [sse_energies, avx_energies]
    times_data = [sse_times, avx_times]


    # _create_heatmap(energies_data, x_labels, y_labels, "title_a")
    create_heatmap(times_data, x_labels, y_labels, "title_b")


def _create_vectorization_scatter_plots():
    folder_name = "R7-5800X"
    parameters = get_config(folder_name)
    benchmark_name = "vector-operations"
    grouping_metric = parameters.limits

    sse_energies, sse_times = process(parameters, benchmark_name, folder_name, grouping_metric, "SSE")
    avx_energies, avx_times = process(parameters, benchmark_name, folder_name, grouping_metric, "AVX")

    energies_data = [(grouping_metric, sse_energies), (grouping_metric, avx_energies)]
    times_data = [(grouping_metric, sse_times), (grouping_metric, avx_times)]

    relative_energies = [1-(e1/e2) for e1,e2 in zip(sse_energies, avx_energies)]

    create_scatter_plot(energies_data, "frequencies [MHz]", "consumed energy [Joules]", "energy comparison of instruction sets", ["SSE", "AVX"])
    create_scatter_plot(times_data, "frequencies [MHz]", "time [s]", "time comparison of instruction sets", ["SSE", "AVX"])
    # create_bar_plot(grouping_metric, relative_energies, "frequencies [MHz]", "relative energy difference", "relative energy difference SSE/AVX")



if __name__ == "__main__":
    _create_vectorization_scatter_plots()