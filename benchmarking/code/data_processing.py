import nltk
import os
import ast

from statistics import mean
from parameters import Parameters


def process(parameters, benchmark_name, folder_name, grouping_metric):
    data, files = _get_data_per_benchmark_per_system(parameters, benchmark_name, folder_name)
    energies, times = _extract_data(data, files, grouping_metric)

    return _get_means(parameters, energies, times, grouping_metric)


def _get_data_per_benchmark_per_system(parameters, benchmark_name, folder_name):
    path = _get_path(folder_name, benchmark_name)
    files_dict = dict()

    # for every benchmark, there is a separate list comprehension, one parameter should be variable, the others are fixed
    # to group by another parameter, the parameter-collection - over which the for loop iterates - has to be changed

    if benchmark_name == "vector-operations":
        for instruction_set in parameters.instruction_sets:
            files_dict[str(instruction_set)] = \
                [file for file in os.listdir(path)
                 if "thread-count-8_" in file
                 and f"_3600MHz" in file
                 and f"instruction-set-{instruction_set}_" in file
                 and "vector-size-4096_" in file
                 and "precision-single_" in file]

    elif benchmark_name == "monte-carlo":
        for limit in parameters.limits:
            files_dict[str(limit)] = \
                [file for file in os.listdir(path)
                 if f"thread-count-8_" in file
                 and f"_{limit}MHz_" in file
                 and f"_optimization-flag-O1_" in file
                 and f"_dot-count-640000000_" in file]

    elif benchmark_name == "heat-stencil":
        for limit in parameters.limits:
            files_dict[str(limit)] = \
                [file for file in os.listdir(path)
                 if f"thread-count-8_" in file
                 and f"_{limit}MHz_" in file
                 and f"_optimization-flag-O1_" in file
                 and f"_map-size-800_" in file]

    elif benchmark_name == "stream":
        for limit in parameters.limits:
            files_dict[str(limit)] = \
                [file for file in os.listdir(path)
                 if f"thread-count-8_" in file
                 and f"_{limit}MHz" in file
                 and f"_stream-array-size-100000000_" in file]

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


def _extract_data(data, files, grouping_metric):
    energies = list()
    times = list()

    for limit in grouping_metric:
        for file in files[str(limit)]:
            energies.append(data[file][0])
            times.append(data[file][1])

    return energies, times


def _get_means(parameters, energies, times, grouping_metric):
    energies_plot_data = list()
    times_plot_data = list()

    for index in range(len(grouping_metric)):
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

    return Parameters(ast.literal_eval(parameters["benchmark_names"]),
                      parameters["start_time"],
                      int(parameters["iterations"]),
                      parameters["limit_type"],
                      _as_list(parameters["limits"]),
                      _as_list(parameters["thread_counts"]),
                      _as_list(parameters["vectorization_sizes"]),
                      _as_list(parameters["vector_sizes"]),
                      ast.literal_eval(parameters["precisions"]),
                      ast.literal_eval(parameters["optimization_flags"]),
                      ast.literal_eval(parameters["instruction_sets"]),
                      _as_list(parameters["stream_array_sizes"]),
                      _as_list(parameters["map_sizes"]),
                      _as_list(parameters["dot_counts"]))


def _build_parameter_dict(folder_name):
    # limit_type, start_time = folder_name.split("_")
    lines = open(f"../outputs/{folder_name}/benchmark-config.txt", "r").readlines()

    parameters = dict()
    for line in lines:
        middle_index = line.index(":")
        end_index = line.index("\n")
        parameters[line[0:middle_index]] = (line[middle_index + 1:end_index])

    return parameters


def _as_list(list_as_string):
    return list(map(int, list_as_string.strip('][').split(', ')))
