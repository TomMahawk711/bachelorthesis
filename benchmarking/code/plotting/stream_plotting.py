from data_processing import process, get_config
from plotting_templates import create_scatter_plot


def _create_stream_plots_i7_by_array_sizes():
    folder_name = "i7-3770_smaller-vectors"
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

    energies_data = [(grouping_metric, energies_2100MHz), (grouping_metric, energies_2100MHz), (grouping_metric, energies_2600MHz),
                     (grouping_metric, energies_3100MHz), (grouping_metric, energies_3600MHz), (grouping_metric, energies_4100MHz)]
    times_data = [(grouping_metric, times_1600MHz), (grouping_metric, times_2100MHz), (grouping_metric, times_2600MHz),
                  (grouping_metric, times_3100MHz), (grouping_metric, times_3600MHz), (grouping_metric, times_4100MHz)]
    copys_data = [(grouping_metric, copys_1600MHz), (grouping_metric, copys_2100MHz), (grouping_metric, copys_2600MHz),
                  (grouping_metric, copys_3100MHz), (grouping_metric, copys_3600MHz), (grouping_metric, copys_4100MHz)]
    scales_data = [(grouping_metric, scales_1600MHz), (grouping_metric, scales_2100MHz), (grouping_metric, scales_2600MHz),
                   (grouping_metric, scales_3100MHz), (grouping_metric, scales_3600MHz), (grouping_metric, scales_4100MHz)]
    adds_data = [(grouping_metric, adds_1600MHz), (grouping_metric, adds_2100MHz), (grouping_metric, adds_2600MHz),
                 (grouping_metric, adds_3100MHz), (grouping_metric, adds_3600MHz), (grouping_metric, adds_4100MHz)]
    triads_data = [(grouping_metric, triads_1600MHz), (grouping_metric, triads_2100MHz), (grouping_metric, triads_2600MHz),
                   (grouping_metric, triads_3100MHz), (grouping_metric, triads_3600MHz), (grouping_metric, triads_4100MHz)]

    create_scatter_plot(energies_data, "array size", "energy [J]", "energy consumption on different array sizes",
                        ["1600MHz", "2100MHz", "2600MHz", "3100MHz", "3600MHz", "4100MHz"], "upper left", x_scale='log')
    create_scatter_plot(times_data, "array size", "time [s]", "execution time on different array sizes",
                        ["1600MHz", "2100MHz", "2600MHz", "3100MHz", "3600MHz", "4100MHz"], "upper left", x_scale='log')
    create_scatter_plot(copys_data, "array size", "bandwidth [MB/s]", "bandwidth on different array sizes",
                        ["1600MHz", "2100MHz", "2600MHz", "3100MHz", "3600MHz", "4100MHz"], "upper right", x_scale='log')
    create_scatter_plot(triads_data, "array size", "bandwidth [MB/s]", "bandwidth on different array sizes",
                        ["1600MHz", "2100MHz", "2600MHz", "3100MHz", "3600MHz", "4100MHz"], "upper right", x_scale='log')


def _create_stream_plots_r7_by_array_sizes():
    folder_name = "R7-5800X_smaller-vectors"
    benchmark_name = "stream"
    parameters = get_config(folder_name)
    grouping_metric = parameters.stream_array_sizes

    energies_2200MHz, times_2200MHz, copys_2200MHz, scales_2200MHz, adds_2200MHz, triads_2200MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2200, thread_count=1)
    energies_2800MHz, times_2800MHz, copys_2800MHz, scales_2800MHz, adds_2800MHz, triads_2800MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2800, thread_count=1)
    energies_3800MHz, times_3800MHz, copys_3800MHz, scales_3800MHz, adds_3800MHz, triads_3800MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3800, thread_count=1)

    mean_power = [e / t for e, t in zip(energies_2200MHz, times_2200MHz)]

    energies_data = [(grouping_metric, energies_2200MHz), (grouping_metric, energies_2800MHz), (grouping_metric, energies_3800MHz)]
    times_data = [(grouping_metric, times_2200MHz), (grouping_metric, times_2800MHz), (grouping_metric, times_3800MHz)]
    copys_data = [(grouping_metric, copys_2200MHz), (grouping_metric, copys_2800MHz), (grouping_metric, copys_3800MHz)]
    scales_data = [(grouping_metric, scales_2200MHz), (grouping_metric, scales_2800MHz), (grouping_metric, scales_3800MHz)]
    adds_data = [(grouping_metric, adds_2200MHz), (grouping_metric, adds_2800MHz), (grouping_metric, adds_3800MHz)]
    triads_data = [(grouping_metric, triads_2200MHz), (grouping_metric, triads_2800MHz), (grouping_metric, triads_3800MHz)]

    create_scatter_plot(energies_data, "array size", "energy [J]", "energy consumption on different array sizes",
                        ["2200MHz", "2800MHz", "3800MHz"], "upper left", x_scale='log')
    create_scatter_plot(times_data, "array size", "time [s]", "execution time on different array sizes",
                        ["2200MHz", "2800MHz", "3800MHz"], "upper left", x_scale='log')
    create_scatter_plot(copys_data, "array size", "bandwidth [MB/s]", "bandwidth on different array sizes",
                        ["2200MHz", "2800MHz", "3800MHz"], "upper right", x_scale='log')
    create_scatter_plot(triads_data, "array size", "bandwidth [MB/s]", "bandwidth on different array sizes",
                        ["2200MHz", "2800MHz", "3800MHz"], "upper right", x_scale='log')


def _create_stream_plots_both():
    benchmark_name = "stream"

    folder_name_r7 = "R7-5800X_smaller-vectors"
    parameters_r7 = get_config(folder_name_r7)
    grouping_metric_r7 = parameters_r7.limits
    energies_r7, times_r7, copys_r7, scales_r7, adds_r7, triads_r7 = process(parameters_r7, benchmark_name, folder_name_r7, grouping_metric_r7, array_size=200000)

    folder_name_i7 = "i7-3770_smaller-vectors"
    parameters_i7 = get_config(folder_name_i7)
    grouping_metric_i7 = parameters_i7.limits
    energies_i7, times_i7, copys_i7, scales_i7, adds_i7, triads_i7 = process(parameters_i7, benchmark_name, folder_name_i7, grouping_metric_i7, array_size=200000)

    energies_data = [(grouping_metric_i7, energies_i7), (grouping_metric_r7, energies_r7)]
    times_data = [(grouping_metric_i7, times_i7), (grouping_metric_r7, times_r7)]
    copys_data = [(grouping_metric_i7, copys_i7), (grouping_metric_r7, copys_r7)]
    triads_data = [(grouping_metric_i7, triads_i7), (grouping_metric_r7, triads_r7)]

    create_scatter_plot(energies_data, "frequency [MHz]", "energy [J]", "energy consumption on different CPUs", ["i7 3770", "R7 5800X"], "upper left")
    create_scatter_plot(times_data, "frequency [MHz]", "time [s]", "execution time on different CPUs", ["i7 3770", "R7 5800X"], "center left")
    create_scatter_plot(copys_data, "frequency [MHz]", "bandwidth [MB/s]", "bandwidth on different CPUs", ["i7 3770", "R7 5800X"], "upper left")
    create_scatter_plot(triads_data, "frequency [MHz]", "bandwidth [MB/s]", "bandwidth on different CPUs", ["i7 3770", "R7 5800X"], "upper left")


def _create_stream_plots_by_frequencies():
    folder_name = "i7-3770_smaller-vectors"
    benchmark_name = "stream"
    parameters = get_config(folder_name)
    grouping_metric = parameters.limits

    energies_1600MHz, times_1600MHz, copys_1600MHz, scales_1600MHz, adds_1600MHz, triads_1600MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=1600)
    energies_2100MHz, times_2100MHz, copys_2100MHz, scales_2100MHz, adds_2100MHz, triads_2100MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2100)
    energies_2600MHz, times_2600MHz, copys_2600MHz, scales_2600MHz, adds_2600MHz, triads_2600MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2600)
    energies_3100MHz, times_3100MHz, copys_3100MHz, scales_3100MHz, adds_3100MHz, triads_3100MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3100)
    energies_3600MHz, times_3600MHz, copys_3600MHz, scales_3600MHz, adds_3600MHz, triads_3600MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3600)
    energies_4100MHz, times_4100MHz, copys_4100MHz, scales_4100MHz, adds_4100MHz, triads_4100MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=4100)

    energies_data = [(grouping_metric, energies_2100MHz)]
    copys_data = [(grouping_metric, copys_1600MHz), (grouping_metric, copys_2100MHz), (grouping_metric, copys_2600MHz),
                  (grouping_metric, copys_3100MHz), (grouping_metric, copys_3600MHz), (grouping_metric, copys_4100MHz)]

    create_scatter_plot(energies_data, "array size", "energy [J]", "energy consumption on different array sizes",
                        ["1600", "2100MHz", "2600", "3100", "3600", "4100"], "upper center")
    create_scatter_plot(copys_data, "frequency [MHz]", "bandwidth [MB/s]", "bandwidth on different array sizes",
                        ["1600MHz", "2100MHz", "2600MHz", "3100MHz", "3600MHz", "4100MHz"], "upper left")


def _create_stream_plots_by_thread_count():
    folder_name = "i7-3770_smaller-vectors"
    benchmark_name = "stream"
    parameters = get_config(folder_name)
    grouping_metric = parameters.thread_counts

    energies_1600MHz, times_1600MHz, copys_1600MHz, scales_1600MHz, adds_1600MHz, triads_1600MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=1600)
    energies_2100MHz, times_2100MHz, copys_2100MHz, scales_2100MHz, adds_2100MHz, triads_2100MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2100)
    energies_2600MHz, times_2600MHz, copys_2600MHz, scales_2600MHz, adds_2600MHz, triads_2600MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2600)
    energies_3100MHz, times_3100MHz, copys_3100MHz, scales_3100MHz, adds_3100MHz, triads_3100MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3100)
    energies_3600MHz, times_3600MHz, copys_3600MHz, scales_3600MHz, adds_3600MHz, triads_3600MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3600)
    energies_4100MHz, times_4100MHz, copys_4100MHz, scales_4100MHz, adds_4100MHz, triads_4100MHz = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=4100)

    energies_data = [(grouping_metric, energies_2100MHz)]
    copys_data = [(grouping_metric, triads_1600MHz), (grouping_metric, triads_2100MHz), (grouping_metric, triads_2600MHz),
                  (grouping_metric, triads_3100MHz), (grouping_metric, triads_3600MHz), (grouping_metric, triads_4100MHz)]

    create_scatter_plot(energies_data, "array size", "energy [J]", "energy consumption on different array sizes",
                        ["1600", "2100MHz", "2600", "3100", "3600", "4100"], "upper center")
    create_scatter_plot(copys_data, "thread count", "bandwidth [MB/s]", "bandwidth on different array sizes",
                        ["1600MHz", "2100MHz", "2600MHz", "3100MHz", "3600MHz", "4100MHz"], "upper left")


if __name__ == "__main__":
    _create_stream_plots_both()
