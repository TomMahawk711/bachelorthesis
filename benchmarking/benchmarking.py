import os
import subprocess
import glob
import time
import nltk
from tqdm import tqdm
from ploting import MeasurementParameters, get_limits


# --------------------MAIN--------------------


def main(measurement_parameters):
    result = _create_file(measurement_parameters.limit_type, "result")
    plot_data = _create_file(measurement_parameters.limit_type, "plot-data")
    plot_data.write(f"{measurement_parameters.limit_type},time\n")

    password = _read_password()

    if measurement_parameters.limit_type == "power-limit":
        power_limit_benchmark(measurement_parameters, result, plot_data, password)

    elif measurement_parameters.limit_type == "frequency-limit":
        frequency_limit_benchmark(measurement_parameters, result, plot_data, password)

    else:
        print("usage: help message not created yet")
        return

    _delete_outputs(measurement_parameters.limit_type)


def _read_password():
    with open("password.txt") as file:
        password = file.readlines()
    return password


def _create_file(limit_type, result_type):
    time_string = time.strftime("%Y%m%d-%H%M%S")
    return open(f"results/{limit_type}_{result_type}_{time_string}.txt", "w")


# --------------------BENCHMARK_STUFF--------------------


def power_limit_benchmark(parameters, result, plot_data, password):
    print("\nrunning power limiting benchmark...")
    os.system("modprobe intel_rapl_msr")
    _enable_cpu_zones(password)
    original_power_limit = _get_power_limit()

    for limit in tqdm(parameters.limits):
        _set_power(limit, password)
        _execute_benchmarks(parameters, limit, password)

    _save_results(parameters, result, plot_data)
    _set_power(original_power_limit, password)


def frequency_limit_benchmark(parameters, result, plot_data, password):
    print("\nrunning frequency limiting benchmark...")
    _set_scaling_governor("userspace", password)

    for limit in tqdm(parameters.limits):
        _set_frequency(limit, password)
        _execute_benchmarks(parameters, limit, password)

    _save_results(parameters, result, plot_data)
    _set_scaling_governor("ondemand", password)


# TODO: verify result for correctness? probably difficult to check for differing benchmarks
def _execute_benchmarks(parameters, limit, password):
    for i in range(0, parameters.iterations):
        for j in range(0, parameters.num_benchmarks):
            subprocess.run([
                f"echo {password}|sudo perf stat -o outputs/{parameters.limit_type}/"
                f"_benchmark{j}_{limit}MHz_iteration{i}.txt -e power/energy-cores/ "
                f"./benchmarks/{parameters.benchmarks[j]}"
            ], shell=True)


def _save_results(parameters, result, plot_data):
    path = f"outputs/{parameters.limit_type}/"

    for i in range(0, parameters.num_benchmarks):
        for limit in parameters.limits:
            output_files = [file for file in os.listdir(path)
                            if os.path.isfile(os.path.join(path, file))
                            and f"{limit}" in file
                            and f"benchmark{i}" in file]
            output_files.sort()
            output_files.sort(key=len)

            result.write(f"\nBenchmark {i} {limit}: \n")

            for file in output_files:
                _write_results(file, parameters.limit_type, result, plot_data)


def _write_results(file, limit_type, result, plot_data):
    with open(f"outputs/{limit_type}/{file}") as f:
        output = f.read()

    start_index = file.find("iteration") + 9
    end_index = file.find(".txt")
    iteration = file[start_index:end_index]

    tokens = nltk.word_tokenize(output)
    energy_measurement = _get_measurement(tokens, "Joules")
    time_measurement = _get_measurement(tokens, "seconds")

    result.write(f"Iteration {iteration}:\n")
    result.write(f"energy: {energy_measurement}J | time: {time_measurement}s\n")
    plot_data.write(f"{energy_measurement},{time_measurement}\n")


def _get_measurement(tokens, unit):
    measurement_index = tokens.index(unit) - 1
    measurement = tokens[measurement_index]
    return float(measurement)


def _delete_outputs(limit_type):
    print("deleting outputs...\n")
    files = glob.glob(f"outputs/{limit_type}/*")
    for f in files:
        os.remove(f)


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
my_iterations = 3
my_benchmarks = ["monte_carlo_par.out 10000000 8", "monte_carlo_ser.out 10000000 8"]
my_num_benchmarks = len(glob.glob1("benchmarks/", "*.out"))
my_threads = 0
my_vector_size = 0

my_limits = get_limits(my_min_value, my_max_value, my_step_size)
my_measurement_parameters = MeasurementParameters(my_limits, my_iterations, my_benchmarks, my_num_benchmarks,
                                                  my_limit_type, my_threads, my_vector_size)

if __name__ == "__main__":
    main(my_measurement_parameters)
