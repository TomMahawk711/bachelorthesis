import os
import subprocess
import glob
import time
import nltk
from tqdm import tqdm


# --------------------MAIN--------------------


def main():
    limit_type = "frequency-limit"
    min_value = 1600
    max_value = 4300
    step_size = 500
    iterations = 20
    num_benchmarks = 2

    result = _create_file(limit_type, "result")
    plot_data = _create_file(limit_type, "plot-data")
    plot_data.write(f"{limit_type},time\n")

    if limit_type == "power-limit":
        power_limit_benchmark(min_value, max_value, step_size, iterations,
                              limit_type, num_benchmarks, result, plot_data)

    elif limit_type == "frequency-limit":
        frequency_limit_benchmark(min_value, max_value, step_size, iterations,
                                  limit_type, num_benchmarks, result, plot_data)

    else:
        print("usage: help message not created yet")
        return

    # TODO: generate plots


def _create_file(limit_type, result_type):
    time_string = time.strftime("%Y%m%d-%H%M%S")
    return open(f"results/{limit_type}_{result_type}_{time_string}.txt", "w")


# --------------------BENCHMARK_STUFF--------------------


def power_limit_benchmark(min_value, max_value, step_size, iterations, limit_type, num_benchmarks, result, plot_data):
    print("\nrunning power limiting benchmark...")

    os.system("modprobe intel_rapl_msr")
    _enable_cpu_zones()
    original_power_limit = _get_power_limit()

    limits = [x for x in range(min_value, max_value, step_size)]

    for limit in tqdm(limits):
        _set_power(limit)
        _execute_benchmarks(iterations, limit, limit_type)
        
    _save_results(limit_type, limits, num_benchmarks, result, plot_data)
    _set_power(original_power_limit)
    _delete_outputs(limit_type)


def frequency_limit_benchmark(min_value, max_value, step_size, iterations,
                              limit_type, num_benchmarks, result, plot_data):
    print("\nrunning frequency limiting benchmark...")

    _set_scaling_governor("userspace")

    limits = [x for x in range(min_value, max_value, step_size)]

    for limit in tqdm(limits):
        _set_frequency(limit)
        _execute_benchmarks(iterations, limit, limit_type)

    _save_results(limit_type, limits, num_benchmarks, result, plot_data)
    _set_scaling_governor("ondemand")
    _delete_outputs(limit_type)


# TODO: fix sudo usage
# TODO: verify result for correctness? probably difficult to check for differing benchmarks
def _execute_benchmarks(iterations, limit, limit_type):
    benchmark_count = len(glob.glob1("benchmarks/", "*.out"))

    for i in range(0, iterations):
        for j in range(0, benchmark_count):
            subprocess.run([
                f"sudo perf stat -o outputs/{limit_type}/_benchmark{j}_{limit}MHz_iteration{i}.txt -e "
                f"power/energy-cores/ ./benchmarks/monte_carlo_par.out 1000000000 8"], shell=True)


def _save_results(limit_type, limits, num_benchmarks, result, plot_data):
    path = f"outputs/{limit_type}/"

    for i in range(0, num_benchmarks):
        for limit in limits:
            output_files = [file for file in os.listdir(path)
                            if os.path.isfile(os.path.join(path, file))
                            and f"{limit}" in file
                            and f"benchmark{i}" in file]
            output_files.sort()
            output_files.sort(key=len)

            result.write(f"\nBenchmark {i} {limit}: \n")

            for file in output_files:
                _write_results(file, limit_type, result, plot_data)


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
    return int(measurement)


def _delete_outputs(limit_type):
    print("deleting outputs...\n")
    files = glob.glob(f"outputs/{limit_type}/*")
    for f in files:
        os.remove(f)


# --------------------POWERCAP_STUFF--------------------


# TODO: fix sudo usage
def _enable_cpu_zones():
    os.system("echo 1234|sudo powercap-set -p intel-rapl -z 0 -e 1")
    os.system("echo 1234|sudo powercap-set -p intel-rapl -z 0:0 -e 1")


def _get_power_limit():
    output = os.popen("powercap-info -p intel-rapl").read()
    tokens = nltk.word_tokenize(output)
    power_limit_index = tokens.index("power_limit_uw") + 2
    return tokens[power_limit_index]


# TODO: fix sudo usage
def _set_power(power):
    os.system("echo 1234|sudo powercap-set -p intel-rapl -z 0 -c 0 -l %s" % power)
    os.system("echo 1234|sudo powercap-set -p intel-rapl -z 0 -c 1 -l %s" % power)
    os.system("echo 1234|sudo powercap-set -p intel-rapl -z 0:0 -c 0 -l %s" % power)


# --------------------CPUFREQ_STUFF--------------------


# TODO: fix sudo usage
def _set_scaling_governor(governor):
    os.system("echo 1234|sudo cpupower frequency-set --governor %s 2>&1 > /dev/null" % governor)


# TODO: fix sudo usage
def _set_frequency(frequency):
    os.system("echo 1234|sudo cpupower --cpu all frequency-set --freq %sMHz 2>&1 > /dev/null" % frequency)


# --------------------RUN--------------------


if __name__ == "__main__":
    main()
