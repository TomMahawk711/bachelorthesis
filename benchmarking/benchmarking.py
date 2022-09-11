import os
import subprocess
import glob
import time
import nltk
from tqdm import tqdm


class MeasurementParameters:
    def __init__(self, limits, iterations, limit_type, thread_counts, vectorization_sizes, vector_sizes, map_sizes, benchmark_names,
                 start_time):
        self.limits = limits
        self.iterations = iterations
        self.limit_type = limit_type
        self.thread_counts = thread_counts
        self.vectorization_sizes = vectorization_sizes
        self.vector_sizes = vector_sizes
        self.map_sizes = map_sizes
        self.benchmark_names = benchmark_names
        self.start_time = start_time


# --------------------MAIN--------------------


def main(measurement_parameters):
    result = dict()
    password = _read_password()
    _create_directory(measurement_parameters, result)
    os.system("cd benchmarks && make")

    if measurement_parameters.limit_type == "power-limit":
        power_limit_benchmark(measurement_parameters, result,  password)
    elif measurement_parameters.limit_type == "frequency-limit":
        frequency_limit_benchmark(measurement_parameters, result, password)
    else:
        print("usage: help message not yet created")
        return

    os.system("cd benchmarks && make clean")


def _read_password():
    with open("password.txt") as file:
        password = file.readlines()
    return password


def _create_directory(parameters, result):
    for benchmark_name in parameters.benchmark_names:
        os.makedirs(
            f"outputs/{parameters.limit_type}_{parameters.start_time}/{benchmark_name}/")

    os.mkdir(f"result/{parameters.limit_type}_{parameters.start_time}/")

    for benchmark_name in parameters.benchmark_names:
        result[benchmark_name] = _create_file(parameters, "result", benchmark_name)


def _create_file(parameters, result_type, benchmark_name):
    return open(f"{result_type}/{parameters.limit_type}_{parameters.start_time}/{benchmark_name}.txt", "w")


# --------------------BENCHMARK_STUFF--------------------


def power_limit_benchmark(parameters, result, password):
    print("\nrunning power limiting benchmark...")
    os.system("modprobe intel_rapl_msr")
    _enable_cpu_zones(password)
    original_power_limit = _get_power_limit()

    for iteration in tqdm(range(0, parameters.iterations)):
        for limit in parameters.limits:
            _set_power(limit, password)
            _execute_benchmarks(parameters, limit, password, iteration)

    _save_results(parameters, result)
    _set_power(original_power_limit, password)


def frequency_limit_benchmark(parameters, result, password):
    print("\nrunning frequency limiting benchmark...")
    _set_scaling_governor("userspace", password)

    for iteration in tqdm(range(0, parameters.iterations)):
        for limit in tqdm(parameters.limits):
            _set_frequency(limit, password)
            _execute_benchmarks(parameters, limit, password, iteration)

    _save_results(parameters, result)
    _set_scaling_governor("ondemand", password)


def _execute_benchmarks(parameters, limit, password, iteration):
    # TODO: add new benchmarks in here, in a for loop if there is a parameter to loop through, also add it in the benchmarks attribute of
    #  the parameters object
    # TODO: fix path of output file for heat stencil

    for thread_count in parameters.thread_counts:

        if "monte-carlo" in parameters.benchmark_names:
            subprocess.run([
                f"echo {password}|sudo perf stat -o outputs/{parameters.limit_type}_{parameters.start_time}/monte-carlo/"
                f""
                f"monte-carlo_thread-count-{thread_count}_{limit}MHz_iteration-{iteration}.txt "
                f""
                f"-e power/energy-cores/ ./benchmarks/monte_carlo.out 100000000 {thread_count}"
            ], shell=True)

        if "vector-operations" in parameters.benchmark_names:
            for vectorization_size in parameters.vectorization_sizes:
                for vector_size in parameters.vector_sizes:
                    os.system(f"cd benchmarks && make vector_operations VECTORIZATION_SIZE={vectorization_size}")

                    subprocess.run([
                        f"echo {password}|sudo perf stat -o outputs/{parameters.limit_type}_{parameters.start_time}/vector-operations/"
                        f""
                        f"vector-operations_vectorization-size-{vectorization_size}_vector-size-{vector_size}_thread-count-{thread_count}_"
                        f"{limit}MHz_iteration-{iteration}.txt "
                        f""
                        f"-e power/energy-cores/ ./benchmarks/vector_operations_float.out {vector_size}"
                    ], shell=True)

        if "heat-stencil" in parameters.benchmark_names:
            for map_size in parameters.map_sizes:
                subprocess.run([
                    f"echo {password}|sudo perf stat -o outputs/{parameters.limit_type}_{parameters.start_time}/heat-stencil/"
                    f""
                    f"heat-stencil_thread-count-{thread_count}_map-size-{map_size}_{limit}MHz_iteration-{iteration}.txt "
                    f""
                    f"-e power/energy-cores/ ./benchmarks/heat_stencil.out {map_size}"
                ], shell=True)

        if "streammaster" in parameters.benchmark_names:
            pass


def _save_results(parameters, result):
    for benchmark_name in parameters.benchmark_names:
        path = f"outputs/{parameters.limit_type}_{parameters.start_time}/{benchmark_name}/"

        for limit in parameters.limits:

            output_files = [file for file in os.listdir(path)
                            if os.path.isfile(os.path.join(path, file))
                            and f"{limit}" in file
                            and f"{benchmark_name}" in file]
            output_files.sort()
            output_files.sort(key=len)

            result[benchmark_name].write(f"\n{benchmark_name} {limit}: \n")

            for file in output_files:
                _write_results(file, parameters, result, benchmark_name)


def _write_results(file, parameters, result, benchmark_name):
    with open(f"outputs/{parameters.limit_type}_{parameters.start_time}/{benchmark_name}/{file}") as f:
        output = f.read()

    start_index = file.find("iteration") + 9
    end_index = file.find(".txt")
    iteration = file[start_index:end_index]

    tokens = nltk.word_tokenize(output)
    energy_measurement = _get_measurement(tokens, "Joules")
    time_measurement = _get_measurement(tokens, "seconds")

    result[benchmark_name].write(f"Iteration {iteration}:\n")
    result[benchmark_name].write(f"energy: {energy_measurement}J | time: {time_measurement}s\n")


def _get_measurement(tokens, unit):
    measurement_index = tokens.index(unit) - 1
    measurement = tokens[measurement_index]
    return float(measurement)


def _delete_old_outputs(parameters):
    # TODO: update for new directory structure

    print("\n deleting old outputs...")
    for benchmark_name in parameters.benchmark_names:
        files = glob.glob(f"outputs/{benchmark_name}/{parameters.limit_type}/*")
        for f in files:
            os.remove(f)


def get_limits(min_value, max_value, step_size):
    return [x for x in range(min_value, max_value, step_size)]


# --------------------POWERCAP_STUFF--------------------


def _enable_cpu_zones(password):
    os.system(f"echo {password}|sudo powercap-set -p intel-rapl -z 0 -e 1")
    os.system(f"echo {password}|sudo powercap-set -p intel-rapl -z 0:0 -e 1")


def _get_power_limit():
    output = os.popen("powercap-info -p intel-rapl").read()
    tokens = nltk.word_tokenize(output)
    power_limit_index = tokens.index("power_limit_uw") + 2
    return tokens[power_limit_index]


def _set_power(power, password):
    os.system(f"echo {password}|sudo powercap-set -p intel-rapl -z 0 -c 0 -l %s" % power)
    os.system(f"echo {password}|sudo powercap-set -p intel-rapl -z 0 -c 1 -l %s" % power)
    os.system(f"echo {password}|sudo powercap-set -p intel-rapl -z 0:0 -c 0 -l %s" % power)


# --------------------CPUFREQ_STUFF--------------------


def _set_scaling_governor(governor, password):
    os.system(f"echo {password}|sudo cpupower frequency-set --governor %s 2>&1 > /dev/null" % governor)


def _set_frequency(frequency, password):
    os.system(f"echo {password}|sudo cpupower --cpu all frequency-set --freq %sMHz 2>&1 > /dev/null" % frequency)


# --------------------RUN--------------------

my_limit_type = "frequency-limit"

my_min_value = 1600
my_max_value = 4300
my_step_size = 500
my_limits = get_limits(my_min_value, my_max_value, my_step_size)

my_iterations = 10
my_thread_counts = [1, 2, 4, 8]
my_vectorization_sizes = [1, 2, 4, 8, 16]
my_vector_sizes = [512, 1024, 2048, 4096]
my_map_sizes = [100, 200, 400, 800]
my_benchmark_names = ["monte-carlo", "vector-operations", "streammaster"]
my_start_time = time.strftime("%Y%m%d-%H%M%S")

my_measurement_parameters = MeasurementParameters(my_limits, my_iterations, my_limit_type, my_thread_counts, my_vectorization_sizes,
                                                  my_vector_sizes, my_map_sizes, my_benchmark_names, my_start_time)

if __name__ == "__main__":
    main(my_measurement_parameters)
