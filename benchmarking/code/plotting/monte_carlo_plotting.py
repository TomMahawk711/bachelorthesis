from data_processing import process, get_config
from plotting_templates import create_bar_plot, create_heatmap, create_scatter_plot


def _create_monte_carlo_plots(folder_name):
    parameters = get_config(folder_name)
    benchmark_name = "monte-carlo"
    grouping_metric = parameters.limits
    energies, times = process(parameters, benchmark_name, folder_name, grouping_metric)
    powers = [energy / time for energy, time in zip(energies, times)]

    energies_data = [(grouping_metric, energies)]
    times_data = [(grouping_metric, times)]
    powers_data = [(grouping_metric, powers)]
    energies_times_data = [(times, energies)]

    #create_scatter_plot(energies_data, "frequencies", "energy [J]", "energy consumption monte carlo", folder_name)
    #create_scatter_plot(times_data, "frequencies", "time", "time monte carlo", folder_name)
    #create_scatter_plot(powers_data, "frequencies", "power", "power consumption monte carlo", folder_name)
    #create_scatter_plot(energies_times_data, "times", "energies", "energy/time monte carlo", folder_name)

    r7_parameters = get_config("R7-5800X")
    r7_grouping_metric = r7_parameters.limits
    r7_energies, r7_times = process(r7_parameters, benchmark_name, "R7-5800X", r7_grouping_metric, thread_count=8)
    r7_powers = [energy / time for energy, time in zip(r7_energies, r7_times)]

    r7_energies_data = [(r7_grouping_metric, r7_energies)]
    r7_times_data = [(r7_grouping_metric, r7_times)]

    both_energies_data = [(grouping_metric, energies), (r7_grouping_metric, r7_energies)]
    both_times_data = [(grouping_metric, times), (r7_grouping_metric, r7_times)]
    both_powers_data = [(grouping_metric, powers), (r7_grouping_metric, r7_powers)]

    #create_scatter_plot(both_energies_data, "frequencies [MHz]", "energy [J]", "energy consumption monte carlo", ["i7 3770", "R7 5800X"], "upper left")
    create_scatter_plot(both_times_data, "frequencies [MHz]", "time [s]", "time monte carlo", ["i7 3770", "R7 5800X"], "upper right")
    #create_scatter_plot(both_powers_data, "times [s]", "power [W]", "power monte carlo", ["i7 3770", "R7 5800X"], "upper left")


if __name__ == "__main__":
    _create_monte_carlo_plots("i7-3770")
