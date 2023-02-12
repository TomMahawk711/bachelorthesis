from data_processing import process, get_config
from plotting_templates import create_bar_plot, create_heatmap, create_scatter_plot


def _create_heat_stencil_plots(folder_name):
    parameters = get_config(folder_name)
    benchmark_name = "monte-carlo"
    grouping_metric = parameters.limits
    energies, times = process(parameters, benchmark_name, folder_name, grouping_metric)

    powers = [energy / time for energy, time in zip(energies, times)]

    energies_data = [(grouping_metric, energies)]
    times_data = [(grouping_metric, times)]
    powers_data = [(grouping_metric, powers)]
    energies_times_data = [(times, energies)]

    create_scatter_plot(energies_data, "frequencies", "energy []", "energy consumption heat stencil", folder_name)
    create_scatter_plot(times_data, "frequencies", "time", "time heat stencil", folder_name)
    create_scatter_plot(powers_data, "frequencies", "power", "power consumption heat stencil", folder_name)
    create_scatter_plot(energies_times_data, "times", "energies", "energy/time heat stencil", folder_name)


if __name__ == "__main__":
    _create_heat_stencil_plots("i7-3770")
