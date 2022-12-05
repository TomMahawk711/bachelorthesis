import nltk
import os

from statistics import mean


def process(parameters):
    data_monte_carlo, files_monte_carlo = _get_data_per_benchmark_per_system(parameters, "monte-carlo", "intel-3770_full-test")

    energies = list()
    times = list()

    for limit in parameters.limits:
        for file in files_monte_carlo[str(limit)]:
            energies.append(data_monte_carlo[file][0])
            times.append(data_monte_carlo[file][1])

    energies_plot_data = list()
    times_plot_data = list()

    for index in range(len(parameters.limits)):
        start_index = parameters.iterations * index
        end_index = start_index + parameters.iterations - 1

        energies_plot_data.append(mean(energies[start_index:end_index]))
        times_plot_data.append(mean(times[start_index:end_index]))

    return energies_plot_data, times_plot_data


def _get_data_per_benchmark_per_system(parameters, benchmark_name, processor):
    path = _get_path(processor, benchmark_name)
    files_dict = dict()

    if benchmark_name == "monte-carlo":
        for limit in parameters.limits:
            files_dict[str(limit)] = \
                [file for file in os.listdir(path)
                 if f"thread-count-8" in file
                 and f"{limit}MHz" in file]

    elif benchmark_name == "vector-operations":
        for vectorization_size in parameters.vectorization_sizes:
            files_dict[str(vectorization_size)] = \
                [file for file in os.listdir(path)
                 if "thread-count-4" in file
                 and "4100MHz" in file
                 and f"vectorization-size-{vectorization_size}" in file
                 and "vector-size-1024" in file]

    data_dict = _get_data(files_dict, path)
    return data_dict, files_dict


def _get_path(processor, benchmark_name):
    path = f"../outputs/{processor}/"
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
