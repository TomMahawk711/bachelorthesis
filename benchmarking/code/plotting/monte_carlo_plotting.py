from data_processing import process, get_config
from plotting_templates import create_scatter_plot


def _create_monte_carlo_plots_by_thread_counts():
    benchmark_name = "monte-carlo"

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

    create_scatter_plot(both_speed_up, "thread count", "speed up", "Monte Carlo: speed up on different thread counts", ["i7 3770 - 2100 MHz", "R7 5800X - 2200 MHz"], "upper left")
    create_scatter_plot(both_energies_data, "thread count", "energy [J]", "Monte Carlo: energy consumption on different thread counts", ["i7 3770 - 2100 MHz", "R7 5800X - 2200 MHz"], "upper right")
    create_scatter_plot(both_times_data, "thread count", "time [s]", "Monte Carlo: wall time on different thread counts", ["i7 3770 - 2100 MHz", "R7 5800X - 2200 MHz"], "upper right")
    create_scatter_plot(both_powers_data, "thread count", "power [W]", "Monte Carlo: power draw on different thread counts", ["i7 3770 - 2100 MHz", "R7 5800X - 2200 MHz"], "upper left")
    # create_scatter_plot(both_energies_times_data, "times", "energies", "energy/time Monte Carlo", ["i7 3770", "R7 5800X"], "upper right")


def _create_monte_carlo_plots_by_frequencies():
    benchmark_name = "monte-carlo"

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

    create_scatter_plot(both_speed_up, "frequency [MHz]", "speedup", "Monte Carlo: speed up on different frequencies", ["i7 3770", "R7 5800X"], "upper left", x_ticks=i7_grouping_metric)
    create_scatter_plot(both_energies_data, "frequency [MHz]", "energy [J]", "Monte Carlo: energy consumption on different frequencies", ["i7 3770", "R7 5800X"], "upper left", x_ticks=i7_grouping_metric)
    create_scatter_plot(both_times_data, "frequency [MHz]", "time [s]", "Monte Carlo: wall time on different frequencies", ["i7 3770", "R7 5800X"], "upper right", x_ticks=i7_grouping_metric)
    create_scatter_plot(both_powers_data, "frequency [MHz]", "power [W]", "Monte Carlo: power draw on different frequencies", ["i7 3770", "R7 5800X"], "upper left", x_ticks=i7_grouping_metric)
    # create_scatter_plot(both_energies_times_data, "times", "energies", "energy/time Monte Carlo", ["i7 3770", "R7 5800X"], "upper right")


def _create_monte_carlo_plots_by_problem_size():
    benchmark_name = "monte-carlo"

    parameters = get_config("i7-3770_smaller-vectors")
    grouping_metric = parameters.map_sizes
    i7_energies, i7_times = process(parameters, benchmark_name, "i7-3770_new", grouping_metric, thread_count=4, frequency=2100)
    i7_powers = [energy / time for energy, time in zip(i7_energies, i7_times)]

    i7_energies_data = [(grouping_metric, i7_energies)]
    i7_times_data = [(grouping_metric, i7_times)]
    i7_powers_data = [(grouping_metric, i7_powers)]
    i7_energies_times_data = [(i7_times, i7_energies)]

    r7_parameters = get_config("R7-5800X_smaller-vectors")
    r7_grouping_metric = r7_parameters.map_sizes
    r7_energies, r7_times = process(r7_parameters, benchmark_name, "R7-5800X_smaller-vectors", r7_grouping_metric, thread_count=4, frequency=2200)
    r7_powers = [energy / time for energy, time in zip(r7_energies, r7_times)]

    r7_energies_data = [(r7_grouping_metric, r7_energies)]
    r7_times_data = [(r7_grouping_metric, r7_times)]
    r7_powers_data = [(grouping_metric, r7_powers)]
    r7_energies_times_data = [(r7_times, r7_energies)]

    both_energies_data = [(grouping_metric, i7_energies), (r7_grouping_metric, r7_energies)]
    both_times_data = [(grouping_metric, i7_times), (r7_grouping_metric, r7_times)]
    both_powers_data = [(grouping_metric, i7_powers), (r7_grouping_metric, r7_powers)]
    both_energies_times_data = [(i7_times, i7_energies), (r7_times, r7_energies)]

    create_scatter_plot(both_energies_data, "frequency [MHz]", "energy [J]", "energy consumption Monte Carlo", ["i7 3770", "R7 5800X"], "upper left")
    create_scatter_plot(both_times_data, "frequency [MHz]", "time [s]", "time Monte Carlo", ["i7 3770", "R7 5800X"], "upper right")
    create_scatter_plot(both_powers_data, "frequency [MHz]", "power [W]", "power consumption Monte Carlo", ["i7 3770", "R7 5800X"], "upper left")
    # create_scatter_plot(both_energies_times_data, "times", "energies", "energy/time Monte Carlo", ["i7 3770", "R7 5800X"], "upper right")


def _create_monte_carlo_plots_by_optimization():
    benchmark_name = "monte-carlo"

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

    create_scatter_plot(both_speed_up, "optimization flag", "speed up", "Monte Carlo: speed up on different optimizations", ["i7 3770", "R7 5800X"], "lower right")
    create_scatter_plot(both_energies_data, "optimization flag", "energy [J]", "Monte Carlo: energy consumption on different optimizations", ["i7 3770", "R7 5800X"], "upper right")
    create_scatter_plot(both_times_data, "optimization flag", "time [s]", "Monte Carlo: wall time on different optimizations", ["i7 3770", "R7 5800X"], "upper right")
    create_scatter_plot(both_powers_data, "optimization flag", "power [W]", "Monte Carlo: power draw on different optimizations", ["i7 3770", "R7 5800X"], "center left")
    # create_scatter_plot(both_energies_times_data, "times", "energies", "energy/time Monte Carlo", ["i7 3770", "R7 5800X"], "upper right")


if __name__ == "__main__":
    _create_monte_carlo_plots_by_optimization()
