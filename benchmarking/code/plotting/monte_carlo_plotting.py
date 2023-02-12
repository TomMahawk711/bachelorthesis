from data_processing import process, get_config
from plotting_templates import create_bar_plot, create_heatmap, create_scatter_plot


def _create_monte_carlo_plots(parameters):
    benchmark_name = "monte-carlo"
    folder_name = "i7-3770"
    grouping_metric = parameters.limits
    energies, times = process(parameters, benchmark_name, folder_name, grouping_metric, "AVX")

    mean_power = [e / t for e, t in zip(energies, times)]

    energies_data = [(grouping_metric, energies)]
    times_data = [(grouping_metric, times)]

    create_scatter_plot(energies_data, "frequencies", "energies", "energy consumption monte carlo", "i7-3770")
    create_scatter_plot(times_data, "frequencies", "energies", "energy consumption monte carlo", "i7-3770")


if __name__ == "__main__":
    _create_monte_carlo_plots(get_config("i7-3770"))
