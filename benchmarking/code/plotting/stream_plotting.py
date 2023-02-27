from data_processing import process, get_config
from plotting_templates import create_scatter_plot


def _create_stream_plots_i7_by_array_sizes():
    folder_name = "i7-3770_smaller-vectors"
    benchmark_name = "stream"
    parameters = get_config(folder_name)
    grouping_metric = parameters.stream_array_sizes
    grouping_metric_label = [(e*8)/1e6 for e in grouping_metric]

    energies_1600MHz, times_1600MHz, copys_1600MHz, scales_1600MHz, adds_1600MHz, triads_1600MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=1600)
    energies_2100MHz, times_2100MHz, copys_2100MHz, scales_2100MHz, adds_2100MHz, triads_2100MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2100)
    energies_2600MHz, times_2600MHz, copys_2600MHz, scales_2600MHz, adds_2600MHz, triads_2600MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2600)
    energies_3100MHz, times_3100MHz, copys_3100MHz, scales_3100MHz, adds_3100MHz, triads_3100MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3100)
    energies_3600MHz, times_3600MHz, copys_3600MHz, scales_3600MHz, adds_3600MHz, triads_3600MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3600)
    energies_4100MHz, times_4100MHz, copys_4100MHz, scales_4100MHz, adds_4100MHz, triads_4100MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=4100)

    mean_power = [e / t for e, t in zip(energies_2100MHz, times_2100MHz)]

    copys_1600MHz = [bw / 1e3 for bw in copys_1600MHz]
    copys_2100MHz = [bw / 1e3 for bw in copys_2100MHz]
    copys_2600MHz = [bw / 1e3 for bw in copys_2600MHz]
    copys_3100MHz = [bw / 1e3 for bw in copys_3100MHz]
    copys_3600MHz = [bw / 1e3 for bw in copys_3600MHz]
    copys_4100MHz = [bw / 1e3 for bw in copys_4100MHz]

    triads_1600MHz = [bw / 1e3 for bw in triads_1600MHz]
    triads_2100MHz = [bw / 1e3 for bw in triads_2100MHz]
    triads_2600MHz = [bw / 1e3 for bw in triads_2600MHz]
    triads_3100MHz = [bw / 1e3 for bw in triads_3100MHz]
    triads_3600MHz = [bw / 1e3 for bw in triads_3600MHz]
    triads_4100MHz = [bw / 1e3 for bw in triads_4100MHz]

    energies_data = [(grouping_metric_label, energies_2100MHz), (grouping_metric_label, energies_2100MHz), (grouping_metric_label, energies_2600MHz),
                     (grouping_metric_label, energies_3100MHz), (grouping_metric_label, energies_3600MHz), (grouping_metric_label, energies_4100MHz)]
    times_data = [(grouping_metric_label, times_1600MHz), (grouping_metric_label, times_2100MHz), (grouping_metric_label, times_2600MHz),
                  (grouping_metric_label, times_3100MHz), (grouping_metric_label, times_3600MHz), (grouping_metric_label, times_4100MHz)]
    copys_data = [(grouping_metric_label, copys_1600MHz), (grouping_metric_label, copys_2100MHz), (grouping_metric_label, copys_2600MHz),
                  (grouping_metric_label, copys_3100MHz), (grouping_metric_label, copys_3600MHz), (grouping_metric_label, copys_4100MHz)]
    scales_data = [(grouping_metric_label, scales_1600MHz), (grouping_metric_label, scales_2100MHz), (grouping_metric_label, scales_2600MHz),
                   (grouping_metric_label, scales_3100MHz), (grouping_metric_label, scales_3600MHz), (grouping_metric_label, scales_4100MHz)]
    adds_data = [(grouping_metric_label, adds_1600MHz), (grouping_metric_label, adds_2100MHz), (grouping_metric_label, adds_2600MHz),
                 (grouping_metric_label, adds_3100MHz), (grouping_metric_label, adds_3600MHz), (grouping_metric_label, adds_4100MHz)]
    triads_data = [(grouping_metric_label, triads_1600MHz), (grouping_metric_label, triads_2100MHz), (grouping_metric_label, triads_2600MHz),
                   (grouping_metric_label, triads_3100MHz), (grouping_metric_label, triads_3600MHz), (grouping_metric_label, triads_4100MHz)]

    create_scatter_plot(energies_data, "array size [MB]", "energy [J]", "Stream: energy consumption on different array sizes",
                        ["1600 MHz", "2100 MHz", "2600 MHz", "3100 MHz", "3600 MHz", "4100 MHz"], "upper left", x_scale='log', x_ticks=grouping_metric_label)
    create_scatter_plot(times_data, "array size [MB]", "time [s]", "Stream: wall time on different array sizes",
                        ["1600 MHz", "2100 MHz", "2600 MHz", "3100 MHz", "3600 MHz", "4100 MHz"], "upper left", x_scale='log', x_ticks=grouping_metric_label)
    create_scatter_plot(copys_data, "array size [MB]", "bandwidth [GB/s]", "Stream: copy bandwidth on different array sizes",
                        ["1600 MHz", "2100 MHz", "2600 MHz", "3100 MHz", "3600 MHz", "4100 MHz"], "upper right", x_scale='log')
    create_scatter_plot(triads_data, "array size [MB]", "bandwidth [GB/s]", "Stream: triad bandwidth on different array sizes",
                        ["1600 MHz", "2100 MHz", "2600 MHz", "3100 MHz", "3600 MHz", "4100 MHz"], "upper right", x_scale='log')


def _create_stream_plots_r7_by_array_sizes():
    folder_name = "R7-5800X_smaller-vectors"
    benchmark_name = "stream"
    parameters = get_config(folder_name)
    grouping_metric = parameters.stream_array_sizes
    grouping_metric_label = [(e*8)/1e6 for e in grouping_metric]

    energies_2200MHz, times_2200MHz, copys_2200MHz, scales_2200MHz, adds_2200MHz, triads_2200MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2200, thread_count=1)
    energies_2800MHz, times_2800MHz, copys_2800MHz, scales_2800MHz, adds_2800MHz, triads_2800MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2800, thread_count=1)
    energies_3800MHz, times_3800MHz, copys_3800MHz, scales_3800MHz, adds_3800MHz, triads_3800MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3800, thread_count=1)

    mean_power = [e / t for e, t in zip(energies_2200MHz, times_2200MHz)]

    copys_2200MHz = [bw / 1e3 for bw in copys_2200MHz]
    copys_2800MHz = [bw / 1e3 for bw in copys_2800MHz]
    copys_3800MHz = [bw / 1e3 for bw in copys_3800MHz]

    triads_2200MHz = [bw / 1e3 for bw in triads_2200MHz]
    triads_2800MHz = [bw / 1e3 for bw in triads_2800MHz]
    triads_3800MHz = [bw / 1e3 for bw in triads_3800MHz]

    energies_data = [(grouping_metric_label, energies_2200MHz), (grouping_metric_label, energies_2800MHz), (grouping_metric_label, energies_3800MHz)]
    times_data = [(grouping_metric_label, times_2200MHz), (grouping_metric_label, times_2800MHz), (grouping_metric_label, times_3800MHz)]
    copys_data = [(grouping_metric_label, copys_2200MHz), (grouping_metric_label, copys_2800MHz), (grouping_metric_label, copys_3800MHz)]
    scales_data = [(grouping_metric_label, scales_2200MHz), (grouping_metric_label, scales_2800MHz), (grouping_metric_label, scales_3800MHz)]
    adds_data = [(grouping_metric_label, adds_2200MHz), (grouping_metric_label, adds_2800MHz), (grouping_metric_label, adds_3800MHz)]
    triads_data = [(grouping_metric_label, triads_2200MHz), (grouping_metric_label, triads_2800MHz), (grouping_metric_label, triads_3800MHz)]

    create_scatter_plot(energies_data, "array size [MB]", "energy [J]", "Stream: energy consumption on different array sizes",
                        ["2200 MHz", "2800 MHz", "3800 MHz"], "upper left", x_scale='log', x_ticks=grouping_metric_label)
    create_scatter_plot(times_data, "array size [MB]", "time [s]", "Stream: wall time on different array sizes",
                        ["2200 MHz", "2800 MHz", "3800 MHz"], "upper left", x_scale='log', x_ticks=grouping_metric_label)
    create_scatter_plot(copys_data, "array size [MB]", "bandwidth [GB/s]", "Stream: copy bandwidth on different array sizes",
                        ["2200 MHz", "2800 MHz", "3800 MHz"], "upper right", x_scale='log')
    create_scatter_plot(triads_data, "array size [MB]", "bandwidth [GB/s]", "Stream: triad bandwidth on different array sizes",
                        ["2200 MHz", "2800 MHz", "3800 MHz"], "upper right", x_scale='log')


def _create_stream_plots_both():
    benchmark_name = "stream"

    folder_name_r7 = "R7-5800X_smaller-vectors"
    parameters_r7 = get_config(folder_name_r7)
    grouping_metric_r7 = parameters_r7.limits
    energies_r7, times_r7, copys_r7, scales_r7, adds_r7, triads_r7 = \
        process(parameters_r7, benchmark_name, folder_name_r7, grouping_metric_r7, array_size=6400000)
    speed_up_r7 = [times_r7[0] / time for time in times_r7]

    folder_name_i7 = "i7-3770_smaller-vectors"
    parameters_i7 = get_config(folder_name_i7)
    grouping_metric_i7 = parameters_i7.limits
    energies_i7, times_i7, copys_i7, scales_i7, adds_i7, triads_i7 = \
        process(parameters_i7, benchmark_name, folder_name_i7, grouping_metric_i7, array_size=6400000)
    speed_up_i7 = [times_i7[0] / time for time in times_i7]

    energies_data = [(grouping_metric_i7, energies_i7), (grouping_metric_r7, energies_r7)]
    times_data = [(grouping_metric_i7, times_i7), (grouping_metric_r7, times_r7)]
    speed_up_data = [(grouping_metric_i7, speed_up_i7), (grouping_metric_r7, speed_up_r7)]
    copys_data = [(grouping_metric_i7, copys_i7), (grouping_metric_r7, copys_r7)]
    triads_data = [(grouping_metric_i7, triads_i7), (grouping_metric_r7, triads_r7)]

    create_scatter_plot(energies_data, "frequency [MHz]", "energy [J]", "Stream: energy consumption on different CPUs", ["i7 3770", "R7 5800X"], "upper left", x_ticks=grouping_metric_i7)
    create_scatter_plot(speed_up_data, "frequency [MHz]", "speed up", "Stream: speed up on different CPUs", ["i7 3770", "R7 5800X"], "upper left", x_ticks=grouping_metric_i7)
    create_scatter_plot(times_data, "frequency [MHz]", "time [s]", "Stream: wall time on different CPUs", ["i7 3770", "R7 5800X"], "upper right", x_ticks=grouping_metric_i7)
    create_scatter_plot(copys_data, "frequency [MHz]", "bandwidth [GB/s]", "Stream: copy bandwidth on different CPUs", ["i7 3770", "R7 5800X"], "upper left", x_ticks=grouping_metric_i7)
    create_scatter_plot(triads_data, "frequency [MHz]", "bandwidth [GB/s]", "Stream: triads bandwidth on different CPUs", ["i7 3770", "R7 5800X"], "upper left", x_ticks=grouping_metric_i7)


def _create_stream_plots_by_frequencies():
    folder_name = "i7-3770_smaller-vectors"
    benchmark_name = "stream"
    parameters = get_config(folder_name)
    grouping_metric = parameters.limits

    energies_1600MHz, times_1600MHz, copys_1600MHz, scales_1600MHz, adds_1600MHz, triads_1600MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=1600)
    energies_2100MHz, times_2100MHz, copys_2100MHz, scales_2100MHz, adds_2100MHz, triads_2100MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2100)
    energies_2600MHz, times_2600MHz, copys_2600MHz, scales_2600MHz, adds_2600MHz, triads_2600MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2600)
    energies_3100MHz, times_3100MHz, copys_3100MHz, scales_3100MHz, adds_3100MHz, triads_3100MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3100)
    energies_3600MHz, times_3600MHz, copys_3600MHz, scales_3600MHz, adds_3600MHz, triads_3600MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3600)
    energies_4100MHz, times_4100MHz, copys_4100MHz, scales_4100MHz, adds_4100MHz, triads_4100MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=4100)

    energies_data = [(grouping_metric, energies_2100MHz)]
    copys_data = [(grouping_metric, copys_1600MHz), (grouping_metric, copys_2100MHz), (grouping_metric, copys_2600MHz),
                  (grouping_metric, copys_3100MHz), (grouping_metric, copys_3600MHz), (grouping_metric, copys_4100MHz)]

    create_scatter_plot(energies_data, "array size", "energy [J]", "Stream: energy consumption on different array sizes",
                        ["1600 MHz", "2100 MHz", "2600 MHz", "3100 MHz", "3600 MHz", "4100 MHz"], "upper center", x_ticks=grouping_metric)
    create_scatter_plot(copys_data, "frequency [MHz]", "bandwidth [MB/s]", "Stream: copy bandwidth on different array sizes",
                        ["1600 MHz", "2100 MHz", "2600 MHz", "3100 MHz", "3600 MHz", "4100 MHz"], "upper left", x_ticks=grouping_metric)


def _create_stream_plots_i7_by_thread_count():
    folder_name = "i7-3770_new"
    benchmark_name = "stream"
    parameters = get_config(folder_name)
    grouping_metric = parameters.thread_counts

    energies_1600MHz, times_1600MHz, copys_1600MHz, scales_1600MHz, adds_1600MHz, triads_1600MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=1600, array_size=400000)
    energies_2100MHz, times_2100MHz, copys_2100MHz, scales_2100MHz, adds_2100MHz, triads_2100MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2100, array_size=400000)
    energies_2600MHz, times_2600MHz, copys_2600MHz, scales_2600MHz, adds_2600MHz, triads_2600MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2600, array_size=400000)
    energies_3100MHz, times_3100MHz, copys_3100MHz, scales_3100MHz, adds_3100MHz, triads_3100MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3100, array_size=400000)
    energies_3600MHz, times_3600MHz, copys_3600MHz, scales_3600MHz, adds_3600MHz, triads_3600MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3600, array_size=400000)
    energies_4100MHz, times_4100MHz, copys_4100MHz, scales_4100MHz, adds_4100MHz, triads_4100MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=4100, array_size=400000)

    energies_data = [(grouping_metric, energies_2100MHz)]
    copys_data = [(grouping_metric, copys_1600MHz), (grouping_metric, copys_2100MHz), (grouping_metric, copys_2600MHz),
                  (grouping_metric, copys_3100MHz), (grouping_metric, copys_3600MHz), (grouping_metric, copys_4100MHz)]

    create_scatter_plot(energies_data, "array size", "energy [J]", "Stream: energy consumption on different array sizes",
                        ["1600 MHz", "2100 MHz", "2600 MHz", "3100 MHz", "3600 MHz", "4100 MHz"], "upper center", x_ticks=grouping_metric)
    create_scatter_plot(copys_data, "thread count", "bandwidth [GB/s]", "Stream: copy bandwidth on different array sizes",
                        ["1600 MHz", "2100 MHz", "2600 MHz", "3100 MHz", "3600 MHz", "4100 MHz"], "upper right", x_ticks=grouping_metric)


def _create_stream_plots_r7_by_thread_count():
    folder_name = "R7-5800X_new"
    benchmark_name = "stream"
    parameters = get_config(folder_name)
    grouping_metric = parameters.thread_counts

    energies_2200MHz, times_2200MHz, copys_2200MHz, scales_2200MHz, adds_2200MHz, triads_2200MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2200, array_size=1600000)
    energies_2800MHz, times_2800MHz, copys_2800MHz, scales_2800MHz, adds_2800MHz, triads_2800MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2800, array_size=1600000)
    energies_3800MHz, times_3800MHz, copys_3800MHz, scales_3800MHz, adds_3800MHz, triads_3800MHz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, frequency=3800, array_size=1600000)

    copys_2200MHz = [bw / 1e3 for bw in copys_2200MHz]
    copys_2800MHz = [bw / 1e3 for bw in copys_2800MHz]
    copys_3800MHz = [bw / 1e3 for bw in copys_3800MHz]

    energies_data = [(grouping_metric, energies_2200MHz)]
    copys_data = [(grouping_metric, copys_3800MHz)]

    create_scatter_plot(energies_data, "array size", "energy [J]", "Stream: energy consumption for different thread counts",
                        ["2200 MHz", "2800 MHz", "3800 MHz"], "upper center")
    create_scatter_plot(copys_data, "thread count", "bandwidth [GB/s]", "Stream: copy bandwidth for different thread counts",
                        ["3800 MHz"], "upper right")


def _create_stream_plots_both_by_thread_count():
    i7_folder_name = "i7-3770_new-stream"
    benchmark_name = "stream"
    i7_parameters = get_config(i7_folder_name)
    i7_grouping_metric = i7_parameters.thread_counts

    energies_4100MHz, times_4100MHz, copys_4100MHz, scales_4100MHz, adds_4100MHz, triads_4100MHz = \
        process(i7_parameters, benchmark_name, i7_folder_name, i7_grouping_metric, frequency=4100, array_size=400000)

    copys_4100MHz = [bw / 1e3 for bw in copys_4100MHz]

    r7_folder_name = "R7-5800X_new"
    benchmark_name = "stream"
    r7_parameters = get_config(r7_folder_name)
    r7_grouping_metric = r7_parameters.thread_counts

    energies_3800MHz, times_3800MHz, copys_3800MHz, scales_3800MHz, adds_3800MHz, triads_3800MHz = \
        process(r7_parameters, benchmark_name, r7_folder_name, r7_grouping_metric, frequency=3800, array_size=1600000)

    copys_3800MHz = [bw / 1e3 for bw in copys_3800MHz]

    energies_data = [(i7_grouping_metric, energies_4100MHz), (r7_grouping_metric, energies_3800MHz)]
    copys_data = [(i7_grouping_metric, copys_4100MHz), (r7_grouping_metric, copys_3800MHz)]

    create_scatter_plot(energies_data, "thread count", "energy [J]", "Stream: energy consumption for different thread counts",
                        ["i7 3770 - 4100 MHz - 3.2 MiB", "R7 5800X - 3800 MHz - 12.8 MiB"], "center right")
    create_scatter_plot(copys_data, "thread count", "bandwidth [GB/s]", "Stream: copy bandwidth for different thread counts",
                        ["i7 3770 - 4100 MHz - 3.2 MiB", "R7 5800X - 3800 MHz - 12.8 MiB"], "center right")


if __name__ == "__main__":
    _create_stream_plots_both_by_thread_count()
