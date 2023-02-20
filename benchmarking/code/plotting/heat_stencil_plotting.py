from data_processing import process, get_config
from plotting_templates import create_bar_plot, create_heatmap, create_scatter_plot


def _create_heat_stencil_plots_by_thread_counts():
    benchmark_name = "heat-stencil"

    parameters = get_config("i7-3770")
    grouping_metric = parameters.thread_counts
    i7_energies, i7_times = process(parameters, benchmark_name, "i7-3770", grouping_metric, frequency=2100)
    i7_powers = [energy / time for energy, time in zip(i7_energies, i7_times)]

    i7_energies_data = [(grouping_metric, i7_energies)]
    i7_times_data = [(grouping_metric, i7_times)]
    i7_powers_data = [(grouping_metric, i7_powers)]
    i7_energies_times_data = [(i7_times, i7_energies)]

    r7_parameters = get_config("R7-5800X")
    r7_grouping_metric = r7_parameters.thread_counts
    r7_energies, r7_times = process(r7_parameters, benchmark_name, "R7-5800X", r7_grouping_metric, frequency=2200)
    r7_powers = [energy / time for energy, time in zip(r7_energies, r7_times)]

    r7_energies_data = [(r7_grouping_metric, r7_energies)]
    r7_times_data = [(r7_grouping_metric, r7_times)]
    r7_powers_data = [(grouping_metric, r7_powers)]
    r7_energies_times_data = [(r7_times, r7_energies)]

    both_energies_data = [(grouping_metric, i7_energies), (r7_grouping_metric, r7_energies)]
    both_times_data = [(grouping_metric, i7_times), (r7_grouping_metric, r7_times)]
    both_powers_data = [(grouping_metric, i7_powers), (r7_grouping_metric, r7_powers)]
    both_energies_times_data = [(i7_times, i7_energies), (r7_times, r7_energies)]

    create_scatter_plot(both_energies_data, "thread_count", "energy [J]", "energy consumption heat stencil", ["i7 3770", "R7 5800X"], "upper left")
    create_scatter_plot(both_times_data, "thread count", "time [s]", "time heat stencil", ["i7 3770", "R7 5800X"], "upper right")
    create_scatter_plot(both_powers_data, "thread count", "power [W]", "power consumption heat stencil", ["i7 3770", "R7 5800X"], "upper left")
    # create_scatter_plot(both_energies_times_data, "times", "energies", "energy/time heat stencil", ["i7 3770", "R7 5800X"], "upper right")


def _create_heat_stencil_plots_by_frequencies():
    benchmark_name = "heat-stencil"

    parameters = get_config("i7-3770")
    grouping_metric = parameters.limits
    i7_energies, i7_times = process(parameters, benchmark_name, "i7-3770", grouping_metric, thread_count=4)
    i7_powers = [energy / time for energy, time in zip(i7_energies, i7_times)]

    i7_energies_data = [(grouping_metric, i7_energies)]
    i7_times_data = [(grouping_metric, i7_times)]
    i7_powers_data = [(grouping_metric, i7_powers)]
    i7_energies_times_data = [(i7_times, i7_energies)]

    r7_parameters = get_config("R7-5800X")
    r7_grouping_metric = r7_parameters.limits
    r7_energies, r7_times = process(r7_parameters, benchmark_name, "R7-5800X", r7_grouping_metric, thread_count=4)
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


def _create_heat_stencil_plots_by_problem_size():
    benchmark_name = "heat-stencil"

    parameters = get_config("i7-3770")
    grouping_metric = parameters.map_sizes
    i7_energies, i7_times = process(parameters, benchmark_name, "i7-3770", grouping_metric, thread_count=4, frequency=2100)
    i7_powers = [energy / time for energy, time in zip(i7_energies, i7_times)]

    i7_energies_data = [(grouping_metric, i7_energies)]
    i7_times_data = [(grouping_metric, i7_times)]
    i7_powers_data = [(grouping_metric, i7_powers)]
    i7_energies_times_data = [(i7_times, i7_energies)]

    r7_parameters = get_config("R7-5800X")
    r7_grouping_metric = r7_parameters.map_sizes
    r7_energies, r7_times = process(r7_parameters, benchmark_name, "R7-5800X", r7_grouping_metric, thread_count=4, frequency=2200)
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

    parameters = get_config("i7-3770")
    grouping_metric = parameters.optimization_flags
    i7_energies, i7_times = process(parameters, benchmark_name, "i7-3770", grouping_metric, thread_count=4, frequency=2100)
    i7_powers = [energy / time for energy, time in zip(i7_energies, i7_times)]

    i7_energies_data = [(grouping_metric, i7_energies)]
    i7_times_data = [(grouping_metric, i7_times)]
    i7_powers_data = [(grouping_metric, i7_powers)]
    i7_energies_times_data = [(i7_times, i7_energies)]

    r7_parameters = get_config("R7-5800X")
    r7_grouping_metric = r7_parameters.optimization_flags
    r7_energies, r7_times = process(r7_parameters, benchmark_name, "R7-5800X", r7_grouping_metric, thread_count=4, frequency=2200)
    r7_powers = [energy / time for energy, time in zip(r7_energies, r7_times)]

    r7_energies_data = [(r7_grouping_metric, r7_energies)]
    r7_times_data = [(r7_grouping_metric, r7_times)]
    r7_powers_data = [(grouping_metric, r7_powers)]
    r7_energies_times_data = [(r7_times, r7_energies)]

    both_energies_data = [(grouping_metric, i7_energies), (r7_grouping_metric, r7_energies)]
    both_times_data = [(grouping_metric, i7_times), (r7_grouping_metric, r7_times)]
    both_powers_data = [(grouping_metric, i7_powers), (r7_grouping_metric, r7_powers)]
    both_energies_times_data = [(i7_times, i7_energies), (r7_times, r7_energies)]

    create_scatter_plot(both_energies_data, "frequency [MHz]", "energy [J]", "energy consumption heat stencil", ["i7 3770", "R7 5800X"], "upper right")
    create_scatter_plot(both_times_data, "frequency [MHz]", "time [s]", "time heat stencil", ["i7 3770", "R7 5800X"], "upper right")
    create_scatter_plot(both_powers_data, "frequency [MHz]", "power [W]", "power consumption heat stencil", ["i7 3770", "R7 5800X"], "center left")
    # create_scatter_plot(both_energies_times_data, "times", "energies", "energy/time heat stencil", ["i7 3770", "R7 5800X"], "upper right")


if __name__ == "__main__":
    _create_heat_stencil_plots_by_optimization()
