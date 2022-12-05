import nltk
import os
import matplotlib.pyplot as plt
import time

from statistics import mean
from MeasurementParameters import MeasurementParameters
from benchmarking import get_limits


def create_plots(measurement_parameters):
    # TODO: split up into several functions

    data_monte_carlo, files_monte_carlo = _get_data_per_benchmark_per_system(measurement_parameters, "monte-carlo", "intel-3770_full-test")

    print(f"data: {data_monte_carlo}")
    print(f"files: {files_monte_carlo}")

    energies = list()
    times = list()

    for limit in measurement_parameters.limits:
        for file in files_monte_carlo[str(limit)]:
            energies.append(data_monte_carlo[file][0])
            times.append(data_monte_carlo[file][1])

    energies_plot_data = list()
    times_plot_data = list()

    for index in range(len(measurement_parameters.limits)):
        start_index = measurement_parameters.iterations * index
        end_index = start_index + measurement_parameters.iterations - 1

        energies_plot_data.append(mean(energies[start_index:end_index]))
        times_plot_data.append(mean(times[start_index:end_index]))


    x = measurement_parameters.limits
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


def _get_data_per_benchmark_per_system(parameters, benchmark_name, processor):
    path = _get_path(processor, benchmark_name)
    files_dict = dict()

    if benchmark_name == "monte-carlo":
        for limit in parameters.limits:
            files_dict[str(limit)] = \
                [file for file in os.listdir(path)
                 if f"thread-count-8" in file and f"{limit}MHz" in file]

    elif benchmark_name == "vector-operations":
        for vectorization_size in parameters.vectorization_sizes:
            files_dict[str(vectorization_size)] = \
                [file for file in os.listdir(path)
                 if "thread-count-4" in file and "4100MHz" in file and f"vectorization-size-{vectorization_size}" in file and "vector-size-1024" in file]

    data_dict = _get_data(files_dict, path)
    return data_dict, files_dict


def _get_path(processor, benchmark_name):
    path = f"outputs/{processor}/"
    print(os.listdir(path))

    folders = [folder for folder in os.listdir(path) if benchmark_name in folder]

    return f"{path}{folders[-1]}"


def _get_data(files_dict, path):
    plot_data_dict = dict()

    for key, value in files_dict.items():
        files_dict[key].sort()

        for file in files_dict[key]:
            with open(path + "/" + file) as f:
                output = f.read()

            tokens = nltk.word_tokenize(output)
            energy_measurement = _get_measurement(tokens, "Joules")
            time_measurement = _get_measurement(tokens, "seconds")

            plot_data_dict[file] = (energy_measurement, time_measurement)

    return plot_data_dict


def _get_measurement(tokens, unit):
    measurement_index = tokens.index(unit) - 1
    measurement = tokens[measurement_index]
    return float(measurement)


def _create_scatter_plot(x_size, y_size, position, title, x_label, y_label, x, y):
    # ax = plt.subplot(x_size, y_size, position)
    plt.title(title)
    # ax.set_xscale("log", base=2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x, y, marker="x")


def _get_config():
    my_min_value = 1600
    my_max_value = 4300
    my_step_size = 500

    my_benchmark_names = ["monte-carlo", "vector-operations", "heat-stencil"]
    my_start_time = time.strftime("%Y%m%d-%H%M%S")
    my_iterations = 10
    my_limit_type = "frequency-limit"
    my_limits = get_limits(my_min_value, my_max_value, my_step_size)
    my_thread_counts = [1, 2, 4, 8]
    my_vectorization_sizes = [1, 2, 4, 8, 16]
    my_vector_sizes = [512, 1024, 2048, 4096]
    my_map_sizes = [100, 200, 400, 800]

    return MeasurementParameters(my_benchmark_names, my_start_time, my_iterations, my_limit_type, my_limits, my_thread_counts,
                                 my_vectorization_sizes, my_vector_sizes, my_map_sizes)


if __name__ == "__main__":
    create_plots(_get_config())
