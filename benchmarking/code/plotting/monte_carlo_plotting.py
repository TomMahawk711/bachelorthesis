from data_processing import process, get_config
from plotting_templates import create_bar_plot, create_heatmap, create_scatter_plot


def _create_monte_carlo_plots(folder_name):
    parameters = get_config(folder_name)
    benchmark_name = "monte-carlo"
    grouping_metric = parameters.limits
    energies, times = process(parameters, benchmark_name, folder_name, grouping_metric)

    mean_power = [e / t for e, t in zip(energies, times)]

    energies_data = [(grouping_metric, energies)]
    times_data = [(grouping_metric, times)]

    create_scatter_plot(energies_data, "frequencies", "energies", "energy consumption monte carlo", folder_name)
    create_scatter_plot(times_data, "frequencies", "energies", "energy consumption monte carlo", folder_name)


if __name__ == "__main__":
    _create_monte_carlo_plots("i7-3770")
