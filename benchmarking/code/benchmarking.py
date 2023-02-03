import os
import subprocess
import time
import nltk
from parameters import Parameters
from tqdm import tqdm


# --------------------MAIN--------------------


def main(parameters):
    password = _read_password()
    _create_output_directory(parameters)
    _save_config(parameters)

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


def _create_output_directory(parameters):
    for benchmark_name in parameters.benchmark_names:
        os.makedirs(f"../outputs/{parameters.limit_type}_{parameters.start_time}/{benchmark_name}/")
        if benchmark_name == "stream":
            os.makedirs(f"../outputs/{parameters.limit_type}_{parameters.start_time}/{benchmark_name}-temp/")


def _save_config(parameters):
    config_file = open(f"../outputs/{parameters.limit_type}_{parameters.start_time}/benchmark-config.txt", "w+")
    config_file.write(
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
        f"stream_array_sizes:{parameters.stream_array_sizes}\n"
        f"map_sizes:{parameters.map_sizes}\n"
        f"dot_counts:{parameters.dot_counts}\n"
    )


# --------------------BENCHMARK_STUFF--------------------


def power_limit_benchmark(parameters, password, perf_stat_command):
    print("\nrunning power limiting benchmark...")

    os.system("modprobe intel_rapl_msr >/dev/null")
    _enable_cpu_zones(password)
    original_power_limit = _get_power_limit()

    for iteration in tqdm(range(0, parameters.iterations), position=0, desc=f"iterations{9 * ' '}", leave=False, colour="#ff0000"):
        for limit in tqdm(parameters.limits, position=1, desc=f"frequency limits{3 * ' '}", leave=False, colour="#ff8000"):
            _set_power_limit(limit, password)
            _execute_benchmarks(parameters, limit, password, iteration, perf_stat_command)

    _set_power_limit(original_power_limit, password)


def frequency_limit_benchmark(parameters, password, perf_stat_command):
    print("\nrunning frequency limiting benchmark...")

    _set_scaling_governor("userspace", password)

    for iteration in tqdm(range(0, parameters.iterations), position=0, desc=f"iterations{9 * ' '}", leave=False, colour="#ff0000"):
        for limit in tqdm(parameters.limits, position=1, desc=f"frequency limits{3 * ' '}", leave=False, colour="#ff8000"):
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
    # add new benchmarks in here, in a for loop if there is a parameter to loop through,
    # also add it in the benchmarks attribute of the parameters object

    for thread_count in tqdm(parameters.thread_counts, position=2, desc=f"thread counts{6 * ' '}", leave=False, colour="#ffff00"):

        if "stream" in parameters.benchmark_names:
            _run_stream(iteration, limit, parameters, password, perf_stat_command, thread_count)

        for precision in tqdm(parameters.precisions, position=3, desc=f"precisions{9 * ' '}", leave=False, colour="#00ff00"):

            if "vector-operations" in parameters.benchmark_names:
                _run_vector_operations(iteration, limit, parameters, password, perf_stat_command, precision, thread_count)

        for optimization_flag in tqdm(parameters.optimization_flags, position=3, desc=f"optimization_flags{1 * ' '}", leave=False,
                                      colour="#00ff00"):

            if "monte-carlo" in parameters.benchmark_names:
                os.system(f"cd ../benchmarks && make monte_carlo OPTIMIZATION_FLAG={optimization_flag} >/dev/null")
                _run_monte_carlo(iteration, limit, optimization_flag, parameters, password, perf_stat_command, thread_count)

            if "heat-stencil" in parameters.benchmark_names:
                os.system(f"cd ../benchmarks && make heat_stencil OPTIMIZATION_FLAG={optimization_flag} >/dev/null")
                _run_heat_stencil(iteration, limit, optimization_flag, parameters, password, perf_stat_command, thread_count)


def _run_vector_operations(iteration, limit, parameters, password, perf_stat_command, precision, thread_count):

    for vector_size in tqdm(parameters.vector_sizes, position=4, desc=f"vector_size{8 * ' '}", leave=False, colour="#0000ff"):

        # TODO: run without vectorization

        for vectorization_size in tqdm(parameters.vectorization_sizes, position=5, desc="vectorization_sizes", leave=False,
                                       colour="#4b0082"):
            for instruction_set in tqdm(parameters.instruction_sets, position=6, desc=f"instruction_sets{3 * ' '}", leave=False,
                                        colour="#8000ff"):
                if not _valid_parameters_for_vectorization(vectorization_size, precision, instruction_set):
                    continue

                os.system(f"cd ../benchmarks && make vector_operations_{instruction_set}_{precision} "
                          f"VECTORIZATION_SIZE={vectorization_size} >/dev/null")

                subprocess.run([
                    f"echo {password}|sudo -S perf stat "
                    +
                    f"-o ../outputs/{parameters.limit_type}_{parameters.start_time}/vector-operations/"
                    +
                    f"vector-operations_instruction-set-{instruction_set}_precision-{precision}_vector-size-{vector_size}_"
                    f"vectorization-size-{vectorization_size}_thread-count-{thread_count}_{limit}MHz_iteration-{iteration}.txt "
                    +
                    f"-e power/energy-{perf_stat_command}/ "
                    +
                    f"./../benchmarks/vector_operations_{instruction_set}_{precision}.out {vector_size} {thread_count} > /dev/null"
                ], shell=True)


def _run_stream(iteration, limit, parameters, password, perf_stat_command, thread_count):
    for stream_array_size in tqdm(parameters.stream_array_sizes, position=4, desc=f"array_size{9 * ' '}", leave=False, colour="#0000ff"):

        os.system(f"cd ../benchmarks/stream && "
                  f"gcc -fopenmp -D_OPENMP -DSTREAM_ARRAY_SIZE={stream_array_size} stream.c -o stream_c.exe >/dev/null && "
                  f"export OMP_NUM_THREADS={thread_count} >/dev/null")

        subprocess.run([
            f"echo {password}|sudo -S perf stat "
            +
            f"-o ../outputs/{parameters.limit_type}_{parameters.start_time}/stream-temp/"
            +
            f"stream-temp_stream-array-size-{stream_array_size}_thread-count-{thread_count}_{limit}MHz_"
            f"iteration-{iteration}.txt "
            +
            f"-e power/energy-{perf_stat_command}/ "
            +
            f"./../benchmarks/stream/stream_c.exe >/dev/null"
        ], shell=True)

        subprocess.run([
            f"./../benchmarks/stream/stream_c.exe "
            +
            f"> ../outputs/{parameters.limit_type}_{parameters.start_time}/stream/"
            +
            f"stream_stream-array-size-{stream_array_size}_thread-count-{thread_count}_{limit}MHz_"
            f"iteration-{iteration}.txt"
        ], shell=True)

        os.system(f"cat ../outputs/{parameters.limit_type}_{parameters.start_time}/stream-temp/"
                  +
                  f"stream-temp_stream-array-size-{stream_array_size}_thread-count-{thread_count}_{limit}MHz_"
                  f"iteration-{iteration}.txt"
                  +
                  f" >> ../outputs/{parameters.limit_type}_{parameters.start_time}/stream/"
                  +
                  f"stream_stream-array-size-{stream_array_size}_thread-count-{thread_count}_{limit}MHz_"
                  f"iteration-{iteration}.txt")


def _run_monte_carlo(iteration, limit, optimization_flag, parameters, password, perf_stat_command, thread_count):
    for dot_count in tqdm(parameters.dot_counts, position=4, desc=f"dot_counts{9 * ' '}", leave=False, colour="#0000ff"):
        subprocess.run([
            f"echo {password}|sudo -S perf stat "
            +
            f"-o ../outputs/{parameters.limit_type}_{parameters.start_time}/monte-carlo/"
            +
            f"monte-carlo_dot-count-{dot_count}_optimization-flag-{optimization_flag}_thread-count-{thread_count}_{limit}MHz_"
            f"iteration-{iteration}.txt "
            +
            f"-e power/energy-{perf_stat_command}/ "
            +
            f"./../benchmarks/monte_carlo.out {dot_count} {thread_count} >/dev/null"
        ], shell=True)


def _run_heat_stencil(iteration, limit, optimization_flag, parameters, password, perf_stat_command, thread_count):
    for map_size in tqdm(parameters.map_sizes, position=4, desc=f"map_sizes{10 * ' '}", leave=False, colour="#0000ff"):
        subprocess.run([
            f"echo {password}|sudo -S perf stat "
            +
            f"-o ../outputs/{parameters.limit_type}_{parameters.start_time}/heat-stencil/"
            +
            f"heat-stencil_optimization-flag-{optimization_flag}_thread-count-{thread_count}_{limit}MHz_iteration-{iteration}.txt "
            +
            f"-e power/energy-{perf_stat_command}/ "
            +
            f"./../benchmarks/heat_stencil.out {map_size} >/dev/null"
        ], shell=True)


def _valid_parameters_for_vectorization(vectorization_size, precision, instruction_set):
    if _invalid_sse_parameters(instruction_set, precision, vectorization_size) or \
            _invalid_sse2_parameters(instruction_set, precision, vectorization_size) or \
            _invalid_avx_parameters(instruction_set, precision, vectorization_size) or \
            _invalid_avx512_parameters(instruction_set, precision, vectorization_size):
        return False

    return True


def _invalid_sse_parameters(instruction_set, precision, vectorization_size):
    return instruction_set == "SSE" and (precision == "double" or vectorization_size != 4)


def _invalid_sse2_parameters(instruction_set, precision, vectorization_size):
    return instruction_set == "SSE2" and (precision == "single" or vectorization_size != 2)


def _invalid_avx_parameters(instruction_set, precision, vectorization_size):
    return instruction_set == "AVX" and ((precision == "single" and vectorization_size != 8) or
                                         (precision == "double" and vectorization_size != 4))


def _invalid_avx512_parameters(instruction_set, precision, vectorization_size):
    return instruction_set == "AVX512" and ((precision == "single" and vectorization_size != 16) or
                                            (precision == "double" and vectorization_size != 8))


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
    os.system(f"echo {password}|sudo cpupower frequency-set --governor %s 2>&1 >/dev/null" % governor)


def _set_frequency(frequency, password):
    os.system(f"echo {password}|sudo cpupower --cpu all frequency-set --freq %sMHz 2>&1 >/dev/null" % frequency)


# --------------------RUN--------------------


def initialize_parameters():
    my_min_value = 1600
    my_max_value = 4300
    my_step_size = 500

    my_benchmark_names = ["stream"]
    my_start_time = time.strftime("%Y%m%d-%H%M%S")
    my_iterations = 10
    my_limit_type = "frequency-limit"
    my_limits = [x for x in range(my_min_value, my_max_value, my_step_size)]
    my_limits = [2200, 2800, 3800]
    my_thread_counts = [1, 2, 4, 8, 16]
    my_vectorization_sizes = [1, 2, 4, 8, 16]
    my_vector_sizes = [512, 1024, 2048, 4096]
    my_precisions = ["single", "double"]
    my_optimization_flags = ["O0", "O1", "O2", "O3", "Os"]
    my_instruction_sets = ["SSE", "SSE2", "AVX"]
    my_stream_array_sizes = [100000, 200000, 400000, 800000, 1600000, 3200000, 6400000, 12800000, 25600000, 51200000]
    my_map_sizes = [100, 200, 400, 800]
    my_dot_counts = [10000000, 20000000, 40000000, 80000000, 160000000, 320000000, 640000000]

    return Parameters(my_benchmark_names, my_start_time, my_iterations, my_limit_type, my_limits, my_thread_counts,
                      my_vectorization_sizes, my_vector_sizes, my_precisions, my_optimization_flags, my_instruction_sets,
                      my_stream_array_sizes, my_map_sizes, my_dot_counts)


if __name__ == "__main__":
    main(initialize_parameters())
