from data_processing import process, get_config
from plotting_templates import create_bar_plot, create_heatmap, create_scatter_plot


def _create_stream_plots(folder_name):
    parameters = get_config(folder_name)
    benchmark_name = "stream"
    grouping_metric = parameters.thread_counts

    energies_plot_data, times_plot_data, copy_plot_data, scale_plot_data, add_plot_data, triad_plot_data = \
        process(parameters, benchmark_name, folder_name, grouping_metric, "foo")

    mean_power = [e / t for e, t in zip(energies_plot_data, times_plot_data)]


if __name__ == "__main__":
    _create_stream_plots(get_config("i7-3770"))
