from data_processing import process, get_config
from plotting_templates import create_scatter_plot


def _create_heat_stencil_plots_by_thread_counts():
    benchmark_name = "heat-stencil"

    parameters = get_config("i7-3770_more-threads")
    i7_grouping_metric = parameters.thread_counts
    i7_energies, i7_times = process(parameters, benchmark_name, "i7-3770_more-threads", i7_grouping_metric, frequency=2100)
    i7_powers = [energy / time for energy, time in zip(i7_energies, i7_times)]
    i7_speed_up = [i7_times[0] / time for time in i7_times]

    i7_energies_data = [(i7_grouping_metric, i7_energies)]
    i7_times_data = [(i7_grouping_metric, i7_times)]
    i7_powers_data = [(i7_grouping_metric, i7_powers)]
    i7_energies_times_data = [(i7_times, i7_energies)]

    r7_parameters = get_config("R7-5800X_new")
    r7_grouping_metric = r7_parameters.thread_counts
    r7_energies, r7_times = process(r7_parameters, benchmark_name, "R7-5800X_new", r7_grouping_metric, frequency=2200)
    r7_powers = [energy / time for energy, time in zip(r7_energies, r7_times)]
    r7_speed_up = [r7_times[0] / time for time in r7_times]

    r7_energies_data = [(r7_grouping_metric, r7_energies)]
    r7_times_data = [(r7_grouping_metric, r7_times)]
    r7_powers_data = [(r7_grouping_metric, r7_powers)]
    r7_energies_times_data = [(r7_times, r7_energies)]

    both_energies_data = [(i7_grouping_metric, i7_energies), (r7_grouping_metric, r7_energies)]
    both_times_data = [(i7_grouping_metric, i7_times), (r7_grouping_metric, r7_times)]
    both_powers_data = [(i7_grouping_metric, i7_powers), (r7_grouping_metric, r7_powers)]
    both_energies_times_data = [(i7_times, i7_energies), (r7_times, r7_energies)]
    both_speed_up = [(i7_grouping_metric, i7_speed_up), (r7_grouping_metric, r7_speed_up)]

    create_scatter_plot(both_speed_up, "thread_count", "speed up", "Heat Stencil: speed up on different thread counts", ["i7 3770 - 2100 MHz", "R7 5800X - 2200 MHz"], "upper left")
    create_scatter_plot(both_energies_data, "thread_count", "energy [J]", "Heat Stencil: energy consumption on different thread counts", ["i7 3770 - 2100 MHz", "R7 5800X - 2200 MHz"], "upper right")
    create_scatter_plot(both_times_data, "thread count", "time [s]", "Heat Stencil: wall time on different thread counts", ["i7 3770 - 2100 MHz", "R7 5800X - 2200 MHz"], "upper right")
    create_scatter_plot(both_powers_data, "thread count", "power [W]", "Heat Stencil: power draw on different thread counts", ["i7 3770 - 2100 MHz", "R7 5800X - 2200 MHz"], "upper left")
    # create_scatter_plot(both_energies_times_data, "times", "energies", "energy/time heat stencil", ["i7 3770", "R7 5800X"], "upper right")


def _create_heat_stencil_plots_by_frequencies():
    benchmark_name = "heat-stencil"

    parameters = get_config("i7-3770_new")
    i7_grouping_metric = parameters.limits
    i7_energies, i7_times = process(parameters, benchmark_name, "i7-3770_new", i7_grouping_metric, thread_count=4)
    i7_powers = [energy / time for energy, time in zip(i7_energies, i7_times)]
    i7_speed_up = [i7_times[0]/time for time in i7_times]

    i7_energies_data = [(i7_grouping_metric, i7_energies)]
    i7_times_data = [(i7_grouping_metric, i7_times)]
    i7_powers_data = [(i7_grouping_metric, i7_powers)]
    i7_energies_times_data = [(i7_times, i7_energies)]

    r7_parameters = get_config("R7-5800X_smaller-vectors")
    r7_grouping_metric = r7_parameters.limits
    r7_energies, r7_times = process(r7_parameters, benchmark_name, "R7-5800X_smaller-vectors", r7_grouping_metric, thread_count=4)
    r7_powers = [energy / time for energy, time in zip(r7_energies, r7_times)]
    r7_speed_up = [r7_times[0] / time for time in r7_times]

    r7_energies_data = [(r7_grouping_metric, r7_energies)]
    r7_times_data = [(r7_grouping_metric, r7_times)]
    r7_powers_data = [(r7_grouping_metric, r7_powers)]
    r7_energies_times_data = [(r7_times, r7_energies)]

    both_energies_data = [(i7_grouping_metric, i7_energies), (r7_grouping_metric, r7_energies)]
    both_times_data = [(i7_grouping_metric, i7_times), (r7_grouping_metric, r7_times)]
    both_powers_data = [(i7_grouping_metric, i7_powers), (r7_grouping_metric, r7_powers)]
    both_energies_times_data = [(i7_times, i7_energies), (r7_times, r7_energies)]
    both_speed_up = [(i7_grouping_metric, i7_speed_up), (r7_grouping_metric, r7_speed_up)]

    create_scatter_plot(both_speed_up, "frequency [MHz]", "speedup", "Heat Stencil: speed up on different frequencies", ["i7 3770", "R7 5800X"], "upper left", x_ticks=i7_grouping_metric)
    create_scatter_plot(both_energies_data, "frequency [MHz]", "energy [J]", "Heat Stencil: energy consumption on different frequencies", ["i7 3770", "R7 5800X"], "upper left", x_ticks=i7_grouping_metric)
    create_scatter_plot(both_times_data, "frequency [MHz]", "time [s]", "Heat Stencil: wall time on different frequencies", ["i7 3770", "R7 5800X"], "upper right", x_ticks=i7_grouping_metric)
    create_scatter_plot(both_powers_data, "frequency [MHz]", "power [W]", "Heat Stencil: power draw on different frequencies", ["i7 3770", "R7 5800X"], "upper left", x_ticks=i7_grouping_metric)
    # create_scatter_plot(both_energies_times_data, "times", "energies", "energy/time heat stencil", ["i7 3770", "R7 5800X"], "upper right")


def _create_heat_stencil_plots_by_problem_size():
    benchmark_name = "heat-stencil"

    parameters = get_config("i7-3770_new")
    grouping_metric = parameters.map_sizes
    i7_energies, i7_times = process(parameters, benchmark_name, "i7-3770_new", grouping_metric, thread_count=4, frequency=2100)
    i7_powers = [energy / time for energy, time in zip(i7_energies, i7_times)]

    i7_energies_data = [(grouping_metric, i7_energies)]
    i7_times_data = [(grouping_metric, i7_times)]
    i7_powers_data = [(grouping_metric, i7_powers)]
    i7_energies_times_data = [(i7_times, i7_energies)]

    r7_parameters = get_config("R7-5800X_new")
    r7_grouping_metric = r7_parameters.map_sizes
    r7_energies, r7_times = process(r7_parameters, benchmark_name, "R7-5800X_new", r7_grouping_metric, thread_count=4, frequency=2200)
    r7_powers = [energy / time for energy, time in zip(r7_energies, r7_times)]

    r7_energies_data = [(r7_grouping_metric, r7_energies)]
    r7_times_data = [(r7_grouping_metric, r7_times)]
    r7_powers_data = [(grouping_metric, r7_powers)]
    r7_energies_times_data = [(r7_times, r7_energies)]

    both_energies_data = [(grouping_metric, i7_energies), (r7_grouping_metric, r7_energies)]
    both_times_data = [(grouping_metric, i7_times), (r7_grouping_metric, r7_times)]
    both_powers_data = [(grouping_metric, i7_powers), (r7_grouping_metric, r7_powers)]
    both_energies_times_data = [(i7_times, i7_energies), (r7_times, r7_energies)]

    create_scatter_plot(both_energies_data, "frequency [MHz]", "energy [J]", "energy consumption heat stencil", ["i7 3770", "R7 5800X"], "upper left")
    create_scatter_plot(both_times_data, "frequency [MHz]", "time [s]", "time heat stencil", ["i7 3770", "R7 5800X"], "upper right")
    create_scatter_plot(both_powers_data, "frequency [MHz]", "power [W]", "power consumption heat stencil", ["i7 3770", "R7 5800X"], "upper left")
    # create_scatter_plot(both_energies_times_data, "times", "energies", "energy/time heat stencil", ["i7 3770", "R7 5800X"], "upper right")


def _create_heat_stencil_plots_by_optimization():
    benchmark_name = "heat-stencil"

    parameters = get_config("i7-3770_new")
    i7_grouping_metric = parameters.optimization_flags
    i7_energies, i7_times = process(parameters, benchmark_name, "i7-3770_new", i7_grouping_metric, thread_count=4, frequency=2100)
    i7_powers = [energy / time for energy, time in zip(i7_energies, i7_times)]
    i7_speed_up = [i7_times[0] / time for time in i7_times]

    i7_energies_data = [(i7_grouping_metric, i7_energies)]
    i7_times_data = [(i7_grouping_metric, i7_times)]
    i7_powers_data = [(i7_grouping_metric, i7_powers)]
    i7_energies_times_data = [(i7_times, i7_energies)]

    r7_parameters = get_config("R7-5800X_new")
    r7_grouping_metric = r7_parameters.optimization_flags
    r7_energies, r7_times = process(r7_parameters, benchmark_name, "R7-5800X_new", r7_grouping_metric, thread_count=4, frequency=2200)
    r7_powers = [energy / time for energy, time in zip(r7_energies, r7_times)]
    r7_speed_up = [r7_times[0] / time for time in r7_times]

    r7_energies_data = [(r7_grouping_metric, r7_energies)]
    r7_times_data = [(r7_grouping_metric, r7_times)]
    r7_powers_data = [(i7_grouping_metric, r7_powers)]
    r7_energies_times_data = [(r7_times, r7_energies)]

    both_energies_data = [(i7_grouping_metric, i7_energies), (r7_grouping_metric, r7_energies)]
    both_times_data = [(i7_grouping_metric, i7_times), (r7_grouping_metric, r7_times)]
    both_powers_data = [(i7_grouping_metric, i7_powers), (r7_grouping_metric, r7_powers)]
    both_energies_times_data = [(i7_times, i7_energies), (r7_times, r7_energies)]
    both_speed_up = [(i7_grouping_metric, i7_speed_up), (r7_grouping_metric, r7_speed_up)]

    create_scatter_plot(both_speed_up, "optimization flag", "speed up", "Heat Stencil: speed up on different optimizations", ["i7 3770", "R7 5800X"], "upper left")
    create_scatter_plot(both_energies_data, "optimization flag", "energy [J]", "Heat Stencil: energy consumption on different optimizations", ["i7 3770", "R7 5800X"], "upper right")
    create_scatter_plot(both_times_data, "optimization flag", "time [s]", "Heat Stencil: wall time on different optimizations", ["i7 3770", "R7 5800X"], "upper right")
    create_scatter_plot(both_powers_data, "optimization flag", "power [W]", "Heat Stencil: power draw on different optimizations", ["i7 3770", "R7 5800X"], "center left")
    # create_scatter_plot(both_energies_times_data, "times", "energies", "energy/time heat stencil", ["i7 3770", "R7 5800X"], "upper right")


def _create_heat_stencil_plots_by_power_draw_thomson():
    benchmark_name = "heat-stencil"
    folder_name = "thomson_6p5-39w"
    parameters = get_config(folder_name)
    grouping_metric = parameters.limits

    energies_1t, times_1t = process(parameters, benchmark_name, folder_name, grouping_metric, thread_count=1)
    energies_2t, times_2t = process(parameters, benchmark_name, folder_name, grouping_metric, thread_count=2)
    energies_4t, times_4t = process(parameters, benchmark_name, folder_name, grouping_metric, thread_count=4)
    energies_6t, times_6t = process(parameters, benchmark_name, folder_name, grouping_metric, thread_count=6)
    energies_8t, times_8t = process(parameters, benchmark_name, folder_name, grouping_metric, thread_count=8)
    energies_16t, times_16t = process(parameters, benchmark_name, folder_name, grouping_metric, thread_count=16)

    powers_1t = [energy / time for energy, time in zip(energies_1t, times_1t)]
    powers_2t = [energy / time for energy, time in zip(energies_2t, times_2t)]
    powers_4t = [energy / time for energy, time in zip(energies_4t, times_4t)]
    powers_6t = [energy / time for energy, time in zip(energies_6t, times_6t)]
    powers_8t = [energy / time for energy, time in zip(energies_8t, times_8t)]
    powers_16t = [energy / time for energy, time in zip(energies_16t, times_16t)]

    speed_up_1t = [times_1t[0] / time for time in times_1t]
    speed_up_2t = [times_2t[0] / time for time in times_2t]
    speed_up_4t = [times_4t[0] / time for time in times_4t]
    speed_up_6t = [times_6t[0] / time for time in times_6t]
    speed_up_8t = [times_8t[0] / time for time in times_8t]
    speed_up_16t = [times_16t[0] / time for time in times_16t]

    plotting_grouping_metric = [gm/1e6 for gm in grouping_metric]

    energies_data = [(plotting_grouping_metric, energies_1t), (plotting_grouping_metric, energies_2t), (plotting_grouping_metric, energies_4t),
                     (plotting_grouping_metric, energies_6t), (plotting_grouping_metric, energies_8t), (plotting_grouping_metric, energies_16t)]

    speed_up_data = [(plotting_grouping_metric, speed_up_1t), (plotting_grouping_metric, speed_up_2t), (plotting_grouping_metric, speed_up_4t),
                     (plotting_grouping_metric, speed_up_6t), (plotting_grouping_metric, speed_up_8t), (plotting_grouping_metric, speed_up_16t)]

    times_data = [(plotting_grouping_metric, times_1t), (plotting_grouping_metric, times_2t), (plotting_grouping_metric, times_4t),
                  (plotting_grouping_metric, times_6t), (plotting_grouping_metric, times_8t), (plotting_grouping_metric, times_16t)]

    powers_data = [(plotting_grouping_metric, powers_1t), (plotting_grouping_metric, powers_2t), (plotting_grouping_metric, powers_4t),
                   (plotting_grouping_metric, powers_6t), (plotting_grouping_metric, powers_8t), (plotting_grouping_metric, powers_16t)]

    create_scatter_plot(speed_up_data, "power [W]", "speed up", "Heat Stencil: speed up on power limits",
                        ["1 thread", "2 threads", "4 threads", "6 threads", "8 threads", "16 threads"], "upper left", x_ticks=plotting_grouping_metric)
    create_scatter_plot(energies_data, "power [W]", "energy [J]", "Heat Stencil: energy consumption on power limits",
                        ["1 thread", "2 threads", "4 threads", "6 threads", "8 threads", "16 threads"], "upper right", x_ticks=plotting_grouping_metric)
    create_scatter_plot(times_data, "power [W]", "time [s]", "Heat Stencil: wall time on power limits",
                        ["1 thread", "2 threads", "4 threads", "6 threads", "8 threads", "16 threads"], "upper right", x_ticks=plotting_grouping_metric)
    create_scatter_plot(powers_data, "power [W]", "power [W]", "Heat Stencil: power draw on power limits",
                        ["1 thread", "2 threads", "4 threads", "6 threads", "8 threads", "16 threads"], "upper left", x_ticks=plotting_grouping_metric)
    # create_scatter_plot(both_energies_times_data, "times", "energies", "energy/time heat stencil", ["i7 3770", "R7 5800X"], "upper right")


if __name__ == "__main__":
    _create_heat_stencil_plots_by_power_draw_thomson()
