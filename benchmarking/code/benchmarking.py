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
    _save_config(parameters)
    os.system("cd ../benchmarks && make > /dev/null")

    perf_stat_command = "cores"
    if not _is_intel_system():
        perf_stat_command = "pkg"

    if parameters.limit_type == "power-limit":
        power_limit_benchmark(parameters, password, perf_stat_command)
    elif parameters.limit_type == "frequency-limit":
        frequency_limit_benchmark(parameters, password, perf_stat_command)
    else:
        print("usage: help message not yet created")
        return

    os.system("cd ../benchmarks && make clean > /dev/null")


def _read_password():
    with open("../password.txt") as file:
        password = file.readlines()
    return password


def _delete_old_outputs(parameters):
    # TODO: update for new directory structure

    print("\n deleting old outputs...")
    for benchmark_name in parameters.benchmark_names:
        files = glob.glob(f"outputs/{benchmark_name}/{parameters.limit_type}/*")
        for f in files:
            os.remove(f)


def _create_output_directory(parameters):
    for benchmark_name in parameters.benchmark_names:
        os.makedirs(f"../outputs/{parameters.limit_type}_{parameters.start_time}/{benchmark_name}/")


def _save_config(parameters):
    file = open(f"../outputs/{parameters.limit_type}_{parameters.start_time}/benchmark-config.txt", "w+")
    file.write(
        f"benchmark_names:{parameters.benchmark_names}\n"
        f"start_time:{parameters.start_time}\n"
        f"iterations:{parameters.iterations}\n"
        f"limit_type:{parameters.limit_type}\n"
        f"limits:{parameters.limits}\n"
        f"thread_counts:{parameters.thread_counts}\n"
        f"vectorization_sizes:{parameters.vectorization_sizes}\n"
        f"vector_sizes:{parameters.vector_sizes}\n"
        f"precisions:{parameters.precisions}\n"
        f"optimization_flags:{parameters.optimization_flags}\n"
        f"instruction_sets:{parameters.instruction_sets}\n"
    )


# --------------------BENCHMARK_STUFF--------------------


def power_limit_benchmark(parameters, password, perf_stat_command):
    print("\nrunning power limiting benchmark...")

    os.system("modprobe intel_rapl_msr")
    _enable_cpu_zones(password)
    original_power_limit = _get_power_limit()

    for iteration in tqdm(range(0, parameters.iterations)):
        for limit in parameters.limits:
            _set_power_limit(limit, password)
            _execute_benchmarks(parameters, limit, password, iteration, perf_stat_command)

    _set_power_limit(original_power_limit, password)


def frequency_limit_benchmark(parameters, password, perf_stat_command):
    print("\nrunning frequency limiting benchmark...")

    _set_scaling_governor("userspace", password)

    for iteration in tqdm(range(0, parameters.iterations)):
        for limit in tqdm(parameters.limits):
            _set_frequency(limit, password)
            _execute_benchmarks(parameters, limit, password, iteration, perf_stat_command)

    _set_scaling_governor("ondemand", password)


def _is_intel_system():
    os.system("lscpu > cpuinfo.txt")
    with open("cpuinfo.txt") as file:
        if "Intel" in file.read():
            os.system("rm cpuinfo.txt")
            return True

    os.system("rm cpuinfo.txt")
    return False


def _execute_benchmarks(parameters, limit, password, iteration, perf_stat_command):
    # TODO: add new benchmarks in here, in a for loop if there is a parameter to loop through, also add it in the benchmarks attribute of
    #  the parameters object

    for thread_count in parameters.thread_counts:

        if "vector-operations" in parameters.benchmark_names:

            for vectorization_size in parameters.vectorization_sizes:
                for vector_size in parameters.vector_sizes:
                    for precision in parameters.precisions:
                        for instruction_set in parameters.instruction_sets:

                            if not _valid_parameters_for_vectorization(vectorization_size, precision, instruction_set):
                                continue

                            os.system(f"cd ../benchmarks && make vector_operations_{instruction_set}_{precision} "
                                      f"VECTORIZATION_SIZE={vectorization_size} "
                                      f"> /dev/null")

                            subprocess.run([
                                f"echo {password}|sudo -S perf stat -o ../outputs/{parameters.limit_type}_{parameters.start_time}/"
                                f"vector-operations/"
                                f""
                                f"vector-operations_instruction-set-{instruction_set}_precision-{precision}_vector-size-{vector_size}_"
                                f"vectorization-size-{vectorization_size}_"
                                f"thread-count-{thread_count}_{limit}MHz_iteration-{iteration}.txt "
                                f""
                                f"-e power/energy-{perf_stat_command}/ "
                                f""
                                f"./../benchmarks/vector_operations_{instruction_set}_{precision}.out {vector_size} {thread_count}"
                            ], shell=True)

        for optimization_flag in parameters.optimization_flags:

            if "monte-carlo" in parameters.benchmark_names:
                subprocess.run([
                    f"echo {password}|sudo -S perf stat -o ../outputs/{parameters.limit_type}_{parameters.start_time}/monte-carlo/"
                    f""
                    f"monte-carlo_optimization-flag-{optimization_flag}_thread-count-{thread_count}_{limit}MHz_iteration-{iteration}.txt "
                    f""
                    f"-e power/energy-{perf_stat_command}/ ./../benchmarks/monte_carlo.out 100000000 {thread_count}"
                ], shell=True)

            if "heat-stencil" in parameters.benchmark_names:
                subprocess.run([
                    f"echo {password}|sudo -S perf stat "
                    f""
                    f"-o ../outputs/{parameters.limit_type}_{parameters.start_time}/heat-stencil/"
                    f""
                    f"heat-stencil_optimization-flag-{optimization_flag}_thread-count-{thread_count}_"
                    f"{limit}MHz_iteration-{iteration}.txt "
                    f""
                    f"-e power/energy-{perf_stat_command}/ "
                    f""
                    f"./../benchmarks/heat_stencil.out 400 > /dev/null"
                ], shell=True)

            if "stream" in parameters.benchmark_names:
                for stream_array_size in parameters.stream_array_sizes:
                    subprocess.run([
                        f"echo {password}|sudo -S perf stat "
                        f""
                        f"-o ../outputs/{parameters.limit_type}_{parameters.start_time}/stream/"
                        f""
                        f"stream_stream-array-size-{stream_array_size}_optimization-flag-{optimization_flag}_thread-count-{thread_count}_"
                        f"{limit}MHz_iteration-{iteration}.txt "
                        f""
                        f"-e power/energy-{perf_stat_command}/ "
                        f""
                        f"./../benchmarks/stream/stream_c.exe > /dev/null"
                    ], shell=True)


def _valid_parameters_for_vectorization(vectorization_size, precision, instruction_set):
    if instruction_set == "SSE" and (precision == "double" or vectorization_size > 4):
        return False

    elif instruction_set == "SSE2" and (precision == "single" or vectorization_size > 2):
        return False

    elif instruction_set == "AVX" and ((precision == "single" and vectorization_size > 8) or
                                       (precision == "double" and vectorization_size > 4)):
        return False

    elif instruction_set == "AVX512" and ((precision == "single" and vectorization_size > 16) or
                                          (precision == "double" and vectorization_size > 8)):
        return False

    return True


# --------------------POWERCAP_STUFF--------------------


def _enable_cpu_zones(password):
    os.system(f"echo {password}|sudo powercap-set -p intel-rapl -z 0 -e 1")
    os.system(f"echo {password}|sudo powercap-set -p intel-rapl -z 0:0 -e 1")


def _get_power_limit():
    output = os.popen("powercap-info -p intel-rapl").read()
    tokens = nltk.word_tokenize(output)
    power_limit_index = tokens.index("power_limit_uw") + 2
    return tokens[power_limit_index]


def _set_power_limit(power_limit, password):
    os.system(f"echo {password}|sudo powercap-set -p intel-rapl -z 0 -c 0 -l %s" % power_limit)
    os.system(f"echo {password}|sudo powercap-set -p intel-rapl -z 0 -c 1 -l %s" % power_limit)
    os.system(f"echo {password}|sudo powercap-set -p intel-rapl -z 0:0 -c 0 -l %s" % power_limit)


# --------------------CPUFREQ_STUFF--------------------


def _set_scaling_governor(governor, password):
    os.system(f"echo {password}|sudo cpupower frequency-set --governor %s 2>&1 > /dev/null" % governor)


def _set_frequency(frequency, password):
    os.system(f"echo {password}|sudo cpupower --cpu all frequency-set --freq %sMHz 2>&1 > /dev/null" % frequency)


# --------------------RUN--------------------

def initialize_parameters():
    my_min_value = 1600
    my_max_value = 4300
    my_step_size = 500

    my_benchmark_names = ["monte-carlo", "vector-operations", "heat-stencil"]
    my_start_time = time.strftime("%Y%m%d-%H%M%S")
    my_iterations = 10
    my_limit_type = "frequency-limit"
    my_limits = [x for x in range(my_min_value, my_max_value, my_step_size)]
    my_limits = [2200, 2800, 3800]
    my_thread_counts = [1, 2, 4, 8, 16]
    my_vectorization_sizes = [1, 2, 4, 8, 16]
    my_vector_sizes = [512, 1024, 2048, 4096, 16384, 65536]
    my_precisions = ["single", "double"]
    my_optimization_flags = ["O0", "O1", "O2", "O3", "Os"]
    my_instruction_sets = ["SSE", "SSE2", "AVX"]
    my_stream_array_sizes = [1e5, 1e6, 1e7, 1e8, 1e9, 1e10]

    return Parameters(my_benchmark_names, my_start_time, my_iterations, my_limit_type, my_limits, my_thread_counts,
                      my_vectorization_sizes, my_vector_sizes, my_precisions, my_optimization_flags, my_instruction_sets,
                      my_stream_array_sizes)


if __name__ == "__main__":
    main(initialize_parameters())
