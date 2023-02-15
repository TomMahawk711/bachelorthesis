import nltk
import os
import ast

from statistics import mean
from benchmarking.code.parameters import Parameters


def process(parameters, benchmark_name, folder_name, grouping_metric, thread_count=8, instruction_set="AVX", precision="double",
            frequency=3800, vector_size=1048576, optimization_flag="O1"):

    data, files = _get_data_per_benchmark_per_system(benchmark_name, folder_name, grouping_metric, thread_count, instruction_set, precision,
                                                     frequency, vector_size, optimization_flag)

    if benchmark_name == "stream":
        energies, times, copy, scale, add, triad = _extract_stream_data(data, files, grouping_metric)
        return _get_stream_means(parameters, energies, times, copy, scale, add, triad, grouping_metric)
    else:
        energies, times = _extract_data(data, files, grouping_metric)
        return _get_means(parameters, energies, times, grouping_metric)


def _get_data_per_benchmark_per_system(benchmark_name, folder_name, grouping_metric, thread_count, instruction_set, precision, frequency,
                                       vector_size, optimization_flag):
    # for every benchmark there is a separate list comprehension to get the corresponding files with measurements in it, there is one
    # variable parameter (grouping_metric) in the list comprehension by which the files will be grouped, all other parameters are fixed or
    # get fixed by passing additional parameters (e.g. parameter_4)

    path = _get_path(folder_name, benchmark_name)
    files_dict = dict()

    # TODO: make separate to group by threads or to group by frequencies/power limits
    if benchmark_name == "vector-operations":
        for limit in grouping_metric:

            files_dict[str(limit)] = \
                [file for file in os.listdir(path)
                 if f"_thread-count-{limit}_" in file
                 and f"_{frequency}MHz_" in file
                 and f"_instruction-set-{instruction_set}_" in file
                 and f"_vector-size-{vector_size}_" in file
                 and f"_precision-{precision}_" in file]

    elif benchmark_name == "monte-carlo":
        for limit in grouping_metric:

            files_dict[str(limit)] = \
                [file for file in os.listdir(path)
                 if f"thread-count-{limit}_" in file
                 and f"_{frequency}MHz_" in file
                 and f"_optimization-flag-{optimization_flag}_" in file
                 and f"_dot-count-640000000_" in file]

    elif benchmark_name == "heat-stencil":
        for limit in grouping_metric:

            files_dict[str(limit)] = \
                [file for file in os.listdir(path)
                 if f"thread-count-{thread_count}_" in file
                 and f"_{limit}MHz_" in file
                 and f"_optimization-flag-O2_" in file
                 and f"_map-size-400_" in file]

    elif benchmark_name == "stream":
        for limit in grouping_metric:

            files_dict[str(limit)] = \
                [file for file in os.listdir(path)
                 if f"thread-count-{thread_count}_" in file
                 and f"_{frequency}MHz_" in file
                 and f"_stream-array-size-{limit}_" in file]

    if benchmark_name == "stream":
        data_dict = _get_stream_data(files_dict, path)
    else:
        data_dict = _get_energy_time_data(files_dict, path)

    # print(files_dict)

    return data_dict, files_dict


def _get_path(folder_name, benchmark_name):
    path = f"../outputs/{folder_name}/"
    folders = [folder for folder in os.listdir(path) if benchmark_name in folder]

    return f"{path}{folders[0]}"


def _get_energy_time_data(files_dict, path):
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


def _get_stream_data(files_dict, path):
    plot_data_dict = dict()

    for key, value in files_dict.items():
        files_dict[key].sort()

        for file in files_dict[key]:
            with open(path + "/" + file) as f:
                output = f.read()

            tokens = nltk.word_tokenize(output)
            energy_measurement = _get_measurement(tokens, "Joules")
            time_measurement = _get_measurement(tokens, "seconds")
            copy_measurement = _get_stream_measurement(tokens, "Copy")
            scale_measurement = _get_stream_measurement(tokens, "Scale")
            add_measurement = _get_stream_measurement(tokens, "Add")
            triad_measurement = _get_stream_measurement(tokens, "Triad")

            plot_data_dict[file] = \
                (energy_measurement, time_measurement, copy_measurement, scale_measurement, add_measurement, triad_measurement)

    return plot_data_dict


def _extract_data(data, files, grouping_metric):
    energies = list()
    times = list()

    for limit in grouping_metric:
        for file in files[str(limit)]:
            energies.append(data[file][0])
            times.append(data[file][1])

    return energies, times


def _extract_stream_data(data, files, grouping_metric):
    energies = list()
    times = list()
    copy = list()
    scale = list()
    add = list()
    triad = list()

    for limit in grouping_metric:
        print(files)
        for file in files[str(limit)]:
            energies.append(data[file][0])
            times.append(data[file][1])
            copy.append(data[file][2])
            scale.append(data[file][3])
            add.append(data[file][4])
            triad.append(data[file][5])

    return energies, times, copy, scale, add, triad


def _get_means(parameters, energies, times, grouping_metric):
    energies_plot_data = list()
    times_plot_data = list()

    for index in range(len(grouping_metric)):
        start_index = parameters.iterations * index
        end_index = start_index + parameters.iterations - 1

        energies_plot_data.append(mean(energies[start_index:end_index+1]))
        times_plot_data.append(mean(times[start_index:end_index+1]))

    return energies_plot_data, times_plot_data


def _get_stream_means(parameters, energies, times, copy, scale, add, triad, grouping_metric):
    energies_plot_data = list()
    times_plot_data = list()
    copy_plot_data = list()
    scale_plot_data = list()
    add_plot_data = list()
    triad_plot_data = list()

    for index in range(len(grouping_metric)):
        start_index = parameters.iterations * index
        end_index = start_index + parameters.iterations - 1

        energies_plot_data.append(mean(energies[start_index:end_index]))
        times_plot_data.append(mean(times[start_index:end_index]))
        copy_plot_data.append(mean(copy[start_index:end_index]))
        scale_plot_data.append(mean(scale[start_index:end_index]))
        add_plot_data.append(mean(add[start_index:end_index]))
        triad_plot_data.append(mean(triad[start_index:end_index]))

    return energies_plot_data, times_plot_data, copy_plot_data, scale_plot_data, add_plot_data, triad_plot_data


def _get_measurement(tokens, metric):
    measurement_index = tokens.index(metric) - 1
    measurement = tokens[measurement_index]
    measurement = measurement.replace(",", "")
    return float(measurement)


def _get_stream_measurement(tokens, metric):
    measurement_index = tokens.index(metric) + 2
    measurement = tokens[measurement_index]
    measurement = measurement.replace(",", "")
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
    lines = open(f"../outputs/{folder_name}/benchmark-config.txt", "r").readlines()

    parameters = dict()
    for line in lines:
        middle_index = line.index(":")
        end_index = line.index("\n")
        parameters[line[0:middle_index]] = (line[middle_index + 1:end_index])

    return parameters


def _as_list(list_as_string):
    return list(map(int, list_as_string.strip('][').split(', ')))
