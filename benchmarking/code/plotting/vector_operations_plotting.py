from data_processing import process, get_config
from plotting_templates import create_heatmap, create_scatter_plot


def _create_vectorization_heatmaps():
    folder_name = "R7-5800X_smaller-vectors"
    parameters = get_config(folder_name)
    benchmark_name = "vector-operations"
    grouping_metric = parameters.limits

    x_labels = parameters.limits
    y_labels = parameters.instruction_sets
    y_labels.remove("SSE2")

    sse_energies, sse_times = process(parameters, benchmark_name, folder_name, grouping_metric, "SSE")
    avx_energies, avx_times = process(parameters, benchmark_name, folder_name, grouping_metric, "AVX")

    energies_data = [sse_energies, avx_energies]
    times_data = [sse_times, avx_times]

    # _create_heatmap(energies_data, x_labels, y_labels, "title_a")
    create_heatmap(times_data, x_labels, y_labels, "title_b")


def _create_vectorization_scatter_plots_grouping_frequencies():
    folder_name = "i7-3770_smaller-vectors"
    parameters = get_config(folder_name)
    benchmark_name = "vector-operations"
    grouping_metric = parameters.limits

    sse_energies_2t, sse_times_2t = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE", precision="single", thread_count=2)
    avx_energies_2t, avx_times_2t = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="single", thread_count=2)

    sse_energies_4t, sse_times_4t = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE", precision="single", thread_count=4)
    avx_energies_4t, avx_times_4t = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="single", thread_count=4)

    sse_energies_8t, sse_times_8t = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE", precision="single", thread_count=8)
    avx_energies_8t, avx_times_8t = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="single", thread_count=8)

    energies_data = [(grouping_metric, sse_energies_2t), (grouping_metric, avx_energies_2t),
                     (grouping_metric, sse_energies_4t), (grouping_metric, avx_energies_4t),
                     (grouping_metric, sse_energies_8t), (grouping_metric, avx_energies_8t)]

    times_data = [(grouping_metric, sse_times_2t), (grouping_metric, avx_times_2t),
                  (grouping_metric, sse_times_4t), (grouping_metric, avx_times_4t),
                  (grouping_metric, sse_times_8t), (grouping_metric, avx_times_8t)]

    relative_energies = [1-(e1/e2) for e1, e2 in zip(sse_energies_2t, avx_energies_2t)]

    create_scatter_plot(energies_data, "frequencies [MHz]", "consumed energy [Joules]", "energy comparison of instruction sets",
                        ["SSE - 2 threads", "AVX - 2 threads", "SSE - 4 threads", "AVX - 4 threads", "SSE - 8 threads", "AVX - 8 threads"], "upper center")
    # create_scatter_plot(times_data, "frequencies [MHz]", "time [s]", "time comparison of instruction sets",
    # ["SSE - 2 threads", "AVX - 2 threads", "SSE - 4 threads", "AVX - 4 threads", "SSE - 8 threads", "AVX - 8 threads"], "upper right")
    # create_bar_plot(grouping_metric, relative_energies, "frequencies [MHz]", "relative energy difference", "relative energy difference SSE/AVX")


def _create_vectorization_scatter_plots_i7_grouping_threads():
    folder_name = "i7-3770_smaller-vectors"
    parameters = get_config(folder_name)
    benchmark_name = "vector-operations"
    grouping_metric = parameters.thread_counts

    energies_2100Mhz, times_2100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="NO-SPECIFIC", precision="single", frequency=2100)
    sse_energies_2100Mhz, sse_times_2100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE", precision="single", frequency=2100)
    avx_energies_2100Mhz, avx_times_2100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="single", frequency=2100)

    energies_3100Mhz, times_3100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="NO-SPECIFIC", precision="single", frequency=3100)
    sse_energies_3100Mhz, sse_times_3100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE", precision="single", frequency=3100)
    avx_energies_3100Mhz, avx_times_3100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="single", frequency=3100)

    energies_4100Mhz, times_4100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="NO-SPECIFIC", precision="single", frequency=4100)
    sse_energies_4100Mhz, sse_times_4100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE", precision="single", frequency=4100)
    avx_energies_4100Mhz, avx_times_4100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="single", frequency=4100)

    energies_data = [(grouping_metric, energies_2100Mhz), (grouping_metric, sse_energies_2100Mhz), (grouping_metric, avx_energies_2100Mhz),
                     (grouping_metric, energies_3100Mhz), (grouping_metric, sse_energies_3100Mhz), (grouping_metric, avx_energies_3100Mhz),
                     (grouping_metric, energies_4100Mhz), (grouping_metric, sse_energies_4100Mhz), (grouping_metric, avx_energies_4100Mhz)]

    times_data = [(grouping_metric, sse_times_2100Mhz), (grouping_metric, avx_times_2100Mhz),
                  (grouping_metric, sse_times_3100Mhz), (grouping_metric, avx_times_3100Mhz),
                  (grouping_metric, sse_times_4100Mhz), (grouping_metric, avx_times_4100Mhz)]

    relative_energies = [1 - (e1 / e2) for e1, e2 in zip(sse_energies_2100Mhz, avx_energies_2100Mhz)]

    # create_scatter_plot(energies_data, "frequencies [MHz]", "consumed energy [Joules]", "energy comparison of instruction sets",
    # ["SSE - 2100MHz", "AVX - 2100MHz", "SSE - 3100MHz", "AVX - 3100MHz", "SSE - 4100MHz", "AVX - 4100MHz"], "upper center")
    # TODO: show Philipp
    create_scatter_plot(times_data, "thread count", "time [s]", "time comparison of instruction sets",
                        ["SSE - 2100MHz", "AVX - 2100MHz", "SSE - 3100MHz", "AVX - 3100MHz", "SSE - 4100MHz", "AVX - 4100MHz"], "upper center")
    # create_bar_plot(grouping_metric, relative_energies, "frequencies [MHz]", "relative energy difference", "relative energy difference SSE/AVX")


def _create_vectorization_scatter_plots_r7_grouping_threads():
    folder_name = "R7-5800X_bigger-vectors"
    parameters = get_config(folder_name)
    benchmark_name = "vector-operations"
    grouping_metric = parameters.thread_counts

    # energies_2100Mhz, times_2100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="NO-SPECIFIC", precision="double", frequency=2200)
    # sse_energies_2100Mhz, sse_times_2100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE2", precision="double", frequency=2200)
    # avx_energies_2100Mhz, avx_times_2100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="double", frequency=2200)
    #
    # energies_3100Mhz, times_3100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="NO-SPECIFIC", precision="double", frequency=2800)
    # sse_energies_3100Mhz, sse_times_3100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE2", precision="double", frequency=2800)
    # avx_energies_3100Mhz, avx_times_3100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="double", frequency=2800)

    # energies_4100Mhz, times_4100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="NO-SPECIFIC", precision="double", frequency=3800)
    sse_energies_4100Mhz, sse_times_4100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE2", precision="double", frequency=3800, vector_size=262144)
    avx_energies_4100Mhz, avx_times_4100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="double", frequency=3800, vector_size=262144)

    sse_powers = [energy / time for energy, time in zip(sse_energies_4100Mhz, sse_times_4100Mhz)]
    avx_powers = [energy / time for energy, time in zip(avx_energies_4100Mhz, avx_times_4100Mhz)]

    energies_data = [(grouping_metric, sse_energies_4100Mhz), (grouping_metric, avx_energies_4100Mhz)]
    times_data = [(grouping_metric, sse_times_4100Mhz), (grouping_metric, avx_times_4100Mhz)]
    powers_data = [(grouping_metric, sse_powers), (grouping_metric, avx_powers)]

    # relative_energies = [1 - (e1 / e2) for e1, e2 in zip(sse_energies_2100Mhz, avx_energies_2100Mhz)]

    create_scatter_plot(powers_data, "thread count", "power draw [W]", "power consumption with different instruction sets and thread counts", ["SSE - 3800MHz", "AVX - 3800MHz"],
                        "upper center")
    create_scatter_plot(energies_data, "thread count", "consumed energy [Joules]", "energy comparison of instruction sets", ["SSE - 3800MHz", "AVX - 3800MHz"], "upper center")
    # TODO: show this Philipp
    create_scatter_plot(times_data, "thread count", "time [s]", "time comparison of instruction sets", ["SSE - 3800MHz", "AVX - 3800MHz"], "upper center")
    # create_bar_plot(grouping_metric, relative_energies, "frequencies [MHz]", "relative energy difference", "relative energy difference SSE/AVX")


def _create_vectorization_scatter_plots_r9_grouping_threads():
    folder_name = "R9-7900X_big-vector"
    parameters = get_config(folder_name)
    benchmark_name = "vector-operations"
    grouping_metric = parameters.thread_counts

    # energies_2100Mhz, times_2100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="NO-SPECIFIC", precision="double", frequency=2200)
    # sse_energies_2100Mhz, sse_times_2100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE2", precision="double", frequency=2200)
    # avx_energies_2100Mhz, avx_times_2100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="double", frequency=2200)
    #
    # energies_3100Mhz, times_3100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="NO-SPECIFIC", precision="double", frequency=2800)
    # sse_energies_3100Mhz, sse_times_3100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE2", precision="double", frequency=2800)
    # avx_energies_3100Mhz, avx_times_3100Mhz = process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="double", frequency=2800)

    energies_4700Mhz, times_4700Mhz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="NO-SPECIFIC", precision="single", frequency=4700, vector_size=2097152)
    sse_energies_4700Mhz, sse_times_4700Mhz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="SSE", precision="single", frequency=4700, vector_size=2097152)
    avx_energies_4700Mhz, avx_times_4700Mhz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX", precision="single", frequency=4700, vector_size=2097152)
    avx512_energies_4700Mhz, avx512_times_4700Mhz = \
        process(parameters, benchmark_name, folder_name, grouping_metric, instruction_set="AVX512", precision="single", frequency=4700, vector_size=2097152)

    powers = [energy / time for energy, time in zip(energies_4700Mhz, times_4700Mhz)]
    sse_powers = [energy / time for energy, time in zip(sse_energies_4700Mhz, sse_times_4700Mhz)]
    avx_powers = [energy / time for energy, time in zip(avx_energies_4700Mhz, avx_times_4700Mhz)]
    avx512_powers = [energy / time for energy, time in zip(avx512_energies_4700Mhz, avx512_times_4700Mhz)]

    energies_data = [(grouping_metric, sse_energies_4700Mhz), (grouping_metric, avx_energies_4700Mhz), (grouping_metric, avx512_energies_4700Mhz)]
    times_data = [(grouping_metric, sse_times_4700Mhz), (grouping_metric, avx_times_4700Mhz), (grouping_metric, avx512_times_4700Mhz)]
    powers_data = [(grouping_metric, sse_powers), (grouping_metric, avx_powers), (grouping_metric, avx512_powers)]

    # relative_energies = [1 - (e1 / e2) for e1, e2 in zip(sse_energies_2100Mhz, avx_energies_2100Mhz)]

    # TODO: show this Philipp
    create_scatter_plot(energies_data, "thread count", "consumed energy [Joules]", "energy comparison of instruction sets", ["SSE - 4700MHz", "AVX - 4700MHz", "AVX512 - 4700MHz"],
                        "upper center")
    create_scatter_plot(times_data, "thread count", "time [s]", "time comparison of instruction sets", ["SSE - 4700MHz", "AVX - 4700MHz", "AVX512 - 4700MHz"], "upper center")
    create_scatter_plot(powers_data, "thread count", "power draw [W]", "power consumption with different instruction sets and thread counts",
                        ["SSE - 4700MHz", "AVX - 4700MHz", "AVX512 - 4700MHz"], "upper left")
    # create_bar_plot(grouping_metric, relative_energies, "frequencies [MHz]", "relative energy difference", "relative energy difference SSE/AVX")


if __name__ == "__main__":
    _create_vectorization_scatter_plots_r7_grouping_threads()
