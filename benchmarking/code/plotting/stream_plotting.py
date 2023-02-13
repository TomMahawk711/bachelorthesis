from data_processing import process, get_config
from plotting_templates import create_bar_plot, create_heatmap, create_scatter_plot


# TODO: fix scaling -> make it logarithmic for bandwidths


def _create_stream_plots_i7_grouping_array_sizes():
    folder_name = "i7-3770"
    benchmark_name = "stream"
    parameters = get_config(folder_name)
    grouping_metric = parameters.stream_array_sizes

    energies_1600MHz, times_1600MHz, copys_1600MHz, scales_1600MHz, adds_1600MHz, triads_1600MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=1600)
    energies_2100MHz, times_2100MHz, copys_2100MHz, scales_2100MHz, adds_2100MHz, triads_2100MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2100)
    energies_2600MHz, times_2600MHz, copys_2600MHz, scales_2600MHz, adds_2600MHz, triads_2600MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2600)
    energies_3100MHz, times_3100MHz, copys_3100MHz, scales_3100MHz, adds_3100MHz, triads_3100MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3100)
    energies_3600MHz, times_3600MHz, copys_3600MHz, scales_3600MHz, adds_3600MHz, triads_3600MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3600)
    energies_4100MHz, times_4100MHz, copys_4100MHz, scales_4100MHz, adds_4100MHz, triads_4100MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=4100)

    mean_power = [e / t for e, t in zip(energies_2100MHz, times_2100MHz)]

    energies_data = [(grouping_metric, energies_2100MHz)]
    copys_data = [(grouping_metric, copys_1600MHz), (grouping_metric, copys_2100MHz), (grouping_metric, copys_2600MHz),
                  (grouping_metric, copys_3100MHz), (grouping_metric, copys_3600MHz), (grouping_metric, copys_4100MHz)]

    #create_scatter_plot(energies_data, "array size", "energy [J]", "energy consumption on different array sizes", ["1600", "2100MHz", "2600", "3100", "3600", "4100"], "upper center")
    create_scatter_plot(copys_data, "array size", "bandwidth [MB/s]", "bandwidth on different array sizes", ["1600MHz", "2100MHz", "2600MHz", "3100MHz", "3600MHz", "4100MHz"], "upper center")


def _create_stream_plots_r7_grouping_array_sizes():
    folder_name = "R7-5800X"
    benchmark_name = "stream"
    parameters = get_config(folder_name)
    grouping_metric = parameters.stream_array_sizes

    energies_2200MHz, times_2200MHz, copys_2200MHz, scales_2200MHz, adds_2200MHz, triads_2200MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2200)
    energies_2800MHz, times_2800MHz, copys_2800MHz, scales_2800MHz, adds_2800MHz, triads_2800MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2800)
    energies_3800MHz, times_3800MHz, copys_3800MHz, scales_3800MHz, adds_3800MHz, triads_3800MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3800)

    mean_power = [e / t for e, t in zip(energies_2200MHz, times_2200MHz)]

    energies_data = [(grouping_metric, energies_2200MHz)]
    copys_data = [(grouping_metric, copys_2200MHz), (grouping_metric, copys_2800MHz), (grouping_metric, copys_3800MHz)]

    #create_scatter_plot(energies_data, "array size", "energy [J]", "energy consumption on different array sizes", ["1600", "2100MHz", "2600", "3100", "3600", "4100"], "upper center")
    create_scatter_plot(copys_data, "array size", "bandwidth [MB/s]", "bandwidth on different array sizes", ["2200MHz", "2800MHz", "3800MHz"], "upper center")


def _create_stream_plots_grouping_frequencies():
    folder_name = "i7-3770"
    benchmark_name = "stream"
    parameters = get_config(folder_name)
    grouping_metric = parameters.limits

    energies_1600MHz, times_1600MHz, copys_1600MHz, scales_1600MHz, adds_1600MHz, triads_1600MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=1600)
    energies_2100MHz, times_2100MHz, copys_2100MHz, scales_2100MHz, adds_2100MHz, triads_2100MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2100)
    energies_2600MHz, times_2600MHz, copys_2600MHz, scales_2600MHz, adds_2600MHz, triads_2600MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2600)
    energies_3100MHz, times_3100MHz, copys_3100MHz, scales_3100MHz, adds_3100MHz, triads_3100MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3100)
    energies_3600MHz, times_3600MHz, copys_3600MHz, scales_3600MHz, adds_3600MHz, triads_3600MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3600)
    energies_4100MHz, times_4100MHz, copys_4100MHz, scales_4100MHz, adds_4100MHz, triads_4100MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=4100)

    mean_power = [e / t for e, t in zip(energies_2100MHz, times_2100MHz)]

    energies_data = [(grouping_metric, energies_2100MHz)]
    copys_data = [(grouping_metric, copys_1600MHz), (grouping_metric, copys_2100MHz), (grouping_metric, copys_2600MHz),
                  (grouping_metric, copys_3100MHz), (grouping_metric, copys_3600MHz), (grouping_metric, copys_4100MHz)]

    #create_scatter_plot(energies_data, "array size", "energy [J]", "energy consumption on different array sizes", ["1600", "2100MHz", "2600", "3100", "3600", "4100"], "upper center")
    create_scatter_plot(copys_data, "array size", "bandwidth [MB/s]", "bandwidth on different array sizes", ["1600MHz", "2100MHz", "2600MHz", "3100MHz", "3600MHz", "4100MHz"], "upper center")


if __name__ == "__main__":
    _create_stream_plots_r7_grouping_array_sizes()
