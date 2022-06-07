import csv
import os
import statistics

import matplotlib.pyplot as plt


class MeasurementParameters:
    def __init__(self, limits, iterations, num_benchmarks):
        self.limits = limits
        self.iterations = iterations
        self.num_benchmarks = num_benchmarks


def create_plots(measurement_parameters):
    data = _get_data_from_file()
    energy_per_benchmark_per_limit, time_per_benchmark_per_limit = _get_measurements(data, measurement_parameters)

    mean_energy_measurements = _get_mean_measurements(energy_per_benchmark_per_limit, measurement_parameters)
    mean_time_measurements = _get_mean_measurements(time_per_benchmark_per_limit, measurement_parameters)

    mean_power = [e / t for e, t in zip(mean_energy_measurements[0], mean_time_measurements[0])]

    x = measurement_parameters.limits
    y1 = mean_time_measurements[0]
    y2 = mean_power
    y3 = mean_energy_measurements[0]

    grid_x_size = 2
    grid_y_size = 2

    _create_scatter_plot(grid_x_size, grid_y_size, 1, "execution time/frequency", "frequency [MHz]", "time [s]", x, y1)
    _create_scatter_plot(grid_x_size, grid_y_size, 2, "power/frequency", "frequency [MHz]", "power [W]", x, y2)
    _create_scatter_plot(grid_x_size, grid_y_size, 3, "energy/frequency", "frequency [MHz]", "energy [J]", x, y3)
    _create_scatter_plot(grid_x_size, grid_y_size, 4, "execution time/energy", "time [s]", "energy [J]", y1, y3)

    plt.tight_layout()
    plt.savefig("test_plots.png")
    plt.show()


def _get_limits(min_value, max_value, step_size):
    return [x for x in range(min_value, max_value, step_size)]


def _get_data_from_file():
    path = "results/"
    plot_files = [file for file in os.listdir(path) if "plot-data" in file]
    plot_files.sort()
    plot_file = plot_files[-1]

    data = []
    with open(f"{path}{plot_file}", 'r') as file:
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
    for benchmark in range(0, measurement_parameters.num_benchmarks):
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

    for benchmark in range(0, measurement_parameters.num_benchmarks):
        mean_measurements[benchmark] = \
            _get_mean_measurements_aux(measurements_per_benchmark_per_limit, measurement_parameters, benchmark)

    return mean_measurements


def _get_mean_measurements_aux(measurements_per_benchmark_per_limit, measurement_parameters, benchmark):
    mean_measurements = []

    for limit in measurement_parameters.limits:
        measurements_float = [float(i) for i in measurements_per_benchmark_per_limit[benchmark, limit]]
        mean_measurements.append(statistics.mean(measurements_float))

    return mean_measurements


def _create_scatter_plot(x_size, y_size, position, title, x_label, y_label, x, y):
    plt.subplot(x_size, y_size, position)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.scatter(x, y)


my_min_value = 1600
my_max_value = 4300
my_step_size = 500
my_iterations = 3
my_num_benchmarks = 2

my_limits = _get_limits(my_min_value, my_max_value, my_step_size)
my_measurement_parameters = MeasurementParameters(my_limits, my_iterations, my_num_benchmarks)

create_plots(my_measurement_parameters)
