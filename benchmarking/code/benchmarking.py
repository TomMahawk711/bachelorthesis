import os
import subprocess
import glob
import time
import nltk
from parameters import Parameters
from tqdm import tqdm


# --------------------MAIN--------------------


def main(parameters):
    password = _read_password()
    _create_output_directory(parameters)
    _save_benchmarking_config(parameters)
    os.system("cd benchmarks && make")

    if parameters.limit_type == "power-limit":
        power_limit_benchmark(parameters, password)
    elif parameters.limit_type == "frequency-limit":
        frequency_limit_benchmark(parameters, password)
    else:
        print("usage: help message not yet created")
        return

    os.system("cd benchmarks && make clean")


def _read_password():
    with open("../password.txt") as file:
        password = file.readlines()
    return password


def _create_output_directory(parameters):
    for benchmark_name in parameters.benchmark_names:
        os.makedirs(f"outputs/{parameters.limit_type}_{parameters.start_time}/{benchmark_name}/")


def _save_benchmarking_config(parameters):
    # TODO: check if this works
    file = open(f"outputs/{parameters.limit_type}_{parameters.start_time}/benchmark-config.txt", "w+")
    file.write(
        f"benchmark_names:{parameters.benchmark_names}"
        f"start_time:{parameters.start_time}"
        f"iterations:{parameters.iterations}"
        f"limit_type:{parameters.limit_type}"
        f"limits:{parameters.limits}"
        f"thread_counts:{parameters.thread_counts}"
        f"vectorization_sizes:{parameters.vectorization_sizes}"
        f"vector_sizes:{parameters.vector_sizes}"
        f"map_sizes:{parameters.map_sizes}"
    )


# --------------------BENCHMARK_STUFF--------------------


def power_limit_benchmark(parameters, password):
    print("\nrunning power limiting benchmark...")
    os.system("modprobe intel_rapl_msr")
    _enable_cpu_zones(password)
    original_power_limit = _get_power_limit()

    for iteration in tqdm(range(0, parameters.iterations)):
        for limit in parameters.limits:
            _set_power(limit, password)
            _execute_benchmarks(parameters, limit, password, iteration)

    _set_power(original_power_limit, password)


def frequency_limit_benchmark(parameters, password):
    print("\nrunning frequency limiting benchmark...")
    _set_scaling_governor("userspace", password)

    for iteration in tqdm(range(0, parameters.iterations)):
        for limit in tqdm(parameters.limits):
            _set_frequency(limit, password)
            _execute_benchmarks(parameters, limit, password, iteration)

    _set_scaling_governor("ondemand", password)


def _execute_benchmarks(parameters, limit, password, iteration):
    # TODO: add new benchmarks in here, in a for loop if there is a parameter to loop through, also add it in the benchmarks attribute of
    #  the parameters object

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

        if "stream" in parameters.benchmark_names:
            pass


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

def get_config():
    my_min_value = 1600
    my_max_value = 4300
    my_step_size = 500

    my_benchmark_names = ["monte-carlo", "vector-operations", "heat-stencil", "stream"]
    my_start_time = time.strftime("%Y%m%d-%H%M%S")
    my_iterations = 10
    my_limit_type = "frequency-limit"
    my_limits = get_limits(my_min_value, my_max_value, my_step_size)
    my_thread_counts = [1, 2, 4, 8]
    my_vectorization_sizes = [1, 2, 4, 8, 16]
    my_vector_sizes = [512, 1024, 2048, 4096]
    my_map_sizes = [100, 200, 400, 800]

    return Parameters(my_benchmark_names, my_start_time, my_iterations, my_limit_type, my_limits, my_thread_counts,
                      my_vectorization_sizes, my_vector_sizes, my_map_sizes)


if __name__ == "__main__":
    main(get_config())
