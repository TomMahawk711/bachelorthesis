from data_processing import process, get_config
from plotting_templates import create_bar_plot, create_heatmap, create_scatter_plot


def _create_heat_stencil_plots():
    folder_name = "i7-3770"
    parameters = get_config(folder_name)
    benchmark_name = "heat-stencil"
    grouping_metric = parameters.thread_counts
    energies, times = process(parameters, benchmark_name, folder_name, grouping_metric, frequency=2100)
    powers = [energy / time for energy, time in zip(energies, times)]

    energies_data = [(grouping_metric, energies)]
    times_data = [(grouping_metric, times)]
    powers_data = [(grouping_metric, powers)]
    energies_times_data = [(times, energies)]

    #create_scatter_plot(energies_data, "frequencies", "energy [J]", "energy consumption heat stencil", folder_name)
    #create_scatter_plot(times_data, "frequencies", "time", "time heat stencil", folder_name)
    #create_scatter_plot(powers_data, "frequencies", "power", "power consumption heat stencil", folder_name)
    #create_scatter_plot(energies_times_data, "times", "energies", "energy/time heat stencil", folder_name)

    r7_parameters = get_config("R7-5800X")
    r7_grouping_metric = r7_parameters.thread_counts
    r7_energies, r7_times = process(r7_parameters, benchmark_name, "R7-5800X", r7_grouping_metric, frequency=2200)
    r7_powers = [energy / time for energy, time in zip(r7_energies, r7_times)]

    r7_energies_data = [(r7_grouping_metric, r7_energies)]
    r7_times_data = [(r7_grouping_metric, r7_times)]

    # create_scatter_plot(r7_energies_data, "frequencies", "energy [J]", "energy consumption heat stencil", ["R7 5800X"], "upper left")
    # create_scatter_plot(times_data, "frequencies", "time", "time heat stencil", folder_name)
    # create_scatter_plot(powers_data, "frequencies", "power", "power consumption heat stencil", folder_name)
    # create_scatter_plot(energies_times_data, "times", "energies", "energy/time heat stencil", folder_name)

    both_energies_data = [(grouping_metric, energies), (r7_grouping_metric, r7_energies)]
    both_times_data = [(grouping_metric, times), (r7_grouping_metric, r7_times)]
    both_powers_data = [(grouping_metric, powers), (r7_grouping_metric, r7_powers)]
    both_energies_times_data = [(times, energies), (r7_times, r7_energies)]

    #create_scatter_plot(both_energies_data, "frequencies [MHz]", "energy [J]", "energy consumption heat stencil", ["i7 3770", "R7 5800X"], "upper left")
    #create_scatter_plot(both_times_data, "frequencies [MHz]", "time [s]", "time heat stencil", ["i7 3770", "R7 5800X"], "upper right")
    #create_scatter_plot(both_powers_data, "times [s]", "power [W]", "power heat stencil", ["i7 3770", "R7 5800X"], "upper left")
    create_scatter_plot(both_energies_times_data, "times", "energies", "energy/time heat stencil", ["i7 3770", "R7 5800X"], "upper left")


if __name__ == "__main__":
    _create_heat_stencil_plots()
