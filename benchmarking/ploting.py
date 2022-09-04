import csv
import nltk
import os
import statistics
import time
import matplotlib.pyplot as plt

from benchmarking import MeasurementParameters, get_limits


def create_plots(measurement_parameters):
    data, files = _get_data_vector(measurement_parameters, "vector-operations")

    data_as_list = list()

    for file in files["1"]:
        data_as_list += data[file]

    energies_as_list = data_as_list[2 - 1::2]
    times_as_list = data_as_list[::2]

    print(energies_as_list)
    print(times_as_list)

    # data_monte_carlo = _get_data_from_file("monte-carlo")
    # energy_per_benchmark_per_limit, time_per_benchmark_per_limit = _get_measurements(data_monte_carlo, measurement_parameters)
    #
    # mean_energy_measurements = _get_mean_measurements(energy_per_benchmark_per_limit, measurement_parameters)
    # mean_time_measurements = _get_mean_measurements(time_per_benchmark_per_limit, measurement_parameters)
    #
    # mean_power = [e / t for e, t in zip(mean_energy_measurements[0], mean_time_measurements[0])]
    #
    # x = measurement_parameters.limits
    # y1 = mean_time_measurements[0]
    # y2 = mean_power
    # y3 = mean_energy_measurements[0]
    #
    # grid_x_size = 2
    # grid_y_size = 2
    #
    # _create_scatter_plot(grid_x_size, grid_y_size, 1, "execution time/frequency", "frequency [MHz]", "time [s]", x, y1)
    # _create_scatter_plot(grid_x_size, grid_y_size, 2, "power/frequency", "frequency [MHz]", "power [W]", x, y2)
    # _create_scatter_plot(grid_x_size, grid_y_size, 3, "energy/frequency", "frequency [MHz]", "energy [J]", x, y3)
    # _create_scatter_plot(grid_x_size, grid_y_size, 4, "execution time/energy", "time [s]", "energy [J]", y1, y3)
    #
    # plt.tight_layout()
    # plt.grid()
    # plt.savefig("test_plots.png")
    # plt.show()


def _get_data_vector(parameters, benchmark_name):
    path = "outputs/"
    folders = [folder for folder in os.listdir(path) if parameters.limit_type in folder]
    folders.sort()
    folders.sort(key=len)
    path += f"{folders[-1]}/{benchmark_name}"

    files_vectorization = dict()
    plot_data = dict()

    files_vectorization["1"] = \
        [file for file in os.listdir(path) if "_vectorization-size-1_" in file and "_vector-size-2048_" in file]
    files_vectorization["2"] = \
        [file for file in os.listdir(path) if "_vectorization-size-2_" in file and "_vector-size-2048_" in file]
    files_vectorization["4"] = \
        [file for file in os.listdir(path) if "_vectorization-size-4_" in file and "_vector-size-2048_" in file]
    files_vectorization["8"] = \
        [file for file in os.listdir(path) if "_vectorization-size-8_" in file and "_vector-size-2048_" in file]
    files_vectorization["16"] = \
        [file for file in os.listdir(path) if "_vectorization-size-16_" in file and "_vector-size-2048_" in file]

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


def _get_data_from_file(benchmark_name):
    plot_files = []
    path = "plot-data/"
    folders = [f.path for f in os.scandir(path) if f.is_dir()]

    folders.sort()
    path = folders[-1]

    plot_files += [file for file in os.listdir(path) if benchmark_name in file]

    plot_files.sort()
    plot_file = plot_files[-1]

    data = []
    with open(f"{path}/{plot_file}", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data.append(row)

    return data


def _get_measurements(data, measurement_parameters):
    energy_per_benchmark_per_limit = {}
    time_per_benchmark_per_limit = {}

    start_index = 0
    end_index = measurement_parameters.iterations
    for benchmark in range(0, len(measurement_parameters.benchmark_names) - 1):
        for limit in measurement_parameters.limits:
            energy_per_benchmark_per_limit[benchmark, limit], time_per_benchmark_per_limit[benchmark, limit] = \
                _get_measurements_aux(data, start_index, end_index)

            start_index = end_index
            end_index = start_index + measurement_parameters.iterations

    return energy_per_benchmark_per_limit, time_per_benchmark_per_limit


def _get_measurements_aux(data, start_index, end_index):
    energy_measurements_per_benchmark_per_limit = []
    time_measurements_per_benchmark_per_limit = []

    for index in range(start_index, end_index):
        energy_measurements_per_benchmark_per_limit.append(data[index][0])
        time_measurements_per_benchmark_per_limit.append(data[index][1])

    return energy_measurements_per_benchmark_per_limit, time_measurements_per_benchmark_per_limit


def _get_mean_measurements(measurements_per_benchmark_per_limit, measurement_parameters):
    mean_measurements = {}

    for benchmark in range(0, len(measurement_parameters.benchmark_names) - 1):
        mean_measurements[benchmark] = \
            _get_mean_measurements_aux(measurements_per_benchmark_per_limit, measurement_parameters, benchmark)

    return mean_measurements


def _get_mean_measurements_aux(measurements_per_benchmark_per_limit, measurement_parameters, benchmark):
    mean_measurements = []

    for limit in measurement_parameters.limits:
        measurements_float = [float(i) for i in measurements_per_benchmark_per_limit[benchmark, limit]]
        mean_measurements.append(statistics.mean(measurements_float))

    return mean_measurements


# def _create_scatter_plot(x_size, y_size, position, title, x_label, y_label, x, y):
    # plt.subplot(x_size, y_size, position)
    # plt.title(title)
    # plt.xlabel(x_label)
    # plt.ylabel(y_label)
    # plt.plot(x, y, marker="x")
    # pass


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
