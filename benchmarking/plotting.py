import csv
import nltk
import os
import time
import matplotlib.pyplot as plt

from statistics import mean
from benchmarking import MeasurementParameters, get_limits


def create_plots(measurement_parameters):
    # TODO: split up into several functions

    data, files = _get_data_vectorization(measurement_parameters, "vector-operations")
    energies = list()
    times = list()

    for vectorization_size in measurement_parameters.vectorization_sizes:
        for file in files[str(vectorization_size)]:
            energies.append(data[file][0])
            times.append(data[file][1])

    energies_plot_data = list()
    times_plot_data = list()

    for index in range(len(measurement_parameters.vectorization_sizes)):
        start_index = measurement_parameters.iterations * index
        end_index = start_index + measurement_parameters.iterations - 1

        energies_plot_data.append(mean(energies[start_index:end_index]))
        times_plot_data.append(mean(times[start_index:end_index]))

    print(energies_plot_data)
    print(times_plot_data)

    x = measurement_parameters.vectorization_sizes
    mean_power = [e/t for e, t in zip(energies_plot_data, times_plot_data)]

    grid_x_size = 2
    grid_y_size = 2

    _create_scatter_plot(grid_x_size, grid_y_size, 1, "vectorization size/frequency", "vectorization size", "time [s]", x, times_plot_data)
    _create_scatter_plot(grid_x_size, grid_y_size, 2, "vectorization size/energy", "vectorization size", "energy [J]", x, energies_plot_data)
    _create_scatter_plot(grid_x_size, grid_y_size, 3, "vectorization size/power", "vectorization size", "power [W]", x, mean_power)
    _create_scatter_plot(grid_x_size, grid_y_size, 4, "execution time/energy", "time [s]", "energy [J]", times_plot_data, energies_plot_data)

    plt.tight_layout()
    plt.grid()
    plt.savefig("test_plots.png")
    plt.show()


def _get_data_vectorization(parameters, benchmark_name):

    # TODO: put following five lines into a function
    path = "outputs/"
    folders = [folder for folder in os.listdir(path) if parameters.limit_type in folder]
    folders.sort()
    folders.sort(key=len)
    path += f"{folders[-1]}/{benchmark_name}"

    files_vectorization = dict()
    plot_data = dict()

    for vectorization_size in parameters.vectorization_sizes:
        files_vectorization[str(vectorization_size)] = \
            [file for file in os.listdir(path) if f"_vectorization-size-{vectorization_size}_" in file and "_vector-size-2048_" in file]

    for key, value in files_vectorization.items():
        files_vectorization[key].sort()

        for file in files_vectorization[key]:
            with open(path + "/" + file) as f:
                output = f.read()

            tokens = nltk.word_tokenize(output)
            energy_measurement = _get_measurement(tokens, "Joules")
            time_measurement = _get_measurement(tokens, "seconds")

            plot_data[file] = (energy_measurement, time_measurement)

    return plot_data, files_vectorization


def _get_measurement(tokens, unit):
    measurement_index = tokens.index(unit) - 1
    measurement = tokens[measurement_index]
    return float(measurement)


def _create_scatter_plot(x_size, y_size, position, title, x_label, y_label, x, y):
    plt.subplot(x_size, y_size, position)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x, y, marker="x")


if __name__ == "__main__":
    my_limit_type = "frequency-limit"

    my_min_value = 4100
    my_max_value = 4300
    my_step_size = 500
    my_limits = get_limits(my_min_value, my_max_value, my_step_size)

    my_iterations = 10
    my_thread_counts = [8]
    my_vectorization_sizes = [1, 2, 4, 8, 16]
    my_vector_sizes = [1024, 2048]
    my_benchmark_names = ["vector-operations"]
    my_start_time = time.strftime("%Y%m%d-%H%M%S")

    my_measurement_parameters = MeasurementParameters(my_limits, my_iterations, my_limit_type, my_thread_counts,
                                                      my_vectorization_sizes, my_vector_sizes, my_benchmark_names,
                                                      my_start_time)
    create_plots(my_measurement_parameters)
