import matplotlib.pyplot as plt

from data_processing import process
from parameters import Parameters


def create_plots(parameters):
    energies_plot_data, times_plot_data = process(parameters, "monte-carlo")

    x = parameters.limits
    mean_power = [e / t for e, t in zip(energies_plot_data, times_plot_data)]

    grid_x_size = 2
    grid_y_size = 2

    # _create_scatter_plot(grid_x_size, grid_y_size, 1, "thread_count/time", "thread_count", "time [s]", x, times_plot_data)
    # _create_scatter_plot(grid_x_size, grid_y_size, 2, "thread_count/energy", "thread_count", "energy [J]", x, energies_plot_data)
    # _create_scatter_plot(grid_x_size, grid_y_size, 3, "thread_count/power", "thread_count", "power [W]", x, mean_power)
    _create_scatter_plot(grid_x_size, grid_y_size, 4, "execution time/energy", "time [s]", "energy [J]", times_plot_data, energies_plot_data)

    plt.tight_layout()
    plt.grid()
    plt.savefig("test_plots.png")
    plt.show()


def _create_scatter_plot(x_size, y_size, position, title, x_label, y_label, x, y):
    # ax = plt.subplot(x_size, y_size, position)
    plt.title(title)
    # ax.set_xscale("log", base=2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x, y, marker="x")


def _get_config(folder_name):
    limit_type, start_time = folder_name.split("_")
    lines = open(f"../outputs/{limit_type}_{start_time}/benchmark-config.txt", "w+").readlines()
    parameters = list()

    for line in lines:
        start_index = line.index(":")
        end_index = line.index("\n")
        parameters.append(line[start_index + 1:end_index])

    return Parameters(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6],
                      parameters[7], parameters[8])


if __name__ == "__main__":
    create_plots(_get_config())
