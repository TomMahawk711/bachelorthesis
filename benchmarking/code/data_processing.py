import nltk
import os

from statistics import mean
from parameters import Parameters


def process(parameters, benchmark_name, folder_name):
    data, files = _get_data_per_benchmark_per_system(parameters, benchmark_name, folder_name)
    energies, times = _extract_data(parameters, data, files)

    return _get_means(parameters, energies, times)


def _get_data_per_benchmark_per_system(parameters, benchmark_name, folder_name):
    path = _get_path(folder_name, benchmark_name)
    files_dict = dict()

    # for every benchmark there is a separate list comprehension, one parameter should be variable, the other are fixed

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
                 if "thread-count-8" in file
                 and "4100MHz" in file
                 and f"vectorization-size-{vectorization_size}" in file
                 and "vector-size-4096" in file]

    if benchmark_name == "stream":
        for limit in parameters.limits:
            files_dict[str(limit)] = \
                [file for file in os.listdir(path)
                 if f"thread-count-8" in file
                 and f"{limit}MHz" in file]

    data_dict = _get_data(files_dict, path)
    return data_dict, files_dict


def _get_path(folder_name, benchmark_name):
    path = f"../outputs/{folder_name}/"
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


def _extract_data(parameters, data, files):
    energies = list()
    times = list()
    print(files)
    for limit in parameters.limits:     # parameter to iterate over has to be changed here...
        for file in files[str(limit)]:
            energies.append(data[file][0])
            times.append(data[file][1])

    return energies, times


def _get_means(parameters, energies, times):
    energies_plot_data = list()
    times_plot_data = list()

    for index in range(len(parameters.limits)):  # ...and here
        start_index = parameters.iterations * index
        end_index = start_index + parameters.iterations - 1

        energies_plot_data.append(mean(energies[start_index:end_index]))
        times_plot_data.append(mean(times[start_index:end_index]))

    return energies_plot_data, times_plot_data


def _get_measurement(tokens, unit):
    measurement_index = tokens.index(unit) - 1
    measurement = tokens[measurement_index]
    return float(measurement)


def get_config(folder_name):
    parameters = _build_parameter_dict(folder_name)

    return Parameters(parameters["benchmark_names"],
                      parameters["start_time"],
                      int(parameters["iterations"]),
                      parameters["limit_type"],
                      _as_list(parameters["limits"]),
                      _as_list(parameters["thread_counts"]),
                      _as_list(parameters["vectorization_sizes"]),
                      _as_list(parameters["vector_sizes"]),
                      _as_list(parameters["map_sizes"]))


def _build_parameter_dict(folder_name):
    limit_type, start_time = folder_name.split("_")
    lines = open(f"../outputs/{limit_type}_{start_time}/benchmark-config.txt", "r").readlines()

    parameters = dict()
    for line in lines:
        middle_index = line.index(":")
        end_index = line.index("\n")
        parameters[line[0:middle_index]] = (line[middle_index + 1:end_index])

    return parameters

def _as_list(list_as_string):
    return list(map(int, list_as_string.strip('][').split(', ')))